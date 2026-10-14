import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Netflix Trend Forecasting Dashboard",
    page_icon="🎬",
    layout="wide",
)

BASE_DIR = Path(__file__).resolve().parent

st.title("🎬 Netflix Trend Forecasting Dashboard")
st.caption("Historical Content Analysis | Time Series Forecasting")
st.info(
    "Note: The source dataset ends on September 25, 2021. "
    "Forecast values are model estimates, not verified actual Netflix counts."
)

# =========================================================
# HELPERS
# =========================================================
@st.cache_data
def load_csv(filename):
    path = BASE_DIR / filename
    if not path.exists():
        return None
    try:
        return pd.read_csv(path)
    except Exception as exc:
        st.warning(f"Could not read `{filename}`: {exc}")
        return None


def find_col(df, candidates):
    """Find a column using case-insensitive, whitespace-insensitive names."""
    lookup = {
        str(col).strip().lower().replace(" ", "_"): col
        for col in df.columns
    }
    for name in candidates:
        key = name.strip().lower().replace(" ", "_")
        if key in lookup:
            return lookup[key]
    return None


def numeric_col(df, exclude=None):
    """Return the first column with values that can be converted to numbers."""
    exclude = set(exclude or [])
    for col in df.columns:
        if col in exclude:
            continue
        values = pd.to_numeric(df[col], errors="coerce")
        if values.notna().any():
            return col
    return None


# =========================================================
# LOAD PROJECT OUTPUTS
# =========================================================
yearly = load_csv("yearly_additions.csv")
content_type = load_csv("yearly_content_type.csv")
comparison = load_csv("model_comparison.csv")
forecast = load_csv("final_forecast.csv")
evaluation = load_csv("forecast_evaluation.csv")

# =========================================================
# HISTORICAL DATA
# =========================================================
if yearly is None or yearly.empty:
    st.error(
        "The file `yearly_additions.csv` was not found or is empty."
    )
    st.write("Expected location:")
    st.code(str(BASE_DIR / "yearly_additions.csv"))
    st.write("Run `python analyze_trends.py` from the project folder, then refresh.")
    st.stop()

year_col = find_col(yearly, ["year", "date_year", "added_year"])
count_col = find_col(
    yearly,
    [
        "count",
        "content_count",
        "total",
        "additions",
        "titles_added",
        "title_count",
        "num_titles",
    ],
)

# Fallbacks for CSV files with unexpected but valid column names.
if year_col is None:
    year_col = yearly.columns[0] if len(yearly.columns) else None
if count_col is None and year_col is not None:
    count_col = numeric_col(yearly, exclude=[year_col])

if year_col is None or count_col is None:
    st.error("Could not identify the year and count columns in yearly_additions.csv.")
    st.write("Columns found:", yearly.columns.tolist())
    st.stop()

yearly[year_col] = pd.to_numeric(yearly[year_col], errors="coerce")
yearly[count_col] = pd.to_numeric(yearly[count_col], errors="coerce")
yearly = yearly.dropna(subset=[year_col, count_col]).sort_values(year_col)

if yearly.empty:
    st.error("No usable rows were found in yearly_additions.csv.")
    st.stop()

yearly[year_col] = yearly[year_col].astype(int)

# =========================================================
# SIDEBAR FILTER
# =========================================================
st.sidebar.header("Dashboard Filters")

min_year = int(yearly[year_col].min())
max_year = int(yearly[year_col].max())

if min_year < max_year:
    selected_range = st.sidebar.slider(
        "Historical year range",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
    )
else:
    selected_range = (min_year, max_year)
    st.sidebar.caption(f"Year available: {min_year}")

filtered = yearly[
    yearly[year_col].between(selected_range[0], selected_range[1])
].copy()

# =========================================================
# KPI CARDS
# =========================================================
total_additions = int(filtered[count_col].sum()) if not filtered.empty else 0
peak_row = filtered.loc[filtered[count_col].idxmax()] if not filtered.empty else None

k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Content Additions", f"{total_additions:,}")
k2.metric("Years Analyzed", f"{filtered[year_col].nunique():,}")
k3.metric(
    "Peak Addition Year",
    str(int(peak_row[year_col])) if peak_row is not None else "N/A",
)
k4.metric(
    "Peak Year Additions",
    f"{int(peak_row[count_col]):,}" if peak_row is not None else "N/A",
)

st.divider()

# =========================================================
# HISTORICAL TREND
# =========================================================
st.subheader("📈 Historical Netflix Content Additions")

history_fig = px.line(
    filtered,
    x=year_col,
    y=count_col,
    markers=True,
    template="plotly_white",
    labels={year_col: "Year", count_col: "Titles Added"},
    title="Yearly Content Additions",
)
history_fig.update_layout(margin=dict(l=10, r=10, t=55, b=10))
st.plotly_chart(history_fig, use_container_width=True)

# =========================================================
# MOVIE VS TV SHOW TRENDS
# =========================================================
st.subheader("🎞️ Movie vs TV Show Trends")

