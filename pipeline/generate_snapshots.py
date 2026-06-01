import cv2
import os
from ultralytics import YOLO

# Make sure static directory exists
os.makedirs("app/static", exist_ok=True)

print("Initializing YOLO model...")
model = YOLO("yolov8n.pt")

cameras = [
    {"name": "cam1", "path": "data/videos/CAM 1.mp4", "frame_num": 100},
    {"name": "cam2", "path": "data/videos/CAM 2.mp4", "frame_num": 100},
    {"name": "cam3", "path": "data/videos/CAM 3.mp4", "frame_num": 100}
]

for cam in cameras:
    print(f"Processing frame for {cam['name']}...")
    if not os.path.exists(cam["path"]):
        print(f"Video file missing: {cam['path']}")
        continue

    cap = cv2.VideoCapture(cam["path"])
    cap.set(cv2.CAP_PROP_POS_FRAMES, cam["frame_num"])
    ret, frame = cap.read()
    cap.release()

    if not ret:
        print(f"Failed to read frame {cam['frame_num']} from {cam['path']}")
        continue

    # Run inference to detect people (class 0)
    results = model.predict(source=frame, classes=[0], conf=0.3, verbose=False)
    
    # Draw detections on the frame
    annotated_frame = frame.copy()
    
    # Draw tripwire for camera 3
    if cam["name"] == "cam3":
        h, w, _ = annotated_frame.shape
        LINE_X = int(w * 0.5) # Center line
        # Draw a beautiful neon purple tripwire boundary line
        cv2.line(annotated_frame, (LINE_X, 0), (LINE_X, h), (246, 92, 139), 4)
        cv2.putText(annotated_frame, "CAM3: ENTRY/EXIT TRIPWIRE BOUNDARY", (LINE_X + 20, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (246, 92, 139), 3)

    if len(results) > 0:
        boxes = results[0].boxes
        for i, box in enumerate(boxes):
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
            conf = float(box.conf[0])
            track_id = i + 1  # Simulated Track ID for snapshot
            
            # Draw violet bounding box
            cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (139, 92, 246), 3)
            
            # Label
            label = f"Person ID:{track_id} ({conf:.2f})"
            (w_l, h_l), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
            cv2.rectangle(annotated_frame, (x1, y1 - h_l - 10), (x1 + w_l, y1), (139, 92, 246), -1)
            cv2.putText(annotated_frame, label, (x1, y1 - 8),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
    # Save the annotated frame
    output_path = f"app/static/{cam['name']}.jpg"
    cv2.imwrite(output_path, annotated_frame)
    print(f"Saved annotated camera frame to {output_path}")

print("Camera snapshots generated successfully!")
