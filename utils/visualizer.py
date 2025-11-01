import plotly.graph_objects as go
import pandas as pd

def plot_cases_deaths(df: pd.DataFrame, country: str):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["date"], y=df["cases_avg"],
        mode="lines", name="7-day Avg Cases"
    ))
    fig.add_trace(go.Scatter(
        x=df["date"], y=df["deaths_avg"],
        mode="lines", name="7-day Avg Deaths"
    ))
    fig.update_layout(
        title=f"COVID-19 Cases & Deaths Trends in {country}",
        xaxis_title="Date",
        yaxis_title="Count",
        template="plotly_white"
    )
    return fig


def plot_vaccinations(df: pd.DataFrame, country: str):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["date"], y=df["people_vaccinated"],
        mode="lines", name="People Vaccinated"
    ))
    fig.update_layout(
        title=f"Vaccination Progress in {country}",
        xaxis_title="Date",
        yaxis_title="People Vaccinated",
        template="plotly_white"
    )
    return fig


def plot_icu(df: pd.DataFrame, country: str):
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df["date"], y=df["icu_patients"],
        name="ICU Patients"
    ))
    fig.update_layout(
        title=f"ICU Patients Over Time in {country}",
        xaxis_title="Date",
        yaxis_title="Patients",
        template="plotly_white"
    )
    return fig
