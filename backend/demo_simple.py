#!/usr/bin/env python3
"""
Project Hermes Demo
------------------

This script demonstrates the travel planning capabilities of Project Hermes.
"""

from travel_crew import TravelCrew

# Basic example usage of the TravelCrew class
if __name__ == "__main__":
    print("Initializing Travel Crew...")
    travel_crew = TravelCrew()

    query = "Plan a weekend trip to San Francisco"
    print(f"Processing query: {query}")

    try:
        plan = travel_crew.create_travel_plan(query)

        print("\nTravel Plan Generated:")
        print(f"Success: {plan.success}")
        print(f"Confidence: {plan.confidence_score}")

        if plan.success and hasattr(plan, "travel_plan"):
            print("\nOverview:")
            print(plan.travel_plan.overview[:200] + "...")

            print("\nItinerary:")
            print(plan.travel_plan.itinerary[:200] + "...")
    except Exception as e:
        print(f"Error: {e}")
