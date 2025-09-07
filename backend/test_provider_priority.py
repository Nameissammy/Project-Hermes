#!/usr/bin/env python3
"""
Test the new provider priority order (Gemini -> Claude -> OpenAI)
"""

import os
import sys
from dotenv import load_dotenv

# Add the backend directory to the Python path
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

# Load environment variables
load_dotenv()

# Import the new multi-provider TravelCrew
try:
    from travel_crew_multi_provider import TravelCrew

    print("Successfully imported multi-provider TravelCrew")
except ImportError as e:
    print(f"Error importing multi-provider TravelCrew: {e}")
    sys.exit(1)


def test_auto_detection():
    """Test the auto-detection of providers."""
    print("\n--- Testing Provider Auto-Detection ---")

    # Check available API keys
    has_gemini = bool(os.getenv("GEMINI_API_KEY"))
    has_claude = bool(os.getenv("CLAUDE_API_KEY"))
    has_openai = bool(os.getenv("OPENAI_API_KEY"))

    print("Available API Keys:")
    print(f"- Gemini (primary):   {'YES' if has_gemini else 'NO'}")
    print(f"- Claude (secondary): {'YES' if has_claude else 'NO'}")
    print(f"- OpenAI (tertiary):  {'YES' if has_openai else 'NO'}")

    try:
        # Auto-detect the provider
        crew = TravelCrew()

        # Get information about the selected provider
        provider_name = crew.llm_provider_name
        llm_type = type(crew.llm).__name__

        print(f"\n✅ Auto-detected provider: {provider_name}")
        print(f"   LLM Type: {llm_type}")

        # Verify the expected priority order
        if has_gemini:
            assert provider_name == "gemini", "Gemini should be used first if available"
            print("✅ Priority 1 (Gemini) correctly selected")
        elif has_claude:
            assert provider_name == "claude", "Claude should be used second if available"
            print("✅ Priority 2 (Claude) correctly selected")
        elif has_openai:
            assert provider_name == "openai", "OpenAI should be used third if available"
            print("✅ Priority 3 (OpenAI) correctly selected")
        else:
            print("❌ No API keys available, auto-detection should have failed")

    except Exception as e:
        if not (has_gemini or has_claude or has_openai):
            print(f"✅ Expected failure with no API keys: {e}")
        else:
            print(f"❌ Auto-detection failed unexpectedly: {e}")


def test_explicit_selection():
    """Test explicit provider selection."""
    print("\n--- Testing Explicit Provider Selection ---")

    # Test each provider explicitly if the API key is available
    has_gemini = bool(os.getenv("GEMINI_API_KEY"))
    has_claude = bool(os.getenv("CLAUDE_API_KEY"))
    has_openai = bool(os.getenv("OPENAI_API_KEY"))

    if has_gemini:
        try:
            crew = TravelCrew(llm_provider="gemini")
            print(f"✅ Explicitly selected Gemini: {type(crew.llm).__name__}")
        except Exception as e:
            print(f"❌ Failed to explicitly select Gemini: {e}")
    else:
        print("⚠️ Skipping Gemini test (no API key)")

    if has_claude:
        try:
            crew = TravelCrew(llm_provider="claude")
            print(f"✅ Explicitly selected Claude: {type(crew.llm).__name__}")
        except Exception as e:
            print(f"❌ Failed to explicitly select Claude: {e}")
    else:
        print("⚠️ Skipping Claude test (no API key)")

    if has_openai:
        try:
            crew = TravelCrew(llm_provider="openai")
            print(f"✅ Explicitly selected OpenAI: {type(crew.llm).__name__}")
        except Exception as e:
            print(f"❌ Failed to explicitly select OpenAI: {e}")
    else:
        print("⚠️ Skipping OpenAI test (no API key)")


def main():
    """Run all tests."""
    print("Testing Multi-Provider Priority Order")
    print("======================================")
    print("Priority: 1. Gemini → 2. Claude → 3. OpenAI")

    test_auto_detection()
    test_explicit_selection()

    print("\nTests completed!")


if __name__ == "__main__":
    main()
