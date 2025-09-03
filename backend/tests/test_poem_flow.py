import sys
from pathlib import Path

from fastapi.testclient import TestClient  # type: ignore

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:  # pragma: no cover (environmental)
    sys.path.insert(0, str(SRC))

from project_hermes.api import app  # noqa: E402
from project_hermes.main import kickoff  # noqa: E402


def test_kickoff_fake_output(monkeypatch):
    monkeypatch.setenv("POEM_FAKE_OUTPUT", "FAKE POEM")
    poem = kickoff("test topic")
    assert poem == "FAKE POEM"


def test_health():
    client = TestClient(app)
    r = client.get("/healthz")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ok"


def test_poem_endpoint(monkeypatch):
    monkeypatch.setenv("POEM_FAKE_OUTPUT", "API POEM")
    client = TestClient(app)
    r = client.get("/poem/demo")
    assert r.status_code == 200
    data = r.json()
    assert data["poem"] == "API POEM"
    assert data["topic"] == "demo"
    assert data["success"] is True
    # attempts may be zero if we short-circuit with fake output
    assert data["attempts"] >= 0


def test_poem_endpoint_forced_error(monkeypatch):
    # Force simulated error and ensure structured failure response
    monkeypatch.delenv("POEM_FAKE_OUTPUT", raising=False)
    monkeypatch.setenv("POEM_FORCE_ERROR", "1")
    client = TestClient(app)
    r = client.get("/poem/broken")
    assert r.status_code == 200  # still 200 unless POEM_STRICT=1
    data = r.json()
    assert data["success"] is False
    assert data["error"]
    assert data["poem"] == "<error generating poem>"