"""Core analysis: returns, rolling metrics, correlation, resampling."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from src.config import PROCESSED_DIR, ROLLING_LONG, ROLLING_SHORT, TICKERS
from src.utils import cumulative_log_return, log_returns_from_prices, summary_stats, vectorized_summary


def load_prices_wide(path: Path | None = None) -> pd.DataFrame:
    path = path or PROCESSED_DIR / "prices_wide.csv"
    df = pd.read_csv(path, index_col=0, parse_dates=True)
    df.index = pd.to_datetime(df.index)
    return df.sort_index()


def daily_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """Simple daily percentage returns."""
    return prices.pct_change().dropna(how="all")


def rolling_moving_averages(prices: pd.DataFrame) -> pd.DataFrame:
    """Stack 20-day and 60-day moving averages for each ticker (long format metadata in columns)."""
    parts = []
    for col in prices.columns:
        ma20 = prices[col].rolling(window=ROLLING_SHORT).mean().rename(f"{col}_MA20")
        ma60 = prices[col].rolling(window=ROLLING_LONG).mean().rename(f"{col}_MA60")
        parts.extend([ma20, ma60])
    return pd.concat(parts, axis=1)


def rolling_volatility(returns: pd.DataFrame, window: int = ROLLING_SHORT) -> pd.DataFrame:
    """Rolling standard deviation of daily returns."""
    return returns.rolling(window=window).std()


def correlation_matrix(returns: pd.DataFrame) -> pd.DataFrame:
    return returns.corr()


def monthly_mean_returns(returns: pd.DataFrame) -> pd.DataFrame:
    """Group by calendar month and average daily returns."""
    monthly = returns.groupby(returns.index.to_period("M")).mean()
    monthly.index = monthly.index.astype(str)
    return monthly


def resample_monthly_returns(returns: pd.DataFrame) -> pd.DataFrame:
    """Resample to month-end and compound daily returns within each month."""
    compounded = (1 + returns).resample("ME").prod() - 1
    return compounded


def run_full_analysis(prices: pd.DataFrame | None = None) -> dict:
    """Run all analysis steps and return a dict of results for notebooks/plots."""
    prices = prices if prices is not None else load_prices_wide()
    simple_ret = daily_returns(prices)
    log_ret = log_returns_from_prices(prices).dropna(how="all")

    stats_loop = summary_stats(simple_ret)
    stats_broadcast = vectorized_summary(simple_ret)
    cum_log = cumulative_log_return(log_ret)

    ma = rolling_moving_averages(prices)
    roll_vol = rolling_volatility(simple_ret)
    corr = correlation_matrix(simple_ret)
    monthly_gb = monthly_mean_returns(simple_ret)
    monthly_rs = resample_monthly_returns(simple_ret)

    # Volatility spike dates (top 1% rolling vol per ticker)
    vol_spikes = {}
    for col in roll_vol.columns:
        threshold = roll_vol[col].quantile(0.99)
        spikes = roll_vol[col][roll_vol[col] >= threshold].dropna()
        vol_spikes[col] = spikes

    return {
        "prices": prices,
        "simple_returns": simple_ret,
        "log_returns": log_ret,
        "stats_loop": stats_loop,
        "stats_broadcast": stats_broadcast,
        "cumulative_log_return": cum_log,
        "moving_averages": ma,
        "rolling_volatility": roll_vol,
        "correlation": corr,
        "monthly_groupby": monthly_gb,
        "monthly_resample": monthly_rs,
        "volatility_spikes": vol_spikes,
    }


if __name__ == "__main__":
    results = run_full_analysis()
    print("Correlation matrix:\n", results["correlation"])
    print("\nSummary stats:\n", results["stats_loop"])
