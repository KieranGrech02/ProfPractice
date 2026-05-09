from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database import get_db
from models import Alert, TimelineEvent
from schemas import AlertCreate, AlertListResponse, AlertResponse, AlertUpdate

router = APIRouter(prefix="/api/alerts", tags=["alerts"])


@router.get("/", response_model=list[AlertListResponse])
def list_alerts(
    status: str | None = Query(None),
    severity: str | None = Query(None),
    source: str | None = Query(None),
    search: str | None = Query(None),
    sort_by: str = Query("created_at"),
    sort_order: str = Query("desc"),
    db: Session = Depends(get_db),
):
    query = db.query(Alert)
    if status:
        query = query.filter(Alert.status == status)
    if severity:
        query = query.filter(Alert.severity == severity)
    if source:
        query = query.filter(Alert.source == source)
    if search:
        query = query.filter(
            Alert.title.ilike(f"%{search}%")
            | Alert.description.ilike(f"%{search}%")
            | Alert.mitre_technique_name.ilike(f"%{search}%")
        )
    sort_col = getattr(Alert, sort_by, Alert.created_at)
    if sort_order == "asc":
        query = query.order_by(sort_col.asc())
    else:
        query = query.order_by(sort_col.desc())
    return query.all()


@router.get("/{alert_id}", response_model=AlertResponse)
def get_alert(alert_id: int, db: Session = Depends(get_db)):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert


@router.post("/", response_model=AlertResponse, status_code=201)
def create_alert(alert_in: AlertCreate, db: Session = Depends(get_db)):
    alert = Alert(**alert_in.model_dump())
    db.add(alert)
    db.flush()
    timeline = TimelineEvent(
        alert_id=alert.id,
        event_type="alert_created",
        description=f"Alert created: {alert.title}",
    )
    db.add(timeline)
    db.commit()
    db.refresh(alert)
    return alert


@router.patch("/{alert_id}", response_model=AlertResponse)
def update_alert(alert_id: int, update: AlertUpdate, db: Session = Depends(get_db)):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    update_data = update.model_dump(exclude_unset=True)
    if "status" in update_data and update_data["status"] != alert.status:
        old_status = alert.status
        timeline = TimelineEvent(
            alert_id=alert.id,
            event_type="status_change",
            description=f"Status changed from {old_status} to {update_data['status']}",
        )
        db.add(timeline)

    if "analyst_notes" in update_data:
        timeline = TimelineEvent(
            alert_id=alert.id,
            event_type="note_added",
            description=f"Analyst note updated",
        )
        db.add(timeline)

    for key, value in update_data.items():
        setattr(alert, key, value)

    db.commit()
    db.refresh(alert)
    return alert


@router.delete("/{alert_id}", status_code=204)
def delete_alert(alert_id: int, db: Session = Depends(get_db)):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    db.delete(alert)
    db.commit()
