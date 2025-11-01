import pandas as pd
import os

DATA_PATH = "data/synthetic-pandemic-data.csv"

def load_offline_data() -> pd.DataFrame:
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"{DATA_PATH} not found. Run generate_fake_data.py first.")
    df = pd.read_csv(DATA_PATH)
    df["date"] = pd.to_datetime(df["date"])
    return df
