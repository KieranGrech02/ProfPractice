from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Alert, EnrichmentResult, TimelineEvent
from schemas import EnrichmentResultResponse, EnrichRequest
from services.threat_intel import ThreatIntelService

router = APIRouter(prefix="/api/enrichment", tags=["enrichment"])

threat_intel = ThreatIntelService()


@router.post("/{alert_id}", response_model=list[EnrichmentResultResponse])
async def enrich_alert(alert_id: int, db: Session = Depends(get_db)):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    results = []
    indicators = []
    if alert.source_ip:
        indicators.append(("ip", alert.source_ip))
    if alert.destination_ip:
        indicators.append(("ip", alert.destination_ip))
    if alert.file_hash:
        indicators.append(("hash", alert.file_hash))

    for indicator_type, indicator in indicators:
        enrichment_data = await threat_intel.enrich(indicator, indicator_type)
        for source_name, data in enrichment_data.items():
            enrichment = EnrichmentResult(
                alert_id=alert.id,
                indicator=indicator,
                indicator_type=indicator_type,
                source=source_name,
                malicious=data.get("malicious", 0),
                reputation_score=data.get("reputation_score"),
                raw_result=str(data),
            )
            db.add(enrichment)
            results.append(enrichment)

    timeline = TimelineEvent(
        alert_id=alert.id,
        event_type="enrichment_completed",
        description=f"Threat intelligence enrichment completed for {len(indicators)} indicator(s)",
    )
    db.add(timeline)
    db.commit()
    for r in results:
        db.refresh(r)
    return results


@router.post("/lookup", response_model=dict)
async def lookup_indicator(request: EnrichRequest):
    result = await threat_intel.enrich(request.indicator, request.indicator_type)
    return result
