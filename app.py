import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import pycountry
from utils.data_loader import load_offline_data

st.set_page_config(page_title="Pandemic Analytics Dashboard", layout="wide")

#   Load data  
@st.cache_data
def get_data():
    df = load_offline_data()
    df["iso_alpha"] = df["location"].apply(lambda x: pycountry.countries.lookup(x).alpha_3 if x in [c.name for c in pycountry.countries] else None)
    return df

df = get_data()

st.title("🧬 Pandemic Analytics Dashboard 2.0")
st.caption("Offline synthetic data – no internet connection required.")

#   World map  
st.subheader("🌍 Select a Country")

map_metric = st.selectbox("Choose a metric to visualize on the world map:",
                          ["new_cases", "new_deaths", "people_vaccinated", "icu_patients"])

latest = df.groupby(["location", "iso_alpha"])[map_metric].mean().reset_index()

fig_map = px.choropleth(
    latest,
    locations="iso_alpha",
    color=map_metric,
    hover_name="location",
    color_continuous_scale="Viridis",
    title=f"Average {map_metric.replace('_',' ').title()} by Country"
)
fig_map.update_layout(height=500, margin=dict(l=0, r=0, t=40, b=0))

st.plotly_chart(fig_map, use_container_width=True)

#   Country selection  
st.subheader("📊 Country Details")

countries = sorted(df["location"].unique())
country = st.selectbox("Select Country:", countries, index=countries.index("Germany") if "Germany" in countries else 0)
data_country = df[df["location"] == country].sort_values("date")

#   Tabs for different analyses  
tab1, tab2, tab3 = st.tabs(["Overview", "Trends", "Comparisons"])

# --- Overview ---
with tab1:
    st.markdown(f"### {country} – Overview")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Average Daily Cases", f"{data_country['new_cases'].mean():.0f}")
    col2.metric("Average Daily Deaths", f"{data_country['new_deaths'].mean():.0f}")
    col3.metric("Total Vaccinated", f"{data_country['people_vaccinated'].max():,.0f}")
    col4.metric("Average ICU Patients", f"{data_country['icu_patients'].mean():.0f}")

# --- Trends ---
with tab2:
    st.markdown("#### Time Series Trends")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data_country["date"], y=data_country["new_cases"], mode="lines", name="New Cases"))
    fig.add_trace(go.Scatter(x=data_country["date"], y=data_country["new_deaths"], mode="lines", name="New Deaths"))
    fig.add_trace(go.Scatter(x=data_country["date"], y=data_country["icu_patients"], mode="lines", name="ICU Patients"))
    fig.update_layout(height=450, template="plotly_white", legend_title="Metrics", xaxis_title="Date", yaxis_title="Count")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### Vaccination Progress")
    fig2 = px.area(data_country, x="date", y="people_vaccinated",
                   title="People Vaccinated Over Time", template="plotly_white")
    st.plotly_chart(fig2, use_container_width=True)

# --- Comparison ---

with tab3:
    st.markdown("#### Country Comparisons")

    # Build a safe default list (avoid Streamlit default value error)
    default_comparisons = []
    for name in ["France", "India"]:
        if name in countries and name != country:
            default_comparisons.append(name)

    available_comparisons = [c for c in countries if c != country]

    selected_countries = st.multiselect(
        "Compare with other countries:",
        available_comparisons,
        default=default_comparisons
    )

    if selected_countries:
        df_comp = df[df["location"].isin([country] + selected_countries)]
        fig3 = px.line(
            df_comp,
            x="date",
            y="new_cases",
            color="location",
            title="New Cases Comparison",
            template="plotly_white"
        )
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.info("Select one or more countries to compare.")
    if selected_countries:
        df_comp = df[df["location"].isin([country] + selected_countries)]
        fig3 = px.line(df_comp, x="date", y="new_cases", color="location",
                       title="New Cases Comparison", template="plotly_white")
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.info("Select one or more countries to compare.")

st.success(" Dashboard loaded successfully in offline mode.")
