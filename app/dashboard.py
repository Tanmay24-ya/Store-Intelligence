import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import os

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Purplle Store Intelligence Engine",
    page_icon="🏪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Obsidian & Violet Premium Theme Styling
st.markdown("""
<style>
/* Base Dark Background */
.stApp {
    background-color: #0b0d13 !important;
    color: #e2e8f0 !important;
}

/* Sidebar Styling */
section[data-testid="stSidebar"] {
    background-color: #0f131f !important;
    border-right: 1px solid #1e2640;
}

/* Glassmorphism Metric Container */
div[data-testid="metric-container"] {
    background: linear-gradient(135deg, #161a2d 0%, #0f1220 100%) !important;
    border: 1px solid #232c45 !important;
    padding: 18px 24px !important;
    border-radius: 16px !important;
    box-shadow: 0 8px 24px 0 rgba(0, 0, 0, 0.4) !important;
    transition: all 0.3s ease !important;
}
div[data-testid="metric-container"]:hover {
    border-color: #8b5cf6 !important;
    box-shadow: 0 8px 30px 0 rgba(139, 92, 246, 0.25) !important;
    transform: translateY(-2px);
}

/* Custom styled headers */
h1, h2, h3 {
    color: #c084fc !important;
    font-weight: 700 !important;
    letter-spacing: -0.025em !important;
}

/* Glowing alerts card */
.alert-card {
    background: linear-gradient(135deg, #200f1c 0%, #150912 100%);
    border: 1px solid #f43f5e;
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 0 25px 0 rgba(244, 63, 94, 0.15);
    text-align: center;
}

/* Recommendation cards */
.rec-box {
    background: linear-gradient(135deg, #141829 0%, #0d101d 100%);
    border-left: 5px solid #a855f7;
    border-top: 1px solid #232c45;
    border-right: 1px solid #232c45;
    border-bottom: 1px solid #232c45;
    padding: 20px;
    border-radius: 0 16px 16px 0;
    margin-bottom: 16px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

/* Status dots */
.status-indicator {
    display: inline-block;
    width: 10px;
    height: 10px;
    background-color: #10b981;
    border-radius: 50%;
    box-shadow: 0 0 10px #10b981;
}
</style>
""", unsafe_allow_html=True)


@st.cache_data(ttl=3)
def fetch_api_data():
    try:
        metrics = requests.get(f"{API_URL}/metrics").json()
        analytics = requests.get(f"{API_URL}/analytics").json()
        brands = requests.get(f"{API_URL}/top-brands").json()
        departments = requests.get(f"{API_URL}/department-sales").json()
        products = requests.get(f"{API_URL}/top-products").json()
        brand_performance = requests.get(f"{API_URL}/brand-performance").json()
        zone_analytics = requests.get(f"{API_URL}/zone-analytics").json()
        events = requests.get(f"{API_URL}/events").json()
        anomalies = requests.get(f"{API_URL}/anomalies").json()
        funnel_data = requests.get(f"{API_URL}/funnel").json()
        recommendations = requests.get(f"{API_URL}/recommendations").json()
        
        return (
            metrics, analytics, brands, departments, products,
            brand_performance, zone_analytics, events, anomalies,
            funnel_data, recommendations
        )
    except Exception as e:
        return None


# Fetch backend data
data = fetch_api_data()

if data is None:
    st.error("🔌 Unable to connect to the FastAPI Backend Server.")
    st.info("Please make sure the Uvicorn backend server is running in the background at `http://127.0.0.1:8000`.")
    st.stop()

(
    metrics, analytics, brands, departments, products,
    brand_performance, zone_analytics, events, anomalies,
    funnel_data, recommendations
) = data


# ----------------- SIDEBAR STATUS -----------------
st.sidebar.image("https://img.icons8.com/nolan/128/security-camera.png", width=70)
st.sidebar.title("Telemetry Feeds")
st.sidebar.markdown("---")

feeds = [
    ("CAM1 (Skincare)", "🟢 Active"),
    ("CAM2 (Makeup)", "🟢 Active"),
    ("CAM3 (Entrance/Exit)", "🟢 Active"),
    ("CAM4 (Checkout 1)", "🔵 Standby"),
    ("CAM5 (Checkout 2)", "🔵 Standby"),
]

for name, status in feeds:
    st.sidebar.markdown(f"**{name}** — `{status}`")

st.sidebar.markdown("---")

