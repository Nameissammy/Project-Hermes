#!/usr/bin/env python3
"""
Project Hermes Demo
------------------

This script demonstrates the travel planning capabilities of Project Hermes.
It creates a TravelCrew instance and generates a travel plan for a sample query.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def run_demo():
    """Run a simple travel planning demo."""
    try:
        # Import TravelCrew here to avoid import errors
        from travel_crew import TravelCrew

        # Determine which provider to use based on environment variables
        provider = None  # Auto-detect
        if len(sys.argv) > 1:
            provider = sys.argv[1]
            print(f"Using specified provider: {provider}")

        # Print information about available API keys
        if os.getenv("OPENAI_API_KEY"):
            print("✓ OpenAI API key found")
        else:
            print("✗ OpenAI API key not found")

        if os.getenv("GEMINI_API_KEY"):
            print("✓ Gemini API key found")
        else:
            print("✗ Gemini API key not found")

        if os.getenv("CLAUDE_API_KEY"):
            print("✓ Claude API key found")
        else:
            print("✗ Claude API key not found")

        # Try to determine the provider from API keys
        model_name = "gpt-4-turbo"  # Default
        if provider == "gemini" or (
            provider is None and not os.getenv("OPENAI_API_KEY") and os.getenv("GEMINI_API_KEY")
        ):
            model_name = "gemini-pro"
            print("Using Gemini Pro model")
        elif provider == "claude" or (
            provider is None
            and not os.getenv("OPENAI_API_KEY")
            and not os.getenv("GEMINI_API_KEY")
            and os.getenv("CLAUDE_API_KEY")
        ):
            model_name = "claude-3-opus-20240229"
            print("Using Claude model")
        else:
            print("Using GPT-4 Turbo model")

        print("\nInitializing TravelCrew...")
        # Initialize the travel crew with the determined model
        travel_crew = TravelCrew(model_name=model_name)

        # Sample travel query
        query = "Plan a 3-day weekend trip to San Francisco for a couple interested in food and culture with a budget of $1500"

        print(f'\nGenerating travel plan for query: "{query}"\n')
        print("This may take a minute or two...\n")

        # Generate the travel plan
        result = travel_crew.create_travel_plan(query)

        # Print the result
        print("\n" + "=" * 80)
        print(f"SUCCESS: Travel plan generated using {model_name}")
        print(f"Confidence Score: {result.confidence_score:.2f}")
        print("=" * 80 + "\n")

        # Print travel plan sections
        print("OVERVIEW:")
        print("-" * 80)
        print(result.travel_plan.overview)
        print("\nITINERARY:")
        print("-" * 80)
        print(result.travel_plan.itinerary)
        print("\nSAFETY INFORMATION:")
        print("-" * 80)
        print(result.travel_plan.safety)
        print("\nBUDGET BREAKDOWN:")
        print("-" * 80)
        print(result.travel_plan.finance)

        return 0
    except ImportError as e:
        print(f"Error: {e}")
        print("\nMake sure you're running this script from the backend directory.")
        print("Try: cd backend && python demo.py")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        print("\nTry running with a specific provider:")
        print("python demo.py gemini")
        print("python demo.py claude")
        print("python demo.py openai")
        return 1


if __name__ == "__main__":
    sys.exit(run_demo())
