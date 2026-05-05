import enum
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from database import Base


class Severity(str, enum.Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFORMATIONAL = "informational"


class Status(str, enum.Enum):
    OPEN = "open"
    INVESTIGATING = "investigating"
    RESOLVED = "resolved"
    FALSE_POSITIVE = "false_positive"


def utcnow():
    return datetime.now(timezone.utc)


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    severity = Column(String, nullable=False)
    status = Column(String, default="open")
    source = Column(String)
    source_ip = Column(String, nullable=True)
    destination_ip = Column(String, nullable=True)
    hostname = Column(String, nullable=True)
    username = Column(String, nullable=True)
    file_hash = Column(String, nullable=True)
    mitre_tactic = Column(String, nullable=True)
    mitre_technique_id = Column(String, nullable=True)
    mitre_technique_name = Column(String, nullable=True)
    analyst_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=utcnow)
    updated_at = Column(DateTime, default=utcnow, onupdate=utcnow)

    enrichments = relationship(
        "EnrichmentResult", back_populates="alert", cascade="all, delete-orphan"
    )
    timeline_events = relationship(
        "TimelineEvent", back_populates="alert", cascade="all, delete-orphan"
    )


class EnrichmentResult(Base):
    __tablename__ = "enrichment_results"

    id = Column(Integer, primary_key=True, index=True)
    alert_id = Column(Integer, ForeignKey("alerts.id"))
    indicator = Column(String, nullable=False)
    indicator_type = Column(String, nullable=False)
    source = Column(String, nullable=False)
    malicious = Column(Integer, default=0)
    reputation_score = Column(Integer, nullable=True)
    raw_result = Column(Text, nullable=True)
    created_at = Column(DateTime, default=utcnow)

    alert = relationship("Alert", back_populates="enrichments")


class TimelineEvent(Base):
    __tablename__ = "timeline_events"

    id = Column(Integer, primary_key=True, index=True)
    alert_id = Column(Integer, ForeignKey("alerts.id"))
    event_type = Column(String, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=utcnow)

    alert = relationship("Alert", back_populates="timeline_events")
