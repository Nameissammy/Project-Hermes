from crewai import Task


class BaseTask:
    """Base class for all task creators."""

    def create_task(self, agent, description: str, expected_output: str, inputs: dict) -> Task:
        """Create a task with consistent structure."""
        return Task(
            agent=agent, description=description, expected_output=expected_output, inputs=inputs
        )


class ConfidenceTask(BaseTask):
    """Task for determining if a prompt is travel-related."""

    def create_confidence_task(self, agent, query):
        return self.create_task(
            agent=agent,
            description="Analyze the prompt and return a confidence score and the original prompt.",
            expected_output="A JSON object with 'score' and 'prompt'.",
            inputs={"query": query},
        )


class OrchestratorTask(BaseTask):
    """Tasks for the orchestrator agent."""

    def create_breakdown_task(self, agent, query):
        """Task to break down the query into component parts."""
        return self.create_task(
            agent=agent,
            description=(
                "Break down the travel query into key components that need to be "
                "researched or addressed by specialist agents."
            ),
            expected_output="A JSON object with component parts of the travel request.",
            inputs={"query": query},
        )

    def create_synthesis_task(self, agent, specialist_outputs):
        """Task to synthesize all outputs into a cohesive response."""
        return self.create_task(
            agent=agent,
            description=(
                "Synthesize all specialist findings into a cohesive, personalized travel plan."
            ),
            expected_output=(
                "A comprehensive travel plan in JSON format with sections for each specialist area."
            ),
            inputs={"specialist_outputs": specialist_outputs},
        )


class InfoTask(BaseTask):
    """Tasks for the information specialist agent."""

    def create_info_task(self, agent, location_data):
        return self.create_task(
            agent=agent,
            description=(
                "Research and provide real-time, location-specific information "
                "including weather forecasts, local events, and travel advisories."
            ),
            expected_output=(
                "A JSON object with weather, local news, events, and advisories "
                "for the specified location."
            ),
            inputs={"location_data": location_data},
        )


class SafetyTask(BaseTask):
    """Tasks for the safety guardian agent."""

    def create_safety_task(self, agent, location_data):
        return self.create_task(
            agent=agent,
            description=(
                "Provide safety information including emergency contacts, risk areas, "
                "and travel insurance recommendations."
            ),
            expected_output=(
                "A JSON object with emergency contacts, risk areas, and travel "
                "insurance recommendations."
            ),
            inputs={"location_data": location_data},
        )


class ExperienceTask(BaseTask):
    """Tasks for the experience curator agent."""

    def create_experience_task(self, agent, preferences, location_data):
        return self.create_task(
            agent=agent,
            description=(
                "Recommend personalized experiences based on traveler preferences "
                "including restaurants, attractions, and local activities."
            ),
            expected_output=(
                "A JSON object with personalized recommendations for restaurants, "
                "attractions, and activities."
            ),
            inputs={"preferences": preferences, "location_data": location_data},
        )


class LogisticTask(BaseTask):
    """Tasks for the logistics planner agent."""

    def create_logistic_task(self, agent, travel_details):
        return self.create_task(
            agent=agent,
            description=(
                "Plan travel logistics including flight options, accommodations, "
                "and transportation between destinations."
            ),
            expected_output=(
                "A JSON object with flight options, accommodations, and "
                "transportation recommendations."
            ),
            inputs={"travel_details": travel_details},
        )


class FinanceTask(BaseTask):
    """Tasks for the finance manager agent."""

    def create_finance_task(self, agent, budget, expenses):
        return self.create_task(
            agent=agent,
            description=(
                "Analyze the travel budget, allocate funds to different categories, "
                "and flag any over-budget recommendations."
            ),
            expected_output=(
                "A JSON object with budget allocation, spending recommendations, "
                "and any budget warnings."
            ),
            inputs={"budget": budget, "expenses": expenses},
        )
