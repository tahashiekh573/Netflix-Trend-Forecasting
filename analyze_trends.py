
import pandas as pd
import matplotlib.pyplot as plt

print("=" * 60)
print("NETFLIX TREND FORECASTING")
print("HISTORICAL TREND ANALYSIS")
print("=" * 60)

df = pd.read_csv("Dataset.csv")

df["date_added"] = pd.to_datetime(
    df["date_added"],
    errors="coerce"
)

# Keep rows with valid addition dates
df = df.dropna(subset=["date_added"]).copy()
df["year"] = df["date_added"].dt.year

# Yearly totals
yearly = (
    df.groupby("year")
    .size()
    .rename("titles_added")
    .reset_index()
)

# Separate content types
yearly_type = (
    df.groupby(["year", "type"])
    .size()
    .unstack(fill_value=0)
)

# Save historical summaries
yearly.to_csv("yearly_additions.csv", index=False)
yearly_type.to_csv("yearly_content_type.csv")

print("\nYearly Content Additions:")
print(yearly.to_string(index=False))

print("\nContent Type by Year:")
print(yearly_type.to_string())

# Chart 1: Total additions per year
plt.figure(figsize=(10, 5))
plt.plot(
    yearly["year"],
    yearly["titles_added"],
    marker="o"
)
plt.title("Netflix Titles Added Per Year")
plt.xlabel("Year")
plt.ylabel("Number of Titles Added")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("historical_trend.png", dpi=300)
plt.close()

# Chart 2: Movies vs TV Shows
ax = yearly_type.plot(
    kind="bar",
    figsize=(11, 5)
)
ax.set_title("Netflix Movies and TV Shows Added Per Year")
ax.set_xlabel("Year")
ax.set_ylabel("Number of Titles Added")
ax.legend(title="Content Type")
plt.tight_layout()
plt.savefig("content_type_trend.png", dpi=300)
plt.close()

print("\nSaved files:")
print("- yearly_additions.csv")
print("- yearly_content_type.csv")
print("- historical_trend.png")
print("- content_type_trend.png")

print("\nHistorical trend analysis completed successfully.")
