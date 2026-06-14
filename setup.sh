#!/usr/bin/env bash
# One-command setup for macOS / Linux
# Usage: ./setup.sh [--demo]

set -euo pipefail
cd "$(dirname "$0")"

RUN_DEMO=0
if [[ "${1:-}" == "--demo" ]]; then
  RUN_DEMO=1
fi

echo "==> Creating virtual environment (.venv) ..."
python3 -m venv .venv

echo "==> Installing dependencies ..."
.venv/bin/python -m pip install -U pip
.venv/bin/pip install -r requirements.txt
if [[ -f requirements-dev.txt ]]; then
  .venv/bin/pip install -r requirements-dev.txt
fi

echo ""
echo "Setup complete."
echo "  Activate:  source .venv/bin/activate"
echo "  Demo run:  .venv/bin/python main.py --demo"
echo "  Tests:     .venv/bin/pytest tests/"

if [[ "$RUN_DEMO" -eq 1 ]]; then
  echo ""
  echo "==> Running demo pipeline ..."
  .venv/bin/python main.py --demo
fi