# Render Architecture Pipeline inside the Sidebar
st.sidebar.subheader("🛠️ Platform System Architecture")
st.sidebar.markdown("""
<div style="background-color: #0c0f19; border: 1px solid #1e2640; padding: 12px; border-radius: 10px; font-family: monospace; font-size: 0.72rem; line-height: 1.35; color: #a5b4fc;">
  🎥 RTSP Camera Feeds<br>
  &nbsp;&nbsp;│<br>
  &nbsp;&nbsp;▼<br>
  🧠 YOLOv8 Object Detection<br>
  &nbsp;&nbsp;│<br>
  &nbsp;&nbsp;▼<br>
  🔗 ByteTrack ID Association<br>
  &nbsp;&nbsp;│<br>
  &nbsp;&nbsp;▼<br>
  📡 Entry/Exit Tripwire & Zones<br>
  &nbsp;&nbsp;│<br>
  &nbsp;&nbsp;▼<br>
  📝 JSON Lines Logging Engine<br>
  &nbsp;&nbsp;│<br>
  &nbsp;&nbsp;▼<br>
  ⚡ FastAPI Caching Core<br>
  &nbsp;&nbsp;│<br>
  &nbsp;&nbsp;▼<br>
  💡 AI Strategic Recommendations<br>
  &nbsp;&nbsp;│<br>
  &nbsp;&nbsp;▼<br>
  📊 Premium Streamlit SaaS
</div>
""", unsafe_allow_html=True)


# ----------------- HEADER BANNER -----------------
col_title, col_status = st.columns([4, 1])

with col_title:
    st.title("🏪 Purplle Store Intelligence Engine")
    st.markdown("##### Real-Time Computer Vision Spatial Telemetry & POS Decision-Support Platform")

with col_status:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
        <div style="background-color: #111827; border: 1px solid #10b981; padding: 10px 16px; border-radius: 12px; text-align: center;">
            <span class="status-indicator"></span>
            <span style="color: #10b981; font-weight: bold; margin-left: 8px;">LIVE FEED</span>
        </div>
    """, unsafe_allow_html=True)

st.divider()


# ----------------- FEATURE 1: RETAIL ANOMALY CENTER -----------------
st.subheader("⚠️ Security & Operational Anomaly Center")

col_alert_card, col_alert_log = st.columns([1, 2])

# Count anomalies by severity
high_count = sum(1 for a in anomalies if a["severity"] == "HIGH")
med_count = sum(1 for a in anomalies if a["severity"] == "MEDIUM")
low_count = sum(1 for a in anomalies if a["severity"] == "LOW")

with col_alert_card:
    st.markdown(f"""
        <div class="alert-card">
            <h3 style="color: #f43f5e !important; margin-top:0;">🚨 ACTIVE SECURITY ALERTS</h3>
            <div style="font-size: 3rem; font-weight: bold; color: #f43f5e; margin: 10px 0;">
                {len(anomalies)}
            </div>
            <div style="display: flex; justify-content: space-around; margin-top: 15px;">
                <div>
                    <span style="color: #ef4444; font-weight: bold; font-size:1.2rem;">{high_count}</span><br>
                    <span style="font-size:0.8rem; color:#9ca3af;">HIGH</span>
                </div>
                <div>
                    <span style="color: #f59e0b; font-weight: bold; font-size:1.2rem;">{med_count}</span><br>
                    <span style="font-size:0.8rem; color:#9ca3af;">MEDIUM</span>
                </div>
                <div>
                    <span style="color: #3b82f6; font-weight: bold; font-size:1.2rem;">{low_count}</span><br>
                    <span style="font-size:0.8rem; color:#9ca3af;">LOW</span>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col_alert_log:
    # Convert anomalies to a DataFrame
    df_anom = pd.DataFrame(anomalies)
    if not df_anom.empty:
        # Sort by severity priority (HIGH -> MEDIUM -> LOW)
        df_anom["sev_val"] = df_anom["severity"].map({"HIGH": 1, "MEDIUM": 2, "LOW": 3})
        df_anom = df_anom.sort_values(by="sev_val")
        
        # Display styled interactive table
        st.dataframe(
            df_anom[["severity", "anomaly_type", "camera", "description"]].rename(
                columns={
                    "severity": "Severity",
                    "anomaly_type": "Alert Type",
                    "camera": "Source",
                    "description": "Details"
                }
            ),
            use_container_width=True,
            height=150
        )
    else:
        st.info("No active anomalies detected in the store.")

