import os
from dotenv import load_dotenv

# Load .env file from parent directory BEFORE any other imports
# Use absolute path to be sure
env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path=env_path)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from utils.schemas import TravelRequest, TravelResponse
from agents.planner import create_plan_agent
from tech_planner.routes import router as tech_router
from event_planner.routes import router as event_router
from learning_planner.routes import router as learning_router
from business_planner.routes import router as business_router

app = FastAPI(title="PlanAI Multi-Agent Planner (FastAPI + LangChain + Groq)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all planner routes
app.include_router(tech_router)
app.include_router(event_router)
app.include_router(learning_router)
app.include_router(business_router)

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "PlanAI Multi-Agent Planner API",
        "version": "1.0.0",
        "endpoints": {
            "plan_trip": "/api/plan_trip (POST)",
            "tech_planner": "/api/tech/plan (POST)",
            "tech_templates": "/api/tech/templates (GET)",
            "event_planner": "/api/event/plan (POST)",
            "event_templates": "/api/event/templates (GET)",
            "event_venues": "/api/event/venues/{location} (GET)",
            "event_vendors": "/api/event/vendors/{location} (GET)",
            "learning_planner": "/api/learning/plan (POST)",
            "learning_health": "/api/learning/health (GET)",
            "business_planner": "/api/business/plan (POST)",
            "business_health": "/api/business/health (GET)",
            "docs": "/docs",
            "openapi": "/openapi.json"
        },
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": "2025-08-22"}

@app.post("/api/plan_trip", response_model=TravelResponse)
async def plan_trip(req: TravelRequest):
    """
    Accepts a TravelRequest and returns multiple plan variants.
    The planner agent is fully agentic: it asks the model to decompose the request,
    then calls domain agents to fetch live data and returns combined variants.
    """
    result = await create_plan_agent(req.dict())
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)), reload=True)
