from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from datetime import datetime


class Event(BaseModel):
    timestamp: str
    camera: str
    event_type: str
    confidence: float
    details: Dict[str, Any]


class Anomaly(BaseModel):
    timestamp: str
    anomaly_type: str
    severity: str  # 'LOW', 'MEDIUM', 'HIGH'
    camera: str
    description: str
    track_id: Optional[int] = None


class FunnelStage(BaseModel):
    stage: str
    count: int
    percentage: float


class FunnelResponse(BaseModel):
    stages: List[FunnelStage]


class MetricsResponse(BaseModel):
    occupancy: int
    entries: int
    exits: int
    total_tracks: int
    total_events: int


class Recommendation(BaseModel):
    category: str  # 'Traffic', 'Revenue', 'Placement', 'Promotion'
    title: str
    impact: str  # 'High', 'Medium', 'Low'
    observation: str
    action: str