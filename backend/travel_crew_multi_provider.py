"""
Project Hermes - Multi-Provider Travel Planning System
------------------------------------------------------

This module implements a multi-provider version of the TravelCrew that can use
different LLM providers based on availability or explicit selection.

Providers are checked in this order:
1. Gemini (Google)
2. Claude (Anthropic)
3. OpenAI (GPT)

The system will use the first available provider unless explicitly specified.
"""

import json
import os
import re
from typing import Any

from crewai import LLM, Agent, Crew, Process, Task
from dotenv import load_dotenv

# Load environment variables (for API keys)
load_dotenv()


class TravelCrew:
    """
    TravelCrew coordinates specialized travel agents to create comprehensive travel plans
    using multiple LLM providers.
    """

    def __init__(self, llm_provider: str | None = None, verbose: bool = True):
        """
        Initialize the crew with a specified language model provider.

        Args:
            llm_provider: The LLM provider to use ('gemini', 'claude', 'openai',
                or None for auto-detect)
            verbose: Whether to enable verbose mode for debugging
        """
        self.verbose = verbose
        self.llm_provider_name = None

        # Initialize the language model based on the provider
        self.llm = self._initialize_llm(llm_provider)

        # Create the specialized agents
        self.destination_expert = self._create_destination_expert()
        self.itinerary_planner = self._create_itinerary_planner()
        self.safety_advisor = self._create_safety_advisor()
        self.budget_analyst = self._create_budget_analyst()
        self.confidence_agent = self._create_confidence_agent()

    def _initialize_llm(self, provider: str | None = None):
        """
        Initialize the language model based on the provider.

        If provider is None, the system will try to use providers in this order:
        1. Gemini (if GEMINI_API_KEY or GOOGLE_API_KEY is set)
        2. Claude (if CLAUDE_API_KEY or ANTHROPIC_API_KEY is set)
        3. OpenAI (if OPENAI_API_KEY is set)

        Args:
            provider: The LLM provider to use ('gemini', 'claude', 'openai',
                or None for auto-detect)

        Returns:
            The initialized language model (crewai.LLM)
        """
        # For explicit provider selection
        if provider:
            return self._get_specific_provider(provider)

        # Try Gemini first
        if os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY"):
            try:
                self.llm_provider_name = "gemini"
                # Use CrewAI/LightLLM provider-prefixed model naming
                # Requirement: only use gemini-2.0-flash for Gemini
                return LLM(model="gemini/gemini-2.0-flash", temperature=0.7)
            except Exception as e:
                if self.verbose:
                    print(f"Could not initialize Gemini: {e}")

        # Try Claude second
        if os.getenv("CLAUDE_API_KEY") or os.getenv("ANTHROPIC_API_KEY"):
            try:
                self.llm_provider_name = "claude"
                return LLM(model="anthropic/claude-3-sonnet-20240229", temperature=0.7)
            except Exception as e:
                if self.verbose:
                    print(f"Could not initialize Claude: {e}")

        # Try OpenAI last
        if os.getenv("OPENAI_API_KEY"):
            try:
                self.llm_provider_name = "openai"
                return LLM(model="openai/gpt-4-turbo", temperature=0.7)
            except Exception as e:
                if self.verbose:
                    print(f"Could not initialize OpenAI: {e}")

        # If no API keys are available or all initializations failed
        raise ValueError(
            "No API keys available for any provider. Please set at least one of "
            "GEMINI_API_KEY/GOOGLE_API_KEY, CLAUDE_API_KEY/ANTHROPIC_API_KEY, or OPENAI_API_KEY."
        )

    def _get_specific_provider(self, provider: str):
        """
        Get a specific LLM provider.

        Args:
            provider: The LLM provider to use ('gemini', 'claude', or 'openai')

        Returns:
            The initialized language model (crewai.LLM)
        """
        p = provider.lower()
        if p in ("google", "gemini"):
            self.llm_provider_name = "gemini"
            if not (os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")):
                raise ValueError("GEMINI_API_KEY or GOOGLE_API_KEY not set")
            return LLM(model="gemini/gemini-2.0-flash", temperature=0.7)
        if p in ("anthropic", "claude"):
            self.llm_provider_name = "claude"
            if not (os.getenv("CLAUDE_API_KEY") or os.getenv("ANTHROPIC_API_KEY")):
                raise ValueError("CLAUDE_API_KEY or ANTHROPIC_API_KEY not set")
            return LLM(model="anthropic/claude-3-sonnet-20240229", temperature=0.7)
        if p in ("openai",):
            self.llm_provider_name = "openai"
            if not os.getenv("OPENAI_API_KEY"):
                raise ValueError("OPENAI_API_KEY not set")
            return LLM(model="openai/gpt-4-turbo", temperature=0.7)
        raise ValueError("Unknown provider. Use 'gemini', 'claude', or 'openai'")

    def _create_destination_expert(self):
        """Create the destination expert agent."""
        return Agent(
            role="Travel Destination Expert",
            goal=(
                "Provide detailed information about travel destinations and recommend "
                "appropriate places based on user preferences"
            ),
            backstory=(
                "You are a highly knowledgeable travel destination expert with deep knowledge of "
                "attractions, local customs, optimal seasons, and hidden gems."
            ),
            verbose=self.verbose,
            llm=self.llm,
        )

    def _create_itinerary_planner(self):
        """Create the itinerary planner agent."""
        return Agent(
            role="Travel Itinerary Planner",
            goal=(
                "Create detailed day-by-day itineraries that balance enjoyment, pacing, and "
                "logistics"
            ),
            backstory=(
                "You design practical schedules, group nearby attractions efficiently, and plan "
                "transport between locations with realistic timing."
            ),
            verbose=self.verbose,
            llm=self.llm,
        )

    def _create_safety_advisor(self):
        """Create the safety advisor agent."""
        return Agent(
            role="Travel Safety Advisor",
            goal=(
                "Provide safety information and recommendations specific to the destination and "
                "plan"
            ),
            backstory=(
                "You track global safety conditions and offer practical advice, health tips, and "
                "emergency resources without causing unnecessary alarm."
            ),
            verbose=self.verbose,
            llm=self.llm,
        )

    def _create_budget_analyst(self):
        """Create the budget analyst agent."""
        return Agent(
            role="Travel Budget Analyst",
            goal=(
                "Create realistic travel budgets and suggest cost optimizations without "
                "harming the experience"
            ),
            backstory=(
                "You estimate costs across accommodation, transportation, food, activities, and "
                "miscellaneous items, and tailor options to different budget levels."
            ),
            verbose=self.verbose,
            llm=self.llm,
        )

    def _create_confidence_agent(self):
        """Create the confidence scoring agent that determines if a query is travel-related."""
        return Agent(
            role="Travel Query Evaluator",
            goal=(
                "Evaluate whether user queries are related to travel planning and provide a "
                "confidence score"
            ),
            backstory=(
                "You distinguish travel planning queries from general questions and output a "
                "confidence score between 0 and 1."
            ),
            verbose=self.verbose,
            llm=self.llm,
        )

    def plan_trip(self, query: str) -> dict[str, Any]:
        """
        Plan a trip based on a natural language query.

        Args:
            query: The natural language query describing the desired trip

        Returns:
            A dictionary containing the travel plan details
        """
        # Create the confidence task
        confidence_task = Task(
            description=(
                f"Analyze this query and determine if it's related to travel planning: "
                f'"{query}"\n\n'
                "Respond with a JSON object containing: \n"
                "1. confidence_score: A number between 0 and 1 (1 = definitely travel-related)\n"
                "2. query: The original query\n\n"
                'Example: {"confidence_score": 0.95, "query": "Plan a trip to Paris"}'
            ),
            expected_output=('{"confidence_score": <float 0-1>, "query": "<original query>"}'),
            agent=self.confidence_agent,
        )

        # Create the destination research task
        destination_task = Task(
            description=(
                f'Research the destination(s) mentioned in this query: "{query}"\n\n'
                "Provide details about: key features and attractions; culture and customs;"
                " best times to visit; and special considerations."
            ),
            expected_output=(
                "A comprehensive destination overview in markdown covering attractions, culture, "
                "best times to visit, and special considerations."
            ),
            agent=self.destination_expert,
        )

        # Create the itinerary planning task
        itinerary_task = Task(
            description=(
                f'Create a detailed itinerary for: "{query}"\n\n'
                "Include arrival/departure logistics, daily activities, meal suggestions, and local"
                " transport between locations. Format as a clear daily schedule."
            ),
            expected_output=(
                "A day-by-day itinerary in markdown with timeslots, activities, meals, and "
                "logistics."
            ),
            agent=self.itinerary_planner,
            context=[destination_task],
        )

        # Create the safety assessment task
        safety_task = Task(
            description=(
                f'Provide safety guidance for: "{query}"\n\n'
                "Include: general safety, itinerary-specific concerns, health tips, and emergency"
                " resources. Format as a traveler safety guide."
            ),
            expected_output=(
                "A practical safety guide in markdown covering general risks, itinerary-specific "
                "concerns, health tips, and emergency contacts/resources."
            ),
            agent=self.safety_advisor,
            context=[destination_task, itinerary_task],
        )

        # Create the budget analysis task
        budget_task = Task(
            description=(
                f'Create a budget for: "{query}"\n\n'
                "Estimate costs for accommodation, transportation, food, activities, and misc."
                " If a budget is provided, fit within it; otherwise, provide budget/mid-range/"
                "luxury"
                " options. Include a clear breakdown with approximate costs."
            ),
            expected_output=(
                "A markdown budget breakdown table with estimated costs by category and total, "
                "plus options for different budget levels if applicable."
            ),
            agent=self.budget_analyst,
            context=[destination_task, itinerary_task, safety_task],
        )

        # Create the crew with the defined agents and tasks
        crew = Crew(
            agents=[
                self.confidence_agent,
                self.destination_expert,
                self.itinerary_planner,
                self.safety_advisor,
                self.budget_analyst,
            ],
            tasks=[
                confidence_task,
                destination_task,
                itinerary_task,
                safety_task,
                budget_task,
            ],
            verbose=self.verbose,
            process=Process.sequential,
        )

        # Execute the crew workflow
        _final_output = crew.kickoff(inputs={"query": query})

        # Parse and format results
        try:

            def _to_text_output(out: Any) -> str:
                """Best-effort conversion of a CrewAI Task output to plain text."""
                if out is None:
                    return ""
                if isinstance(out, str):
                    return out
                # Try common attributes seen in CrewAI TaskOutput types
                for attr in ("raw", "raw_output", "content", "text", "final_output"):
                    val = getattr(out, attr, None)
                    if isinstance(val, str):
                        return val
                try:
                    return str(out)
                except Exception:
                    return ""

            def _extract_json(text: str) -> str | None:
                """Extract the first JSON object from text, if present."""
                if not text:
                    return None
                # Quick path if the whole text is JSON
                text_stripped = text.strip()
                if text_stripped.startswith("{") and text_stripped.endswith("}"):
                    return text_stripped
                # Fallback: find JSON object via regex (non-greedy)
                match = re.search(r"\{.*?\}", text_stripped, re.DOTALL)
                return match.group(0) if match else None

            # Try to parse confidence score result (task 0)
            conf_text = _to_text_output(crew.tasks[0].output)
            conf_json = _extract_json(conf_text)
            confidence_result = json.loads(conf_json) if conf_json else {"confidence_score": 1.0}
            confidence_score = confidence_result.get("confidence_score", 0.0)

            # If confidence is too low, return early
            if confidence_score < 0.6:
                return {
                    "success": False,
                    "confidence_score": confidence_score,
                    "error": "Query does not appear to be related to travel planning",
                    "query": query,
                    "travel_plan": None,
                    "llm_provider": self.llm_provider_name,
                }

            # Otherwise, process the full travel plan
            return {
                "success": True,
                "confidence_score": confidence_score,
                "query": query,
                "llm_provider": self.llm_provider_name,
                "travel_plan": {
                    "overview": _to_text_output(crew.tasks[1].output),
                    "itinerary": _to_text_output(crew.tasks[2].output),
                    "safety": _to_text_output(crew.tasks[3].output),
                    "finance": _to_text_output(crew.tasks[4].output),
                },
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to process travel plan: {str(e)}",
                "confidence_score": 0.0,
                "query": query,
                "llm_provider": self.llm_provider_name,
            }
