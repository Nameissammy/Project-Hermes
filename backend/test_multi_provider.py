"""
Test Multi-Provider LLM Configuration

This script demonstrates how Project Hermes can use different LLM providers
(OpenAI, Gemini, Claude) based on available API keys.
"""

import os
from dotenv import load_dotenv
import sys

# Add the backend directory to the Python path
sys.path.append("/Users/shubhranshumohanty/Developer/Project-Hermes/backend")

# Load environment variables
load_dotenv()

# Check what API keys are available
openai_key = os.getenv("OPENAI_API_KEY")
gemini_key = os.getenv("GEMINI_API_KEY")
claude_key = os.getenv("CLAUDE_API_KEY")

print("API Key Status:")
print(f"- OpenAI API Key: {'Available' if openai_key else 'Not available'}")
print(f"- Gemini API Key: {'Available' if gemini_key else 'Not available'}")
print(f"- Claude API Key: {'Available' if claude_key else 'Not available'}")

# Import the TravelCrew class
try:
    from travel_crew import TravelCrew

    print("\nTravelCrew module imported successfully!")
except ImportError as e:
    print(f"\nError importing TravelCrew: {e}")
    sys.exit(1)


def test_provider(provider_name):
    """Test a specific LLM provider."""
    print(f"\n--- Testing {provider_name.upper()} Provider ---")

    try:
        # Try to create a TravelCrew instance with the specified provider
        crew = TravelCrew(llm_provider=provider_name)
        print(f"✅ Successfully initialized TravelCrew with {provider_name}")

        # Print details about the LLM being used
        llm_type = type(crew.llm).__name__
        print(f"LLM Type: {llm_type}")

        if hasattr(crew.llm, "model_name"):
            print(f"Model Name: {crew.llm.model_name}")
        elif hasattr(crew.llm, "model"):
            print(f"Model Name: {crew.llm.model}")

        return True
    except Exception as e:
        print(f"❌ Failed to initialize with {provider_name}: {e}")
        return False


# Try auto-detection first
print("\n--- Testing AUTO Provider Detection ---")
try:
    crew = TravelCrew()  # No provider specified, should auto-detect
    llm_type = type(crew.llm).__name__
    print(f"✅ Auto-detected and using: {llm_type}")
except Exception as e:
    print(f"❌ Auto-detection failed: {e}")

# Test each provider explicitly
if openai_key:
    test_provider("openai")
else:
    print("\n--- Skipping OpenAI test (no API key) ---")

if gemini_key:
    test_provider("gemini")
else:
    print("\n--- Skipping Gemini test (no API key) ---")

if claude_key:
    test_provider("claude")
else:
    print("\n--- Skipping Claude test (no API key) ---")

print("\nMulti-provider testing completed!")
