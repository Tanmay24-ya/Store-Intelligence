from ultralytics import YOLO
import cv2

model = YOLO("yolov8n.pt")

video = cv2.VideoCapture("data/videos/CAM 3.mp4")

while True:
    ret, frame = video.read()

    if not ret:
        break

    results = model(frame, classes=[0])

    annotated = results[0].plot()

    cv2.imshow("People Detection", annotated)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

video.release()
cv2.destroyAllWindows()