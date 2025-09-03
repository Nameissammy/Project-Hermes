import importlib.metadata

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from project_hermes.main import run_flow
from project_hermes.settings import get_settings


def create_app() -> FastAPI:
    settings = get_settings()
    application = FastAPI(title=settings.app_name)

    # CORS
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


# Preserve existing import path used by uvicorn: "project_hermes.api:app"
app = create_app()
