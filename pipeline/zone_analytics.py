import cv2
import json
from ultralytics import YOLO

# CAM1 = Skincare Section 
VIDEO_PATH = "data/videos/CAM 1.mp4"

model = YOLO("yolov8n.pt")

counted_ids = set()

zone_stats = {
    "skincare_visitors": 0,
    "makeup_visitors": 0
}

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

            zone_stats["skincare_visitors"] += 1

            print(
                f"Skincare Visitor {track_id}"
            )

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