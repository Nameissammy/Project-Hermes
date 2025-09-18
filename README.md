# Project Hermes: Multi-Agent Travel Planning System

Project Hermes is a sophisticated travel planning system that uses a crew of specialized AI agents to generate comprehensive travel plans. Each agent contributes their expertise to create detailed itineraries, safety information, and budget analyses.

## 🚀 Overview

The system uses CrewAI to orchestrate a team of specialized agents:

1. **Confidence Agent**: Evaluates whether queries are travel-related
2. **Orchestrator Agent**: Coordinates the overall planning process
3. **Information Agent**: Provides detailed information about travel destinations
4. **Safety Agent**: Provides safety recommendations specific to the destination
5. **Experience Agent**: Suggests activities and experiences
6. **Logistic Agent**: Plans transportation and accommodation
7. **Finance Agent**: Creates detailed budget breakdowns and cost-saving tips

## 🔌 Multi-Provider Support

Project Hermes supports multiple LLM providers and auto-detects the first available key in this order:

1. Google Gemini (primary)
2. Anthropic Claude (secondary)
3. OpenAI (tertiary)

You can also explicitly specify which provider to use when initializing the crew or via the API. For Gemini, the system uses the exact model `gemini/gemini-2.0-flash`.

## 🏗️ Project Structure

The project is organized into two main directories:

- **[backend/](./backend/)**: Contains the FastAPI server, multi-agent system, and all core functionality
- **frontend/**: Contains the Streamlit-based web interface (under development)

For detailed backend documentation, including setup instructions, architecture overview, and API reference, see the [Backend README](./backend/README.md).

## � Getting Started

This repository is organized into two main components:

1. **Backend**: Contains the CrewAI multi-agent system, API server, and core logic
2. **Frontend**: Contains a simple Streamlit web interface

### Backend Setup

```bash
# Clone the repository
git clone https://github.com/your-username/Project-Hermes.git
cd Project-Hermes/backend

# Install uv if you don't have it
pip install uv

# Create and activate a virtual environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies using pyproject.toml
uv pip install -e .

# Configure your environment
cp .env.example .env
# Edit .env to add your OpenAI API key
```

### Frontend Setup

```bash
cd ../frontend

# Create and activate a virtual environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv pip install -e .

# Configure the frontend (if needed)
cp .env.example .env
# Edit .env if your API is not at localhost:8001
```

## 🚀 Running the System

### Interactive Demo

Run the interactive demo script to test the system with different options:

```bash
cd backend  # Make sure you're in the backend directory
python demo.py
```

This will present you with three demo options:

1. Mocked Travel Crew (no API key needed) - Works without real API keys
2. Simple Crew Test (works with Gemini, Claude, or OpenAI)
3. Direct Travel Crew Test (works with Gemini, Claude, or OpenAI)

**Note:** Options 2 and 3 will try to use providers in this order:

1. Google Gemini (if GEMINI_API_KEY is available)
2. Anthropic Claude (if CLAUDE_API_KEY is available)
3. OpenAI (if OPENAI_API_KEY is available)

You can also run the demo from the project root:

```bash
python demo.py
```

### Test Scripts

Several test scripts are available to validate different aspects of the system:

```bash
# Test with mocked responses (no API key needed)
cd backend
python test_mocked_travel_crew.py

# Test a minimal implementation
python test_minimal_crew.py

# Test a simple CrewAI workflow
python test_simple_crew.py

# Direct test of the travel crew
python test_direct_travel_crew.py
```

### API Server

To run the FastAPI server:

```bash
cd backend
python run_server.py
```

Then access the API at http://localhost:8001/docs

## 🔌 API Endpoints

### POST /travel/plan

Generate a travel plan based on a natural language query.

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
    "overview": "...",
    "itinerary": "...",
    "safety": "...",
    "finance": "..."
  }
}
```

## 🧩 Project Structure

```
Project-Hermes/
├── backend/                    # Backend code and services
│   ├── src/                    # Source code
│   │   └── project_hermes/     # Main package
│   │       ├── crews/          # Multi-agent crew implementations
│   │       │   └── travel_crew/# Travel planning implementation
│   │       │       ├── agents.py   # Agent definitions
│   │       │       ├── flow.py     # Workflow implementation
│   │       │       ├── tasks.py    # Task definitions
│   │       │       └── travel_crew.py # Main crew implementation
│   │       ├── api.py          # FastAPI implementation
│   │       ├── main.py         # CLI entry points
│   │       └── settings.py     # Configuration settings
│   ├── demo.py                 # Demo script
│   ├── pyproject.toml          # Project dependencies and metadata
│   ├── run_server.py           # API server runner
│   └── test_*.py               # Various test scripts
└── frontend/                   # Simple frontend interface
    └── app.py                  # Frontend application
```

## ⚙️ Configuration

The system supports three primary configuration methods:

1. **Environment Variables**: Set in `.env` file or system environment

   - `OPENAI_API_KEY`: Your OpenAI API key (primary)
   - `GEMINI_API_KEY`: Google Gemini API key (alternative)
   - `CLAUDE_API_KEY`: Anthropic Claude API key (alternative)

2. **Explicit Provider Selection**: When initializing TravelCrew

   ```python
   # Use Gemini (primary)
   crew = TravelCrew(llm_provider="gemini")

   # Use Claude (secondary)
   crew = TravelCrew(llm_provider="claude")

   # Use OpenAI (tertiary)
   crew = TravelCrew(llm_provider="openai")
   ```

3. **Mock Mode**: For testing without API keys
   - The system will automatically use mock mode if no API keys are found
   - Returns predetermined responses for testing

## 🧪 Development and Testing

### Running Tests

```bash
cd backend
pytest
```

### Creating New Agents

1. Define a new agent class in `agents.py`
2. Create corresponding tasks in `tasks.py`
3. Update the TravelCrew class to include your new agent

## 📝 Notes for New Users

1. **API Key Setup**: The most important first step is setting up your API keys in the `.env` file
2. **CrewAI Version**: This project requires CrewAI v0.177.0 or higher due to API changes
3. **Python Path**: If you encounter import errors, ensure your Python path includes the `src` directory
4. **Mock Mode**: For quick testing without API keys, the system includes a mock mode

## 🛠️ Troubleshooting

- **Import Errors**: Ensure you're running scripts from the correct directory and the Python path includes `src`
- **API Authentication Errors**: Check your API keys in the `.env` file
- **CrewAI Errors**: Ensure you have CrewAI v0.177.0+ installed

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with [CrewAI](https://github.com/crewAI/crewAI)
- Uses OpenAI's models for agent interactions
- Powered by OpenAI's GPT-4

## 🚀 Quick Start

1. Navigate to the backend directory: `cd backend`
2. Create a virtual environment: `uv venv`
3. Activate the virtual environment: `source .venv/bin/activate` (Windows: `.venv\Scriptsctivate`)
4. Install dependencies: `uv pip install -e .`
5. Create a `.env` file with your API keys (see `.env.example`)
6. Run the demo: `python demo.py`

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.
