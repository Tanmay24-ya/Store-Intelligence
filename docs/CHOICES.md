# Purplle Store Intelligence Engine – Technical Choices

> **Hackathon Submission** · Purplle Store Intelligence Engine · June 2026

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Why YOLOv8?](#why-yolov8)
3. [Why ByteTrack?](#why-bytetrack)
4. [Why JSONL Event Storage?](#why-jsonl-event-storage)
5. [Event Schema Design](#event-schema-design)
6. [Why FastAPI?](#why-fastapi)
7. [API Design Decisions](#api-design-decisions)
8. [Why Streamlit?](#why-streamlit)
9. [Scalability Considerations](#scalability-considerations)
10. [Final Technology Stack](#final-technology-stack)
11. [Live Deployment](#live-deployment)

---

## Overview

This document explains the **technology, model, schema, and architecture decisions** made while building the Purplle Store Intelligence Engine.

Every choice was evaluated against three criteria:

| Criterion | Description |
|---|---|
| **Performance** | Must sustain real-time or near-real-time operation in a retail store environment |
| **Simplicity** | Must be deployable and maintainable without a large infrastructure team |
| **Extensibility** | Must support future enhancements such as multi-store and predictive analytics |

---

## Why YOLOv8?

**YOLOv8** (You Only Look Once, version 8) by Ultralytics is the object detection backbone of the platform.

### Decision Rationale

| Factor | YOLOv8 | Faster R-CNN | SSD | YOLOv5 |
|---|---|---|---|---|
| **Inference Speed** | ✅ Excellent | ⚠️ Slow (two-stage) | ✅ Good | ✅ Good |
| **Detection Accuracy** | ✅ State-of-the-art | ✅ High | ⚠️ Moderate | ✅ High |
| **Deployment Simplicity** | ✅ Single pip install | ❌ Complex | ⚠️ Moderate | ✅ Good |
| **Retail Surveillance** | ✅ Optimized | ⚠️ Overkill | ⚠️ Moderate | ✅ Good |
| **Community & Docs** | ✅ Actively maintained | ⚠️ Declining | ⚠️ Limited | ✅ Strong |
| **Export Formats** | ✅ ONNX, TFLite, TRT | ⚠️ Limited | ⚠️ Limited | ✅ Good |

### Key Advantages

- **Real-time performance** – Nano variant (`yolov8n.pt`) achieves > 30 FPS on CPU, enabling practical deployment without GPU infrastructure
- **Strong accuracy** – Achieves SOTA mAP scores on COCO for the person class (class 0) used in this project
- **One-line deployment** – `from ultralytics import YOLO; model = YOLO("yolov8n.pt")`
- **Robust retail surveillance** – Pre-trained COCO weights generalize extremely well to indoor retail person detection
- **Ultralytics ecosystem** – Active maintenance, regular updates, excellent documentation

### Configuration

```python
model = YOLO("yolov8n.pt")
results = model(frame, classes=[0], conf=0.50, verbose=False)
```

- `classes=[0]` – Filters exclusively for person detections
- `conf=0.50` – Confidence threshold that eliminates low-quality false positives while preserving genuine detections

---

## Why ByteTrack?

**ByteTrack** is the multi-object tracking (MOT) algorithm used to assign persistent identities to detected shoppers across frames.

### Decision Rationale

| Factor | ByteTrack | SORT | DeepSORT | StrongSORT |
|---|---|---|---|---|
| **ID Stability** | ✅ Excellent | ⚠️ Moderate | ✅ Good | ✅ Good |
| **Occlusion Handling** | ✅ Strong | ❌ Poor | ✅ Good | ✅ Good |
| **Computational Cost** | ✅ Very Low | ✅ Low | ⚠️ Moderate (ReID) | ⚠️ Moderate |
| **Crowded Environments** | ✅ Designed for this | ⚠️ Struggles | ⚠️ Moderate | ✅ Good |
| **No ReID Model Needed** | ✅ Yes | ✅ Yes | ❌ Requires ReID | ❌ Requires ReID |

### Key Advantages

- **Stable customer identities** – Prevents the same shopper from being counted multiple times due to detection gaps
- **Handles temporary occlusions** – ByteTrack's low-score detection buffer preserves tracks during moments when a shopper walks behind shelving or another customer
- **Lightweight** – No separate ReID embedding network required, keeping inference overhead minimal
- **Retail-optimized** – ByteTrack's design specifically targets crowded, overlapping-person environments, which is exactly the retail floor scenario

### Why Not DeepSORT?

DeepSORT requires a separate **Re-Identification (ReID) neural network** to compute appearance embeddings, significantly increasing computational cost and deployment complexity. ByteTrack achieves comparable or better tracking performance using only IoU-based association with a dual-threshold strategy.

---

## Why JSONL Event Storage?

All analytics events are stored as **JSON Lines** (`.jsonl`) — one JSON object per line.

### Decision Rationale

| Factor | JSONL | SQLite | PostgreSQL | Parquet |
|---|---|---|---|---|
| **Append-Only Writes** | ✅ O(1) file append | ⚠️ Indexed insert | ⚠️ Network + transaction | ❌ Not append-friendly |
| **Human Readable** | ✅ Fully readable | ❌ Binary | ❌ Network query | ❌ Binary columnar |
| **Zero Configuration** | ✅ Native file I/O | ✅ Embedded | ❌ Requires server | ⚠️ Library required |
| **Stream Processing** | ✅ Line-by-line | ⚠️ Cursor-based | ⚠️ Cursor-based | ✅ Columnar batch |
| **External Integration** | ✅ Universal | ⚠️ SQLite-specific | ✅ Broad | ✅ Broad |

### Key Advantages

- **Append-only logging** – Writing a new event is a single file append with no locking contention
- **Human readable** – Engineers can directly inspect the event log without any tooling
- **Lightweight** – No database server, no migrations, no schema enforcement overhead
- **Stream processing friendly** – Trivially integrable with Kafka, Flink, or Spark for future scale
- **Simple integration** – Any Python script can read or write without a database driver

---

## Event Schema Design

Every analytics event uses a **flat, minimal schema** that captures the essential context without over-engineering.

### Schema

```json
{
  "timestamp": "2026-06-01T10:00:01",
  "camera": "CAM3",
  "event_type": "entry",
  "track_id": 15,
  "confidence": 0.93
}
```

### Field Definitions

| Field | Type | Description |
|---|---|---|
| `timestamp` | `ISO 8601 string` | UTC timestamp of event occurrence |
| `camera` | `string` | Source camera identifier (`CAM1`, `CAM2`, `CAM3`) |
| `event_type` | `string` | Semantic event label (entry, exit, zone_enter, zone_exit, anomaly) |
| `track_id` | `integer` | ByteTrack-assigned unique shopper identifier |
| `confidence` | `float [0–1]` | YOLOv8 detection confidence at event trigger |

### Design Principles

- **Flat structure** – No nested objects; simplifies downstream processing
- **ISO 8601 timestamps** – Universal, sortable, timezone-safe
- **Camera-keyed** – Every event is unambiguously associated with its source zone
- **Track ID as primary key** – Enables cross-event shopper journey reconstruction
- **Confidence preserved** – Allows downstream filtering by detection quality

---

## Why FastAPI?

**FastAPI** is the REST API framework serving all analytics endpoints.

### Decision Rationale

| Factor | FastAPI | Flask | Django REST | Express (Node) |
|---|---|---|---|---|
| **Performance** | ✅ ASGI async, top-tier | ⚠️ WSGI sync | ⚠️ WSGI sync | ✅ Async |
| **Auto OpenAPI Docs** | ✅ Built-in `/docs` | ❌ Manual | ⚠️ Third-party | ❌ Manual |
| **Type Safety** | ✅ Pydantic + Python types | ❌ None | ⚠️ Serializers | ❌ None |
| **Streamlit Integration** | ✅ Seamless HTTP | ✅ Works | ✅ Works | ⚠️ Language mismatch |
| **Learning Curve** | ✅ Minimal | ✅ Minimal | ❌ Steep | ⚠️ Moderate |

### Key Advantages

- **High performance** – ASGI-based async handling supports concurrent dashboard refresh requests without blocking
- **Automatic OpenAPI documentation** – `/docs` endpoint is auto-generated from Pydantic models, requiring zero manual maintenance
- **Type safety** – All request/response models are Pydantic-validated, eliminating an entire class of serialization bugs
- **Seamless Streamlit integration** – Dashboard makes standard HTTP GET requests; FastAPI handles them with minimal overhead

---

## API Design Decisions

### Design Philosophy

All endpoints are **read-only `GET` operations** that return pre-aggregated analytics. This design choice enables:

1. **Response caching** – Aggregates are computed once and cached; multiple dashboard clients share the same computation
2. **Stateless clients** – The dashboard does not need to maintain any local analytics state
3. **Simple integration** – Any third-party BI tool can consume these endpoints with zero custom integration work

### Endpoint Contracts

```
GET /metrics
  → Returns: total_footfall, current_occupancy, unique_shoppers,
             peak_occupancy, avg_dwell_time, conversion_rate

GET /funnel
  → Returns: stages [ { stage, visitors, conversion_pct } ]
             Stages: Entry → Zone Visit → Checkout → Purchase

GET /anomalies
  → Returns: alerts [ { type, severity, description, timestamp } ]
             Severities: LOW · MEDIUM · HIGH · CRITICAL

GET /recommendations
  → Returns: recommendations [ { priority, title, description, action } ]
             Priority: IMMEDIATE · HIGH · MEDIUM · LOW
```

---

## Why Streamlit?

**Streamlit** is the frontend framework powering the analytics dashboard.

### Decision Rationale

| Factor | Streamlit | React + D3 | Grafana | Dash (Plotly) |
|---|---|---|---|---|
| **Development Speed** | ✅ Hours | ❌ Days/weeks | ⚠️ Configuration | ✅ Days |
| **Python Native** | ✅ Pure Python | ❌ JavaScript | ⚠️ Mixed | ✅ Python |
| **Plotly Integration** | ✅ First-class | ⚠️ Manual | ✅ Built-in | ✅ First-class |
| **Deployment** | ✅ Streamlit Cloud | ⚠️ Custom server | ⚠️ Self-hosted | ⚠️ Custom server |
| **Custom Styling** | ✅ CSS injection | ✅ Full control | ⚠️ Limited | ✅ Good |

### Key Advantages

- **Rapid dashboard development** – Entire analytics UI built in pure Python without frontend engineering overhead
- **Interactive visualizations** – Native Plotly integration delivers gauge charts, funnel diagrams, bar charts, and time-series plots
- **Streamlit Cloud deployment** – One-click deployment with automatic HTTPS and public URL at zero cost
- **Strong analytics ecosystem** – Designed specifically for data and analytics applications

---

## Scalability Considerations

The current architecture is designed for **single-store deployment**. The following enhancements are planned for production scale:

### Compute Layer
- **GPU inference** – Upgrade from CPU to NVIDIA GPU for YOLOv8 to support higher frame rates and more simultaneous camera streams

### Data Layer
- **Kafka event streaming** – Replace JSONL file append with Kafka topics for distributed, high-throughput event delivery
- **Cloud object storage** – Archive processed events to S3/GCS for long-term retention and batch analytics
- **TimescaleDB** – Migrate from JSONL to a time-series database for high-performance metric queries at scale

### Application Layer
- **Multi-store deployment** – Horizontally scale the FastAPI backend across multiple store instances with a shared analytics aggregation layer
- **Real-time analytics pipelines** – Apache Flink or Spark Streaming for sub-second cross-store aggregations
- **Predictive forecasting models** – LSTM or Prophet models for footfall forecasting and proactive staffing recommendations

---

## Final Technology Stack

### Computer Vision Pipeline

| Component | Technology | Purpose |
|---|---|---|
| **Object Detection** | YOLOv8n (Ultralytics) | Real-time person detection |
| **Video Processing** | OpenCV | Frame capture and preprocessing |
| **Multi-Object Tracking** | ByteTrack | Persistent shopper ID assignment |

### Backend

| Component | Technology | Purpose |
|---|---|---|
| **API Framework** | FastAPI | REST analytics endpoints |
| **Data Validation** | Pydantic | Request/response schema enforcement |
| **ASGI Server** | Uvicorn | High-performance async serving |

### Frontend

| Component | Technology | Purpose |
|---|---|---|
| **Dashboard Framework** | Streamlit | Interactive analytics UI |
| **Charting Library** | Plotly | Gauge, funnel, bar, and time-series charts |

### Analytics & Data

| Component | Technology | Purpose |
|---|---|---|
| **Data Processing** | Pandas | Event aggregation and metric computation |
| **Numerical Computing** | NumPy | Statistical calculations |
| **Event Storage** | JSONL | Append-only event log |
| **Transaction Data** | CSV | POS transaction records |

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
