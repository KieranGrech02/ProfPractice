from collections import defaultdict

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Alert

router = APIRouter(prefix="/api/correlations", tags=["correlations"])


def _build_graph(alerts: list[Alert]) -> dict:
    nodes = []
    edges = []
    seen_edges = set()

    alert_map = {a.id: a for a in alerts}

    index_by_field: dict[str, dict[str, list[int]]] = defaultdict(lambda: defaultdict(list))
    # could also correlate on mitre technique but it gets too noisy
    correlation_fields = [
        ("source_ip", "Source IP"),
        ("destination_ip", "Destination IP"),
        ("hostname", "Hostname"),
        ("username", "Username"),
        ("file_hash", "File Hash"),
    ]

    for a in alerts:
        for field, _ in correlation_fields:
            val = getattr(a, field)
            if val and val not in ("Multiple", "SYSTEM"):
                index_by_field[field][val].append(a.id)

    for field, label in correlation_fields:
        for val, ids in index_by_field[field].items():
            if len(ids) < 2:
                continue
            for i in range(len(ids)):
                for j in range(i + 1, len(ids)):
                    edge_key = (min(ids[i], ids[j]), max(ids[i], ids[j]), field)
                    if edge_key not in seen_edges:
                        seen_edges.add(edge_key)
                        edges.append({
                            "source": ids[i],
                            "target": ids[j],
                            "reason": f"{label}: {val}",
                            "type": field,
                        })

    connected_ids = set()
    for e in edges:
        connected_ids.add(e["source"])
        connected_ids.add(e["target"])

    for aid in connected_ids:
        a = alert_map[aid]
        nodes.append({
            "id": a.id,
            "title": a.title,
            "severity": a.severity,
            "status": a.status,
            "source": a.source,
            "source_ip": a.source_ip,
            "hostname": a.hostname,
            "username": a.username,
            "mitre_tactic": a.mitre_tactic,
            "mitre_technique_id": a.mitre_technique_id,
            "mitre_technique_name": a.mitre_technique_name,
            "connections": sum(
                1 for e in edges if e["source"] == a.id or e["target"] == a.id
            ),
        })

    return {"nodes": nodes, "edges": edges}


@router.get("/graph")
def get_correlation_graph(db: Session = Depends(get_db)):
    alerts = db.query(Alert).all()
    return _build_graph(alerts)


@router.get("/clusters")
def get_clusters(db: Session = Depends(get_db)):
    alerts = db.query(Alert).all()
    graph = _build_graph(alerts)

    adjacency: dict[int, set[int]] = defaultdict(set)
    for e in graph["edges"]:
        adjacency[e["source"]].add(e["target"])
        adjacency[e["target"]].add(e["source"])

    visited = set()
    clusters = []
    node_map = {n["id"]: n for n in graph["nodes"]}

    for node in graph["nodes"]:
        if node["id"] in visited:
            continue
        cluster_ids = []
        stack = [node["id"]]
        while stack:
            nid = stack.pop()
            if nid in visited:
                continue
            visited.add(nid)
            cluster_ids.append(nid)
            for neighbor in adjacency.get(nid, []):
                if neighbor not in visited:
                    stack.append(neighbor)

        if len(cluster_ids) >= 2:
            cluster_nodes = [node_map[nid] for nid in cluster_ids if nid in node_map]
            shared = set()
            for e in graph["edges"]:
                if e["source"] in cluster_ids and e["target"] in cluster_ids:
                    shared.add(e["reason"])
            clusters.append({
                "id": min(cluster_ids),
                "alert_count": len(cluster_ids),
                "alerts": cluster_nodes,
                "shared_indicators": list(shared),
                "max_severity": _worst_severity([n["severity"] for n in cluster_nodes]),
            })

    clusters.sort(key=lambda c: c["alert_count"], reverse=True)
    return clusters


def _worst_severity(severities: list[str]) -> str:
    order = ["critical", "high", "medium", "low", "informational"]
    for sev in order:
        if sev in severities:
            return sev
    return "informational"
