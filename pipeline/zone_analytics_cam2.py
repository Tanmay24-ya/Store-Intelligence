import json
from ultralytics import YOLO

VIDEO_PATH = "data/videos/CAM 2.mp4"

model = YOLO("yolov8n.pt")

counted_ids = set()

with open("data/zone_stats.json") as f:
    zone_stats = json.load(f)

results = model.track(
    source=VIDEO_PATH,
    persist=True,
    classes=[0],
    stream=True
)

for result in results:

    if result.boxes.id is None:
        continue

    track_ids = result.boxes.id.int().cpu().tolist()

    for track_id in track_ids:

        if track_id not in counted_ids:

            counted_ids.add(track_id)

            zone_stats["makeup_visitors"] += 1

            print(f"Makeup Visitor {track_id}")

with open(
    "data/zone_stats.json",
    "w"
) as f:

    json.dump(
        zone_stats,
        f,
        indent=4
    )

print(zone_stats)