import json
from crewai import Crew, Process
from .agents import (
    ConfidenceAgent,
    ExperienceAgent,
    FinanceAgent,
    InfoAgent,
    LogisticAgent,
    OrchestratorAgent,
    SafetyAgent,
)
from .tasks import ConfidenceTask


class TravelCrew:
    def __init__(self, verbose: bool = True):
        self.verbose = verbose

    def create_crew(self) -> Crew:
        # Create all agents
        confidence_agent = ConfidenceAgent(verbose=self.verbose).agent
        orchestrator_agent = OrchestratorAgent(verbose=self.verbose).agent
        info_agent = InfoAgent(verbose=self.verbose).agent
        safety_agent = SafetyAgent(verbose=self.verbose).agent
        experience_agent = ExperienceAgent(verbose=self.verbose).agent
        logistic_agent = LogisticAgent(verbose=self.verbose).agent
        finance_agent = FinanceAgent(verbose=self.verbose).agent

        # Create the tasks
        confidence_task = ConfidenceTask().create_confidence_task(
            agent=confidence_agent,
            query="This is a placeholder query that will be replaced at runtime",
        )

        # Return the crew with agents and tasks
        return Crew(
            agents=[
                confidence_agent,
                orchestrator_agent,
                info_agent,
                safety_agent,
                experience_agent,
                logistic_agent,
                finance_agent,
            ],
            tasks=[confidence_task],  # We'll only add the confidence task initially
            verbose=self.verbose,
            process=Process.sequential,
        )

    def plan_trip(self, query: str) -> dict:
        # Create a crew with agents and tasks
        crew = self.create_crew()

        # Update the confidence task with the actual query
        if crew.tasks and len(crew.tasks) > 0:
            # Replace the placeholder query with the actual query
            crew.tasks[0].description = crew.tasks[0].description.replace(
                "This is a placeholder query that will be replaced at runtime", query
            )

        # Execute the crew
        result = crew.kickoff()

        try:
            # Parse the confidence score result
            confidence_result = json.loads(result)
            confidence_score = float(confidence_result.get("score", 0))

            # If confidence is too low, return early
            if confidence_score < 0.6:
                return {
                    "success": False,
                    "error": "The query does not appear to be travel-related.",
                    "confidence_score": confidence_score,
                    "query": query,
                }

            # For simplicity in this test version, just return a successful result
            # In a real implementation, we would run the full workflow with all tasks
            return {
                "success": True,
                "confidence_score": confidence_score,
                "query": query,
                "travel_plan": {
                    "overview": "This is a mock travel plan overview.",
                    "itinerary": "This is a mock itinerary.",
                    "safety": "This is mock safety information.",
                    "finance": "This is mock budget information.",
                },
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to process travel plan: {str(e)}",
                "confidence_score": 0,
                "query": query,
            }
