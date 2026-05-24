# SOC Alert Triage Dashboard

SOC alert triage dashboard built with Vue 3 + FastAPI for my UTS Professional Practice subject (43030). The idea was to build something that simulates what a SOC analyst actually uses day-to-day, covering alert triage, threat intel enrichment, and MITRE ATT&CK mapping.

## Setup

**Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

Backend runs on port 8000, frontend on 5173. DB gets seeded with sample alerts automatically on first run.

## Features

- Dashboard with alert stats, severity chart, volume over time, top ATT&CK techniques
- Alert list with search/filter, click into detail view for full triage workflow
- Threat intel enrichment (VirusTotal + AbuseIPDB, falls back to mock data without API keys)
- MITRE ATT&CK coverage view
- Alert correlation graph using D3.js - groups alerts by shared indicators (IPs, hostnames, users)
- Investigation timeline across all alerts

## Threat Intel API Keys (optional)

If you want real enrichment instead of mock data, set these env vars:
```
VIRUSTOTAL_API_KEY=your_key
ABUSEIPDB_API_KEY=your_key
```

## Tech

- Vue 3 / Vue Router / Tailwind CSS
- Chart.js + vue-chartjs for graphs
- D3.js for correlation force graph
- FastAPI + SQLAlchemy + SQLite
