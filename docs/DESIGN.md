# Purplle Store Intelligence Engine – Design Document

> **Hackathon Submission** · Purplle Store Intelligence Engine · June 2026

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [Data Flow](#data-flow)
4. [AI-Assisted Decisions](#ai-assisted-decisions)
5. [Business Impact](#business-impact)
6. [Live Deployment](#live-deployment)

---

## Overview

**Purplle Store Intelligence Engine** is a production-grade retail analytics platform that fuses **real-time Computer Vision telemetry** with **POS transaction analytics** to deliver actionable operational intelligence for physical retail stores.

The system ingests live camera feeds from multiple store zones, tracks individual customer journeys using state-of-the-art multi-object tracking, analyzes behavioral engagement, detects operational anomalies, and surfaces AI-generated business recommendations — all through a premium real-time dashboard.

### Core Capabilities

| Capability | Description |
|---|---|
| **Real-Time Detection** | YOLOv8 detects shoppers across all camera streams with sub-second latency |
| **Persistent Tracking** | ByteTrack assigns stable IDs across frames and occlusions |
| **Zone Intelligence** | Per-section engagement analytics for Skincare, Makeup, and Checkout zones |
| **Funnel Analytics** | End-to-end customer journey from entry to purchase |
| **Anomaly Detection** | Automated alerts for congestion, traffic spikes, and operational irregularities |
| **AI Recommendations** | Rule-based + CV-driven business suggestions for store managers |

---

## System Architecture

The platform is designed as a **layered pipeline** where each layer has a clearly defined responsibility. Data flows top-down from raw video input to actionable dashboard insights.

```
Store Cameras (CAM1 – Entrance, CAM2 – Skincare, CAM3 – Makeup)
        │
        ▼
Detection Layer  ── YOLOv8n ── Bounding Boxes · Confidence · Class 0
        │
        ▼
Tracking Layer  ── ByteTrack ── Persistent Track IDs · Dwell Time · Re-ID
        │
   ┌────┴────┐
   ▼         ▼
Entry/Exit  Zone Analytics
Analytics   Occupancy · Engagement · Heatmap
   └────┬────┘
        │
        ▼
Event Logging Engine  ── JSONL Append-Only Store (events.jsonl)
        │
        ▼
FastAPI Analytics Core  ── /metrics · /anomalies · /funnel · /recommendations
        │
   ┌────┴────┐
   ▼         ▼
Anomaly    Recommendation
Engine     Engine
   └────┬────┘
        │
        ▼
Streamlit Dashboard  ── Occupancy · Funnel · KPIs · Alerts · Recs
```

### Layer Responsibilities

| Layer | Technology | Responsibility |
|---|---|---|
| **Camera** | RTSP / Video Files | Multi-zone video ingestion |
| **Detection** | YOLOv8n | Per-frame person detection |
| **Tracking** | ByteTrack | Persistent multi-object tracking |
| **Analytics** | Python, Pandas | Entry/exit, zone occupancy, dwell time |
| **Event Store** | JSONL | Append-only structured event logging |
| **API** | FastAPI + Pydantic | Structured REST analytics endpoints |
| **Dashboard** | Streamlit + Plotly | Real-time interactive visualization |

---

## Data Flow

### 1. Camera Layer

The platform ingests multiple simultaneous store camera feeds. Each camera covers a dedicated store zone:

| Camera | Zone | Analytics Produced |
|---|---|---|
| **CAM1** | Entrance / Exit | Entry/exit counts, tripwire events, footfall |
| **CAM2** | Skincare Zone | Zone occupancy, dwell time, engagement score |
| **CAM3** | Makeup Zone | Zone occupancy, dwell time, engagement score |

---

### 2. Detection Layer

**YOLOv8** (nano variant, `yolov8n.pt`) performs real-time person detection on every incoming frame.

**Detection Output per Frame:**
```json
{
  "frame_id": 480,
  "camera": "CAM3",
  "detections": [
    { "bbox": [120, 85, 340, 420], "confidence": 0.93, "class": 0, "label": "person" }
  ]
}
```

- **Bounding Boxes** – `[x1, y1, x2, y2]` pixel coordinates
- **Confidence Score** – Detection certainty (threshold: 0.50)
- **Class 0** – Person class (COCO dataset label)

---

### 3. Tracking Layer

**ByteTrack** consumes YOLOv8 detections and maintains a persistent registry of active tracks across frames.

**Key Properties:**
- Each detected shopper receives a **unique, stable Track ID**
- Track IDs persist across **temporary occlusions** (e.g., shoppers behind shelving)
- Enables accurate **dwell time computation** (first seen → last seen per track)
- Prevents **double-counting** across re-appearances

---

### 4. Analytics Layer

The analytics engine operates on ByteTrack output and computes store-level KPIs:

| Metric | Computation Method |
|---|---|
| **Store Occupancy** | Count of active Track IDs in current frame |
| **Total Footfall** | Cumulative unique Track IDs crossing entry tripwire |
| **Zone Engagement** | Active Track IDs within zone bounding polygon |
| **Dwell Time** | `(last_frame – first_frame) × frame_duration` per Track ID |
| **Customer Funnel** | Entry → Zone Visit → Checkout → Exit (stage counts) |
| **Conversion Rate** | `(checkout_visitors / total_entrants) × 100` |

---

### 5. Event Logging Layer

All analytics events are serialized and appended to `data/events.jsonl` using the JSON Lines format.

**Event Schema:**
```json
{
  "timestamp": "2026-06-01T10:00:01",
  "camera": "CAM3",
  "event_type": "entry",
  "track_id": 15,
  "confidence": 0.93
}
```

**Supported Event Types:**

| `event_type` | Description |
|---|---|
| `entry` | Track ID crossed the entry tripwire |
| `exit` | Track ID crossed the exit tripwire |
| `zone_enter` | Track ID entered a zone polygon |
| `zone_exit` | Track ID exited a zone polygon |
| `occupancy_snapshot` | Periodic store occupancy capture |
| `anomaly` | Detected operational anomaly |

Why **JSONL**? Append-only writes are O(1), zero-parse overhead during ingestion, human-readable, and trivially streamable to downstream processors.

---

### 6. FastAPI Layer

The **FastAPI** backend exposes structured REST endpoints consumed by the dashboard and external integrations.

| Endpoint | Method | Description |
|---|---|---|
| `/health` | `GET` | Service health check |
| `/metrics` | `GET` | Global CV metrics: occupancy, footfall, dwell time |
| `/anomalies` | `GET` | Active anomaly alerts with severity |
| `/funnel` | `GET` | Customer journey conversion stages |
| `/recommendations` | `GET` | AI-generated actionable recommendations |
| `/zone-analytics` | `GET` | Per-zone visitor and engagement counts |
| `/events` | `GET` | Raw event log with filtering support |

All responses are **Pydantic-validated** and served with **OpenAPI documentation** auto-generated at `/docs`.

---

### 7. Dashboard Layer

**Streamlit** renders the analytics through a premium dark-themed dashboard with glassmorphism styling and interactive **Plotly** visualizations.

| Section | Visualizations |
|---|---|
| **Store Overview** | Live occupancy gauge, footfall counter, KPI cards |
| **Retail Analytics & KPIs** | Revenue trends, zone traffic, dwell time distributions |
| **Anomaly Center** | Alert timeline, severity badges, operational risk flags |
| **Funnel Analytics** | Funnel chart, stage conversion rates |
| **Recommendation Engine** | AI-generated cards with priority levels |
| **Camera Intelligence Panel** | Processed snapshot grid with tracking overlays |

---

## AI-Assisted Decisions

The **Recommendation Engine** synthesizes Computer Vision telemetry and POS transaction data to generate contextual, actionable business recommendations.

### Example 1 – Zone Rebalancing

**Condition:** Makeup Zone traffic is ≥ 40% higher than Skincare Zone over the last 2 hours.

**Recommendation:**
> Increase promotional displays and sampling activities in the high-traffic Makeup Zone to maximize conversion.

---

### Example 2 – Checkout Optimization

**Condition:** Average checkout dwell time exceeds 8 minutes.

**Recommendation:**
> Place impulse-purchase display units near checkout counters. Open additional POS lanes to reduce queue buildup and improve revenue-per-transaction.

---

### Example 3 – Brand Inventory Expansion

**Condition:** A single brand contributes ≥ 35% of zone revenue while occupying < 15% of shelf space.

**Recommendation:**
> Expand shelf allocation and front-facing display visibility for the top-performing brand to capture demand and reduce stockout risk.

---

## Business Impact

| Dimension | Before | After |
|---|---|---|
| **Occupancy Visibility** | End-of-day manual count | Real-time live count |
| **Anomaly Detection** | Staff report (delayed) | Automated alert (< 1 min) |
| **Zone Performance** | Monthly review | Continuous live analytics |
| **Staffing Allocation** | Fixed schedule | Traffic-pattern-driven |
| **Merchandising Decisions** | Intuition-based | CV + POS data-driven |
| **Customer Funnel** | Unknown | Fully tracked and staged |

### Strategic Enablers

- **Real-time operational visibility** – Store managers gain instant awareness of live conditions
- **Improved customer experience** – Reduced congestion, optimized queues, better zone navigation
- **Better workforce allocation** – Staff deployment guided by real-time traffic data
- **Data-driven merchandising** – Promotion and shelf decisions backed by zone engagement analytics
- **Faster decision-making** – Automated intelligence replaces manual observation and delayed reports

---

## 🚀 Live Deployment

### Live Dashboard
[https://store-intelligence-ta.streamlit.app/](https://store-intelligence-ta.streamlit.app/)

### Backend API Documentation
[https://store-intelligence-2a9l.onrender.com/docs](https://store-intelligence-2a9l.onrender.com/docs)

### Source Code Repository
[https://github.com/Tanmay24-ya/Store-Intelligence](https://github.com/Tanmay24-ya/Store-Intelligence)

---

*Document Version: 1.0 · Purplle Store Intelligence Engine Hackathon Submission · June 2026*
