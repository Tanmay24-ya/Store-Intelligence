from collections import deque
from typing import List
from .schemas import Event

events: List[Event] = []
occupancy = 0
entry_count = 0
exit_count = 0
seen_track_ids = set()
recent_events = deque(maxlen=200)