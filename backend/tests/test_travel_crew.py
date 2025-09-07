import json
from unittest.mock import MagicMock, patch

import pytest

from project_hermes.crews.travel_crew.flow import TravelFlow, TravelState
from project_hermes.crews.travel_crew.travel_crew import TravelCrew


@pytest.fixture
def mock_crew():
    with patch("project_hermes.crews.travel_crew.travel_crew.Crew") as mock_crew:
        mock_instance = MagicMock()
        mock_crew.return_value = mock_instance
        yield mock_instance


class TestTravelCrew:
    def test_plan_trip_low_confidence(self, mock_crew):
        # Set up mock result state with low confidence
        mock_result_state = TravelState(query="test query", confidence_score=0.4)
        mock_crew.kickoff.return_value = mock_result_state

        # Create the travel crew and call plan_trip
        travel_crew = TravelCrew()
        result = travel_crew.plan_trip("test query")

        # Verify the result shows the query is not travel-related
        assert not result["success"]
        assert "not appear to be travel-related" in result["error"]
        assert result["confidence_score"] == 0.4
        assert result["query"] == "test query"

    def test_plan_trip_success(self, mock_crew):
        # Set up mock result state with high confidence and a final plan
        mock_result_state = TravelState(
            query="Plan a trip to Paris",
            confidence_score=0.9,
            final_plan={"itinerary": "Sample Paris itinerary"},
        )
        mock_crew.kickoff.return_value = mock_result_state

        # Create the travel crew and call plan_trip
        travel_crew = TravelCrew()
        result = travel_crew.plan_trip("Plan a trip to Paris")

        # Verify the result contains the travel plan
        assert result["success"]
        assert result["confidence_score"] == 0.9
        assert result["query"] == "Plan a trip to Paris"
        assert result["travel_plan"] == {"itinerary": "Sample Paris itinerary"}

    def test_plan_trip_failure(self, mock_crew):
        # Set up mock result state with high confidence but no final plan
        mock_result_state = TravelState(
            query="Plan a trip to Mars", confidence_score=0.8, final_plan=None
        )
        mock_crew.kickoff.return_value = mock_result_state

        # Create the travel crew and call plan_trip
        travel_crew = TravelCrew()
        result = travel_crew.plan_trip("Plan a trip to Mars")

        # Verify the result shows a failure to generate a plan
        assert not result["success"]
        assert "Failed to generate a travel plan" in result["error"]
        assert result["confidence_score"] == 0.8
        assert result["query"] == "Plan a trip to Mars"


@pytest.fixture
def mock_agents():
    with (
        patch("project_hermes.crews.travel_crew.flow.ConfidenceAgent") as mock_confidence_agent,
        patch("project_hermes.crews.travel_crew.flow.OrchestratorAgent") as mock_orchestrator_agent,
        patch("project_hermes.crews.travel_crew.flow.InfoAgent") as mock_info_agent,
        patch("project_hermes.crews.travel_crew.flow.SafetyAgent") as mock_safety_agent,
        patch("project_hermes.crews.travel_crew.flow.ExperienceAgent") as mock_experience_agent,
        patch("project_hermes.crews.travel_crew.flow.LogisticAgent") as mock_logistic_agent,
        patch("project_hermes.crews.travel_crew.flow.FinanceAgent") as mock_finance_agent,
    ):
        # Set up mock agents
        agents = {
            "confidence": MagicMock(),
            "orchestrator": MagicMock(),
            "info": MagicMock(),
            "safety": MagicMock(),
            "experience": MagicMock(),
            "logistic": MagicMock(),
            "finance": MagicMock(),
        }

        mock_confidence_agent.return_value.agent = agents["confidence"]
        mock_orchestrator_agent.return_value.agent = agents["orchestrator"]
        mock_info_agent.return_value.agent = agents["info"]
        mock_safety_agent.return_value.agent = agents["safety"]
        mock_experience_agent.return_value.agent = agents["experience"]
        mock_logistic_agent.return_value.agent = agents["logistic"]
        mock_finance_agent.return_value.agent = agents["finance"]

        yield agents


