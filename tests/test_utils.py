"""Tests for utility functions."""

import numpy as np
import pandas as pd
import pytest

from src.utils import (
    cumulative_log_return,
    log_returns_from_prices,
    summary_stats,
    vectorized_summary,
)


def test_log_returns_from_prices_calculation():
    """log(P_t / P_{t-1}); first row NaN, subsequent rows match formula."""
    prices = pd.DataFrame({"A": [100.0, 110.0, 121.0], "B": [50.0, 55.0, 52.5]})
    log_ret = log_returns_from_prices(prices)

    assert np.isnan(log_ret.iloc[0, 0])
    assert np.isnan(log_ret.iloc[0, 1])
    assert log_ret.iloc[1, 0] == pytest.approx(np.log(110.0 / 100.0))
    assert log_ret.iloc[2, 0] == pytest.approx(np.log(121.0 / 110.0))
    assert log_ret.iloc[1, 1] == pytest.approx(np.log(55.0 / 50.0))
    assert log_ret.iloc[2, 1] == pytest.approx(np.log(52.5 / 55.0))


def test_log_returns_first_row_is_nan():
    prices = pd.DataFrame({"A": [100.0, 110.0, 105.0]})
    log_ret = log_returns_from_prices(prices)
    assert np.isnan(log_ret.iloc[0, 0])
    assert log_ret.iloc[1, 0] == pytest.approx(np.log(1.1))


def test_summary_stats_and_vectorized_match():
    returns = pd.DataFrame(
        {
            "GOOGL": [0.01, -0.02, 0.015, 0.005],
            "NVDA": [0.03, -0.01, 0.02, -0.005],
        }
    )
    loop = summary_stats(returns)
    broadcast = vectorized_summary(returns)
    pd.testing.assert_frame_equal(loop, broadcast)


def test_cumulative_log_return_sums():
    log_ret = pd.DataFrame({"A": [0.01, 0.02, -0.01]})
    cum = cumulative_log_return(log_ret)
    assert cum.iloc[-1, 0] == pytest.approx(0.02)
