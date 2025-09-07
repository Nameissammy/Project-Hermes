"""
Realistic Test of Project Hermes Travel Planning System

This script tests the travel planning system with a realistic query,
using the Gemini provider which has a valid API key.
"""

import os
import sys
import json
from dotenv import load_dotenv

# Add necessary paths
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
backend_dir = os.path.join(project_root, "backend")
src_dir = os.path.join(backend_dir, "src")
sys.path.append(backend_dir)
sys.path.append(src_dir)

# Load environment variables
load_dotenv()

# Import the travel crew
from travel_crew import TravelCrew


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
    print_section("PROJECT HERMES - REALISTIC TEST")

    # Check available providers
    print("Available API Keys:")
    print(
        f"- OpenAI: {'Available' if os.getenv('OPENAI_API_KEY') and os.getenv('OPENAI_API_KEY') != 'dummy_key_for_testing' else 'Not available'}"
    )
    print(f"- Gemini: {'Available' if os.getenv('GEMINI_API_KEY') else 'Not available'}")
    print(f"- Claude: {'Available' if os.getenv('CLAUDE_API_KEY') else 'Not available'}")

    # Use Gemini for this test (it has a valid API key)
    provider = "gemini"
    print(f"\nUsing {provider.upper()} provider for this test")

    # Define a realistic travel query
    query = "Plan a 5-day family vacation to Japan in spring for 2 adults and 2 children (ages 8 and 12). We're interested in cultural experiences, kid-friendly activities, and some nature exploration. Our budget is around $8000 excluding flights."

    print_section("TRAVEL QUERY")
    print(query)

    try:
        # Create a TravelCrew instance with the Gemini provider
        travel_crew = TravelCrew(llm_provider=provider)

        # Track the start time
        import time

        start_time = time.time()

        # Plan the trip
        print("\nPlanning trip...")
        result = travel_crew.create_travel_plan(query)

        # Calculate and display the time taken
        elapsed_time = time.time() - start_time
        print(f"\nTime taken: {elapsed_time:.2f} seconds")

        # Display the result
        display_travel_plan(result)

    except Exception as e:
        print(f"\nError running test: {e}")

        # If there's a quota error with Gemini, suggest using mock mode
        if "quota" in str(e).lower() or "rate limit" in str(e).lower():
            print("\nLooks like we hit a quota limit with the Gemini API.")
            print("Let's try with our mock implementation instead.")

            # Run the mock implementation
            try:
                from test_mock_travel import mock_travel_plan

                print("\nUsing mock travel data:")
                display_travel_plan(mock_travel_plan)
            except Exception as mock_error:
                print(f"Error with mock implementation: {mock_error}")


if __name__ == "__main__":
    main()
