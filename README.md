# Netflix Trend Forecasting Model

## Project Overview

This project analyzes historical Netflix content additions and uses forecasting models to estimate future trends. It includes yearly trend analysis, forecasting model comparison, and an interactive Streamlit dashboard.

**Task:** Task 5 (Advanced) – Netflix Trend Forecasting Model

## Objectives

- Analyze historical Netflix content additions by year.
- Identify trends in Movies and TV Shows.
- Build and compare forecasting models.
- Generate future content addition predictions.
- Evaluate model performance using MAE and RMSE.
- Visualize historical trends and predictions through an interactive dashboard.

## Dataset

**Dataset File:** `Dataset.csv`

Important columns include:

- `type` — Content type (Movie or TV Show).
- `date_added` — Date the title was added to Netflix.
- `release_year` — Original release year.

**Data limitation:** The latest `date_added` value in the dataset is September 25, 2021. Therefore, forecasts are estimates based on historical data and should not be treated as verified current Netflix counts.

## Project Workflow

1. Inspect and prepare the dataset.
2. Analyze yearly Netflix content additions.
3. Visualize historical trends and content-type patterns.
4. Build forecasting models.
5. Evaluate and compare model performance.
6. Generate future forecasts.
7. Display results in an interactive dashboard.

## Forecasting Models

### 1. Linear Regression

Used as a baseline model to estimate trends in yearly Netflix content additions.

### 2. Holt Exponential Smoothing

Used as a time-series forecasting model to analyze historical trends and estimate future content additions.

## Model Evaluation

Models were evaluated using historical data, with 2018–2020 used as the test period.

| Model | MAE | RMSE |
|---|---:|---:|
| Linear Regression | 1118.85 | 1125.43 |
| Holt Exponential Smoothing | 855.33 | 1010.85 |

Holt Exponential Smoothing achieved lower MAE and RMSE than Linear Regression on the selected test period. However, the evaluation period contains only three years, and the prediction errors remain substantial.

## Forecast Results

The final Holt model was trained using complete yearly data from 2008–2020 to generate forecasts for 2021–2025.

The results are stored in `final_forecast.csv` and visualized in `final_forecast.png`.

These values are model-generated estimates, not verified actual Netflix content counts. The source dataset ends in September 2021, and 2021 is only partially represented.

## Interactive Dashboard

The project includes an interactive Streamlit dashboard (`app.py`) with the following features:

- KPI cards for total content additions and peak year.
- Historical yearly content-addition chart.
- Interactive historical year-range filter.
- Movies vs TV Shows trend visualization.
- Future forecasting chart and prediction table.
- Forecast model comparison.
- Model evaluation results.
- Historical data table.

## Project Files

| File | Description |
|---|---|
| `Dataset.csv` | Original Netflix dataset |
| `inspect_data.py` | Initial dataset inspection |
| `analyze_trends.py` | Historical trend analysis |
| `forecast_model.py` | Linear Regression forecasting |
| `compare_models.py` | Forecast model comparison |
| `final_forecast.py` | Final Holt forecasting |
| `app.py` | Interactive Streamlit dashboard |
| `yearly_additions.csv` | Yearly content addition counts |
| `yearly_content_type.csv` | Yearly breakdown by content type |
| `forecast_evaluation.csv` | Forecast evaluation results |
| `model_comparison.csv` | Comparison of forecasting models |
| `future_forecast.csv` | Linear Regression forecast |
| `final_forecast.csv` | Final Holt forecast |
| `historical_trend.png` | Historical trend visualization |
| `content_type_trend.png` | Content-type trend visualization |
| `model_comparison.png` | Model comparison chart |
| `future_forecast.png` | Initial forecast chart |
| `final_forecast.png` | Final forecast chart |

Some CSV and image files are generated when the analysis scripts run.

## Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Scikit-learn
- Statsmodels
- Streamlit
- Plotly

## Installation

Open PowerShell in the project directory:

```powershell
cd "E:\ML-Task\Netflix Trend Forecasting"
```

Install the required libraries:

```powershell
python -m pip install pandas numpy matplotlib scikit-learn statsmodels streamlit plotly
```

## Run the Project

Run the analysis scripts in order:

```powershell
python inspect_data.py
python analyze_trends.py
python forecast_model.py
python compare_models.py
python final_forecast.py
```

## Launch the Dashboard

Run:

```powershell
python -m streamlit run app.py
```

Open the local URL displayed in the terminal, usually:

`http://localhost:8501`

If port 8501 is already in use, run:

```powershell
python -m streamlit run app.py --server.port 8502
```

Then open:

`http://localhost:8502`

## Limitations and Future Improvements

- The dataset only contains additions through September 25, 2021.
- The test period covers only three years.
- Forecasting errors remain substantial.
- Future work could use more recent data, test additional forecasting methods, and evaluate models over a longer period.

## Conclusion

This project demonstrates a complete time-series forecasting workflow, including historical trend analysis, model development, evaluation, future prediction, and interactive visualization.

Holt Exponential Smoothing performed better than Linear Regression on the selected 2018–2020 test period. More recent data and further evaluation would help improve forecasting reliability.

---

**Project Name:** Netflix Trend Forecasting Model  
**Task:** Task 5 (Advanced)  
**Focus:** Time Series Forecasting, Predictive Analytics, Trend Analysis, and Model Evaluation
