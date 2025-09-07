"""
Simple Test of Provider Selection in TravelCrew
"""

import os
import sys
from dotenv import load_dotenv

# Add the backend directory to the Python path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(backend_dir)

# Load environment variables
load_dotenv()

# Import the TravelCrew class
from travel_crew import TravelCrew


def test_provider(provider_name=None):
    """Test the TravelCrew with a specific provider."""
    print(f"\n--- Testing TravelCrew with {provider_name or 'auto-detected'} provider ---")

    # Create a TravelCrew instance with the specified provider
    crew = TravelCrew(llm_provider=provider_name)

    # Get the LLM type
    llm_type = type(crew.llm).__name__
    print(f"Using LLM: {llm_type}")

    # Basic functionality test
    print("\nTesting plan trip method:")
    query = "What's the capital of France?"
    try:
        result = crew.plan_trip(query)
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error: {e}")

    return crew


# Test with different providers
print("Available API Keys:")
print(f"- OpenAI: {'Yes' if os.getenv('OPENAI_API_KEY') else 'No'}")
print(f"- Gemini: {'Yes' if os.getenv('GEMINI_API_KEY') else 'No'}")
print(f"- Claude: {'Yes' if os.getenv('CLAUDE_API_KEY') else 'No'}")

# Auto-detect
auto_crew = test_provider()

# Test each provider explicitly
openai_crew = test_provider("openai")
gemini_crew = test_provider("gemini")
claude_crew = test_provider("claude")

print("\nAll provider tests completed!")
