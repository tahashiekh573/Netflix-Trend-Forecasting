
import pandas as pd

print("=" * 60)
print("NETFLIX TREND FORECASTING")
print("DATASET INSPECTION")
print("=" * 60)

df = pd.read_csv("Dataset.csv")

print("\n1. Dataset Shape")
print(f"Rows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}")

print("\n2. Available Columns")
print(df.columns.tolist())

print("\n3. Missing Values")
print(df.isnull().sum())

print("\n4. Duplicate Rows")
print(df.duplicated().sum())

print("\n5. Content Type Distribution")
print(df["type"].value_counts())

print("\n6. Release Year Range")
print(df["release_year"].min(), "to", df["release_year"].max())

# Parse Netflix addition dates
df["date_added"] = pd.to_datetime(
    df["date_added"],
    errors="coerce"
)

print("\n7. Netflix Content Addition Date Range")
print("Earliest:", df["date_added"].min())
print("Latest:", df["date_added"].max())

print("\n8. Titles Added Per Year")
yearly_additions = (
    df.dropna(subset=["date_added"])
    .assign(year=lambda x: x["date_added"].dt.year)
    .groupby("year")
    .size()
    .rename("titles_added")
)

print(yearly_additions.to_string())

yearly_additions.to_csv("yearly_additions.csv")

print("\nSaved: yearly_additions.csv")
print("\nDataset inspection completed.")
