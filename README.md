# Financial Analysis

Personal repository for financial data analysis with Python and Jupyter Notebook.

## Setup

```powershell
cd C:\Users\ltz\Projects\financial-analysis
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m ipykernel install --user --name financial-analysis --display-name "Python (financial-analysis)"
```

## Usage

Open this folder in VS Code, select the `.venv` interpreter, then open notebooks under `notebooks/`.

```powershell
jupyter lab
```

## Project Structure

```
financial-analysis/
├── notebooks/          # Jupyter notebooks
├── data/               # Local data (raw files gitignored)
├── src/                # Reusable Python modules
├── requirements.txt
└── README.md
```

## Stack

- Python 3.13
- Jupyter / ipykernel
- pandas, numpy, scipy, statsmodels
- matplotlib, seaborn
- yfinance (market data)
- openpyxl (Excel)
