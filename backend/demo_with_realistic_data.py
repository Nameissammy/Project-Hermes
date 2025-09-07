"""
Simplified Test of Project Hermes Travel Planning System

This script tests the travel planning system with our mock data
to demonstrate the output format and functionality.
"""

import os
import sys
import json
from dotenv import load_dotenv

# Add necessary paths
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
backend_dir = os.path.join(project_root, "backend")
sys.path.append(backend_dir)

# Load environment variables
load_dotenv()

# Create a realistic travel plan mockup
mock_travel_plan = {
    "success": True,
    "confidence_score": 0.95,
    "query": "Plan a 5-day family vacation to Japan in spring for 2 adults and 2 children (ages 8 and 12)",
    "travel_plan": {
        "overview": "This 5-day family trip to Japan in spring combines cultural experiences, kid-friendly activities, and nature exploration within your $8,000 budget (excluding flights). You'll experience cherry blossoms, visit family-friendly museums, explore temples, and enjoy interactive activities perfect for children aged 8 and 12.",
        "itinerary": [
            {
                "day": "Day 1 - Tokyo: Family-Friendly Introduction",
                "activities": [
                    {
                        "time": "9:00 AM",
                        "description": "Arrival and check-in at family-friendly hotel in Shinjuku",
                    },
                    {
                        "time": "11:00 AM",
                        "description": "Visit Meiji Shrine and Yoyogi Park (perfect for cherry blossom viewing in spring)",
                    },
                    {"time": "1:00 PM", "description": "Lunch at Harajuku Kiddy Land food court"},
                    {
                        "time": "2:30 PM",
                        "description": "Explore Harajuku's Takeshita Street (fun shopping for kids)",
                    },
                    {
                        "time": "4:30 PM",
                        "description": "Tokyo Anime Center or Pokémon Center (based on children's interests)",
                    },
                    {
                        "time": "6:30 PM",
                        "description": "Dinner at family-friendly Izakaya with kid's menu",
                    },
                ],
            },
            {
                "day": "Day 2 - Tokyo: Educational Fun",
                "activities": [
                    {"time": "8:30 AM", "description": "Breakfast at hotel"},
                    {
                        "time": "10:00 AM",
                        "description": "TeamLab Borderless Digital Art Museum (interactive experiences kids will love)",
                    },
                    {"time": "1:00 PM", "description": "Lunch at Odaiba food court"},
                    {
                        "time": "2:30 PM",
                        "description": "Miraikan Science Museum with hands-on exhibits",
                    },
                    {"time": "5:00 PM", "description": "Tokyo Tower observation deck"},
                    {
                        "time": "7:00 PM",
                        "description": "Dinner at kid-friendly sushi restaurant with conveyor belt",
                    },
                ],
            },
            {
                "day": "Day 3 - Hakone: Nature Day",
                "activities": [
                    {"time": "8:00 AM", "description": "Check out and take train to Hakone"},
                    {
                        "time": "10:30 AM",
                        "description": "Hakone Open Air Museum (art and large play structures)",
                    },
                    {"time": "1:00 PM", "description": "Lunch at local restaurant"},
                    {
                        "time": "2:30 PM",
                        "description": "Hakone Ropeway with views of Mt. Fuji (weather permitting)",
                    },
                    {"time": "4:00 PM", "description": "Lake Ashi boat cruise"},
                    {
                        "time": "6:00 PM",
                        "description": "Check in to traditional ryokan with family room",
                    },
                    {
                        "time": "7:00 PM",
                        "description": "Traditional Japanese dinner and onsen experience",
                    },
                ],
            },
            {
                "day": "Day 4 - Kyoto: Cultural Immersion",
                "activities": [
                    {"time": "7:30 AM", "description": "Traditional Japanese breakfast at ryokan"},
                    {"time": "9:00 AM", "description": "Train to Kyoto"},
                    {
                        "time": "11:30 AM",
                        "description": "Arashiyama Bamboo Grove and Monkey Park (kids will love seeing the monkeys)",
                    },
                    {"time": "1:30 PM", "description": "Lunch at local restaurant"},
                    {
                        "time": "3:00 PM",
                        "description": "Kimono/Yukata experience for the whole family (kid sizes available)",
                    },
                    {
                        "time": "5:00 PM",
                        "description": "Fushimi Inari Shrine (walk just part of the trail with kids)",
                    },
                    {
                        "time": "7:00 PM",
                        "description": "Dinner at family-friendly restaurant in Kyoto",
                    },
                ],
            },
            {
                "day": "Day 5 - Kyoto: Interactive Cultural Activities",
                "activities": [
                    {"time": "8:30 AM", "description": "Breakfast at hotel"},
                    {"time": "10:00 AM", "description": "Visit Nijo Castle"},
                    {"time": "12:00 PM", "description": "Lunch near Nishiki Market"},
                    {
                        "time": "1:30 PM",
                        "description": "Samurai and Ninja experience (interactive lessons for kids)",
                    },
                    {
                        "time": "3:30 PM",
                        "description": "Wagashi (Japanese sweet) making class for the family",
                    },
                    {"time": "5:30 PM", "description": "Shopping for souvenirs at Nishiki Market"},
                    {
                        "time": "7:00 PM",
                        "description": "Farewell dinner with traditional entertainment",
                    },
                ],
            },
        ],
        "safety": {
            "overall_safety": "High",
            "local_emergency_number": "110 for police, 119 for ambulance/fire",
            "family_specific_tips": "Japan is very child-friendly with excellent facilities for families. Most restaurants have children's menus or can accommodate children.",
            "health_considerations": "Bring comfortable walking shoes as you'll do a lot of walking. Spring can bring some rain, so pack light rain jackets.",
        },
        "finance": {
            "total_budget": 8000,
            "accommodation": 2500,
            "food": 1500,
            "local_transportation": 900,
            "activities": 1800,
            "souvenirs": 800,
            "contingency": 500,
            "budget_tips": "Consider getting a Japan Rail Pass before arrival if you plan to use the bullet train. Family tickets are available at many attractions. Convenience stores offer affordable meal options.",
        },
    },
}


