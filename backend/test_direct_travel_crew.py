"""
Project Hermes - Direct Travel Crew Test
----------------------------------------

This script tests the TravelCrew class directly without going through the API.
It allows for quick testing of the core functionality with the updated CrewAI implementation.
"""

import json
import os
import sys
from dotenv import load_dotenv

# Load environment variables for API keys
load_dotenv()


def print_section(title):
    """Print a formatted section title."""
    print("\n" + "=" * 60)
    print(f" {title} ".center(60, "-"))
    print("=" * 60)


def test_travel_crew():
    """Test the TravelCrew directly."""

    print_section("TESTING TRAVEL CREW")

    # Import the multi-provider TravelCrew
    try:
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from travel_crew_multi_provider import TravelCrew

        print("Successfully imported TravelCrew from multi-provider implementation")
    except ImportError:
        print("Failed to import multi-provider TravelCrew, falling back to original implementation")
        from travel_crew import TravelCrew

    # Create the TravelCrew instance (will auto-select provider)
    try:
        # Create a TravelCrew instance using the multi-provider implementation
        # This will automatically select the best available provider (Gemini → Claude → OpenAI)
        travel_crew = TravelCrew(verbose=True)
        print(f"Using real CrewAI implementation with provider: {travel_crew.llm_provider_name}")
    except Exception as e:
        print(f"Error creating TravelCrew: {str(e)}")
        print("Falling back to mock implementation...")

        # Define a simple mock class with the same interface
        class MockTravelCrew:
            def __init__(self, verbose=True):
                self.verbose = verbose
                self.llm_provider_name = "mock"

            def plan_trip(self, query):
                print(f"Mock planning trip for query: {query}")
                return {
                    "success": True,
                    "confidence_score": 0.85,
                    "query": query,
                    "llm_provider": "mock",
                    "travel_plan": {
                        "overview": "This is a mock travel plan overview.",
                        "itinerary": "This is a mock itinerary.",
                        "safety": "This is mock safety information.",
                        "finance": "This is mock budget information.",
                    },
                }

        travel_crew = MockTravelCrew(verbose=True)
        return

    # Example travel query
    query = "Plan a weekend trip to Paris for a couple with a budget of $2000"

    print(f"\nQuery: {query}")
    print("\nProcessing request...")

    # Plan the trip
    result = travel_crew.plan_trip(query)

    # Display results
    print_section("RESPONSE SUMMARY")
    print(f"Success: {result.get('success', False)}")
    print(f"Confidence Score: {result.get('confidence_score', 0)}")
    print(f"Provider: {result.get('llm_provider', 'unknown')}")

    if not result.get("success", False):
        print(f"\nError: {result.get('error', 'Unknown error')}")
        return

    travel_plan = result.get("travel_plan", {})
    if not travel_plan:
        print("\nNo travel plan details available.")
        return

    print_section("TRAVEL PLAN")

    # Print the plan components
    for key, value in travel_plan.items():
        print(f"\n{key.upper()}:")
        print(value)

    # Print the full JSON response for reference
    print_section("FULL JSON RESPONSE")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    test_travel_crew()
