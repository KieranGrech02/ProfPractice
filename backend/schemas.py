from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AlertBase(BaseModel):
    title: str
    description: Optional[str] = None
    severity: str
    source: Optional[str] = None
    source_ip: Optional[str] = None
    destination_ip: Optional[str] = None
    hostname: Optional[str] = None
    username: Optional[str] = None
    file_hash: Optional[str] = None
    mitre_tactic: Optional[str] = None
    mitre_technique_id: Optional[str] = None
    mitre_technique_name: Optional[str] = None


class AlertCreate(AlertBase):
    pass


class AlertUpdate(BaseModel):
    status: Optional[str] = None
    analyst_notes: Optional[str] = None
    severity: Optional[str] = None


class EnrichmentResultResponse(BaseModel):
    id: int
    alert_id: int
    indicator: str
    indicator_type: str
    source: str
    malicious: int
    reputation_score: Optional[int] = None
    raw_result: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class TimelineEventResponse(BaseModel):
    id: int
    alert_id: int
    event_type: str
    description: str
    created_at: datetime

    model_config = {"from_attributes": True}


class AlertResponse(AlertBase):
    id: int
    status: str
    analyst_notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    enrichments: list[EnrichmentResultResponse] = []
    timeline_events: list[TimelineEventResponse] = []

    model_config = {"from_attributes": True}


class AlertListResponse(AlertBase):
    id: int
    status: str
    analyst_notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class DashboardStats(BaseModel):
    total_alerts: int
    open_alerts: int
    investigating_alerts: int
    resolved_alerts: int
    critical_alerts: int
    high_alerts: int
    medium_alerts: int
    low_alerts: int


class SeverityBreakdown(BaseModel):
    severity: str
    count: int


class TechniqueCount(BaseModel):
    technique_id: str
    technique_name: str
    tactic: str
    count: int


class AlertVolumePoint(BaseModel):
    date: str
    count: int


class EnrichRequest(BaseModel):
    indicator: str
    indicator_type: str
