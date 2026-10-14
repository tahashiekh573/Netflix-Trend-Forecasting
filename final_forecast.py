
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from statsmodels.tsa.holtwinters import Holt

warnings.filterwarnings("ignore")

print("=" * 60)
print("NETFLIX TREND FORECASTING")
print("FINAL HOLT MODEL")
print("=" * 60)

# Load dataset
df = pd.read_csv("Dataset.csv")
df["date_added"] = pd.to_datetime(
    df["date_added"], errors="coerce"
)
df = df.dropna(subset=["date_added"]).copy()
df["year"] = df["date_added"].dt.year

# Use complete years only: 2008-2020
yearly = (
    df[df["year"] <= 2020]
    .groupby("year")
    .size()
    .reindex(range(2008, 2021), fill_value=0)
)

# Fit final model using all complete historical years
model = Holt(
    yearly.astype(float),
    initialization_method="estimated"
).fit(optimized=True)

# Forecast five years beyond the final complete year
future_years = np.arange(2021, 2026)
predictions = np.maximum(
    0,
    np.asarray(model.forecast(5))
)

forecast_df = pd.DataFrame({
    "Year": future_years,
    "Forecast_Titles_Added": np.round(
        predictions
    ).astype(int)
})

forecast_df.to_csv("final_forecast.csv", index=False)

print("\nHistorical period: 2008-2020")
print("\nForecast estimates:")
print(forecast_df.to_string(index=False))

# Save chart
plt.figure(figsize=(10, 5))
plt.plot(
    yearly.index,
    yearly.values,
    marker="o",
    label="Historical Additions"
)
plt.plot(
    future_years,
    predictions,
    marker="o",
    linestyle="--",
    label="Holt Forecast"
)
plt.axvline(
    2020,
    linestyle=":",
    label="Last Complete Historical Year"
)
plt.title("Netflix Content Addition Forecast")
plt.xlabel("Year")
plt.ylabel("Titles Added")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("final_forecast.png", dpi=300)
plt.close()

print("\nSaved files:")
print("- final_forecast.csv")
print("- final_forecast.png")
print("\nFinal forecasting completed successfully.")