@pytest.fixture
def mock_tasks():
    with (
        patch("project_hermes.crews.travel_crew.flow.ConfidenceTask") as mock_confidence_task,
        patch("project_hermes.crews.travel_crew.flow.OrchestratorTask") as mock_orchestrator_task,
        patch("project_hermes.crews.travel_crew.flow.InfoTask") as mock_info_task,
        patch("project_hermes.crews.travel_crew.flow.SafetyTask") as mock_safety_task,
        patch("project_hermes.crews.travel_crew.flow.ExperienceTask") as mock_experience_task,
        patch("project_hermes.crews.travel_crew.flow.LogisticTask") as mock_logistic_task,
        patch("project_hermes.crews.travel_crew.flow.FinanceTask") as mock_finance_task,
    ):
        # Set up mock task instances
        tasks = {
            "confidence": MagicMock(),
            "orchestrator_breakdown": MagicMock(),
            "orchestrator_synthesis": MagicMock(),
            "info": MagicMock(),
            "safety": MagicMock(),
            "experience": MagicMock(),
            "logistic": MagicMock(),
            "finance": MagicMock(),
        }

        # Set up return values for create_*_task methods
        mock_confidence_task.return_value.create_confidence_task.return_value = tasks["confidence"]

        mock_orchestrator_task.return_value.create_breakdown_task.return_value = tasks[
            "orchestrator_breakdown"
        ]
        mock_orchestrator_task.return_value.create_synthesis_task.return_value = tasks[
            "orchestrator_synthesis"
        ]
        mock_info_task.return_value.create_info_task.return_value = tasks["info"]
        mock_safety_task.return_value.create_safety_task.return_value = tasks["safety"]
        mock_experience_task.return_value.create_experience_task.return_value = tasks["experience"]
        mock_logistic_task.return_value.create_logistic_task.return_value = tasks["logistic"]
        mock_finance_task.return_value.create_finance_task.return_value = tasks["finance"]

        yield tasks


class TestTravelFlow:
    def test_analyze_confidence(self, mock_agents, mock_tasks):
        # Set up mock confidence task result
        mock_tasks["confidence"].execute.return_value = json.dumps({"score": 0.8})

        # Create the flow and run analyze_confidence
        flow = TravelFlow()
        flow.state = TravelState(query="Plan a trip to Tokyo")
        flow.analyze_confidence()

        # Verify the confidence score was set correctly
        assert flow.state.confidence_score == 0.8

    def test_analyze_confidence_error(self, mock_agents, mock_tasks):
        # Set up mock confidence task result with invalid JSON
        mock_tasks["confidence"].execute.return_value = "not valid json"

        # Create the flow and run analyze_confidence
        flow = TravelFlow()
        flow.state = TravelState(query="Plan a trip to Tokyo")
        flow.analyze_confidence()

        # Verify the error was caught and handled
        assert flow.state.confidence_score == 0
        assert flow.state.success is False
        assert "Failed to parse confidence score" in flow.state.error

    def test_breakdown_query(self, mock_agents, mock_tasks):
        # Set up mock breakdown task result
        mock_breakdown = {
            "locations": {"destination": "Tokyo"},
            "budget": 5000,
            "preferences": {"dining": "local cuisine"},
        }
        mock_tasks["orchestrator_breakdown"].execute.return_value = json.dumps(mock_breakdown)

        # Create the flow and run breakdown_query
        flow = TravelFlow()
        flow.state = TravelState(query="Plan a trip to Tokyo", confidence_score=0.8)
        flow.breakdown_query()

        # Verify the query breakdown was set correctly
        assert flow.state.query_breakdown == mock_breakdown
        assert flow.state.budget == 5000
        assert flow.state.preferences == {"dining": "local cuisine"}

    def test_breakdown_query_skipped(self, mock_agents, mock_tasks):
        # Create the flow and run breakdown_query with low confidence
        flow = TravelFlow()
        flow.state = TravelState(query="Plan a trip to Tokyo", confidence_score=0.5)
        flow.breakdown_query()

        # Verify the function was skipped
        assert flow.state.query_breakdown is None
        assert mock_tasks["orchestrator_breakdown"].execute.call_count == 0
