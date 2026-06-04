"""Synthetic OHLCV for offline runs when yfinance is rate-limited."""

from __future__ import annotations

import numpy as np
import pandas as pd

from src.config import TICKERS

# Roughly match recent price scales and vol characteristics
_PROFILE = {
    "GOOGL": {"start": 140.0, "vol": 0.018, "drift": 0.00035},
    "AVGO": {"start": 1200.0, "vol": 0.025, "drift": 0.00045},
    "SLV": {"start": 22.0, "vol": 0.022, "drift": 0.00015},
    "NVDA": {"start": 450.0, "vol": 0.035, "drift": 0.00055},
}


def generate_synthetic_ohlcv(
    tickers: list[str] | None = None,
    years: int = 2,
    seed: int = 42,
) -> dict[str, pd.DataFrame]:
    """
    Generate business-day OHLCV panels via geometric Brownian motion.
    Used only when live download fails; re-run without --demo for real data.
    """
    tickers = tickers or TICKERS
    rng = np.random.default_rng(seed)
    n_days = 252 * years
    days = pd.bdate_range(end=pd.Timestamp.today().normalize(), periods=n_days)

    frames: dict[str, pd.DataFrame] = {}
    for symbol in tickers:
        profile = _PROFILE[symbol]
        shocks = rng.normal(profile["drift"], profile["vol"], n_days)
        close = profile["start"] * np.cumprod(1 + shocks)
        noise = rng.normal(0, 0.003, n_days)
        open_ = close * (1 + noise)
        high = np.maximum(open_, close) * (1 + np.abs(rng.normal(0, 0.004, n_days)))
        low = np.minimum(open_, close) * (1 - np.abs(rng.normal(0, 0.004, n_days)))
        volume = rng.integers(1_000_000, 50_000_000, n_days)

        frames[symbol] = pd.DataFrame(
            {"Open": open_, "High": high, "Low": low, "Close": close, "Volume": volume},
            index=days,
        )
    return frames