if content_type is not None and not content_type.empty:
    ct_year = find_col(content_type, ["year", "date_year", "added_year"])
    ct_type = find_col(content_type, ["type", "content_type", "category"])
    ct_count = find_col(
        content_type,
        [
            "count",
            "content_count",
            "total",
            "additions",
            "titles_added",
            "title_count",
            "num_titles",
        ],
    )

    if ct_year is None:
        ct_year = content_type.columns[0] if len(content_type.columns) else None
    if ct_type is None:
        # For a typical year/type/count table, type is the second column.
        if len(content_type.columns) >= 3:
            ct_type = content_type.columns[1]
    if ct_count is None and ct_year is not None:
        ct_count = numeric_col(content_type, exclude=[ct_year, ct_type])

    if ct_year is not None and ct_type is not None and ct_count is not None:
        content_type[ct_year] = pd.to_numeric(content_type[ct_year], errors="coerce")
        content_type[ct_count] = pd.to_numeric(content_type[ct_count], errors="coerce")
        ct_filtered = content_type.dropna(subset=[ct_year, ct_count]).copy()
        ct_filtered = ct_filtered[
            ct_filtered[ct_year].between(selected_range[0], selected_range[1])
        ]

        if not ct_filtered.empty:
            type_fig = px.line(
                ct_filtered,
                x=ct_year,
                y=ct_count,
                color=ct_type,
                markers=True,
                template="plotly_white",
                labels={
                    ct_year: "Year",
                    ct_count: "Titles Added",
                    ct_type: "Content Type",
                },
                title="Yearly Additions by Content Type",
            )
            type_fig.update_layout(margin=dict(l=10, r=10, t=55, b=10))
            st.plotly_chart(type_fig, use_container_width=True)
        else:
            st.warning("No content-type records exist in the selected year range.")
    else:
        st.warning("Could not identify the columns in yearly_content_type.csv.")
        st.write("Columns found:", content_type.columns.tolist())
else:
    st.info("`yearly_content_type.csv` is missing. Run `analyze_trends.py` to create it.")

# =========================================================
# FUTURE FORECAST
# =========================================================
st.subheader("🔮 Future Content Forecast")

if forecast is not None and not forecast.empty:
    forecast_year_col = find_col(
        forecast, ["year", "forecast_year", "prediction_year", "ds"]
    )
    forecast_value_col = find_col(
        forecast,
        [
            "forecast",
            "predicted",
            "prediction",
            "predicted_count",
            "predicted_additions",
            "titles_forecast",
            "holt_forecast",
            "yhat",
        ],
    )

    if forecast_year_col is None:
        forecast_year_col = forecast.columns[0] if len(forecast.columns) else None
    if forecast_value_col is None and forecast_year_col is not None:
        forecast_value_col = numeric_col(forecast, exclude=[forecast_year_col])

    if forecast_year_col is not None and forecast_value_col is not None:
        forecast[forecast_year_col] = pd.to_numeric(
            forecast[forecast_year_col], errors="coerce"
        )
        forecast[forecast_value_col] = pd.to_numeric(
            forecast[forecast_value_col], errors="coerce"
        )
        forecast_clean = forecast.dropna(
            subset=[forecast_year_col, forecast_value_col]
        ).copy()

        if not forecast_clean.empty:
            forecast_fig = px.line(
                forecast_clean,
                x=forecast_year_col,
                y=forecast_value_col,
                markers=True,
                template="plotly_white",
                labels={
                    forecast_year_col: "Year",
                    forecast_value_col: "Forecasted Titles",
                },
                title="Holt Exponential Smoothing Forecast",
            )
            forecast_fig.update_layout(margin=dict(l=10, r=10, t=55, b=10))
            st.plotly_chart(forecast_fig, use_container_width=True)
            st.dataframe(forecast_clean, use_container_width=True)
        else:
            st.warning("Forecast CSV has no valid numeric forecast rows.")
            st.dataframe(forecast.head())
    else:
        st.warning("Could not identify forecast columns.")
        st.write("Columns found:", forecast.columns.tolist())
        st.dataframe(forecast.head())
else:
    st.info("`final_forecast.csv` is missing. Run `final_forecast.py` first.")

# =========================================================
# MODEL COMPARISON
# =========================================================
st.subheader("🧪 Forecast Model Comparison")

if comparison is not None and not comparison.empty:
    st.dataframe(comparison, use_container_width=True)

    model_col = find_col(comparison, ["model", "model_name", "name"])
    metric_cols = [
        col for col in comparison.columns
        if str(col).strip().lower() in ["mae", "rmse", "mse", "r2", "r_squared"]
    ]

    if model_col is not None and metric_cols:
        plot_data = comparison.melt(
            id_vars=[model_col],
            value_vars=metric_cols,
            var_name="Metric",
            value_name="Score",
        )
        plot_data["Score"] = pd.to_numeric(plot_data["Score"], errors="coerce")
        plot_data = plot_data.dropna(subset=["Score"])

        if not plot_data.empty:
            comparison_fig = px.bar(
                plot_data,
                x=model_col,
                y="Score",
                color="Metric",
                barmode="group",
                template="plotly_white",
                title="Model Evaluation Metrics (lower MAE/RMSE is better)",
            )
            st.plotly_chart(comparison_fig, use_container_width=True)
else:
    st.info("`model_comparison.csv` is missing. Run `compare_models.py` first.")

if evaluation is not None and not evaluation.empty:
    with st.expander("View Forecast Evaluation Details"):
        st.dataframe(evaluation, use_container_width=True)

# =========================================================
# RAW DATA TABLE
# =========================================================
with st.expander("View Historical Data"):
    st.dataframe(filtered, use_container_width=True)

st.success("Dashboard loaded successfully.")
