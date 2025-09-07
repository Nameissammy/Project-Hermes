import json

from crewai import Crew
from crewai.flow import Flow, listen, start
from pydantic import BaseModel

from .agents import (
    ConfidenceAgent,
    ExperienceAgent,
    FinanceAgent,
    InfoAgent,
    LogisticAgent,
    OrchestratorAgent,
    SafetyAgent,
)
from .tasks import (
    ConfidenceTask,
    ExperienceTask,
    FinanceTask,
    InfoTask,
    LogisticTask,
    OrchestratorTask,
    SafetyTask,
)


class TravelState(BaseModel):
    query: str = ""
    confidence_score: float = 0.0
    query_breakdown: dict | None = None
    info_results: dict | None = None
    safety_results: dict | None = None
    experience_results: dict | None = None
    logistic_results: dict | None = None
    finance_results: dict | None = None
    final_plan: dict | None = None
    error: str | None = None
    success: bool = True
    budget: float = 0.0
    preferences: dict | None = None


class TravelFlow(Flow[TravelState]):
    @start()
    def analyze_confidence(self) -> None:
        agent = ConfidenceAgent().agent
        task = ConfidenceTask().create_confidence_task(agent=agent, query=self.state.query)

        # Create a crew with just the confidence agent and task
        confidence_crew = Crew(agents=[agent], tasks=[task], verbose=True)

        # Run the crew to get the result
        result = confidence_crew.kickoff()

        try:
            parsed = json.loads(result)
            self.state.confidence_score = float(parsed.get("score", 0))
        except Exception as e:
            self.state.error = f"Failed to parse confidence score: {str(e)}"
            self.state.confidence_score = 0
            self.state.success = False

    @listen(analyze_confidence)
    def breakdown_query(self) -> None:
        # Skip this step if confidence score is too low
        if self.state.confidence_score < 0.6:
            return

        agent = OrchestratorAgent().agent
        task = OrchestratorTask().create_breakdown_task(agent=agent, query=self.state.query)

        # Create a crew with just this agent and task
        crew = Crew(agents=[agent], tasks=[task], verbose=True)

        # Run the crew to get the result
        result = crew.kickoff()

        try:
            self.state.query_breakdown = json.loads(result)

            # Extract budget and preferences from breakdown
            if self.state.query_breakdown:
                self.state.budget = float(self.state.query_breakdown.get("budget", 0))
                self.state.preferences = self.state.query_breakdown.get("preferences", {})
        except Exception as e:
            self.state.error = f"Failed to parse query breakdown: {str(e)}"
            self.state.success = False

    @listen(breakdown_query)
    def gather_info(self) -> None:
        # Skip if previous step was skipped or failed
        if not self.state.query_breakdown:
            return

        agent = InfoAgent().agent
        task = InfoTask().create_info_task(
            agent=agent,
            query=self.state.query,
            destination=self.state.query_breakdown.get("destination", ""),
            activities=self.state.query_breakdown.get("activities", []),
        )

        # Create a crew with just this agent and task
        crew = Crew(agents=[agent], tasks=[task], verbose=True)

        # Run the crew to get the result
        result = crew.kickoff()

        try:
            self.state.info_results = json.loads(result)
        except Exception as e:
            self.state.error = f"Failed to parse info results: {str(e)}"
            self.state.success = False

    @listen(breakdown_query)
    def assess_safety(self) -> None:
        # Skip if previous step was skipped or failed
        if not self.state.query_breakdown:
            return

        agent = SafetyAgent().agent
        task = SafetyTask().create_safety_task(
            agent=agent, location_data=self.state.query_breakdown.get("locations", {})
        )

        # Create a crew with just this agent and task
        crew = Crew(agents=[agent], tasks=[task], verbose=True)

        # Run the crew to get the result
        result = crew.kickoff()

        try:
            self.state.safety_results = json.loads(result)
        except Exception as e:
            self.state.error = f"Failed to parse safety results: {str(e)}"
            self.state.success = False

    @listen(breakdown_query)
    def curate_experiences(self) -> None:
        # Skip if previous step was skipped or failed
        if not self.state.query_breakdown:
            return

        agent = ExperienceAgent().agent
        task = ExperienceTask().create_experience_task(
            agent=agent,
            preferences=self.state.preferences,
            location_data=self.state.query_breakdown.get("locations", {}),
        )

        # Create a crew with just this agent and task
        crew = Crew(agents=[agent], tasks=[task], verbose=True)

        # Run the crew to get the result
        result = crew.kickoff()
        try:
            self.state.experience_results = json.loads(result)
        except Exception as e:
            self.state.error = f"Failed to parse experience results: {str(e)}"
            self.state.success = False

    @listen(breakdown_query)
    def plan_logistics(self) -> None:
        # Skip if previous step was skipped or failed
        if not self.state.query_breakdown:
            return

        agent = LogisticAgent().agent
        task = LogisticTask().create_logistic_task(
            agent=agent,
            travel_details={
                "dates": self.state.query_breakdown.get("dates", {}),
                "locations": self.state.query_breakdown.get("locations", {}),
                "travelers": self.state.query_breakdown.get("travelers", {}),
            },
        )

        # Create a crew with just this agent and task
        crew = Crew(agents=[agent], tasks=[task], verbose=True)

        # Run the crew to get the result
        result = crew.kickoff()

        try:
            self.state.logistic_results = json.loads(result)
        except Exception as e:
            self.state.error = f"Failed to parse logistic results: {str(e)}"
            self.state.success = False

    @listen(breakdown_query)
    def manage_finances(self) -> None:
        # Skip if previous step was skipped or failed
        if not self.state.query_breakdown:
            return

        agent = FinanceAgent().agent
        task = FinanceTask().create_finance_task(
            agent=agent,
            budget=self.state.budget,
            expenses=self.state.query_breakdown.get("expected_expenses", {}),
        )

        # Create a crew with just this agent and task
        crew = Crew(agents=[agent], tasks=[task], verbose=True)

        # Run the crew to get the result
        result = crew.kickoff()

        try:
            self.state.finance_results = json.loads(result)
        except Exception as e:
            self.state.error = f"Failed to parse finance results: {str(e)}"
            self.state.success = False

    @listen("gather_info")
    @listen("assess_safety")
    @listen("curate_experiences")
    @listen("plan_logistics")
    @listen("manage_finances")
    def synthesize_plan(self) -> None:
        # Skip if any of the required results are missing
        if not all(
            [
                self.state.info_results,
                self.state.safety_results,
                self.state.experience_results,
                self.state.logistic_results,
                self.state.finance_results,
            ]
        ):
            return

        agent = OrchestratorAgent().agent
        task = OrchestratorTask().create_synthesis_task(
            agent=agent,
            specialist_outputs={
                "info": self.state.info_results,
                "safety": self.state.safety_results,
                "experience": self.state.experience_results,
                "logistics": self.state.logistic_results,
                "finance": self.state.finance_results,
            },
        )

        # Create a crew with just this agent and task
        crew = Crew(agents=[agent], tasks=[task], verbose=True)

        # Run the crew to get the result
        result = crew.kickoff()

        try:
            self.state.final_plan = json.loads(result)
        except Exception as e:
            self.state.error = f"Failed to parse final plan: {str(e)}"
            self.state.success = False
