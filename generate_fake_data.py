import pandas as pd
import numpy as np
from datetime import datetime
import os
import sys

#  Configuration
countries = [
    "Germany", "France", "United Kingdom", "Italy", "Spain",
    "Poland", "Sweden", "Norway", "United States", "Canada",
    "Japan", "South Korea", "India", "Brazil", "Australia"
]
start_date = datetime(2023, 1, 1)
end_date = datetime(2024, 12, 31)

# === Generate Dates ===
dates = pd.date_range(start_date, end_date, freq="D")

print(f"[INFO] Generating synthetic data for {len(countries)} countries and {len(dates)} days...")

# Generate Fake Data
rows = []
rng = np.random.default_rng(42)

for country in countries:
    base_cases = rng.integers(100, 2000)
    base_deaths = rng.integers(1, 50)
    base_vaccinated = rng.integers(10_000_000, 100_000_000)
    base_icu = rng.integers(100, 5000)
    wave = np.sin(np.linspace(0, 8, len(dates))) * rng.integers(100, 800)

    for i, date in enumerate(dates):
        new_cases = abs(base_cases + rng.normal(0, 300) + wave[i])
        new_deaths = abs(base_deaths + rng.normal(0, 10))
        icu_patients = abs(base_icu + rng.normal(0, 200))
        vaccinated = base_vaccinated + i * rng.integers(500, 2000)

        rows.append({
            "location": country,
            "date": date.strftime("%Y-%m-%d"),
            "new_cases": round(new_cases),
            "new_deaths": round(new_deaths),
            "people_vaccinated": vaccinated,
            "icu_patients": round(icu_patients)
        })

# Create DataFrame
df = pd.DataFrame(rows)
print(f"[INFO] Generated {len(df):,} rows.")

# === Save CSV ===
os.makedirs("data", exist_ok=True)
output_path = os.path.join("data", "synthetic-pandemic-data.csv")

try:
    df.to_csv(output_path, index=False)
    print(f"[SUCCESS] Saved to: {os.path.abspath(output_path)}")
except Exception as e:
    print(f"[ERROR] Could not save file: {e}")
    sys.exit(1)

print("[DONE] Data generation complete.")
