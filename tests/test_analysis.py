"""Tests for analysis module."""

import numpy as np
import pandas as pd

from src.analysis import correlation_matrix, daily_returns, run_full_analysis
from src.config import TICKERS
from src.data_fetch import load_demo_prices


def test_daily_returns_shape():
    prices = load_demo_prices()
    rets = daily_returns(prices)
    assert rets.shape[1] == len(TICKERS)
    assert len(rets) == len(prices) - 1


def test_correlation_matrix_properties():
    prices = load_demo_prices()
    corr = correlation_matrix(daily_returns(prices))
    assert list(corr.columns) == TICKERS
    assert np.allclose(np.diag(corr), 1.0)
    assert np.allclose(corr, corr.T)


def test_run_full_analysis_keys():
    results = run_full_analysis(load_demo_prices())
    expected = {
        "prices",
        "simple_returns",
        "log_returns",
        "stats_loop",
        "stats_broadcast",
        "cumulative_log_return",
        "moving_averages",
        "rolling_volatility",
        "correlation",
        "monthly_groupby",
        "monthly_resample",
        "volatility_spikes",
    }
    assert expected <= set(results.keys())
    pd.testing.assert_frame_equal(
        results["stats_loop"],
        results["stats_broadcast"],
        check_names=True,
    )
