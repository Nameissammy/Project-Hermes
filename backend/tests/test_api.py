from __future__ import annotations

import sys
from pathlib import Path
from typing import Any
from unittest.mock import patch

from fastapi.testclient import TestClient

# Ensure package src is importable
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from project_hermes.api import app  # noqa: E402


def _mock_kickoff_success(self, *args: Any, **kwargs: Any) -> str:
    # Set outputs on the crew tasks to simulate a full successful run
    # 0: confidence, 1: overview, 2: itinerary, 3: safety, 4: finance
    if getattr(self, "tasks", None):
        self.tasks[0].output = '{"confidence_score": 0.9, "query": "ok"}'
        self.tasks[1].output = "Overview text"
        self.tasks[2].output = "Itinerary text"
        self.tasks[3].output = "Safety text"
        self.tasks[4].output = "Finance text"
    return "OK"


def test_healthz():
    client = TestClient(app)
    r = client.get("/healthz")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ok"


def test_travel_plan_post_mocked():
    client = TestClient(app)
    payload = {
        "query": "Plan a weekend trip to Paris",
        "llm_provider": "gemini",
    }
    with patch("crewai.Crew.kickoff", _mock_kickoff_success):
        r = client.post("/travel/plan", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["success"] is True
    assert data["confidence_score"] >= 0.6
    assert data["travel_plan"]["overview"] == "Overview text"
    assert data["llm_provider"] in {None, "gemini", "claude", "openai"}
