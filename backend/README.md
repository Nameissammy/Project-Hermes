# Project Hermes: Multi-Agent AI Tour Guide Backend

This backend is a FastAPI server powered by CrewAI, orchestrating a multi-agent system to generate comprehensive travel plans from user prompts. The architecture uses a centralized, versioned prompt library and Crew Flow for robust orchestration.

## 1. Prerequisites

- Python >= 3.10 < 3.14
- [uv](https://docs.astral.sh/uv/) for dependency management
- At least one of the following API keys in `.env`:
  - OpenAI API key (primary)
  - Google Gemini API key (alternative)
  - Anthropic Claude API key (alternative)

## 2. Installation

```bash
cd backend
uv venv  # creating a virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .  # install package in editable mode
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

1. **Provider Auto-Detection**: The system will automatically use the first available API key in this order:

   - Gemini (if `GEMINI_API_KEY` is set)
   - Claude (if `CLAUDE_API_KEY` is set)
   - OpenAI (if `OPENAI_API_KEY` is set)

2. **Explicit Provider Selection**: You can specify which provider to use:

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

3. **Provider Options**:
   - `"openai"`: Uses OpenAI's GPT-4 (default)
   - `"gemini"`: Uses Google's Gemini model
   - `"claude"`: Uses Anthropic's Claude model
   - `None`: Auto-detects based on available API keys

## 5. Running the Demo

The project includes an interactive demo script that lets you explore different features:

```bash
python demo.py
```

This will present you with three demo options:

1. Mocked Travel Crew (no API key needed) - Works without real API keys
2. Simple Crew Test (requires API key) - Requires OpenAI API key
3. Direct Travel Crew Test (requires API key) - Requires OpenAI API key

**Note:** Options 2 and 3 require a valid OpenAI API key in your `.env` file. If you don't have an API key, use option 1 for a mocked demonstration.

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

**Response:**

```json
{
  "success": true,
  "confidence_score": 0.95,
  "llm_provider": "ChatGoogleGenerativeAI",
  "travel_plan": {
    "overview": "Paris, the City of Light, offers a perfect romantic weekend...",
    "itinerary": "Day 1: Arrive at Charles de Gaulle Airport...",
    "safety": "Paris is generally safe for tourists, but be aware of pickpockets...",
    "finance": "Estimated Budget Breakdown: Flights: $800, Accommodation: $400..."
  }
}
```

### Centralized Prompt Library

- Prompts for all agents/tasks are versioned and loaded from `prompt_library.json` at runtime.

### Crew Flow Orchestration

- Flow starts with ConfidenceAgent
- If confidence >= 0.6, OrchestratorAgent triggers parallel specialist agents
- OrchestratorAgent synthesizes all outputs into a final travel plan
- If confidence < 0.6, flow terminates and error is returned

## 7. API Usage

### Run the Server

```bash
uvicorn project_hermes.api:app --host 0.0.0.0 --port 8001 --reload
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
	"llm_provider": "ChatOpenAI"
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
	src/project_hermes/
		api.py                # FastAPI endpoints
		main.py               # Entry points
		settings.py           # App settings
		logging.py            # Logging config
		crews/travel_crew/
			prompt_library.json # Centralized prompts
			agents.py           # Agent classes
			tasks.py            # Task classes
			flow.py             # Crew Flow definition
			travel_crew.py      # Crew wrapper
			utils.py            # Prompt loader
```

## 9. Testing

- Tests cover prompt library loading, conditional flow, and full response structure.
- Example: test irrelevant prompt returns error, valid prompt returns travel plan.

## 10. Extending

- Add new agents/tasks by updating `prompt_library.json` and agent/task classes.
- Prompts are versioned for easy updates and rollback.

## 11. Backward Compatibility

- The `/poem/{prompt}` endpoint remains for legacy use.

## 12. Dependency Management

This project uses [uv](https://docs.astral.sh/uv/) with `pyproject.toml` for dependency management instead of traditional requirements.txt files. This provides faster, more reliable package installation and dependency resolution.

### Verifying Your Setup

You can run the included `verify_setup.py` script to check your environment:

```bash
cd backend
./verify_setup.py
```

The script will:

1. Show your Python version
2. List your Python path
3. Check for required dependencies
4. Provide instructions for setting up your environment with uv

### Installing Dependencies

```bash
# Install uv if not already installed
pip install uv

# Create and activate virtual environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies from pyproject.toml
uv pip install -e .
```

## 13. Support

- CrewAI docs: https://docs.crewai.com
- FastAPI docs: https://fastapi.tiangolo.com
- uv docs: https://docs.astral.sh/uv/
