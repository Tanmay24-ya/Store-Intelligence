import json
import os

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

EVENTS_FILE = os.path.join(
    BASE_DIR,
    "pipeline",
    "events.jsonl"
)


def load_events():

    events = []

    if not os.path.exists(EVENTS_FILE):
        return events

    with open(EVENTS_FILE, "r") as f:

        for line in f:

            if line.strip():
                events.append(json.loads(line))

    return events