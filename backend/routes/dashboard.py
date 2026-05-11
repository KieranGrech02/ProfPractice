from collections import Counter
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Alert
from schemas import (
    AlertVolumePoint,
    DashboardStats,
    SeverityBreakdown,
    TechniqueCount,
)

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/stats", response_model=DashboardStats)
def get_stats(db: Session = Depends(get_db)):
    alerts = db.query(Alert).all()
    return DashboardStats(
        total_alerts=len(alerts),
        open_alerts=sum(1 for a in alerts if a.status == "open"),
        investigating_alerts=sum(1 for a in alerts if a.status == "investigating"),
        resolved_alerts=sum(1 for a in alerts if a.status == "resolved"),
        critical_alerts=sum(1 for a in alerts if a.severity == "critical"),
        high_alerts=sum(1 for a in alerts if a.severity == "high"),
        medium_alerts=sum(1 for a in alerts if a.severity == "medium"),
        low_alerts=sum(1 for a in alerts if a.severity == "low"),
    )


@router.get("/severity-breakdown", response_model=list[SeverityBreakdown])
def get_severity_breakdown(db: Session = Depends(get_db)):
    alerts = db.query(Alert).all()
    counts = Counter(a.severity for a in alerts)
    return [
        SeverityBreakdown(severity=sev, count=cnt) for sev, cnt in counts.items()
    ]


@router.get("/top-techniques", response_model=list[TechniqueCount])
def get_top_techniques(limit: int = 10, db: Session = Depends(get_db)):
    alerts = db.query(Alert).filter(Alert.mitre_technique_id.isnot(None)).all()
    technique_map: dict[str, TechniqueCount] = {}
    for a in alerts:
        key = a.mitre_technique_id
        if key in technique_map:
            technique_map[key].count += 1
        else:
            technique_map[key] = TechniqueCount(
                technique_id=a.mitre_technique_id,
                technique_name=a.mitre_technique_name or "",
                tactic=a.mitre_tactic or "",
                count=1,
            )
    sorted_techniques = sorted(
        technique_map.values(), key=lambda t: t.count, reverse=True
    )
    return sorted_techniques[:limit]


@router.get("/alert-volume", response_model=list[AlertVolumePoint])
def get_alert_volume(days: int = 30, db: Session = Depends(get_db)):
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    alerts = db.query(Alert).filter(Alert.created_at >= cutoff).all()
    date_counts: dict[str, int] = {}
    for a in alerts:
        date_str = a.created_at.strftime("%Y-%m-%d")
        date_counts[date_str] = date_counts.get(date_str, 0) + 1

    result = []
    for i in range(days):
        d = cutoff + timedelta(days=i)
        date_str = d.strftime("%Y-%m-%d")
        result.append(AlertVolumePoint(date=date_str, count=date_counts.get(date_str, 0)))
    return result
