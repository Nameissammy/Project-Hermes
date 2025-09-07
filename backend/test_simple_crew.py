"""
Very Simple CrewAI Test with Multi-Provider Support
"""

import os
import sys
from crewai import Agent, Crew, Process, Task
from dotenv import load_dotenv

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

print("Starting simple CrewAI test...")
print("Using multi-provider support with priority:")
print("Gemini -> Claude -> OpenAI")

# Try to import the TravelCrew multi-provider for LLM
try:
    from travel_crew_multi_provider import TravelCrew

    travel_crew = TravelCrew()
    llm = travel_crew.llm
    llm_name = travel_crew.llm_provider_name or "Unknown"
    print(f"Successfully initialized LLM: {llm_name}")
except ImportError as e:
    print(f"Error importing multi-provider: {e}")
    print("Falling back to default LLM")
    llm = None

# Create a simple agent
researcher = Agent(
    role="Researcher",
    goal="Research about a topic",
    backstory="You're a researcher that loves to research topics",
    verbose=True,
    llm=llm,  # Use our multi-provider LLM
)

# Create a simple task
research_task = Task(
    description="Research about the topic of AI",
    expected_output="A comprehensive summary of AI technology and its applications",
    agent=researcher,
)

# Create a crew with the agent and task
crew = Crew(
    agents=[researcher],
    tasks=[research_task],
    verbose=True,
    process=Process.sequential,
)

# Run the crew
print("\nRunning the crew...")
result = crew.kickoff()

print("\nCrew result:")
print(result)
