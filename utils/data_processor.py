import pandas as pd

def preprocess_data(df: pd.DataFrame, country: str) -> pd.DataFrame:
    """
    Filter and clean the OWID data for a given country.
    Adds rolling averages for smoother visualization.
    """
    df_country = df[df["location"] == country].copy()
    if df_country.empty:
        raise ValueError(f"No data found for {country}. Check country name spelling.")
    
    df_country = df_country[["date", "new_cases", "new_deaths", "people_vaccinated", "icu_patients"]]
    df_country["date"] = pd.to_datetime(df_country["date"])
    
    # Compute 7-day rolling averages
    df_country["cases_avg"] = df_country["new_cases"].rolling(7).mean()
    df_country["deaths_avg"] = df_country["new_deaths"].rolling(7).mean()
    
    # Fill missing values
    df_country.fillna(0, inplace=True)
    return df_country
