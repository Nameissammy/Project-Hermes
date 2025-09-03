# Project Hermes Backend (API Server)

FastAPI + crewAI flow exposing a poem generation endpoint using a Gemini model (via crewAI's LLM layer). This guide makes the project reproducible on any machine without manual `sys.path` hacks.

## 1. Prerequisites

- Python >= 3.10 < 3.14
- [uv](https://docs.astral.sh/uv/) installed (fast dependency manager):
  ```bash
  pip install uv
  ```
- A valid Gemini (Google Generative Language) API key in `.env`.

## 2. Clone & Install

From repo root:

```bash
cd backend
uv sync  # install dependencies from pyproject + uv.lock if present
uv pip install -e .  # install package in editable mode so 'project_hermes' is importable
```

This avoids needing `sys.path.insert` everywhere.

## 3. Environment Variables

Create `backend/.env` (never commit secrets):

```env
GEMINI_API_KEY=your_key_here
# Or fallback name used elsewhere:
GOOGLE_API_KEY=your_key_here
```

CrewAI/LLM layer will pick up either.

Optional for deterministic tests:

```env
POEM_SENTENCE_COUNT=3
POEM_TOPIC=ai testing
```

## 4. Run the Flow Manually

Because the package is installed editable, you can now run:

```bash
uv run -m project_hermes.main "quantum security"
```

This generates a poem and writes `poem.txt`.

## 5. Run the API Server

Two supported methods:

Method A (direct):

```bash
uv run uvicorn project_hermes.api:app --reload --port 8001
```

Method B (helper script):

```bash
uv run python run_server.py
```

Test endpoint:

```bash
curl http://127.0.0.1:8001/poem/ai
```

Swagger docs available at: http://127.0.0.1:8001/docs
ReDoc at: http://127.0.0.1:8001/redoc

## 6. What the Endpoint Does

`GET /poem/{prompt}` triggers the crewAI flow with `{prompt}` as the topic plus a random (or overridden) sentence count, returning JSON:

```json
{ "poem": "...", "topic": "ai" }
```

## 7. Project Structure (Backend)

```
backend/
	pyproject.toml          # package + dependencies
	run_server.py           # dev helper (adds src to path then launches uvicorn)
	src/project_hermes/
		__init__.py
		main.py               # flow + kickoff function
		api.py                # FastAPI app
		crews/poem_crew/
			poem_crew.py        # Crew & agents
			config/
				agents.yaml
				tasks.yaml
```

## 8. Removing sys.path Hacks

Earlier you ran commands like:

```
uv run python -c "import sys, os; sys.path.insert(0, 'backend/src'); import project_hermes; print('import ok')"
```

Those were temporary workarounds because Python couldn't find `backend/src` on `sys.path`. After installing editable (`uv pip install -e .` inside `backend`), you no longer need these. The package `project_hermes` is now resolvable from any working directory in the repo.

## 9. Common Issues

| Symptom                               | Cause                              | Fix                                             |
| ------------------------------------- | ---------------------------------- | ----------------------------------------------- |
| `ModuleNotFoundError: project_hermes` | Not installed editable / wrong CWD | Run install step or `cd backend` before running |
| 400 Gemini auth error                 | Missing / invalid API key          | Set valid `GEMINI_API_KEY` or `GOOGLE_API_KEY`  |
| Empty or partial poem                 | Model timeout/low tokens           | Adjust model config in crew YAML or flow        |
| Overwritten poem file                 | Same filename                      | Add timestamp logic if persistence matters      |

## 10. Suggested Improvements

- Add tests (pytest) for flow determinism with `POEM_SENTENCE_COUNT`.
- Add health endpoint (`/healthz`).
- Add structured logging (e.g. `structlog`).
- Parameterize model + temperature in env or YAML.

## 11. Quick Start (Copy/Paste)

```bash
git clone https://github.com/Nameissammy/Project-Hermes.git
cd Project-Hermes/backend
cp .env.example .env   # then edit key
uv sync
uv pip install -e .
uv run uvicorn project_hermes.api:app --reload --port 8001
curl http://127.0.0.1:8001/poem/ai
```

## 12. Example Response

```json
{
  "poem": "The AI ... (lines)",
  "topic": "ai"
}
```

---

Everything above ensures others can reproduce the API server behavior without manual path tweaking.

### Customizing

**Add your `OPENAI_API_KEY` into the `.env` file**

- Modify `src/project_hermes/config/agents.yaml` to define your agents
- Modify `src/project_hermes/config/tasks.yaml` to define your tasks
- Modify `src/project_hermes/crew.py` to add your own logic, tools and specific args
- Modify `src/project_hermes/main.py` to add custom inputs for your agents and tasks

## Support

- crewAI docs: https://docs.crewai.com
- FastAPI docs: https://fastapi.tiangolo.com
- uv docs: https://docs.astral.sh/uv/
