"""Streamlit dashboard for the financial analysis project."""

from __future__ import annotations

import io
import os
from collections.abc import Callable
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from matplotlib.figure import Figure

from src.analysis import run_full_analysis
from src.config import TICKERS
from src.data_fetch import run_pipeline
from src.plotting import (
    plot_correlation_heatmap,
    plot_cumulative_returns,
    plot_monthly_returns_bar,
    plot_rolling_volatility,
)

st.set_page_config(
    page_title="Financial Analysis Demo",
    page_icon="📈",
    layout="wide",
)

TICKER_LABELS = {
    "GOOGL": "Google",
    "AVGO": "Broadcom",
    "SLV": "Silver ETF",
    "NVDA": "NVIDIA",
}


def _on_streamlit_cloud() -> bool:
    """Detect Streamlit Community Cloud (prefer bundled demo data)."""
    env = os.environ.get("STREAMLIT_RUNTIME_ENVIRONMENT", "").lower()
    return env in {"cloud", "streamlit-cloud", "community-cloud"} or bool(
        os.environ.get("STREAMLIT_SHARING")
    )


@st.cache_data(show_spinner="Loading prices…", ttl=3600)
def load_prices(use_demo: bool):
    return run_pipeline(demo=use_demo, save=False)


def load_analysis(use_demo: bool) -> dict:
    try:
        prices = load_prices(use_demo)
    except Exception as exc:
        if use_demo:
            raise
        st.warning(f"Live yfinance fetch failed: {exc}. Using demo data.")
        prices = load_prices(True)
    return run_full_analysis(prices)


def render_figure(plot_fn: Callable[..., Path | Figure], data: Any) -> None:
    """Render matplotlib output via PNG bytes (reliable on Streamlit Cloud)."""
    fig = plot_fn(data, save=False)
    if not isinstance(fig, Figure):
        st.warning("Chart could not be rendered.")
        return
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=120, bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    st.image(buf, use_container_width=True)


def main() -> None:
    st.title("Stock Financial Analysis Dashboard")
    st.caption(
        "GOOGL · AVGO · SLV · NVDA ｜ "
        "[GitHub](https://github.com/bobooooo6868/financial-analysis-demo)"
    )

    default_demo = _on_streamlit_cloud()

    with st.sidebar:
        st.header("Settings")
        use_demo = st.toggle(
            "Use demo data",
            value=default_demo,
            help="Recommended on Streamlit Cloud. Turn off for live yfinance quotes.",
        )
        if not use_demo:
            st.warning("Live mode needs yfinance and may be slow or rate-limited.")
        if st.button("Clear cache & refresh"):
            st.cache_data.clear()
            st.rerun()

    try:
        results = load_analysis(use_demo)
    except Exception as exc:
        st.error(f"Failed to load analysis: {exc}")
        st.info("Try enabling **Use demo data** in the sidebar, then refresh.")
        st.stop()

    prices = results["prices"]
    stats = results["stats_loop"]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Trading days", f"{len(prices)}")
    col2.metric("Tickers", len(TICKERS))
    col3.metric("Highest volatility", stats["std"].idxmax())
    col4.metric("Data source", "Demo" if use_demo else "yfinance")

    tab_overview, tab_stats, tab_tests, tab_charts = st.tabs(
        ["Overview", "Returns", "Tests", "Charts"]
    )

    with tab_overview:
        st.subheader("Close prices (last 10 rows)")
        st.dataframe(prices.tail(10).round(2), use_container_width=True)

        st.subheader("Daily return correlation")
        st.dataframe(results["correlation"].round(3), use_container_width=True)

        tech = ["GOOGL", "AVGO", "NVDA"]
        tech_corr = results["correlation"].loc[tech, tech].values
        upper = tech_corr[np.triu_indices(len(tech), k=1)]
        slv_mean = results["correlation"].loc["SLV", tech].mean()
        st.write(
            f"Tech avg correlation: **{upper.mean():.3f}** ｜ "
            f"SLV vs tech avg: **{slv_mean:.3f}**"
        )

    with tab_stats:
        st.subheader("Daily return statistics")
        st.dataframe(stats.round(6), use_container_width=True)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Monthly mean daily returns (last 6)**")
            st.dataframe(results["monthly_groupby"].tail(6).round(6), use_container_width=True)
        with c2:
            st.markdown("**Month-end compounded returns (last 6)**")
            st.dataframe(results["monthly_resample"].tail(6).round(6), use_container_width=True)

    with tab_tests:
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("**Jarque–Bera normality**")
            st.dataframe(results["normality_tests"].round(4), use_container_width=True)
        with c2:
            st.markdown("**ADF — price level**")
            st.dataframe(results["adf_price_tests"].round(4), use_container_width=True)
        with c3:
            st.markdown("**ADF — daily returns**")
            st.dataframe(results["adf_return_tests"].round(4), use_container_width=True)

        reject = int(results["normality_tests"]["reject_normal_5pct"].sum())
        nonstat = int((~results["adf_price_tests"]["stationary_5pct"]).sum())
        stat = int(results["adf_return_tests"]["stationary_5pct"].sum())
        st.info(
            f"Reject normality {reject}/{len(TICKERS)} ｜ "
            f"Non-stationary prices {nonstat}/{len(TICKERS)} ｜ "
            f"Stationary returns {stat}/{len(TICKERS)}"
        )

    with tab_charts:
        st.subheader("Cumulative log returns")
        render_figure(plot_cumulative_returns, results["cumulative_log_return"])

        left, right = st.columns(2)
        with left:
            st.subheader("Correlation heatmap")
            render_figure(plot_correlation_heatmap, results["correlation"])
        with right:
            st.subheader("20-day rolling volatility")
            render_figure(plot_rolling_volatility, results["rolling_volatility"])

        st.subheader("Monthly mean daily returns (last 12 months)")
        render_figure(plot_monthly_returns_bar, results["monthly_groupby"])

    with st.expander("Ticker glossary"):
        for symbol in TICKERS:
            st.write(f"- **{symbol}**: {TICKER_LABELS[symbol]}")


main()
