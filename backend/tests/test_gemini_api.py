"""
Integration test for Gemini API (skipped by default).
Set RUN_INTEGRATION=1 to enable.
"""

import os
import pytest
from dotenv import load_dotenv

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION") != "1",
    reason="Skipping Gemini integration test (set RUN_INTEGRATION=1 to run)",
)


def test_gemini_api_basic():
    import google.generativeai as genai

    # Load environment variables
    load_dotenv()

    # Get API key from environment
    api_key = os.getenv("GEMINI_API_KEY")
    assert api_key, "GEMINI_API_KEY not set"

    # Configure the Gemini API
    genai.configure(api_key=api_key)

    # Try a tiny content generation
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content("ping")
    text = getattr(response, "text", "").strip()
    assert isinstance(text, str)
    assert len(text) >= 0
