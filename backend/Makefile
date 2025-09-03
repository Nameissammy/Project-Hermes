SHELL := /bin/sh

.PHONY: run dev compose up down lint type test

run:
	python run_server.py

dev:
	uvicorn project_hermes.api:app --host 0.0.0.0 --port 8001 --reload

compose:
	docker compose -f docker-compose.yml up --build

up:
	docker compose up -d

down:
	docker compose down

lint:
	ruff check .

type:
	mypy src

test:
	pytest -q


