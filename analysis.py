# analysis.py
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

def compute_kpis(df: pd.DataFrame, date_col: str, value_col: str) -> dict:
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])
    df = df.sort_values(date_col)

    # Monthly aggregation
    df['month'] = df[date_col].dt.to_period('M')
    monthly = df.groupby('month')[value_col].sum().reset_index()
    monthly['month_str'] = monthly['month'].astype(str)

    values = monthly[value_col].values

    # Core stats
    stats = {
        'total':      float(values.sum()),
        'mean':       float(values.mean()),
        'median':     float(np.median(values)),
        'std':        float(values.std()),
        'min':        float(values.min()),
        'max':        float(values.max()),
        'months':     len(values),
        'monthly_data': monthly,
    }

    # Month-over-month change
    if len(values) >= 2:
        mom = (values[-1] - values[-2]) / values[-2] * 100
        stats['mom_change_pct'] = round(mom, 2)
    else:
        stats['mom_change_pct'] = None

    # Growth trend (slope via linear regression)
    if len(values) >= 3:
        X = np.arange(len(values)).reshape(-1, 1)
        reg = LinearRegression().fit(X, values)
        stats['trend_slope'] = float(reg.coef_[0])
        stats['trend_direction'] = 'upward' if reg.coef_[0] > 0 else 'downward'

        # Forecast next 3 months
        future_X = np.arange(len(values), len(values)+3).reshape(-1, 1)
        stats['forecast_3m'] = reg.predict(future_X).tolist()
    else:
        stats['trend_direction'] = 'insufficient data'
        stats['forecast_3m'] = []

    # Anomaly detection (simple z-score)
    z_scores = (values - values.mean()) / (values.std() + 1e-9)
    anomaly_months = monthly['month_str'].values[np.abs(z_scores) > 2].tolist()
    stats['anomalies'] = anomaly_months

    return stats