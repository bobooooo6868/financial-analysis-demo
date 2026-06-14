.PHONY: setup demo test streamlit lock

PYTHON ?= python3
VENV := .venv
BIN := $(VENV)/bin
PY := $(BIN)/python
PIP := $(BIN)/pip

setup:
	$(PYTHON) -m venv $(VENV)
	$(PY) -m pip install -U pip
	$(PIP) install -r requirements.txt
	$(PIP) install -r requirements-dev.txt
	@echo "Run: make demo"

demo: setup
	$(PY) main.py --demo

test: setup
	$(PY) -m pytest tests/

streamlit: setup
	$(BIN)/streamlit run app.py

lock:
	$(PIP) freeze > requirements-lock.txt
