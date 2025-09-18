# Project Hermes: Multi-Agent AI Tour Guide Backend

This backend is a FastAPI server powered by CrewAI, orchestrating a multi-agent system to generate comprehensive travel plans from user prompts. The architecture uses a centralized, versioned prompt library and Crew Flow for robust orchestration.

## 1. Prerequisites

- Python >= 3.10 < 3.14
- [uv](https://docs.astral.sh/uv/) for dependency management
- At least one of the following API keys in `.env` (order of preference):
  - Google Gemini API key (primary)
  - Anthropic Claude API key (secondary)
  - OpenAI API key (tertiary)

## 2. Installation

Preferred (Makefile):

```bash
cd backend
make venv      # create .venv
make install   # install project + dev extras
```

Optionally activate:

```bash
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

## 3. Environment Variables

Create `backend/.env` and set at least one of these API keys (see `.env.example`):

```bash
# Google Gemini API Key (primary)
GEMINI_API_KEY=your_gemini_api_key_here

# Anthropic Claude API Key (secondary)
CLAUDE_API_KEY=your_claude_api_key_here

# OpenAI API Key (tertiary)
OPENAI_API_KEY=your_openai_api_key_here
```

## 4. Multi-Provider Support

Project Hermes supports multiple LLM providers:

1. Provider Auto-Detection: The system will automatically use the first available API key in this order:

- Gemini (if `GEMINI_API_KEY` or `GOOGLE_API_KEY` is set)
- Claude (if `CLAUDE_API_KEY` or `ANTHROPIC_API_KEY` is set)
- OpenAI (if `OPENAI_API_KEY` is set)

2. Explicit Provider Selection: You can specify which provider to use:

```python
# In Python code
travel_crew = TravelCrew(llm_provider="gemini")
```

```json
// In API requests
{
  "query": "Plan a weekend trip to Paris",
  "llm_provider": "claude"
}
```

3. Provider Options and Models:

- "gemini": Uses Google's Gemini with exact model `gemini/gemini-2.0-flash`
- "claude": Uses Anthropic Claude (e.g., `anthropic/claude-3-sonnet-20240229`)
- "openai": Uses OpenAI GPT-4 family (e.g., `openai/gpt-4-turbo`)
- null/omitted: Auto-detects based on available API keys (Gemini → Claude → OpenAI)

## 5. Demos (deprecated)

Legacy demo scripts were removed to prevent drift. Use the FastAPI endpoint or the Streamlit frontend instead.

## 6. API Endpoints

### `/travel/plan` (POST)

Generate a comprehensive travel plan from a natural language query.

**Request Body:**

```json
{
  "query": "Plan a weekend trip to Paris for a couple with a budget of $2000",
  "llm_provider": "gemini" // Optional: "openai", "gemini", "claude", or null for auto-detect
}
```

**Response (example):**

```json
{
  "success": true,
  "confidence_score": 0.95,
  "llm_provider": "gemini",
  "travel_plan": {
    "overview": "Paris, the City of Light, offers a perfect romantic weekend...",
    "itinerary": "Day 1: Arrive at Charles de Gaulle Airport...",
    "safety": "Paris is generally safe for tourists, but be aware of pickpockets...",
    "finance": "Estimated Budget Breakdown: Flights: $800, Accommodation: $400..."
  }
}
```

### Orchestration

- Flow starts with a confidence check to ensure the query is travel-related.
- If confidence >= 0.6, the system runs destination research, itinerary planning, safety guidance, and budget analysis (sequentially), then returns a structured plan.
- If confidence < 0.6, the API returns an error explaining the query isn’t travel-related.

## 7. API Usage

### Run the Server

```bash
make dev  # uvicorn reload on 127.0.0.1:8001
```

### Plan a Trip

```bash
# Basic query
curl -X POST "http://127.0.0.1:8001/travel/plan" \
	-H "Content-Type: application/json" \
	-d '{"query":"Plan a weekend trip to Paris"}'

# With specific provider
curl -X POST "http://127.0.0.1:8001/travel/plan" \
	-H "Content-Type: application/json" \
	-d '{"query":"Plan a weekend trip to Paris", "llm_provider":"gemini"}'
```

### Response Structure

```json
{
	"success": true,
	"query": "Plan a weekend trip to Paris",
	"travel_plan": { ... },
	"confidence_score": 0.92,
  "llm_provider": "gemini"
}
```

If the prompt is not travel-related:

```json
{
  "success": false,
  "error": "The query does not appear to be travel-related.",
  "confidence_score": 0.2,
  "query": "What is the capital of France?"
}
```

## 8. Project Structure

```
backend/
  Makefile
  pyproject.toml
  src/project_hermes/
    api.py                       # FastAPI endpoints
    settings.py                  # App settings and CORS
    crews/travel_crew_multi_provider.py  # Multi-provider crew
  tests/                         # Pytest suite (unit + optional integration)
```

## 9. Testing

```bash
make test             # unit tests only (RUN_INTEGRATION=0)
make test-integration # include integration (RUN_INTEGRATION=1)
make coverage         # coverage report
```

Notes:

- Integration tests require real API keys.
- By default integration tests are skipped.

## 10. Extending

- Add new agents/tasks by updating `prompt_library.json` and agent/task classes.
- Prompts are versioned for easy updates and rollback.

## 11. Backward Compatibility

- The legacy poem endpoint has been removed from the API.

## 12. CORS

- CORS is enabled and configurable via the `CORS_ALLOW_ORIGINS` environment variable (comma-separated). Defaults to `http://localhost:3000,http://127.0.0.1:3000`.

## 13. Dependency Management

Primary workflow uses the Makefile (pip + venv). Optional uv workflow:

```bash
pip install uv
uv venv
source .venv/bin/activate
uv pip install -e .
```

### Makefile Cheat Sheet

```bash
make venv            # create virtual env
make install         # install deps
make dev             # run dev server
make lint            # ruff checks
make format          # auto-format
make type            # mypy type checks
make test            # unit tests
make test-integration# full suite
make coverage        # coverage report
make clean           # remove caches
make clean-all       # remove caches + venv
make upgrade         # upgrade outdated packages
make freeze          # freeze current versions
```

## 14. Support

- CrewAI docs: https://docs.crewai.com
- FastAPI docs: https://fastapi.tiangolo.com
- uv docs: https://docs.astral.sh/uv/
