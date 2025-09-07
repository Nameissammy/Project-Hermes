"""
Debug script to verify imports and paths
"""

import os
import sys
import json
from dotenv import load_dotenv

# Add the src directory to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(project_root, "src")
sys.path.append(src_path)

# Load environment variables
load_dotenv()

print(f"Python version: {sys.version}")
print(f"Working directory: {os.getcwd()}")
print(f"Project root: {project_root}")
print(f"Src path: {src_path}")
print(f"Src path exists: {os.path.exists(src_path)}")
print(f"Python path: {sys.path}")

# Try to import crewai
try:
    from crewai import Crew, Process, Agent, Task

    print("\n✅ Successfully imported CrewAI modules")
except ImportError as e:
    print(f"\n❌ Error importing CrewAI: {e}")

# Try to import from project_hermes
try:
    import project_hermes

    print(f"\n✅ Successfully imported project_hermes")
    print(f"project_hermes path: {project_hermes.__file__}")

    # Try to import the travel_crew module
    try:
        from project_hermes.crews.travel_crew.travel_crew import TravelCrew

        print("✅ Successfully imported TravelCrew")

        # Try to create a TravelCrew instance
        try:
            crew = TravelCrew(verbose=True)
            print("✅ Successfully created TravelCrew instance")
        except Exception as e:
            print(f"❌ Error creating TravelCrew instance: {e}")
    except ImportError as e:
        print(f"❌ Error importing TravelCrew: {e}")
except ImportError as e:
    print(f"\n❌ Error importing project_hermes: {e}")

    # List the contents of the src directory
    print("\nContents of src directory:")
    for root, dirs, files in os.walk(src_path):
        level = root.replace(src_path, "").count(os.sep)
        indent = " " * 4 * level
        print(f"{indent}{os.path.basename(root)}/")
        sub_indent = " " * 4 * (level + 1)
        for file in files:
            print(f"{sub_indent}{file}")

# Try to run in mock mode
print("\nTesting in mock mode:")
os.environ["OPENAI_API_KEY"] = "mock-api-key"

try:
    from unittest.mock import patch

    mock_response = json.dumps({"score": 0.85, "prompt": "Test query"})

    # Try to import the TravelCrew again
    try:
        from project_hermes.crews.travel_crew.travel_crew import TravelCrew

        # Mock the Crew.kickoff method
        with patch("crewai.Crew.kickoff", return_value=mock_response):
            travel_crew = TravelCrew(verbose=True)
            result = travel_crew.plan_trip("Test query")
            print("✅ Successfully ran TravelCrew in mock mode")
            print(f"Result: {json.dumps(result, indent=2)}")
    except ImportError as e:
        print(f"❌ Error importing TravelCrew for mock test: {e}")
except Exception as e:
    print(f"❌ Error in mock test: {e}")
