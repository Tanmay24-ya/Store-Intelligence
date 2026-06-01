from ultralytics import YOLO
import cv2
from event_logger import log_event

MODEL_PATH = "yolov8n.pt"
VIDEO_PATH = "data/videos/CAM 3.mp4"

LINE_X = 950
BUFFER = 30

model = YOLO(MODEL_PATH)

video = cv2.VideoCapture(VIDEO_PATH)

frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(video.get(cv2.CAP_PROP_FPS))

fourcc = cv2.VideoWriter_fourcc(*"mp4v")

out = cv2.VideoWriter(
    "output.mp4",
    fourcc,
    fps,
    (frame_width, frame_height)
)

track_side = {}

entry_count = 0
exit_count = 0
occupancy = 0

cv2.namedWindow("Tracking", cv2.WND_PROP_FULLSCREEN)

cv2.setWindowProperty(
    "Tracking",
    cv2.WND_PROP_FULLSCREEN,
    cv2.WINDOW_FULLSCREEN
)

while True:

    ret, frame = video.read()

    if not ret:
        break

    results = model.track(
        frame,
        persist=True,
        tracker="bytetrack.yaml",
        classes=[0],
        conf=0.25
    )

    annotated = results[0].plot()

    cv2.line(
        annotated,
        (LINE_X, 0),
        (LINE_X, frame_height),
        (0, 255, 0),
        3
    )

    cv2.line(
        annotated,
        (LINE_X - BUFFER, 0),
        (LINE_X - BUFFER, frame_height),
        (0, 255, 255),
        1
    )

    cv2.line(
        annotated,
        (LINE_X + BUFFER, 0),
        (LINE_X + BUFFER, frame_height),
        (0, 255, 255),
        1
    )

    boxes = results[0].boxes

    current_inside_ids = set()

    if boxes.id is not None:

        for box, track_id in zip(boxes.xyxy, boxes.id):

            track_id = int(track_id)

            x1, y1, x2, y2 = map(int, box)

            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2

            cv2.circle(
                annotated,
                (center_x, center_y),
                6,
                (0, 0, 255),
                -1
            )

            if center_x < (LINE_X - BUFFER):
                current_side = "left"

            elif center_x > (LINE_X + BUFFER):
                current_side = "right"

            else:
                current_side = "middle"

            if current_side == "left":
                current_inside_ids.add(track_id)

            if track_id not in track_side:

                track_side[track_id] = current_side

                log_event(
                    event_type="person_detected",
                    camera="CAM3",
                    confidence=1.0,
                    details={
                        "track_id": track_id,
                        "first_side": current_side
                    }
                )

                continue

            previous_side = track_side[track_id]

            if current_side == "middle":
                continue

            if (
                previous_side == "right"
                and current_side == "left"
            ):
                entry_count += 1

                log_event(
                    event_type="customer_entry",
                    camera="CAM3",
                    confidence=1.0,
                    details={
                        "track_id": track_id,
                        "direction": "right_to_left"
                    }
                )

            elif (
                previous_side == "left"
                and current_side == "right"
            ):
                exit_count += 1

                log_event(
                    event_type="customer_exit",
                    camera="CAM3",
                    confidence=1.0,
                    details={
                        "track_id": track_id,
                        "direction": "left_to_right"
                    }
                )

            track_side[track_id] = current_side

    occupancy = len(current_inside_ids)

    cv2.putText(
        annotated,
        f"OCCUPANCY: {occupancy}",
        (40, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 255, 0),
        2
    )

    cv2.putText(
        annotated,
        f"ENTRY: {entry_count}",
        (40, 100),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.putText(
        annotated,
        f"EXIT: {exit_count}",
        (40, 150),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        2
    )

    cv2.putText(
        annotated,
        f"TRACKS: {len(track_side)}",
        (40, 200),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 255, 255),
        2
    )

    out.write(annotated)

    cv2.imshow("Tracking", annotated)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

video.release()
out.release()
cv2.destroyAllWindows()