import json
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

EVENTS_FILE = os.path.join(
    BASE_DIR,
    "pipeline",
    "events.jsonl"
)


def log_event(
    event_type,
    camera,
    confidence,
    details
):
    event = {
        "timestamp": datetime.utcnow().isoformat(),
        "camera": camera,
        "event_type": event_type,
        "confidence": confidence,
        "details": details
    }

    with open(EVENTS_FILE, "a") as f:
        f.write(json.dumps(event) + "\n")