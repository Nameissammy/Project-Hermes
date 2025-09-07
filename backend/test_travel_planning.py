#!/usr/bin/env python
"""
Simple test script for the travel crew implementation.
"""

import json
import sys
from pathlib import Path

# Add the project to the Python path
src_path = Path(__file__).parent.parent / "src"
sys.path.append(str(src_path.absolute()))

from project_hermes.crews.travel_crew.travel_crew import TravelCrew


def test_travel_related_query():
    """Test with a travel-related query."""
    travel_crew = TravelCrew(verbose=True)
    result = travel_crew.plan_trip("Plan a weekend trip to Paris")
    print("\n=== Travel-Related Query Result ===")
    print(json.dumps(result, indent=2))
    assert result["success"] is True
    assert "travel_plan" in result
    assert result["confidence_score"] >= 0.6
    print("✅ Travel-related query test passed")


def test_non_travel_query():
    """Test with a non-travel-related query."""
    travel_crew = TravelCrew(verbose=True)
    result = travel_crew.plan_trip("What is the capital of France?")
    print("\n=== Non-Travel Query Result ===")
    print(json.dumps(result, indent=2))
    assert result["success"] is False
    assert "error" in result
    assert "not appear to be travel-related" in result["error"]
    assert result["confidence_score"] < 0.6
    print("✅ Non-travel query test passed")


if __name__ == "__main__":
    print("Testing travel planning system...")
    test_travel_related_query()
    test_non_travel_query()
    print("\nAll tests passed! 🎉")
