
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error

print("=" * 60)
print("NETFLIX TREND FORECASTING MODEL")
print("=" * 60)

# 1. Load and prepare data
df = pd.read_csv("Dataset.csv")

df["date_added"] = pd.to_datetime(
    df["date_added"],
    errors="coerce"
)

df = df.dropna(subset=["date_added"]).copy()
df["year"] = df["date_added"].dt.year

yearly = (
    df.groupby("year")
    .size()
    .reset_index(name="titles_added")
    .sort_values("year")
)

# Note: 2021 is incomplete, so use complete years
# through 2020 for the initial model evaluation.
model_data = yearly[yearly["year"] <= 2020].copy()

X = model_data[["year"]]
y = model_data["titles_added"]

# 2. Chronological train/test split
# Train on earlier years, test on the latest 3 complete years.
X_train = X.iloc[:-3]
X_test = X.iloc[-3:]
y_train = y.iloc[:-3]
y_test = y.iloc[-3:]

# 3. Train baseline model
model = LinearRegression()
model.fit(X_train, y_train)

# 4. Evaluate on unseen later years
test_predictions = np.maximum(
    0, model.predict(X_test)
)

mae = mean_absolute_error(y_test, test_predictions)
rmse = np.sqrt(mean_squared_error(y_test, test_predictions))

print("\nModel: Linear Regression")
print("Training years:", int(X_train["year"].min()),
      "to", int(X_train["year"].max()))
print("Testing years:", X_test["year"].tolist())

evaluation = pd.DataFrame({
    "Year": X_test["year"].values,
    "Actual_Titles": y_test.values,
    "Predicted_Titles": np.round(test_predictions).astype(int)
})

print("\nTest Predictions:")
print(evaluation.to_string(index=False))

print(f"\nMean Absolute Error (MAE): {mae:.2f}")
print(f"Root Mean Squared Error (RMSE): {rmse:.2f}")

evaluation.to_csv("forecast_evaluation.csv", index=False)

# 5. Retrain using all complete years for future estimates
final_model = LinearRegression()
final_model.fit(X, y)

future_years = np.arange(2021, 2026)
future_X = pd.DataFrame({"year": future_years})

future_predictions = np.maximum(
    0, final_model.predict(future_X)
)

future_df = pd.DataFrame({
    "Year": future_years,
    "Forecast_Titles_Added": np.round(
        future_predictions
    ).astype(int)
})

future_df.to_csv("future_forecast.csv", index=False)

print("\nFuture Forecasts (estimates, not guarantees):")
print(future_df.to_string(index=False))

# 6. Plot historical data and future forecasts
plt.figure(figsize=(10, 5))

plt.plot(
    X["year"],
    y,
    marker="o",
    label="Historical Data"
)

plt.plot(
    future_years,
    future_predictions,
    marker="o",
    linestyle="--",
    label="Linear Regression Forecast"
)

plt.axvline(
    2020,
    linestyle=":",
    label="Last Complete Historical Year"
)

plt.title("Netflix Content Addition Trend Forecast")
plt.xlabel("Year")
plt.ylabel("Titles Added")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("future_forecast.png", dpi=300)
plt.close()

print("\nSaved files:")
print("- forecast_evaluation.csv")
print("- future_forecast.csv")
print("- future_forecast.png")
print("\nForecasting process completed.")