def print_section(title):
    """Print a formatted section title."""
    print("\n" + "=" * 60)
    print(f" {title} ".center(60, "-"))
    print("=" * 60)


def display_travel_plan(result):
    """Display the travel plan in a readable format."""
    if not result:
        print("No result to display")
        return

    print_section("RESPONSE SUMMARY")
    print(f"Success: {result.get('success', False)}")
    print(f"Confidence Score: {result.get('confidence_score', 0)}")

    if not result.get("success", False):
        print(f"\nError: {result.get('error', 'Unknown error')}")
        return

    travel_plan = result.get("travel_plan", {})
    if not travel_plan:
        print("\nNo travel plan details available.")
        return

    print_section("TRAVEL PLAN")

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


def main():
    """Main test function."""
    print_section("PROJECT HERMES - DEMO WITH REALISTIC DATA")

    # Display API provider information
    print("Using mock data to demonstrate the system's capabilities.")
    print("In a real scenario, this would be generated by Gemini, Claude, or OpenAI.\n")

    # Display the query
    query = "Plan a 5-day family vacation to Japan in spring for 2 adults and 2 children (ages 8 and 12). We're interested in cultural experiences, kid-friendly activities, and some nature exploration. Our budget is around $8000 excluding flights."

    print_section("TRAVEL QUERY")
    print(query)

    # Display the mock result
    print("\nDisplaying realistic travel plan:")
    display_travel_plan(mock_travel_plan)

    print("\nThis demonstrates how the system would work with a real LLM provider.")
    print(
        "The actual system is capable of generating similar plans for any destination and preferences."
    )


if __name__ == "__main__":
    main()
