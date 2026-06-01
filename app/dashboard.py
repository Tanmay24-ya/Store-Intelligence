import streamlit as st
import pandas as pd
import requests
import plotly.express as px

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Store Intelligence Dashboard",
    page_icon="🏪",
    layout="wide"
)

st.markdown("""
<style>
.main {
    background-color: #0f1117;
}
div[data-testid="metric-container"] {
    background-color: #1c1f26;
    border: 1px solid #2d3748;
    padding: 15px;
    border-radius: 12px;
}
h1,h2,h3 {
    color: #c084fc;
}
</style>
""", unsafe_allow_html=True)


@st.cache_data(ttl=5)
def load_data():

    metrics = requests.get(
        f"{API_URL}/metrics"
    ).json()

    analytics = requests.get(
        f"{API_URL}/analytics"
    ).json()

    brands = requests.get(
        f"{API_URL}/top-brands"
    ).json()

    departments = requests.get(
        f"{API_URL}/department-sales"
    ).json()

    products = requests.get(
        f"{API_URL}/top-products"
    ).json()

    brand_performance = requests.get(
        f"{API_URL}/brand-performance"
    ).json()

    zone_analytics = requests.get(
        f"{API_URL}/zone-analytics"
    ).json()

    events = requests.get(
        f"{API_URL}/events"
    ).json()

    zone_data = requests.get(
        f"{API_URL}/zone-analytics"
    ).json()

    return (
        metrics,
        analytics,
        brands,
        departments,
        products,
        brand_performance,
        zone_analytics,
        events,
        zone_data
    )


try:

    (
        metrics,
        analytics,
        brands,
        departments,
        products,
        brand_performance,
        zone_analytics,
        events,
        zone_data
    ) = load_data()

except Exception as e:

    st.error(
        f"Cannot connect to FastAPI server: {e}"
    )

    st.stop()


st.title("🏪 Store Intelligence Dashboard")

st.markdown(
    "Real-time Retail Analytics powered by Computer Vision and POS Data"
)

st.divider()


# Store KPIs


st.subheader("Store KPIs")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Occupancy",
    metrics["occupancy"]
)

c2.metric(
    "Entries",
    metrics["entries"]
)

c3.metric(
    "Exits",
    metrics["exits"]
)

c4.metric(
    "Visitors",
    analytics["visitors"]
)

st.divider()


# Business KPIs


st.subheader("Business KPIs")

c5, c6, c7, c8 = st.columns(4)

c5.metric(
    "GMV",
    f"₹{analytics['gmv']:,.0f}"
)

c6.metric(
    "NMV",
    f"₹{analytics['nmv']:,.2f}"
)

c7.metric(
    "Transactions",
    analytics["transactions"]
)

c8.metric(
    "Conversion %",
    f"{analytics['conversion_rate']:.2f}%"
)

st.divider()


# Zone Analytics


st.subheader("Zone Analytics")

z1, z2, z3 = st.columns(3)

z1.metric(
    "Skincare Visitors",
    zone_analytics["skincare_visitors"]
)

z2.metric(
    "Makeup Visitors",
    zone_analytics["makeup_visitors"]
)

z3.metric(
    "Total Zone Visitors",
    zone_analytics["total_zone_visitors"]
)

zone_df = pd.DataFrame({
    "Zone": ["Skincare", "Makeup"],
    "Visitors": [
        zone_analytics["skincare_visitors"],
        zone_analytics["makeup_visitors"]
    ]
})

fig = px.pie(
    zone_df,
    names="Zone",
    values="Visitors",
    title="Zone Visitor Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# Charts


left, right = st.columns(2)

with left:

    st.subheader("Top Brands by GMV")

    brand_df = pd.DataFrame(
        brands["top_brands"]
    )

    fig = px.bar(
        brand_df,
        x="brand",
        y="gmv",
        title="Top Brands"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    st.subheader("Department Revenue")

    dept_df = pd.DataFrame(
        departments["department_sales"]
    )

    fig = px.bar(
        dept_df,
        x="department",
        y="gmv",
        title="Department Sales"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()


# Top Products


st.subheader("Top Products")

product_df = pd.DataFrame(
    products["top_products"]
)

st.dataframe(
    product_df,
    use_container_width=True,
    height=350
)

st.divider()

# Brand Performance


st.subheader("Brand Performance")

brand_perf_df = pd.DataFrame(
    brand_performance["brand_performance"]
)

st.dataframe(
    brand_perf_df,
    use_container_width=True,
    height=350
)

st.divider()


#------------------------------

st.divider()

st.subheader("🏆 Top Brands by GMV")

fig = px.bar(
    brand_df.head(10),
    x="brand",
    y="gmv",
    color="gmv",
    title="Top Brands by GMV"
)

fig.update_layout(
    plot_bgcolor="#0f1117",
    paper_bgcolor="#0f1117",
    font_color="white"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

st.subheader("Department Sales")

fig = px.bar(
    dept_df,
    x="department",
    y="gmv",
    color="gmv",
    title="Department Revenue"
)

fig.update_layout(
    plot_bgcolor="#0f1117",
    paper_bgcolor="#0f1117",
    font_color="white"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# Recent Events

st.subheader("Recent Events")

events_list = events.get(
    "events",
    []
)

if len(events_list) > 0:

    events_df = pd.json_normalize(
        events_list
    )

    if "timestamp" in events_df.columns:

        events_df = events_df.sort_values(
            by="timestamp",
            ascending=False
        )

    st.dataframe(
        events_df,
        use_container_width=True,
        height=400
    )

else:

    st.info(
        "No events available."
    )

st.divider()


# Business Insights

st.subheader("Business Insights")

top_brand = brand_df.iloc[0]["brand"]
top_department = dept_df.iloc[0]["department"]

st.info(f"""
• Top Revenue Brand: {top_brand}

• Top Revenue Department: {top_department}

• Zone Visitors: {analytics['visitors']}

• Conversion Rate: {analytics['conversion_rate']:.2f}%

• Most Visited Zone:
{"Makeup" if zone_data["makeup_visitors"] > zone_data["skincare_visitors"] else "Skincare"}
""")


st.divider()

st.success(
    "🟢 Store Intelligence System Online"
)