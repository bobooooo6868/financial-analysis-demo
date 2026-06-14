# Financial Analysis Demo

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![CI](https://github.com/bobooooo6868/financial-analysis-demo/actions/workflows/ci.yml/badge.svg)](https://github.com/bobooooo6868/financial-analysis-demo/actions/workflows/ci.yml)
[![Live Demo](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://financial-analysis-demo.streamlit.app)

**Problem:** Retail and tech investors need a fast way to compare risk, correlation, and return patterns across multiple tickers—without manual spreadsheets or fragmented Yahoo Finance exports.

**Solution:** A modular Python pipeline that pulls live prices via `yfinance`, cleans and merges multi-ticker data, runs vectorized analytics (returns, rolling volatility, correlation, normality & ADF tests), and ships results through CLI, Jupyter, pytest, CI, and a Streamlit dashboard.

**Result:** A reproducible end-to-end stock analytics project with automated tests, one-click charts, an interactive live demo, and a portfolio-ready GitHub repo—demonstrating data engineering, statistics, and deployment in one place.

| | |
|---|---|
| **Live Demo** | [Streamlit App](https://financial-analysis-demo.streamlit.app) · [Report (Notebook)](https://nbviewer.org/github/bobooooo6868/financial-analysis-demo/blob/master/notebooks/main.ipynb) |
| **Repository** | [github.com/bobooooo6868/financial-analysis-demo](https://github.com/bobooooo6868/financial-analysis-demo) |

> If your Streamlit URL differs, update the badge link above from **Manage app** on [share.streamlit.io](https://share.streamlit.io/).

## Tech Stack

| Layer | Tools |
|-------|--------|
| Data | [yfinance](https://github.com/ranaroussi/yfinance), Pandas, NumPy |
| Analytics | SciPy (Jarque–Bera), statsmodels (ADF), vectorized NumPy stats |
| Visualization | Matplotlib, Seaborn, **Plotly** |
| App & Report | Streamlit, Jupyter |
| Quality | pytest, GitHub Actions |

**Tickers:** GOOGL · AVGO · SLV (silver ETF) · NVDA — ~2 years of daily closes.

## Highlights

- **Live fetch:** `fetch_data.py` pulls a single ticker and prints daily & period returns.
- **Batch pipeline:** `main.py` / `src/data_fetch.py` build a merged wide price table for four symbols.
- **Statistics:** correlation matrix, rolling vol, monthly resample, normality & stationarity tests.
- **Offline fallback:** bundled demo CSV + `--demo` flag when Yahoo rate-limits.
- **CI:** every push runs `pytest` and `python main.py --demo`.
- **Fiverr cover asset:** AAPL Plotly line chart exported from [`01_stock_overview.ipynb`](notebooks/01_stock_overview.ipynb) → `images/aapl_plotly_cover.png`.

## Fiverr Gig Cover (AAPL · Plotly)

Single-stock Apple close-price line chart (1Y), exported as PNG for marketplace thumbnails.

![AAPL Plotly cover — Fiverr gig asset](images/aapl_plotly_cover.png)

## Screenshots

### Cumulative log returns

![Cumulative log returns](images/cumulative_log_returns.png)

### Return correlation

![Correlation heatmap](images/correlation_heatmap.png)

### 20-day rolling volatility

![Rolling volatility](images/rolling_volatility.png)

### Monthly mean daily returns (last 12 months)

![Monthly returns](images/monthly_returns_bar.png)

## Quick Start (2 commands)

**Fastest path after clone** — offline demo, no yfinance required:

```bash
git clone https://github.com/bobooooo6868/financial-analysis-demo.git
cd financial-analysis-demo
```

**Windows (PowerShell)**

```powershell
.\setup.ps1 -RunDemo
```

**macOS / Linux**

```bash
chmod +x setup.sh
./setup.sh --demo
```

Or with Make: `make demo` (creates `.venv`, installs deps, runs `main.py --demo`).

### Manual setup

```bash
python3 -m venv .venv && source .venv/bin/activate   # Windows: py -3.13 -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py --demo
```

**Dependencies:** `requirements.txt` pins core runtime (Streamlit Cloud–friendly). For notebooks/tests/plotly export, also install `requirements-dev.txt`. Python **3.13** (`.python-version`).

| Command | Purpose |
|---------|---------|
| `python fetch_data.py GOOGL` | Live single-ticker quote + % change |
| `python main.py` | Full pipeline (live data) + charts |
| `python main.py --demo` | Offline demo data (CI / rate limits) |
| `streamlit run app.py` | Interactive dashboard |
| `pytest tests/` | Run unit tests |

## Project Layout

```
financial-analysis-demo/
├── setup.ps1 / setup.sh   # One-command environment setup
├── Makefile               # make setup | demo | test
├── requirements.txt       # Pinned direct dependencies
├── requirements-lock.txt  # Optional full pip freeze lock
├── app.py                 # Streamlit dashboard
├── fetch_data.py          # Single-ticker live fetch + returns
├── main.py                # CLI pipeline
├── src/                   # data_fetch, analysis, plotting, utils
├── notebooks/main.ipynb   # Full report (pre-executed)
├── tests/                 # pytest
└── images/                # Exported charts
```

## Report & Notebooks

| File | Role |
|------|------|
| [`notebooks/main.ipynb`](notebooks/main.ipynb) | **Main report** — analysis, tests, conclusions |
| [`notebooks/01_stock_overview.ipynb`](notebooks/01_stock_overview.ipynb) | AAPL intro + **Plotly cover PNG** export |

View online: [GitHub](https://github.com/bobooooo6868/financial-analysis-demo/blob/master/notebooks/main.ipynb) · [nbviewer](https://nbviewer.org/github/bobooooo6868/financial-analysis-demo/blob/master/notebooks/main.ipynb)

## Data Notes

- Market data via yfinance (delayed; for education/research only).
- Default paths use **live** data (`main.ipynb`, Streamlit); use `--demo` or the Streamlit toggle when offline or rate-limited.

## License

[MIT License](LICENSE)
