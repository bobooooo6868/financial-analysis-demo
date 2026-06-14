"""Tests for data fetch and demo data."""

from src.config import DEMO_PRICES_PATH, TICKERS
from src.data_fetch import load_demo_prices, run_pipeline


def test_run_pipeline_demo_column_names():
    """run_pipeline(demo=True) returns wide table with expected ticker columns."""
    prices = run_pipeline(demo=True, save=False)
    assert list(prices.columns) == TICKERS


def test_demo_prices_file_exists():
    assert DEMO_PRICES_PATH.exists()


def test_load_demo_prices_columns_and_rows():
    prices = load_demo_prices()
    assert list(prices.columns) == TICKERS
    assert len(prices) >= 200
    assert prices.isna().sum().sum() == 0


def test_run_pipeline_demo_matches_bundled_file():
    pipeline = run_pipeline(demo=True, save=False)
    bundled = load_demo_prices()
    pipeline.index = pipeline.index.normalize()
    bundled.index = bundled.index.normalize()
    assert list(pipeline.columns) == list(bundled.columns)
    assert len(pipeline) == len(bundled)
