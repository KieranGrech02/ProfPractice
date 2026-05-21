from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, SessionLocal, engine
from routes import alerts, correlations, dashboard, enrichment, mitre
from seed_data import seed_database

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SOC Alert Triage Dashboard", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(alerts.router)
app.include_router(correlations.router)
app.include_router(dashboard.router)
app.include_router(enrichment.router)
app.include_router(mitre.router)


@app.on_event("startup")
def on_startup():
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()


@app.get("/api/health")
def health():
    return {"status": "ok"}