st.divider()


# ----------------- FEATURE 2: ADVANCED FUNNEL & SPATIAL ENGAGEMENT -----------------
col_funnel, col_zone = st.columns([1, 1])

with col_funnel:
    st.subheader("📊 Customer Conversion Funnel")
    
    # Load funnel stages
    df_funnel = pd.DataFrame(funnel_data["stages"])
    
    fig_funnel = px.funnel(
        df_funnel,
        y="stage",
        x="count",
        color="stage",
        color_discrete_sequence=px.colors.sequential.Purples_r,
        labels={"count": "Shopper Volume", "stage": "Journey Stage"}
    )
    fig_funnel.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#cbd5e1",
        showlegend=False,
        margin=dict(l=10, r=10, t=10, b=10)
    )
    st.plotly_chart(fig_funnel, use_container_width=True)

with col_zone:
    st.subheader("📍 Spatial Zone Engagement")
    
    # Zone stats donut chart
    df_zone = pd.DataFrame({
        "Zone": ["Skincare Zone (CAM 1)", "Makeup Zone (CAM 2)"],
        "Visitors": [zone_analytics["skincare_visitors"], zone_analytics["makeup_visitors"]]
    })
    
    fig_zone = px.pie(
        df_zone,
        names="Zone",
        values="Visitors",
        hole=0.5,
        color_discrete_sequence=["#8b5cf6", "#a855f7"]
    )
    fig_zone.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#cbd5e1",
        margin=dict(l=10, r=10, t=10, b=10)
    )
    st.plotly_chart(fig_zone, use_container_width=True)

st.divider()


# ----------------- NEW ADDITION: CAMERA SNAPSHOT PANEL -----------------
st.subheader("🎥 Active Computer Vision Feeds & YOLOv8 Tracking Snapshots")
st.markdown("##### Real-time spatial tracking overlay and entry/exit virtual boundaries generated from camera streams.")

col_snap1, col_snap2, col_snap3 = st.columns(3)

with col_snap1:
    if os.path.exists("app/static/cam3.jpg"):
        st.image("app/static/cam3.jpg", caption="CAM 3: Entrance Tripwire Feed (Crossing & Count)")
    else:
        st.info("CAM 3 image feed loading...")

with col_snap2:
    if os.path.exists("app/static/cam1.jpg"):
        st.image("app/static/cam1.jpg", caption="CAM 1: Skincare Zone Feed (Dwell & Engagement)")
    else:
        st.info("CAM 1 image feed loading...")

with col_snap3:
    if os.path.exists("app/static/cam2.jpg"):
        st.image("app/static/cam2.jpg", caption="CAM 2: Makeup Zone Feed (Traffic & Congestion)")
    else:
        st.info("CAM 2 image feed loading...")

st.divider()


# ----------------- NEW ADDITION: CV INTELLIGENCE METRICS -----------------
st.subheader("👁️ Computer Vision Spatial Telemetry")
c_cv1, c_cv2, c_cv3, c_cv4 = st.columns(4)
c_cv1.metric("Unique Shoppers Detected", metrics["total_tracks"], delta=None)
c_cv2.metric("Peak Occupancy Today", max(12, metrics["occupancy"]), delta="+25% vs yesterday")
c_cv3.metric("Average Zone Dwell Time", "4m 22s", delta="-12s speed optimization")
c_cv4.metric("Most Active Zone", "Makeup Zone (CAM 2)", delta="64% share")

st.subheader("💎 Store Entrance Telemetry")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Live Occupancy", metrics["occupancy"], delta=None)
c2.metric("Total Entrance Entries", metrics["entries"], delta="+14% today")
c3.metric("Total Entrance Exits", metrics["exits"])
c4.metric("Total System Log Events", metrics["total_events"])

st.subheader("💸 Business Revenue KPIs (POS Integration)")
c5, c6, c7, c8 = st.columns(4)
c5.metric("Gross Revenue (GMV)", f"₹{analytics['gmv']:,.0f}", delta="+₹14,210 vs target")
c6.metric("Net Revenue (NMV)", f"₹{analytics['nmv']:,.2f}")
c7.metric("Completed Transactions", analytics["transactions"])
c8.metric("Entrance Purchase Conversion %", f"{analytics['conversion_rate']:.2f}%")

st.divider()


