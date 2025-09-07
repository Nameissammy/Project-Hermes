"""
Mocked Travel Planning System Test
This script demonstrates the travel planning system using a mock implementation
"""

import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("Starting mocked travel planning test...")

# Mock travel plan data
mock_travel_plan = {
    "success": True,
    "confidence_score": 0.95,
    "travel_plan": {
        "overview": "A weekend getaway to Paris for a couple with a budget of $2000. This plan includes accommodations, dining experiences, and key attractions.",
        "itinerary": [
            {
                "day": "Day 1 - Friday",
                "activities": [
                    {"time": "9:00 AM", "description": "Arrive at Charles de Gaulle Airport"},
                    {
                        "time": "11:00 AM",
                        "description": "Check-in at budget-friendly hotel in Le Marais",
                    },
                    {"time": "1:00 PM", "description": "Lunch at Café de Flore"},
                    {"time": "3:00 PM", "description": "Visit the Louvre Museum"},
                    {"time": "7:00 PM", "description": "Dinner at L'As du Fallafel"},
                ],
            },
            {
                "day": "Day 2 - Saturday",
                "activities": [
                    {"time": "8:00 AM", "description": "Breakfast at local bakery"},
                    {"time": "10:00 AM", "description": "Explore Eiffel Tower"},
                    {"time": "1:00 PM", "description": "Picnic lunch at Champ de Mars"},
                    {"time": "3:00 PM", "description": "Seine River cruise"},
                    {"time": "7:00 PM", "description": "Dinner at Le Petit Châtelet"},
                ],
            },
            {
                "day": "Day 3 - Sunday",
                "activities": [
                    {"time": "9:00 AM", "description": "Breakfast at hotel"},
                    {"time": "10:30 AM", "description": "Visit Montmartre and Sacré-Cœur"},
                    {"time": "1:00 PM", "description": "Lunch at La Maison Rose"},
                    {"time": "3:00 PM", "description": "Last-minute shopping"},
                    {"time": "6:00 PM", "description": "Departure to airport"},
                ],
            },
        ],
        "safety": {
            "overall_safety": "High",
            "local_emergency_number": "112",
            "safety_tips": "Keep valuables secure, beware of pickpockets at tourist spots",
            "health_considerations": "No specific health concerns, standard travel precautions apply",
        },
        "finance": {
            "total_budget": 2000,
            "accommodation": 600,
            "food": 500,
            "transportation": 400,
            "activities": 300,
            "shopping": 200,
        },
    },
}


def display_travel_plan(result):
    """Display the travel plan in a readable format."""
    if not result:
        print("No result to display")
        return

    print("\n=== RESPONSE SUMMARY ===")
    print(f"Success: {result.get('success', False)}")
    print(f"Confidence Score: {result.get('confidence_score', 0)}")

    if not result.get("success", False):
        print(f"\nError: {result.get('error', 'Unknown error')}")
        return

    travel_plan = result.get("travel_plan", {})
    if not travel_plan:
        print("\nNo travel plan details available.")
        return

    print("\n=== TRAVEL PLAN ===")

    # Print the plan overview
    if "overview" in travel_plan:
        print("\n📋 OVERVIEW")
        print(travel_plan["overview"])

    # Print itinerary
    if "itinerary" in travel_plan:
        print("\n🗓️ ITINERARY")
        itinerary = travel_plan["itinerary"]
        if isinstance(itinerary, list):
            for day in itinerary:
                print(f"\n📅 {day.get('day', 'Day')}:")
                for activity in day.get("activities", []):
                    print(f"  • {activity.get('time', '')} - {activity.get('description', '')}")
        else:
            print(itinerary)  # Fallback if not in expected format

    # Print safety information
    if "safety" in travel_plan:
        print("\n🛡️ SAFETY INFORMATION")
        safety = travel_plan["safety"]
        if isinstance(safety, dict):
            for key, value in safety.items():
                print(f"  • {key.replace('_', ' ').title()}: {value}")
        else:
            print(safety)

    # Print budget information
    if "finance" in travel_plan:
        print("\n💰 BUDGET")
        finance = travel_plan["finance"]
        if isinstance(finance, dict):
            for category, amount in finance.items():
                if isinstance(amount, (int, float)):
                    print(f"  • {category.replace('_', ' ').title()}: ${amount}")
                else:
                    print(f"  • {category.replace('_', ' ').title()}: {amount}")
        else:
            print(finance)


# Display the mock travel plan
print("\nMocked travel plan generated successfully!")
display_travel_plan(mock_travel_plan)
print("\nTest completed successfully without needing any API keys!")
