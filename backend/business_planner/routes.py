"""Business Planner Routes"""
from fastapi import HTTPException
from pydantic import BaseModel, Field
from typing import Literal
from . import router
from agents.business_planner import create_business_plan


class BusinessRequest(BaseModel):
    """Business plan request model"""
    business_idea: str = Field(..., description="Core business concept and what problem it solves")
    industry: str = Field(..., description="Industry sector (e.g., 'Technology', 'Healthcare', 'E-commerce')")
    target_market: str = Field(..., description="Target customer segment (e.g., 'Small businesses', 'Millennials')")
    business_model: str = Field(..., description="Revenue model (e.g., 'B2B SaaS', 'B2C Marketplace', 'Subscription')")
    funding_needed: str = Field(..., description="Estimated funding requirement (e.g., '$500K', 'Bootstrapped')")
    location: str = Field(..., description="Business location or target region")


class BusinessResponse(BaseModel):
    """Business plan response model"""
    success: bool
    business_plan: dict


@router.post("/plan", response_model=BusinessResponse)
async def plan_business(request: BusinessRequest):
    """
    Generate a comprehensive business startup plan.
    
    Creates a detailed business plan including:
    - Business Model Canvas (9 building blocks)
    - Funding Strategy (stages, sources, pitch deck)
    - Market Analysis (TAM/SAM/SOM, trends, insights)
    - Competitive Analysis (SWOT, positioning)
    - Financial Projections (3-year forecast)
    - Go-to-Market Strategy (launch, channels, growth)
    - Actionable Next Steps
    """
    try:
        # Generate business plan using AI agent
        business_plan = await create_business_plan(
            business_idea=request.business_idea,
            industry=request.industry,
            target_market=request.target_market,
            business_model=request.business_model,
            funding_needed=request.funding_needed,
            location=request.location
        )
        
        return BusinessResponse(
            success=True,
            business_plan=business_plan
        )
        
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(ve)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate business plan: {str(e)}")


@router.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "service": "business_planner"}
