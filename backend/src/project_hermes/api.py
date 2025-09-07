import importlib.metadata

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import importlib.metadata
from project_hermes.settings import get_settings
from project_hermes.logging import configure_logging

configure_logging()


class TravelRequest(BaseModel):
    query: str
    llm_provider: str | None = None  # Added provider selection


class TravelResponse(BaseModel):
    success: bool
    query: str
    travel_plan: dict | None = None
    error: str | None = None
    confidence_score: float | None = None
    llm_provider: str | None = None  # Added to show which provider was used


def create_app() -> FastAPI:
    settings = get_settings()
    application = FastAPI(title=settings.app_name)

    origins = [o.strip() for o in settings.cors_origins.split(",") if o.strip()]
    application.add_middleware(
        CORSMiddleware,
        allow_origins=origins or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @application.get("/healthz")
    def healthcheck() -> dict:
        try:
            version = importlib.metadata.version("project_hermes")
        except importlib.metadata.PackageNotFoundError:
            version = "0.0.0"
        return {"status": "ok", "version": version, "env": settings.environment}

    @application.post("/travel/plan", response_model=TravelResponse)
    async def plan_travel(request: TravelRequest) -> TravelResponse:
        from project_hermes.crews.travel_crew.travel_crew import TravelCrew

        travel_crew = TravelCrew(verbose=True, llm_provider=request.llm_provider)
        result = travel_crew.plan_trip(request.query)

        # Add the provider info to the response
        if hasattr(travel_crew.llm, "__class__"):
            llm_type = travel_crew.llm.__class__.__name__
            result["llm_provider"] = llm_type

        return TravelResponse(**result)

    # Keep existing poem endpoint for backward compatibility
    from project_hermes.main import run_flow

    @application.get("/poem/{prompt}")
    def generate_poem(prompt: str):
        state = run_flow(prompt)
        return {
            "poem": state.poem,
            "topic": state.topic,
            "model": state.model_used,
            "attempts": state.attempts,
            "success": state.success,
            "error": state.error_message,
        }

    return application


app = create_app()
