"""
Very Simple Provider Test
"""

import os
from dotenv import load_dotenv
import sys

# Add the backend directory to the Python path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(backend_dir)

# Load environment variables
load_dotenv()

# Import the TravelCrew class
from travel_crew import TravelCrew

# Print available API keys
print("Available API Keys:")
print(f"- OpenAI: {'Yes' if os.getenv('OPENAI_API_KEY') else 'No'}")
print(f"- Gemini: {'Yes' if os.getenv('GEMINI_API_KEY') else 'No'}")
print(f"- Claude: {'Yes' if os.getenv('CLAUDE_API_KEY') else 'No'}")

# Test with auto-detection
print("\n--- Testing with Auto-Detection ---")
auto_crew = TravelCrew()
print(f"Auto-detected LLM type: {type(auto_crew.llm).__name__}")

# Test with explicit providers
print("\n--- Testing with OpenAI ---")
try:
    openai_crew = TravelCrew(llm_provider="openai")
    print(f"OpenAI LLM type: {type(openai_crew.llm).__name__}")
except Exception as e:
    print(f"OpenAI error: {e}")

print("\n--- Testing with Gemini ---")
try:
    gemini_crew = TravelCrew(llm_provider="gemini")
    print(f"Gemini LLM type: {type(gemini_crew.llm).__name__}")
except Exception as e:
    print(f"Gemini error: {e}")

print("\n--- Testing with Claude ---")
try:
    claude_crew = TravelCrew(llm_provider="claude")
    print(f"Claude LLM type: {type(claude_crew.llm).__name__}")
except Exception as e:
    print(f"Claude error: {e}")

print("\nAll provider tests completed!")
