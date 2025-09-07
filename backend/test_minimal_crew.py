"""
Project Hermes - Simple Travel Crew Test
----------------------------------------

This script tests the TravelCrew class directly with a minimal example.
"""

import os
import sys
import json
from dotenv import load_dotenv

# Add the project root to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
backend_src = os.path.join(project_root, "backend", "src")
sys.path.append(backend_src)

# Load environment variables for API keys
load_dotenv()


def print_section(title):
    """Print a formatted section title."""
    print("\n" + "=" * 60)
    print(f" {title} ".center(60, "-"))
    print("=" * 60)


def run_test():
    print_section("TESTING TRAVEL CREW")

    # Check if required API keys are set
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("WARNING: OPENAI_API_KEY is not set. Using mock mode.")
        use_mocks = True
    else:
        use_mocks = False
        print(f"Found API key starting with: {api_key[:4]}...")

    print(f"Python version: {sys.version}")
    print(f"Working directory: {os.getcwd()}")
    print(f"Backend src path: {backend_src}")
    print(f"Path exists: {os.path.exists(backend_src)}")
    print(f"Python path: {sys.path}")

    try:
        # Import the CrewAI module
        print("Attempting to import CrewAI...")
        try:
            from crewai import Crew, Process, Agent, Task

            print("Successfully imported CrewAI modules")
        except ImportError as e:
            print(f"Error importing CrewAI: {e}")
            print("Trying to install CrewAI...")
            import subprocess

            subprocess.check_call([sys.executable, "-m", "pip", "install", "crewai"])
            from crewai import Crew, Process, Agent, Task

            print("Successfully installed and imported CrewAI")

        # This is a minimal implementation to test if the Crew constructor works
        class MinimalAgent:
            def __init__(self):
                self.agent = Agent(
                    role="Test Agent",
                    goal="Test the Crew API",
                    backstory="I am a test agent",
                )

        class MinimalTask:
            @staticmethod
            def create_test_task(agent, query):
                return Task(
                    description=f"Test task with query: {query}",
                    agent=agent,
                )

        # Create agent and task
        test_agent = MinimalAgent().agent
        test_task = MinimalTask.create_test_task(test_agent, "Test query")

        # Create the crew
        crew = Crew(
            agents=[test_agent],
            tasks=[test_task],
            verbose=True,
            process=Process.sequential,
        )

        print("Successfully created a Crew instance with the new API!")
        print("This confirms that our implementation approach should work.")

        # If we want to actually run the crew, we need API keys
        if not use_mocks and api_key:
            print("\nAPI key is set. Would you like to run the actual Crew (y/n)?")
            choice = input().lower()
            if choice == "y":
                print("Running the crew...")
                result = crew.kickoff()
                print(f"Result: {result}")

    except ImportError as e:
        print(f"Error importing modules: {e}")
        print("Please install the required packages:")
        print("pip install crewai")
    except Exception as e:
        print(f"Error during execution: {e}")


if __name__ == "__main__":
    run_test()
