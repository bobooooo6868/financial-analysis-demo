"""Streamlit dashboard for the financial analysis project."""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

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
    "GOOGL": "谷歌",
    "AVGO": "博通",
    "SLV": "白银 ETF",
    "NVDA": "英伟达",
}


@st.cache_data(show_spinner="正在加载数据并分析…")
def load_analysis(use_demo: bool) -> dict:
    prices = run_pipeline(demo=use_demo, save=False)
    return run_full_analysis(prices)


def render_figure(plot_fn, results: dict, key: str) -> None:
    """Render a matplotlib figure in Streamlit without writing to disk."""
    plot_fn(results[key], save=False)
    fig = plt.gcf()
    st.pyplot(fig, clear_figure=True)


def main() -> None:
    st.title("四只股票金融数据分析")
    st.caption(
        "标的：GOOGL · AVGO · SLV · NVDA ｜ "
        "[GitHub](https://github.com/bobooooo6868/financial-analysis-demo)"
    )

    with st.sidebar:
        st.header("设置")
        use_demo = st.toggle(
            "使用演示数据（推荐）",
            value=True,
            help="云端部署建议开启，避免 yfinance 限流。",
        )
        if not use_demo:
            st.warning("实时下载依赖 yfinance，可能较慢或失败。")
        if st.button("清除缓存并刷新"):
            st.cache_data.clear()
            st.rerun()

    results = load_analysis(use_demo)
    prices = results["prices"]
    stats = results["stats_loop"]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("交易日数", f"{len(prices)}")
    col2.metric("标的数量", len(TICKERS))
    col3.metric("波动最大", stats["std"].idxmax())
    col4.metric("数据来源", "演示数据" if use_demo else "yfinance")

    tab_overview, tab_stats, tab_tests, tab_charts = st.tabs(
        ["概览", "收益统计", "统计检验", "图表"]
    )

    with tab_overview:
        st.subheader("收盘价宽表（最近 10 行）")
        st.dataframe(prices.tail(10).round(2), use_container_width=True)

        st.subheader("日收益相关矩阵")
        st.dataframe(results["correlation"].round(3), use_container_width=True)

        tech = ["GOOGL", "AVGO", "NVDA"]
        tech_corr = results["correlation"].loc[tech, tech].values
        upper = tech_corr[np.triu_indices(len(tech), k=1)]
        slv_mean = results["correlation"].loc["SLV", tech].mean()
        st.write(
            f"科技股平均相关系数：**{upper.mean():.3f}** ｜ "
            f"SLV 与科技股平均相关系数：**{slv_mean:.3f}**"
        )

    with tab_stats:
        st.subheader("日收益描述统计")
        st.dataframe(stats.round(6), use_container_width=True)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**月均日收益（最近 6 个月）**")
            st.dataframe(results["monthly_groupby"].tail(6).round(6), use_container_width=True)
        with c2:
            st.markdown("**月末复合月收益（最近 6 个月）**")
            st.dataframe(results["monthly_resample"].tail(6).round(6), use_container_width=True)

    with tab_tests:
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("**Jarque-Bera 正态性检验**")
            st.dataframe(results["normality_tests"].round(4), use_container_width=True)
        with c2:
            st.markdown("**ADF — 价格水平**")
            st.dataframe(results["adf_price_tests"].round(4), use_container_width=True)
        with c3:
            st.markdown("**ADF — 日收益**")
            st.dataframe(results["adf_return_tests"].round(4), use_container_width=True)

        reject = int(results["normality_tests"]["reject_normal_5pct"].sum())
        nonstat = int((~results["adf_price_tests"]["stationary_5pct"]).sum())
        stat = int(results["adf_return_tests"]["stationary_5pct"].sum())
        st.info(
            f"正态性拒绝 {reject}/{len(TICKERS)} ｜ "
            f"价格非平稳 {nonstat}/{len(TICKERS)} ｜ "
            f"收益平稳 {stat}/{len(TICKERS)}"
        )

    with tab_charts:
        st.subheader("累计对数收益")
        render_figure(plot_cumulative_returns, results, "cumulative_log_return")

        left, right = st.columns(2)
        with left:
            st.subheader("相关矩阵热图")
            render_figure(plot_correlation_heatmap, results, "correlation")
        with right:
            st.subheader("20 日滚动波动率")
            render_figure(plot_rolling_volatility, results, "rolling_volatility")

        st.subheader("最近 12 个月月均日收益")
        render_figure(plot_monthly_returns_bar, results, "monthly_groupby")

    with st.expander("标的说明"):
        for symbol in TICKERS:
            st.write(f"- **{symbol}**：{TICKER_LABELS[symbol]}")


if __name__ == "__main__":
    main()
