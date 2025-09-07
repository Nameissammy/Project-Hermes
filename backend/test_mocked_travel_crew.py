"""
Project Hermes - Travel Crew Test with Mocked Response
"""

import os
import json
from unittest.mock import patch
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up a mock API key if needed
if not os.getenv("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = "mock-api-key"


def print_section(title):
    """Print a formatted section title."""
    print("\n" + "=" * 60)
    print(f" {title} ".center(60, "-"))
    print("=" * 60)


def test_travel_crew_with_mock():
    print_section("TESTING TRAVEL CREW WITH MOCKED RESPONSE")

    # Add the backend/src directory to the Python path
    import sys

    project_root = os.path.dirname(os.path.abspath(__file__))
    backend_src = os.path.join(project_root, "backend", "src")
    sys.path.append(backend_src)

    # Import the necessary modules
    from project_hermes.crews.travel_crew.travel_crew import TravelCrew

    # The response to return when crew.kickoff() is called
    mock_response = json.dumps({"score": 0.85, "prompt": "Plan a trip to Paris"})

    # Use a context manager to patch the Crew.kickoff method
    with patch("crewai.Crew.kickoff", return_value=mock_response):
        # Create a TravelCrew instance
        travel_crew = TravelCrew(verbose=True)

        # Call the plan_trip method
        result = travel_crew.plan_trip("Plan a trip to Paris")

        # Print the result
        print("\nRESULT:")
        print(json.dumps(result, indent=2))

        # Verify the result structure
        print("\nVERIFICATION:")
        print(f"Success: {result.get('success', False)}")
        print(f"Confidence Score: {result.get('confidence_score', 0)}")
        if result.get("success", False):
            travel_plan = result.get("travel_plan", {})
            for key in travel_plan:
                print(f"Travel Plan has {key}: {bool(travel_plan.get(key))}")

        # Return result for assertion in a test environment
        return result


if __name__ == "__main__":
    test_travel_crew_with_mock()
