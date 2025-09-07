import logging

from crewai import Agent

from .utils import get_prompt_library

logger = logging.getLogger(__name__)


class BaseAgent:
    """Base class for all travel crew agents."""

    def __init__(self, verbose: bool = True):
        self.prompt_lib = get_prompt_library()
        self.verbose = verbose

    def create_agent(
        self,
        name: str,
        prompt_key: str,
        role: str,
        goal: str,
        backstory: str,
        tools: list | None = None,
    ) -> Agent:
        """Create an agent with a prompt from the prompt library."""
        prompt = self.prompt_lib.get_prompt_text(prompt_key)

        return Agent(
            name=name,
            prompt_template=prompt,
            role=role,
            goal=goal,
            backstory=backstory,
            tools=tools or [],
            verbose=self.verbose,
        )


class ConfidenceAgent(BaseAgent):
    """Agent that determines if a prompt is travel-related."""

    def __init__(self, verbose: bool = True):
        super().__init__(verbose=verbose)
        self.agent = self.create_agent(
            name="Confidence Analyzer",
            prompt_key="confidence_agent",
            role="Gatekeeper",
            goal="Determine if queries are travel-related",
            backstory=(
                "I analyze incoming queries to determine if they are relevant to travel planning."
            ),
        )


class OrchestratorAgent(BaseAgent):
    """Agent that orchestrates the travel planning process."""

    def __init__(self, verbose: bool = True):
        super().__init__(verbose=verbose)
        self.agent = self.create_agent(
            name="Orchestrator",
            prompt_key="orchestrator_agent",
            role="Conductor",
            goal="Break down travel requests and synthesize specialist findings",
            backstory="I manage the crew and ensure a cohesive travel plan.",
        )


class InfoAgent(BaseAgent):
    """Agent that gathers location-specific information."""

    def __init__(self, verbose: bool = True):
        super().__init__(verbose=verbose)
        self.agent = self.create_agent(
            name="Information Specialist",
            prompt_key="info_crew",
            role="Local Expert",
            goal="Gather real-time, location-specific information",
            backstory=(
                "I provide weather forecasts, local news, and travel advisories for destinations."
            ),
        )


class SafetyAgent(BaseAgent):
    """Agent that ensures traveler safety."""

    def __init__(self, verbose: bool = True):
        super().__init__(verbose=verbose)
        self.agent = self.create_agent(
            name="Safety Guardian",
            prompt_key="safety_crew",
            role="Guardian",
            goal="Ensure traveler safety",
            backstory=(
                "I provide emergency contacts, identify risk areas, and suggest travel insurance."
            ),
        )


class ExperienceAgent(BaseAgent):
    """Agent that personalizes travel experiences."""

    def __init__(self, verbose: bool = True):
        super().__init__(verbose=verbose)
        self.agent = self.create_agent(
            name="Experience Curator",
            prompt_key="experience_crew",
            role="Curator",
            goal="Personalize travel experiences",
            backstory=(
                "I recommend restaurants, attractions, and local experiences based on preferences."
            ),
        )


class LogisticAgent(BaseAgent):
    """Agent that manages travel logistics."""

    def __init__(self, verbose: bool = True):
        super().__init__(verbose=verbose)
        self.agent = self.create_agent(
            name="Logistics Planner",
            prompt_key="logistic_crew",
            role="Planner",
            goal="Manage travel and accommodation logistics",
            backstory="I find flight and hotel options and plan efficient routes.",
        )


class FinanceAgent(BaseAgent):
    """Agent that manages the trip budget."""

    def __init__(self, verbose: bool = True):
        super().__init__(verbose=verbose)
        self.agent = self.create_agent(
            name="Finance Manager",
            prompt_key="finance_agent",
            role="Accountant",
            goal="Manage the trip budget",
            backstory=(
                "I allocate funds, flag over-budget suggestions, and provide spending reports."
            ),
        )
