"""Tests for fetch_data.py live single-ticker helpers."""

import pandas as pd
import pytest

from fetch_data import extract_close, summarize_price_changes


def test_summarize_price_changes():
    close = pd.Series(
        [100.0, 102.0, 101.0],
        index=pd.to_datetime(["2024-01-02", "2024-01-03", "2024-01-04"]),
    )
    summary = summarize_price_changes(close)

    assert summary["latest_close"] == pytest.approx(101.0)
    assert summary["previous_close"] == pytest.approx(102.0)
    assert summary["daily_pct"] == pytest.approx((101.0 / 102.0 - 1) * 100)
    assert summary["period_pct"] == pytest.approx(1.0)


def test_extract_close_normalizes_column():
    df = pd.DataFrame(
        {"Close": [10.0, 11.0], "Open": [9.5, 10.5]},
        index=pd.to_datetime(["2024-01-02", "2024-01-03"]),
    )
    close = extract_close(df)
    assert close.iloc[-1] == pytest.approx(11.0)


def test_summarize_requires_two_rows():
    close = pd.Series([100.0], index=pd.to_datetime(["2024-01-02"]))
    with pytest.raises(ValueError, match="at least 2"):
        summarize_price_changes(close)
