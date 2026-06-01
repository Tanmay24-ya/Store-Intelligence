import json
from fastapi import FastAPI
from app.utils import load_events
from collections import defaultdict
from app.analytics import load_transactions

app = FastAPI(
    title="Store Intelligence System"
)


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


@app.get("/events")
def events():
    return {
        "events": load_events()
    }


@app.get("/metrics")
def metrics():

    events = load_events()

    entries = sum(
        1
        for e in events
        if e["event_type"] == "customer_entry"
    )

    exits = sum(
        1
        for e in events
        if e["event_type"] == "customer_exit"
    )

    detected_ids = set()

    for event in events:

        track_id = (
            event
            .get("details", {})
            .get("track_id")
        )

        if track_id is not None:
            detected_ids.add(track_id)

    return {
        "occupancy": max(0, entries - exits),
        "entries": entries,
        "exits": exits,
        "total_tracks": len(detected_ids),
        "total_events": len(events)
    }


@app.get("/funnel")
def funnel():

    events = load_events()

    detected = len({
        e["details"]["track_id"]
        for e in events
        if (
            e["event_type"] == "person_detected"
            and "track_id" in e["details"]
        )
    })

    entered = sum(
        1
        for e in events
        if e["event_type"] == "customer_entry"
    )

    exited = sum(
        1
        for e in events
        if e["event_type"] == "customer_exit"
    )

    return {
        "detected": detected,
        "entered": entered,
        "exited": exited,
        "current_inside": max(
            0,
            entered - exited
        )
    }

@app.get("/analytics")
def analytics():

    transactions = load_transactions()

    total_transactions = len(
        transactions
    )

    gmv = float(
        transactions["GMV"]
        .fillna(0)
        .sum()
    )

    nmv = float(
        transactions["NMV"]
        .fillna(0)
        .sum()
    )

    try:

        with open(
            "data/zone_stats.json",
            "r"
        ) as f:

            zone_data = json.load(f)

        visitors = (
            zone_data["skincare_visitors"]
            + zone_data["makeup_visitors"]
        )

    except:

        visitors = 0

    conversion_rate = 0

    if visitors > 0:

        conversion_rate = round(
            (
                total_transactions
                / visitors
            ) * 100,
            2
        )

    return {
        "visitors": visitors,
        "transactions": total_transactions,
        "gmv": round(gmv, 2),
        "nmv": round(nmv, 2),
        "conversion_rate": conversion_rate
    }

@app.get("/top-brands")
def top_brands():

    transactions = load_transactions()

    brand_sales = (
        transactions
        .groupby("brand_name")["GMV"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    return {
        "top_brands": [
            {
                "brand": brand,
                "gmv": float(gmv)
            }
            for brand, gmv in brand_sales.items()
        ]
    }

@app.get("/department-sales")
def department_sales():

    transactions = load_transactions()

    departments = (
        transactions
        .groupby("dep_name")["GMV"]
        .sum()
        .sort_values(ascending=False)
    )

    return {
        "department_sales": [
            {
                "department": dep,
                "gmv": float(gmv)
            }
            for dep, gmv in departments.items()
        ]
    }

@app.get("/top-products")
def top_products():

    transactions = load_transactions()

    products = (
        transactions
        .groupby("product_name")
        .agg({
            "qty": "sum",
            "GMV": "sum"
        })
        .sort_values("GMV", ascending=False)
        .head(10)
    )

    return {
        "top_products": [
            {
                "product": product,
                "qty": int(row["qty"]),
                "gmv": float(row["GMV"])
            }
            for product, row in products.iterrows()
        ]
    }

@app.get("/brand-performance")
def brand_performance():

    transactions = load_transactions()

    brands = (
        transactions
        .groupby("brand_name")
        .agg({
            "qty": "sum",
            "GMV": "sum",
            "NMV": "sum",
            "order_id": "nunique"
        })
        .sort_values("GMV", ascending=False)
    )

    return {
        "brand_performance": [
            {
                "brand": brand,
                "units_sold": int(row["qty"]),
                "gmv": float(row["GMV"]),
                "nmv": float(row["NMV"]),
                "transactions": int(row["order_id"])
            }
            for brand, row in brands.iterrows()
        ]
    }

@app.get("/recent-events")
def recent_events():

    events = load_events()

    return {
        "events": events[-20:]
    }


@app.get("/zone-analytics")
def zone_analytics():

    import json

    with open("data/zone_stats.json") as f:
        data = json.load(f)

    return {
        "skincare_visitors": data["skincare_visitors"],
        "makeup_visitors": data["makeup_visitors"],
        "total_zone_visitors":
            data["skincare_visitors"] +
            data["makeup_visitors"]
    }