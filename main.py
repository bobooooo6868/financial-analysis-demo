"""Run full assignment pipeline: fetch data, analyze, save charts."""

import argparse

from src.analysis import run_full_analysis
from src.data_fetch import run_pipeline
from src.plotting import generate_all_figures


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Use synthetic data (when yfinance is rate-limited)",
    )
    args = parser.parse_args()

    print("Downloading and cleaning data...")
    prices = run_pipeline(demo=args.demo)
    print(f"Prices shape: {prices.shape}")

    print("Running analysis...")
    results = run_full_analysis(prices)

    print("Generating figures...")
    paths = generate_all_figures(results)
    for p in paths:
        print(f"  Saved {p}")

    print("\n--- Summary statistics (daily returns) ---")
    print(results["stats_loop"].round(6))
    print("\n--- Correlation matrix ---")
    print(results["correlation"].round(3))

    print("\n--- Normality tests (Jarque-Bera) ---")
    print(results["normality_tests"].round(4))

    print("\n--- ADF stationarity (prices) ---")
    print(results["adf_price_tests"].round(4))

    print("\n--- ADF stationarity (returns) ---")
    print(results["adf_return_tests"].round(4))


if __name__ == "__main__":
    main()
