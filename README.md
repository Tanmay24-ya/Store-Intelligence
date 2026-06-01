# Purplle Store Intelligence Engine

## 🎯 Overview

**Purplle Store Intelligence Engine** is a full‑stack, production‑grade retail analytics platform that fuses **real‑time computer vision** (YOLOv8 + ByteTrack) with **POS transaction data** to deliver actionable insights for store managers.  The system powers a premium SaaS‑style dashboard built with **Streamlit**, backed by a high‑performance **FastAPI** backend.

---

## 🏗️ Architecture

```mermaid
flowchart TD
    A[RTSP Camera Feeds] -->|Video Stream| B[YOLOv8 Object Detection]
    B -->|Bounding Boxes| C[ByteTrack ID Association]
    C -->|Entry/Exit Tripwire| D[Event Engine JSONL]
    D -->|Events + Stats| E[FastAPI Caching Core]
    E -->|REST API| F[AI Recommendation Engine]
    F -->|Recommendations| G[Streamlit Dashboard]
    style A fill:#2d3748,stroke:#4c51bf,color:#e2e8f0
    style B fill:#3b82f6,stroke:#0ea5e9,color:#e2e8f0
    style C fill:#6366f1,stroke:#a78bfa,color:#e2e8f0
    style D fill:#10b981,stroke:#6ee7b7,color:#e2e8f0
    style E fill:#c2410c,stroke:#f59e0b,color:#e2e8f0
    style F fill:#a855f7,stroke:#d8b4fe,color:#e2e8f0
    style G fill:#0f172a,stroke:#1e293b,color:#cbd5e1
```

* **Camera Feeds** – 3 + RTSP streams (Skincare, Makeup, Entrance)
* **YOLOv8** – Detects people (class 0) in real time.
* **ByteTrack** – Provides persistent IDs for each shopper.
* **Event Engine** – Logs entry/exit, zone occupancy, and timestamps to `events.jsonl`.
* **FastAPI** – Serves cached analytics (`/metrics`, `/anomalies`, `/funnel`, `/recommendations`).
* **Streamlit** – Premium UI with glassmorphism, dark theme, and interactive Plotly charts.

---

## ✨ Core Features

| Feature | Description | UI Element |
|---|---|---|
| **Retail Anomaly Center** | Detects zone congestion, after‑hours intrusion, low‑engagement dips. | ⚠️ Active Alerts card + severity‑sorted table |
| **Advanced Funnel Analytics** | Stores‑to‑checkout conversion funnel with drop‑off percentages. | 📊 Funnel chart |
| **AI‑Assisted Recommendations** | Cross‑references CV traffic & POS revenue to suggest merchandising actions. | 💡 Recommendation cards |
| **CV Telemetry Metrics** | Unique shoppers, peak occupancy, average dwell time, most active zone. | 📈 Metric cards |
| **Camera Snapshot Panel** | Static snapshots with bounding boxes & tripwire overlay for CAM 1‑3. | 🖼️ Image panels |
| **Revenue & Brand KPIs** | GMV, NMV, transactions, brand contribution, department performance. | 📊 Bar charts |

All emojis have been removed for a professional look.

---

## 📦 Installation & Setup

```bash
# Clone the repo
git clone https://github.com/Tanmay24-ya/Store-Intelligence.git
cd Store-Intelligence

# Create virtual environment (Windows)
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download YOLOv8 weights (already included in repo)
# If you need to fetch a newer model:
# pip install ultralytics && yolov8 download yolov8n.pt

# Run the pipeline to generate camera snapshots (optional)
python pipeline/generate_snapshots.py

# Start backend API
uvicorn app.main:app --reload

# In a new terminal, start the dashboard
streamlit run app/dashboard.py
```

The backend will be reachable at `http://127.0.0.1:8000` and the dashboard at `http://127.0.0.1:8501`.

---

## 🔗 API Endpoints (FastAPI)

| Endpoint | Method | Description |
|---|---|---|
| `/health` | GET | Simple health check (`{"status":"ok"}`) |
| `/metrics` | GET | Returns global CV metrics (total tracks, occupancy, etc.) |
| `/anomalies` | GET | List of active alerts with severity |
| `/funnel` | GET | Retail conversion funnel stages and counts |
| `/recommendations` | GET | AI‑generated strategic recommendations |
| `/zone-analytics` | GET | Visitor counts per zone |
| `/events` | GET | Raw CV events (timestamp, camera, type, confidence) |

All responses conform to the Pydantic models defined in `app/schemas.py`.

---

## 🎨 UI Screenshots (optional)
> *Add screenshots of the dashboard here – you can export the Streamlit UI via the `View → Screenshot` menu or use `st.camera_input` to embed images.*

---

## 🤝 Contributing

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/awesome-feature`).
3. Follow the existing code style (type‑hinted, Pydantic‑validated).
4. Run tests (`pytest -q`).
5. Submit a Pull Request.

---

## 📜 License

This project is licensed under the **MIT License** – see the `LICENSE` file for details.

---

## 📞 Contact

* **Owner**: Tanmay24-ya – [GitHub](https://github.com/Tanmay24-ya)
* **Email**: dixittanmay041224@gmail.com

Feel free to open an issue for bugs, feature requests, or documentation improvements.