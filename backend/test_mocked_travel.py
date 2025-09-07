#!/usr/bin/env python
"""
This script tests the travel_crew module with mocked LLM responses to avoid API key issues.
It's a simplified test that focuses on the workflow rather than actual API calls.
"""

import json
import logging
from unittest.mock import MagicMock, patch

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# Mocked responses
CONFIDENCE_RESPONSE = json.dumps(
    {"score": 0.95, "reasoning": "This query is explicitly asking for travel planning."}
)
BREAKDOWN_RESPONSE = json.dumps(
    {
        "destination": "Paris",
        "dates": {"start": "2023-09-10", "end": "2023-09-12"},
        "travelers": {"count": 2, "type": "couple"},
        "budget": 2000,
        "preferences": {"interests": ["sightseeing", "cuisine", "culture"]},
    }
)
INFO_RESPONSE = json.dumps(
    {
        "attractions": ["Eiffel Tower", "Louvre Museum", "Notre Dame"],
        "local_info": "Paris is known for its cuisine, art, and romantic atmosphere.",
    }
)
SAFETY_RESPONSE = json.dumps(
    {
        "safety_rating": 4,
        "health_advisories": "No current health advisories for Paris.",
        "travel_advisories": "Exercise normal precautions in France.",
    }
)
EXPERIENCE_RESPONSE = json.dumps(
    {
        "recommended_activities": [
            "Visit the Eiffel Tower",
            "Tour the Louvre",
            "Dine at a local café",
        ]
    }
)
LOGISTIC_RESPONSE = json.dumps(
    {
        "transportation": {"from_airport": "Taxi or train", "around_city": "Metro"},
        "accommodation": {"recommended_areas": ["Le Marais", "Latin Quarter"]},
    }
)
FINANCE_RESPONSE = json.dumps(
    {
        "budget_breakdown": {
            "accommodation": 800,
            "food": 500,
            "activities": 300,
            "transportation": 300,
            "misc": 100,
        }
    }
)
FINAL_PLAN_RESPONSE = json.dumps(
    {
        "overview": "A romantic weekend in Paris for a couple with a $2000 budget.",
        "itinerary": [
            {
                "day": "Day 1",
                "activities": ["Arrive in Paris", "Check into hotel", "Evening at Eiffel Tower"],
            },
            {
                "day": "Day 2",
                "activities": [
                    "Morning at Louvre",
                    "Lunch in Latin Quarter",
                    "Evening Seine cruise",
                ],
            },
            {
                "day": "Day 3",
                "activities": ["Shopping in Le Marais", "Farewell dinner", "Departure"],
            },
        ],
        "budget": {
            "total": 2000,
            "breakdown": {
                "accommodation": 800,
                "food": 500,
                "activities": 300,
                "transportation": 300,
                "misc": 100,
            },
        },
        "safety": {
            "rating": 4,
            "tips": "Keep valuables secure and be aware of pickpockets in tourist areas.",
        },
    }
)


def mock_kickoff(*args, **kwargs):
    """Mock the kickoff method of Crew to return predefined responses based on the task description."""
    # Get the task description from the first task in the crew
    if not kwargs.get("tasks") and not args[0].tasks:
        return "No tasks defined"

    tasks = kwargs.get("tasks", args[0].tasks)
    if not tasks:
        return "No tasks defined"

    task = tasks[0]
    description = task.description.lower()

    # Return appropriate response based on task description
    if "confidence" in description:
        return CONFIDENCE_RESPONSE
    elif "breakdown" in description:
        return BREAKDOWN_RESPONSE
    elif "gather information" in description:
        return INFO_RESPONSE
    elif "safety" in description:
        return SAFETY_RESPONSE
    elif "experience" in description:
        return EXPERIENCE_RESPONSE
    elif "logistic" in description:
        return LOGISTIC_RESPONSE
    elif "finance" in description:
        return FINANCE_RESPONSE
    elif "synthesis" in description:
        return FINAL_PLAN_RESPONSE
    else:
        return json.dumps({"error": "Unknown task type"})


def test_travel_planning():
    """Test the travel planning system with mocked responses."""
    from project_hermes.crews.travel_crew.travel_crew import TravelCrew

    # Create a travel crew instance
    travel_crew = TravelCrew(verbose=True)

    # Mock the Crew.kickoff method to return our predefined responses
    with patch("crewai.Crew.kickoff", side_effect=mock_kickoff):
        # Test with a travel query
        query = "Plan a weekend trip to Paris for a couple with a budget of $2000"
        logger.info(f"Testing query: {query}")

        # Get the travel plan
        result = travel_crew.plan_trip(query)

        # Check the result
        assert result["success"] is True, "Expected success to be True"
        assert result["confidence_score"] >= 0.6, "Expected confidence score >= 0.6"
        assert "travel_plan" in result, "Expected travel_plan in result"

        # Print the result
        logger.info("Test passed! Result:")
        logger.info(json.dumps(result, indent=2))

        return result


if __name__ == "__main__":
    logger.info("Starting mocked travel planning test...")
    try:
        result = test_travel_planning()
        logger.info("All tests passed successfully! 🎉")
    except Exception as e:
        logger.error(f"Test failed: {e}", exc_info=True)
    finally:
        logger.info("Test completed.")
