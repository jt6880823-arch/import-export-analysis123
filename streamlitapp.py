# -------------------------------------------------
# streamlit_app.py
# -------------------------------------------------
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# ---------- Placeholder functions ----------
def cluster_countries(df, n_clusters=3):
    """Simple random clustering (replace with real K-Means later)"""
    np.random.seed(42)
    df = df.copy()
    df["Cluster"] = np.random.randint(0, n_clusters, size=len(df))
    return df


def forecast_trade(series, steps=30):
    """Return a flat forecast (replace with ARIMA later)"""
    if len(series) == 0:
        return [0.0] * steps
    return [series.mean()] * steps


# ---------- App UI ----------
st.title("International Trade Dashboard")
st.markdown(
    "A Streamlit dashboard for **global trade analysis**: imports, exports, clustering, forecasting and interactive maps."
)

# Sidebar navigation
page = st.sidebar.selectbox(
    "Choose a page:",
    [
        "Exploratory Data Analysis (EDA)",
        "Clustering",
        "Forecasting",
        "Interactive Map",
    ],
)

# ---------- Load data ----------
@st.cache_data
def load_data():
    # ----> Replace this with your real CSV/Excel later
    return pd.DataFrame(
        {
            "Country": ["USA", "China", "Germany", "India", "Brazil"],
            "Export": [2500, 2200, 1500, 800, 400],
            "Import": [2000, 1800, 1200, 600, 300],
            "Trade_Balance": [500, 400, 300, 200, 100],
            "Year": [2023, 2023, 2023, 2023, 2023],
        }
    )


df = load_data()

# -------------------------------------------------
# PAGE: Exploratory Data Analysis (EDA)
# -------------------------------------------------
if page == "Exploratory Data Analysis (EDA)":
    st.header("Exploratory Data Analysis")

    st.subheader("Top Exporting Countries")
    top = df.nlargest(5, "Export")[["Country", "Export"]]
    st.bar_chart(top.set_index("Country"))

    st.subheader("Yearly Trade Trends")
    yearly = df.groupby("Year")[["Export", "Import"]].sum()
    st.line_chart(yearly)

# -------------------------------------------------
# PAGE: Clustering
# -------------------------------------------------
elif page == "Clustering":
    st.header("Trade Clustering")
    clustered = cluster_countries(df)

    fig = px.scatter(
        clustered,
        x="Export",
        y="Import",
        color="Cluster",
        size="Trade_Balance",
        hover_name="Country",
        title="Countries clustered by trade value & balance",
    )
    st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------
# PAGE: Forecasting
# -------------------------------------------------
elif page == "Forecasting":
    st.header("Trade Forecasting")

    series = df["Export"]
    forecast = forecast_trade(series, steps=30)

    # Build a proper DataFrame for the line chart
    future_dates = pd.date_range(start="2025-11-15", periods=30, freq="D")
    forecast_df = pd.DataFrame(
        {"Date": future_dates, "Forecasted Export": forecast}
    ).set_index("Date")

    st.subheader("Next 30-day Export Forecast")
    st.line_chart(forecast_df)

    st.info(f"Current average export: **${series.mean():,.0f} M**")

# -------------------------------------------------
# PAGE: Interactive Map
# -------------------------------------------------
elif page == "Interactive Map":
    st.header("Interactive Export Map")

    # Add mock lat/lon (replace with real coordinates later)
    map_df = df.copy()
    map_df["lat"] = [37.8, 35.7, 51.5, 20.6, -14.2]   # USA, China, Germany, India, Brazil
    map_df["lon"] = [-122.4, 104.0, 10.5, 78.9, -51.9]

    st.map(
        map_df,
        latitude="lat",
        longitude="lon",
        size="Export",
        color="Trade_Balance",
        color_continuous_scale=px.colors.cyclical.IceFire,
        zoom=1,
    )

# -------------------------------------------------
# Footer
# -------------------------------------------------
st.markdown("---")
st.caption("**Data source:** Placeholder | Built with ?? using Streamlit")