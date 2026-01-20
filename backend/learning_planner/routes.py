"""Learning Planner Routes"""
from fastapi import HTTPException
from pydantic import BaseModel, Field
from typing import Literal
from . import router
from agents.learning_planner import create_learning_path


class LearningRequest(BaseModel):
    """Learning path request model"""
    topic: str = Field(..., description="Subject to learn (e.g., 'Python Programming', 'Machine Learning')")
    skill_level: Literal["Beginner", "Intermediate", "Advanced"] = Field(..., description="Current skill level")
    duration_weeks: int = Field(..., ge=1, le=52, description="Learning duration in weeks (1-52)")
    learning_goals: str = Field(..., description="Specific learning objectives")
    time_per_week: int = Field(..., ge=1, le=168, description="Available study hours per week (1-168)")


class LearningResponse(BaseModel):
    """Learning path response model"""
    success: bool
    learning_path: dict


@router.post("/plan", response_model=LearningResponse)
async def plan_learning(request: LearningRequest):
    """
    Generate a comprehensive learning path with real resources.
    
    Creates a personalized study plan including:
    - Structured learning phases
    - Real course and book recommendations
    - Week-by-week study schedule
    - Progress tracking system
    - Assessment milestones
    """
    try:
        # Generate learning path using AI agent
        learning_path = await create_learning_path(
            topic=request.topic,
            skill_level=request.skill_level,
            duration_weeks=request.duration_weeks,
            learning_goals=request.learning_goals,
            time_per_week=request.time_per_week
        )
        
        return LearningResponse(
            success=True,
            learning_path=learning_path
        )
        
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(ve)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate learning path: {str(e)}")


@router.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "service": "learning_planner"}
