SHELL := /bin/sh
VENV ?= .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
UVICORN := $(PYTHON) -m uvicorn
PKG := project_hermes
PORT ?= 8001
HOST ?= 127.0.0.1

.DEFAULT_GOAL := help

.PHONY: help venv install sync run dev compose up down lint format type typecheck test test-unit test-integration coverage clean clean-all upgrade freeze deps graph

help:
	@echo "Available targets:";
	@grep -E '^[a-zA-Z_-]+:.*?##' Makefile | awk -F':|##' '{printf "\033[36m%-20s\033[0m %s\n", $$1, $$3}' | sort

venv: ## Create virtual environment
	@test -d $(VENV) || python -m venv $(VENV)
	@echo "[venv] Created $(VENV)"

install: venv ## Install dependencies
	$(PIP) install --upgrade pip
	$(PIP) install -e .[dev]
	@echo "[install] Dependencies installed"

sync: venv ## Sync lock file (uv / pip-tools not configured; placeholder)
	@echo "No sync step defined."

run: ## Run server via helper script
	$(PYTHON) run_server.py

dev: ## Run server in reload mode
	$(UVICORN) $(PKG).api:app --host $(HOST) --port $(PORT) --reload

compose: ## Build and run docker compose (foreground)
	docker compose -f docker-compose.yml up --build

up: ## Start docker compose (detached)
	docker compose up -d

down: ## Stop docker compose
	docker compose down

lint: ## Run Ruff checks
	ruff check .

format: ## Auto-format with Ruff & remove unused imports
	ruff check --select I --fix .
	ruff format . || true

type typecheck: ## Run mypy type checking
	mypy src

test test-unit: ## Run unit tests only (skipping integration)
	RUN_INTEGRATION=0 pytest -q

test-integration: ## Run full test suite incl. integration
	RUN_INTEGRATION=1 pytest -q

coverage: ## Run tests with coverage report
	$(PYTHON) -m pytest --cov=$(PKG) --cov-report=term-missing

clean: ## Remove caches & build artifacts
	rm -rf .pytest_cache **/__pycache__ .mypy_cache
	find . -name '*.pyc' -delete

clean-all: clean ## Also remove virtual environment
	rm -rf $(VENV)

upgrade: venv ## Upgrade all installed packages (cautious)
	$(PIP) list --outdated --format=freeze | cut -d '=' -f1 | xargs -n1 $(PIP) install -U || true

freeze: venv ## Export current environment to requirements-freeze.txt
	$(PIP) freeze > requirements-freeze.txt
	@echo "[freeze] Wrote requirements-freeze.txt"

deps: ## Show top-level dependencies (editable mode)
	$(PIP) list --format=columns | head -n 40

graph: ## Attempt dependency graph (requires pipdeptree)
	$(PIP) install pipdeptree >/dev/null 2>&1 || true
	$(VENV)/bin/pipdeptree | head -n 80


