# SOC Alert Triage Dashboard

A full-stack security operations centre (SOC) alert triage dashboard built with **Vue 3** and **FastAPI**. Designed as a professional development project to build practical skills in threat detection, incident response, and security operations tooling.

## Features

- **Dashboard Overview** — Real-time stats, alert volume trends, severity breakdown, and top MITRE ATT&CK techniques
- **Alert Management** — Search, filter, and triage security alerts with full CRUD operations
- **Threat Intelligence Enrichment** — Enrich indicators (IPs, file hashes) via VirusTotal and AbuseIPDB APIs (with mock fallback)
- **MITRE ATT&CK Mapping** — Visual coverage map showing which tactics and techniques have active alerts
- **Investigation Timeline** — Chronological event log tracking status changes, analyst notes, and enrichment activity
- **Analyst Workflow** — Update alert status, add investigation notes, and track triage progress

## Tech Stack

| Layer    | Technology                        |
| -------- | --------------------------------- |
| Frontend | Vue 3, Vue Router, Tailwind CSS   |
| Charts   | Chart.js + vue-chartjs            |
| Backend  | Python FastAPI                    |
| Database | SQLite via SQLAlchemy             |
| Enrichment | VirusTotal API, AbuseIPDB API  |

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

The API runs on `http://localhost:8000`. The database is seeded with realistic security alerts on first startup.

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The frontend runs on `http://localhost:5173` and proxies API requests to the backend.

### Optional: Real Threat Intelligence

Set environment variables to enable real API enrichment (falls back to realistic mock data if not set):

```bash
export VIRUSTOTAL_API_KEY=your_key_here
export ABUSEIPDB_API_KEY=your_key_here
```

## MITRE ATT&CK Techniques Covered

The seed data includes alerts mapped to techniques across the ATT&CK framework:

- **Initial Access** — Phishing (T1566), Exploit Public-Facing App (T1190), Valid Accounts (T1078)
- **Execution** — PowerShell (T1059.001), Command and Scripting Interpreter (T1059)
- **Persistence** — Scheduled Task (T1053), Boot Autostart Execution (T1547)
- **Privilege Escalation** — Token Manipulation (T1134), UAC Bypass (T1548)
- **Defense Evasion** — Indicator Removal (T1070), Obfuscated Files (T1027)
- **Credential Access** — Brute Force (T1110), OS Credential Dumping (T1003), Kerberoasting (T1558)
- **Discovery** — Network Service Discovery (T1046), Account Discovery (T1087)
- **Lateral Movement** — RDP (T1021.001), Remote Services (T1021)
- **Collection** — Archive Collected Data (T1560)
- **Exfiltration** — Web Service (T1567), Alternative Protocol (T1048)
- **Command and Control** — Application Layer Protocol (T1071), Ingress Tool Transfer (T1105)
- **Impact** — Data Encrypted for Impact (T1486), Network DoS (T1498)

## Project Context

This project was developed as part of the UTS 43030 Professional Practice subject. It addresses Goal 4 of my Professional Learning Plan: building practical threat detection and incident response skills. The project demonstrates applied knowledge in security operations concepts, detection engineering, threat intelligence enrichment, and the MITRE ATT&CK framework.
