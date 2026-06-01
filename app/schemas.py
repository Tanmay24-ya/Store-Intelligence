from pydantic import BaseModel
from typing import Literal, Optional
from datetime import datetime


class Event(BaseModel):
    event_type: Literal["ENTRY", "EXIT"]
    track_id: int
    camera_id: str = "cam_3"
    timestamp: datetime
    direction: Optional[Literal["left_to_right", "right_to_left"]] = None


class MetricsResponse(BaseModel):
    occupancy: int
    entries: int
    exits: int
    total_events: int


class FunnelResponse(BaseModel):
    visitors_seen: int
    entered_store: int
    exited_store: int
    current_inside: int