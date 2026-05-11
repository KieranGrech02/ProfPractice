from collections import Counter

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Alert

router = APIRouter(prefix="/api/mitre", tags=["mitre"])

TACTICS = [
    {"id": "TA0001", "name": "Initial Access"},
    {"id": "TA0002", "name": "Execution"},
    {"id": "TA0003", "name": "Persistence"},
    {"id": "TA0004", "name": "Privilege Escalation"},
    {"id": "TA0005", "name": "Defense Evasion"},
    {"id": "TA0006", "name": "Credential Access"},
    {"id": "TA0007", "name": "Discovery"},
    {"id": "TA0008", "name": "Lateral Movement"},
    {"id": "TA0009", "name": "Collection"},
    {"id": "TA0010", "name": "Exfiltration"},
    {"id": "TA0011", "name": "Command and Control"},
    {"id": "TA0040", "name": "Impact"},
]

TECHNIQUE_MAP = {
    "T1566": {"name": "Phishing", "tactic": "Initial Access"},
    "T1190": {"name": "Exploit Public-Facing Application", "tactic": "Initial Access"},
    "T1078": {"name": "Valid Accounts", "tactic": "Initial Access"},
    "T1059": {"name": "Command and Scripting Interpreter", "tactic": "Execution"},
    "T1059.001": {"name": "PowerShell", "tactic": "Execution"},
    "T1053": {"name": "Scheduled Task/Job", "tactic": "Persistence"},
    "T1547": {"name": "Boot or Logon Autostart Execution", "tactic": "Persistence"},
    "T1548": {"name": "Abuse Elevation Control Mechanism", "tactic": "Privilege Escalation"},
    "T1134": {"name": "Access Token Manipulation", "tactic": "Privilege Escalation"},
    "T1070": {"name": "Indicator Removal", "tactic": "Defense Evasion"},
    "T1027": {"name": "Obfuscated Files or Information", "tactic": "Defense Evasion"},
    "T1110": {"name": "Brute Force", "tactic": "Credential Access"},
    "T1003": {"name": "OS Credential Dumping", "tactic": "Credential Access"},
    "T1558": {"name": "Steal or Forge Kerberos Tickets", "tactic": "Credential Access"},
    "T1046": {"name": "Network Service Discovery", "tactic": "Discovery"},
    "T1087": {"name": "Account Discovery", "tactic": "Discovery"},
    "T1021": {"name": "Remote Services", "tactic": "Lateral Movement"},
    "T1021.001": {"name": "Remote Desktop Protocol", "tactic": "Lateral Movement"},
    "T1560": {"name": "Archive Collected Data", "tactic": "Collection"},
    "T1048": {"name": "Exfiltration Over Alternative Protocol", "tactic": "Exfiltration"},
    "T1567": {"name": "Exfiltration Over Web Service", "tactic": "Exfiltration"},
    "T1071": {"name": "Application Layer Protocol", "tactic": "Command and Control"},
    "T1105": {"name": "Ingress Tool Transfer", "tactic": "Command and Control"},
    "T1486": {"name": "Data Encrypted for Impact", "tactic": "Impact"},
    "T1498": {"name": "Network Denial of Service", "tactic": "Impact"},
}


@router.get("/tactics")
def get_tactics():
    return TACTICS


@router.get("/techniques")
def get_techniques():
    return [
        {"id": tid, "name": info["name"], "tactic": info["tactic"]}
        for tid, info in TECHNIQUE_MAP.items()
    ]


@router.get("/coverage")
def get_coverage(db: Session = Depends(get_db)):
    alerts = db.query(Alert).filter(Alert.mitre_tactic.isnot(None)).all()
    tactic_counts = Counter(a.mitre_tactic for a in alerts)
    technique_counts = Counter(a.mitre_technique_id for a in alerts)

    coverage = []
    for tactic in TACTICS:
        tactic_techniques = [
            {"id": tid, "name": info["name"], "alert_count": technique_counts.get(tid, 0)}
            for tid, info in TECHNIQUE_MAP.items()
            if info["tactic"] == tactic["name"]
        ]
        coverage.append(
            {
                "tactic_id": tactic["id"],
                "tactic_name": tactic["name"],
                "alert_count": tactic_counts.get(tactic["name"], 0),
                "techniques": tactic_techniques,
            }
        )
    return coverage
