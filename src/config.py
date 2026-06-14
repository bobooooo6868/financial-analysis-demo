"""Project constants for the stock analysis assignment."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
DEMO_PRICES_PATH = PROCESSED_DIR / "prices_wide_demo.csv"
IMAGES_DIR = PROJECT_ROOT / "images"

TICKERS = ["GOOGL", "AVGO", "SLV", "NVDA"]
PERIOD = "2y"
ROLLING_SHORT = 20
ROLLING_LONG = 60
