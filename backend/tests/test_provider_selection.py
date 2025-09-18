"""Provider selection smoke tests for TravelCrew."""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

try:
    # Try direct import first (when package is installed/editable)
    from project_hermes.crews.travel_crew_multi_provider import TravelCrew
except ModuleNotFoundError:
    # Fallback for running tests from repo layout (ensure src on sys.path)
    ROOT = Path(__file__).resolve().parent.parent
    SRC = ROOT / "src"
    if str(SRC) not in sys.path:
        sys.path.insert(0, str(SRC))
    from project_hermes.crews.travel_crew_multi_provider import TravelCrew

# Load environment variables
load_dotenv()


def test_auto_detect_initializes_any_available_provider():
    try:
        crew = TravelCrew()
    except Exception as e:
        # If no keys at all, initialization should fail; assert that case clearly
        has_any = any(
            [
                os.getenv("GEMINI_API_KEY"),
                os.getenv("GOOGLE_API_KEY"),
                os.getenv("CLAUDE_API_KEY"),
                os.getenv("ANTHROPIC_API_KEY"),
                os.getenv("OPENAI_API_KEY"),
            ]
        )
        assert not has_any, f"Unexpected failure with keys present: {e}"
        return
    assert crew.llm is not None
    provider = None
    for name in ("llm_provider_name", "provider_name", "llm_provider"):
        if hasattr(crew, name):
            provider = getattr(crew, name)
            break
    assert provider in {"gemini", "claude", "openai"}


def test_explicit_provider_init_skips_when_key_missing(monkeypatch):
    # Force missing keys for openai and expect a failure
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    try:
        TravelCrew(llm_provider="openai")
        raise AssertionError("Expected failure initializing openai without OPENAI_API_KEY")
    except (RuntimeError, ValueError):
        # acceptable failure types
        pass
