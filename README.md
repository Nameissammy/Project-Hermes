git clone https://github.com/your-username/Project-Hermes.git

# Project Hermes

Multi-agent AI travel planning system combining FastAPI (backend), CrewAI orchestration, and a lightweight Streamlit UI.

## ✨ Key Features

- Multi-provider LLM support (auto-detect: Gemini → Claude → OpenAI)
- Strict Gemini model usage (`gemini/gemini-2.0-flash`)
- Confidence gating before executing full planning workflow
- Structured travel plan (overview, itinerary, safety, finance)
- Single FastAPI endpoint: `/travel/plan`
- Optional provider override via request body
- Streamlit frontend for quick interaction
- Makefile-driven developer workflow (lint, type, test, coverage, dev server)

## 🧠 Agent Roles

| Agent        | Purpose                                        |
| ------------ | ---------------------------------------------- |
| Confidence   | Validates travel relevance & adequacy of query |
| Orchestrator | Coordinates downstream tasks                   |
| Information  | Destination research & context                 |
| Safety       | Risk, advisories, local norms                  |
| Experience   | Activities & experiences                       |
| Logistic     | Transport & accommodation structuring          |
| Finance      | Budget estimation & breakdown                  |

## � Project Layout

```
Project-Hermes/
├── backend/                 # FastAPI + CrewAI logic
│   ├── Makefile             # Dev workflow commands
│   ├── src/project_hermes/
│   │   ├── api.py           # FastAPI routes
│   │   ├── settings.py      # App & CORS settings
│   │   └── crews/
│   │       └── travel_crew_multi_provider.py  # Multi-provider crew orchestration
│   └── tests/               # Pytest suite (unit + optional integration)
└── frontend/
    └── app.py               # Streamlit UI
```

Legacy demo scripts and ad-hoc test files have been removed to reduce drift.

## 🚀 Quick Start (Backend)

```bash
git clone https://github.com/your-username/Project-Hermes.git
cd Project-Hermes/backend
make venv
make install
cp .env.example .env  # add at least one API key
make dev              # starts FastAPI on http://127.0.0.1:8001
```

## 🌐 Run the Frontend

In a second terminal:

```bash
cd frontend
uv venv && source .venv/bin/activate
uv pip install -e .
cp .env.example .env  # adjust API_HOST if backend not on default
uv run streamlit run app.py
```

Visit http://localhost:8501 (default Streamlit port).

## 🔑 Environment Variables

Backend `.env` (any subset, order defines auto-detect priority):

```
GEMINI_API_KEY=...
CLAUDE_API_KEY=...
OPENAI_API_KEY=...
# Optional
API_HOST=http://127.0.0.1:8001
CORS_ALLOW_ORIGINS=http://localhost:8501
```

`GOOGLE_API_KEY` or `ANTHROPIC_API_KEY` are also recognized as alternates for Gemini/Claude.

## � API Usage

POST `/travel/plan`

Request:

```json
{
  "query": "Plan a 5-day family trip to Kyoto in April with a mid-range budget",
  "llm_provider": "gemini"
}
```

Response (shape):

```json
{
  "success": true,
  "confidence_score": 0.87,
  "llm_provider": "gemini",
  "travel_plan": {
    "overview": "...",
    "itinerary": [
      {
        "day": "Day 1",
        "activities": [{ "time": "Morning", "description": "..." }]
      }
    ],
    "safety": { "general": "..." },
    "finance": { "total": 2150.0, "accommodation": 800, "summary": "..." }
  }
}
```

If confidence below threshold (e.g. not travel-related):

```json
{
  "success": false,
  "error": "The query does not appear to be travel-related.",
  "confidence_score": 0.22
}
```

## 🧪 Testing

```bash
cd backend
make test             # unit tests
make test-integration # includes live provider test (requires keys)
make coverage
```

Integration tests are skipped unless `RUN_INTEGRATION=1`.

## 🛠 Development Workflow

```bash
make lint     # ruff
make format   # ruff format
make type     # mypy
make dev      # run backend (uvicorn reload)
```

Optional dependency management (uv is already supported):

```bash
pip install uv
uv pip install -e .
```

## 🔄 Provider Selection Logic

Priority: Gemini → Claude → OpenAI. Explicit `llm_provider` in the request overrides auto-detect. Gemini model is locked to `gemini/gemini-2.0-flash` for consistency.

## � Extending

- Add new dimensions (e.g., sustainability, accessibility) by introducing new task logic in the crew orchestration file.
- Guardrail improvements: adjust confidence threshold or add query normalization upstream.

## 🛠 Troubleshooting

| Issue                         | Check                                           |
| ----------------------------- | ----------------------------------------------- |
| 403 / auth errors             | API keys present & valid in `.env`              |
| CORS failure in browser       | `CORS_ALLOW_ORIGINS` includes frontend origin   |
| Empty itinerary               | Query may lack duration / destination specifics |
| Low confidence false negative | Rephrase query with explicit travel intent      |

## 📄 License

MIT – see `LICENSE`.

## 🙏 Acknowledgments

- CrewAI
- FastAPI
- Streamlit

---

For deeper backend details, see `backend/README.md`.