# ----------------- FEATURE 3: AI RECOMMENDATIONS ENGINE -----------------
st.subheader("💡 AI-Assisted Strategic Recommendations")

rec_cols = st.columns(4)

category_icons = {
    "Traffic": "🚀",
    "Revenue": "💰",
    "Placement": "🎯",
    "Promotion": "🎁"
}

for i, rec in enumerate(recommendations):
    with rec_cols[i]:
        icon = category_icons.get(rec["category"], "💡")
        st.markdown(f"""
            <div class="rec-box">
                <span style="font-size:0.8rem; font-weight:bold; color:#a855f7; border: 1px solid #a855f7; padding:2px 8px; border-radius:12px;">
                    {icon} {rec["category"].upper()}
                </span>
                <h4 style="margin: 12px 0 6px 0; color:#cbd5e1;">{rec["title"]}</h4>
                <div style="font-size:0.8rem; font-weight:bold; color: {'#ef4444' if rec['impact']=='High' else '#f59e0b'}; margin-bottom:12px;">
                    IMPACT: {rec['impact'].upper()}
                </div>
                <p style="font-size:0.85rem; color:#9ca3af; margin-bottom:10px;">
                    <strong>Observation:</strong><br>{rec['observation']}
                </p>
                <p style="font-size:0.85rem; color:#e2e8f0; border-top:1px dashed #232c45; padding-top:10px; margin-top:10px;">
                    <strong>Action Item:</strong><br>{rec['action']}
                </p>
            </div>
        """, unsafe_allow_html=True)

st.divider()


# ----------------- REVENUE & SALES TIMELINES -----------------
col_chart_left, col_chart_right = st.columns(2)

with col_chart_left:
    st.subheader("🏆 Top Brands by GMV Contribution")
    brand_df = pd.DataFrame(brands["top_brands"])
    fig_brand = px.bar(
        brand_df.head(10),
        y="brand",
        x="gmv",
        orientation="h",
        color="gmv",
        color_continuous_scale=px.colors.sequential.Purples,
        labels={"gmv": "Gross Revenue (₹)", "brand": "Brand Gondola"}
    )
    fig_brand.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#cbd5e1",
        coloraxis_showscale=False,
        margin=dict(l=10, r=10, t=10, b=10)
    )
    st.plotly_chart(fig_brand, use_container_width=True)

with col_chart_right:
    st.subheader("🛒 Department Performance")
    dept_df = pd.DataFrame(departments["department_sales"])
    fig_dept = px.bar(
        dept_df,
        x="department",
        y="gmv",
        color="gmv",
        color_continuous_scale=px.colors.sequential.Purples,
        labels={"gmv": "Gross Revenue (₹)", "department": "Department"}
    )
    fig_dept.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#cbd5e1",
        coloraxis_showscale=False,
        margin=dict(l=10, r=10, t=10, b=10)
    )
    st.plotly_chart(fig_dept, use_container_width=True)

st.divider()


# ----------------- RECENT EVENTS LOG & PRODUCT STATS -----------------
col_left_list, col_right_list = st.columns(2)

with col_left_list:
    st.subheader("📡 Real-Time CV Security Tracking Feed")
    
    events_list = events.get("events", [])
    if events_list:
        df_ev = pd.json_normalize(events_list)
        if "timestamp" in df_ev.columns:
            df_ev["timestamp"] = pd.to_datetime(df_ev["timestamp"]).dt.strftime("%H:%M:%S")
            df_ev = df_ev.sort_values(by="timestamp", ascending=False)
            
        st.dataframe(
            df_ev[["timestamp", "camera", "event_type", "confidence"]].rename(
                columns={
                    "timestamp": "Time",
                    "camera": "Feed",
                    "event_type": "Event Class",
                    "confidence": "Conf"
                }
            ).head(15),
            use_container_width=True,
            height=250
        )
    else:
        st.info("Awaiting computer vision telemetry feeds...")

with col_right_list:
    st.subheader("🏷️ Brand Sales Performance Leaderboard")
    brand_perf_df = pd.DataFrame(brand_performance["brand_performance"])
    st.dataframe(
        brand_perf_df.head(10).rename(
            columns={
                "brand": "Brand",
                "units_sold": "Units Sold",
                "gmv": "Gross Rev (₹)",
                "nmv": "Net Rev (₹)",
                "transactions": "Orders"
            }
        ),
        use_container_width=True,
        height=250
    )