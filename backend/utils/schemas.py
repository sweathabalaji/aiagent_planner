from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class TravelRequest(BaseModel):
    user_id: Optional[str] = None
    origin: str = Field(..., example="BOM")        # IATA code or city name (prefer IATA)
    destination: str = Field(..., example="FCO")   # IATA code or city name
    start_date: str = Field(..., example="2025-09-01")
    end_date: str = Field(..., example="2025-09-05")
    budget: float = Field(..., example=1200.0)
    travellers: int = Field(1, ge=1)
    interests: Optional[List[str]] = []

class PlanVariant(BaseModel):
    variant: str
    flights: List[Dict]
    hotels: List[Dict]
    itinerary: List[Dict]
    estimated_cost: float

class TravelResponse(BaseModel):
    variants: List[PlanVariant]
    saved_plan_id: Optional[str] = None

# Event Planning Schemas
class EventRequest(BaseModel):
    user_id: Optional[str] = None
    event_name: str = Field(..., example="Sarah's Wedding")
    event_type: str = Field(..., example="wedding")  # wedding, corporate, birthday, conference, etc.
    location: str = Field(..., example="Mumbai")
    event_date: str = Field(..., example="2025-12-15")
    guest_count: int = Field(..., ge=1, example=150)
    budget: float = Field(..., example=500000.0)
    duration: str = Field(..., example="1 day")  # duration in hours/days
    preferences: List[str] = Field(default=[], example=["traditional", "outdoor", "vegetarian"])
    special_requirements: Optional[List[str]] = Field(default=[], example=["wheelchair accessible", "live music"])
    contact_info: Optional[str] = Field(None, example="sarah@email.com")

class EventVenue(BaseModel):
    name: str
    location: str
    capacity: int
    price_per_hour: Optional[float] = None
    price_per_day: Optional[float] = None
    amenities: List[str] = []
    contact: Optional[str] = None
    website: Optional[str] = None
    rating: Optional[float] = None
    description: Optional[str] = None

class EventVendor(BaseModel):
    name: str
    service_type: str  # catering, photography, decoration, entertainment, etc.
    location: str
    price_range: str
    contact: Optional[str] = None
    website: Optional[str] = None
    rating: Optional[float] = None
    specialties: List[str] = []
    description: Optional[str] = None

class EventTimelineItem(BaseModel):
    time: str
    activity: str
    duration: str
    responsible_party: str
    notes: Optional[str] = None

class EventVariant(BaseModel):
    variant: str  # budget, standard, premium
    venues: List[EventVenue]
    vendors: List[EventVendor]
    timeline: List[EventTimelineItem]
    estimated_cost: float
    cost_breakdown: Dict[str, float]

class EventResponse(BaseModel):
    event_name: str
    event_type: str
    variants: List[EventVariant]
    planning_timeline: List[Dict]  # Planning milestones before event
    recommendations: List[str]
    ai_suggestions: List[str]
    saved_event_id: Optional[str] = None
    status: str
    # Add agent analysis fields
    agent_analysis: Optional[Dict[str, Any]] = None
    planning_insights: Optional[List[str]] = []
    contextual_recommendations: Optional[List[str]] = []
    metadata: Optional[Dict[str, Any]] = None
