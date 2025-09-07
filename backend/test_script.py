"""
Project Hermes - Test Script
---------------------------

This script tests the travel planning system directly, without going through the API.
It's useful for debugging and development.
"""

from travel_crew import TravelCrew
import json


def test_travel_query(query):
    """Test a travel planning query."""
    print("\n===== Testing Travel Query =====")
    print(f"Query: {query}")

    # Create travel crew
    travel_crew = TravelCrew()

    # Get travel plan
    result = travel_crew.create_travel_plan(query)

    # Print results
    print("\n===== Results =====")
    print(f"Success: {result['success']}")
    print(f"Confidence Score: {result['confidence_score']}")

    if result["success"]:
        print("\n=== Travel Plan ===")
        plan = result["travel_plan"]
        print("\n--- Overview ---")
        print(plan["overview"])

        print("\n--- Itinerary ---")
        print(plan["itinerary"])

        print("\n--- Safety Information ---")
        print(plan["safety"])

        print("\n--- Budget ---")
        print(plan["finance"])
    else:
        print(f"\nError: {result.get('error', 'Unknown error')}")

    return result


if __name__ == "__main__":
    # Test different types of queries

    # A typical travel query
    travel_query = "Plan a weekend trip to Paris for a couple with a budget of $2000"
    result1 = test_travel_query(travel_query)

    # A non-travel query to test confidence scoring
    non_travel_query = "What's the capital of France?"
    result2 = test_travel_query(non_travel_query)

    # Save results to file for reference
    with open("test_results.json", "w") as f:
        json.dump(
            {
                "travel_query": {"query": travel_query, "result": result1},
                "non_travel_query": {"query": non_travel_query, "result": result2},
            },
            f,
            indent=2,
        )
