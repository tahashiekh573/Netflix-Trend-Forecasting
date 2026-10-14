
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
from statsmodels.tsa.holtwinters import Holt

warnings.filterwarnings("ignore")

# Load dataset and count titles added per year
df = pd.read_csv("Dataset.csv")
df["date_added"] = pd.to_datetime(df["date_added"], errors="coerce")
df = df.dropna(subset=["date_added"]).copy()
df["year"] = df["date_added"].dt.year

yearly = (
    df[df["year"] <= 2020]
    .groupby("year")
    .size()
    .reindex(range(2008, 2021), fill_value=0)
)

# Hold out the final 3 complete years
train = yearly.iloc[:-3]
test = yearly.iloc[-3:]

# Model 1: Linear Regression
linear = LinearRegression()
linear.fit(
    train.index.to_numpy().reshape(-1, 1),
    train.to_numpy()
)

linear_pred = np.maximum(
    0,
    linear.predict(test.index.to_numpy().reshape(-1, 1))
)

# Model 2: Holt's trend method
holt = Holt(
    train.astype(float),
    initialization_method="estimated"
).fit(optimized=True)

holt_pred = np.maximum(
    0,
    np.asarray(holt.forecast(len(test)))
)

def metrics(actual, predicted):
    mae = mean_absolute_error(actual, predicted)
    rmse = np.sqrt(mean_squared_error(actual, predicted))
    return mae, rmse

results = []

for name, predictions in [
    ("Linear Regression", linear_pred),
    ("Holt Exponential Smoothing", holt_pred)
]:
    mae, rmse = metrics(test.to_numpy(), predictions)
    results.append({
        "Model": name,
        "MAE": round(mae, 2),
        "RMSE": round(rmse, 2)
    })

    print(f"\n{name}")
    print(f"MAE: {mae:.2f}")
    print(f"RMSE: {rmse:.2f}")

comparison = pd.DataFrame(results)
comparison.to_csv("model_comparison.csv", index=False)

print("\nModel Comparison:")
print(comparison.to_string(index=False))

# Visualize test predictions
plt.figure(figsize=(10, 5))
plt.plot(test.index, test.values, marker="o", label="Actual")
plt.plot(test.index, linear_pred, marker="o", label="Linear Regression")
plt.plot(test.index, holt_pred, marker="o", label="Holt Forecast")
plt.title("Forecast Model Comparison (Test Years)")
plt.xlabel("Year")
plt.ylabel("Titles Added")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("model_comparison.png", dpi=300)
plt.close()

print("\nSaved: model_comparison.csv")
print("Saved: model_comparison.png")
