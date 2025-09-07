"""
Project Hermes - FastAPI Server
------------------------------

This module implements a FastAPI server that exposes the travel planning
functionality as a REST API.
"""

import os

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from travel_crew_multi_provider import TravelCrew

# Initialize the FastAPI app
app = FastAPI(
    title="Project Hermes Travel API",
    description="A multi-agent AI system for comprehensive travel planning",
    version="1.0.0",
)

# Enable CORS for frontend access (configurable via env)
allowed_origins = os.getenv(
    "CORS_ALLOW_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000"
).split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in allowed_origins if o.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Define request and response models
class TravelRequest(BaseModel):
    query: str
    llm_provider: str | None = None


class TravelPlan(BaseModel):
    overview: str
    itinerary: str
    safety: str
    finance: str


class TravelResponse(BaseModel):
    success: bool
    confidence_score: float
    llm_provider: str | None = None
    error: str | None = None
    travel_plan: TravelPlan | None = None


# Define API endpoints
@app.get("/")
async def root():
    return {
        "message": "Welcome to Project Hermes Travel API",
        "version": "1.0.0",
        "endpoints": {"/travel/plan": "POST - Generate a travel plan"},
    }


@app.post("/travel/plan", response_model=TravelResponse)
async def create_travel_plan(request: TravelRequest):
    try:
        # Initialize travel crew with the requested provider if specified
        travel_crew = TravelCrew(llm_provider=request.llm_provider)

        # Call the travel crew to generate a plan
        result = travel_crew.plan_trip(request.query)

        # Return the result which already has the provider information
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error processing travel plan: {str(e)}"
        ) from e


# Run the server if executed directly
if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8001, reload=True)
