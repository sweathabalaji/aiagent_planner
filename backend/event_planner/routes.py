from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
import logging
import json
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.schemas import EventRequest, EventResponse
from agents.event_planner import create_event_plan_agent

router = APIRouter(prefix="/api/event", tags=["event-planner"])
logger = logging.getLogger(__name__)

@router.post("/plan", response_model=EventResponse)
async def create_event_plan(request: EventRequest):
    """
    Create a comprehensive event plan using AI agents with real-time vendor search
    """
    try:
        logging.info(f"Creating event plan for: {request.event_name} ({request.event_type})")
        
        # Convert request to dictionary for agent processing
        event_data = request.dict()
        
        # Create event plan using the event planning agent
        result = await create_event_plan_agent(event_data)
        
        # Handle case where result might be a string or have errors
        if isinstance(result, str):
            logging.error(f"Agent returned string instead of dict: {result}")
            raise HTTPException(status_code=500, detail="Agent processing error")
        
        if not isinstance(result, dict):
            logging.error(f"Agent returned invalid type: {type(result)}")
            raise HTTPException(status_code=500, detail="Invalid agent response format")
        
        if "error" in result:
            logging.error(f"Agent returned error: {result.get('error')}")
            raise HTTPException(status_code=500, detail=result.get("error", "Agent processing failed"))
        
        # Transform agent response to match EventResponse schema
        transformed_variants = []
        for variant_data in result.get("variants", []):
            # Transform venues to match EventVenue schema
            transformed_venues = []
            for venue in variant_data.get("venues", []):
                if isinstance(venue, dict):
                    transformed_venues.append({
                        "name": venue.get("name", ""),
                        "location": venue.get("location", ""),
                        "capacity": venue.get("capacity", 0),
                        "price_per_day": venue.get("price_per_day"),
                        "amenities": venue.get("amenities", []),
                        "rating": venue.get("rating", 4.0),
                        "description": venue.get("description", "")
                    })
                elif isinstance(venue, str):
                    # Handle string venue data
                    transformed_venues.append({
                        "name": venue[:50] if venue else "Venue",
                        "location": venue[:100] if venue else "",
                        "capacity": 0,
                        "price_per_day": None,
                        "amenities": [],
                        "rating": 4.0,
                        "description": venue[:200] if venue else ""
                    })
            
            # Transform vendors to match EventVendor schema
            transformed_vendors = []
            vendors_data = variant_data.get("vendors", {})
            
            # Handle nested vendor structure (catering, photography, decoration)
            if isinstance(vendors_data, dict):
                for vendor_type, vendor_list in vendors_data.items():
                    if isinstance(vendor_list, list):
                        for vendor in vendor_list:
                            if isinstance(vendor, dict):
                                transformed_vendors.append({
                                    "name": vendor.get("name", ""),
                                    "service_type": vendor.get("service", vendor_type),
                                    "location": vendor.get("location", ""),
                                    "price_range": vendor.get("price", "Contact for pricing"),
                                    "rating": vendor.get("rating", 4.0),
                                    "specialties": vendor.get("specialties", [vendor_type]),
                                    "description": vendor.get("description", "")
                                })
            elif isinstance(vendors_data, list):
                # Handle flat vendor list (fallback)
                for vendor in vendors_data:
                    if isinstance(vendor, dict):
                        transformed_vendors.append({
                            "name": vendor.get("name", ""),
                            "service_type": vendor.get("service_type", ""),
                            "location": vendor.get("location", ""),
                            "price_range": vendor.get("price_range", "Contact for pricing"),
                            "rating": vendor.get("rating", 4.0),
                            "specialties": vendor.get("specialties", []),
                            "description": vendor.get("description", "")
                        })
            
            # Transform timeline to match EventTimelineItem schema
            transformed_timeline = []
            timeline_data = variant_data.get("planning_timeline", [])
            for timeline_item in timeline_data:
                if isinstance(timeline_item, dict):
                    transformed_timeline.append({
                        "time": timeline_item.get("time", ""),
                        "activity": timeline_item.get("activity", ""),
                        "duration": timeline_item.get("duration", ""),
                        "responsible_party": timeline_item.get("responsible_party", ""),
                        "notes": timeline_item.get("notes")
                    })
                elif isinstance(timeline_item, str):
                    # Handle string timeline items
                    transformed_timeline.append({
                        "time": "",
                        "activity": timeline_item,
                        "duration": "",
                        "responsible_party": "",
                        "notes": None
                    })
            
            # Create transformed variant
            transformed_variant = {
                "variant": variant_data.get("variant", ""),
                "venues": transformed_venues,
                "vendors": transformed_vendors,
                "timeline": transformed_timeline,
                "estimated_cost": variant_data.get("estimated_cost", 0.0),
                "cost_breakdown": variant_data.get("cost_breakdown", {})
            }
            transformed_variants.append(transformed_variant)
        
        # Debug: Log what we're getting from agent before transforming to response
        logging.info(f"🔬 ROUTE DEBUG - Agent result keys: {list(result.keys()) if isinstance(result, dict) else 'not dict'}")
        if isinstance(result, dict):
            agent_analysis = result.get("agent_analysis", {})
            logging.info(f"🔬 ROUTE DEBUG - agent_analysis keys: {list(agent_analysis.keys()) if isinstance(agent_analysis, dict) else 'not dict'}")
            if isinstance(agent_analysis, dict) and "full_analysis" in agent_analysis:
                analysis_length = len(agent_analysis.get("full_analysis", ""))
                logging.info(f"🔬 ROUTE DEBUG - full_analysis length: {analysis_length}")
                if analysis_length > 0:
                    logging.info(f"🔬 ROUTE DEBUG - full_analysis preview: {agent_analysis['full_analysis'][:100]}...")

        # Build response according to EventResponse schema
        response = EventResponse(
            event_name=request.event_name,
            event_type=request.event_type,
            variants=transformed_variants,
            planning_timeline=result.get("planning_timeline", []),
            recommendations=result.get("recommendations", []),
            ai_suggestions=result.get("ai_suggestions", []),
            saved_event_id=None,
            status=result.get("status", "success"),
            # Include agent analysis fields
            agent_analysis=result.get("agent_analysis", {"full_analysis": ""}),
            planning_insights=result.get("planning_insights", []),
            contextual_recommendations=result.get("contextual_recommendations", []),
            metadata=result.get("metadata", {})
        )
        
        # Debug: Log what's in the response
        logging.info(f"🔬 ROUTE DEBUG - Response agent_analysis: {response.agent_analysis}")
        logging.info(f"🔬 ROUTE DEBUG - Response planning_insights length: {len(response.planning_insights or [])}")
        logging.info(f"🔬 ROUTE DEBUG - Response contextual_recommendations length: {len(response.contextual_recommendations or [])}")
        
        logging.info(f"Successfully created event plan for: {request.event_name}")
        return response
        
    except Exception as e:
        logging.error(f"Error creating event plan: {str(e)}")
        # Return a basic error response that matches the schema
        error_response = EventResponse(
            event_name=request.event_name,
            event_type=request.event_type,
            variants=[],
            planning_timeline=[],
            recommendations=[f"Error occurred while planning: {str(e)}"],
            ai_suggestions=["Please try again with different parameters"],
            status="error"
        )
        return error_response

@router.get("/templates")
async def get_event_templates():
    """
    Get pre-built event templates for common event types
    """
    templates = {
        "wedding": {
            "typical_duration": "1 day",
            "common_preferences": ["traditional", "outdoor", "vegetarian", "photography", "live music"],
            "typical_guest_count": 150,
            "budget_ranges": {
                "budget": "₹1,00,000 - ₹3,00,000",
                "standard": "₹3,00,000 - ₹8,00,000", 
                "premium": "₹8,00,000 - ₹20,00,000+"
            },
            "essential_vendors": ["venue", "catering", "photography", "decoration", "entertainment"],
            "planning_duration": "8-12 weeks"
        },
        "corporate": {
            "typical_duration": "4-8 hours",
            "common_preferences": ["professional", "indoor", "mixed menu", "presentations", "networking"],
            "typical_guest_count": 100,
            "budget_ranges": {
                "budget": "₹50,000 - ₹1,50,000",
                "standard": "₹1,50,000 - ₹4,00,000",
                "premium": "₹4,00,000 - ₹10,00,000+"
            },
            "essential_vendors": ["venue", "catering", "av_equipment", "photography"],
            "planning_duration": "4-6 weeks"
        },
        "birthday": {
            "typical_duration": "4-6 hours",
            "common_preferences": ["theme", "indoor/outdoor", "entertainment", "cake", "decorations"],
            "typical_guest_count": 50,
            "budget_ranges": {
                "budget": "₹25,000 - ₹75,000",
                "standard": "₹75,000 - ₹2,00,000",
                "premium": "₹2,00,000 - ₹5,00,000+"
            },
            "essential_vendors": ["venue", "catering", "decoration", "entertainment"],
            "planning_duration": "2-4 weeks"
        },
        "conference": {
            "typical_duration": "1-2 days",
            "common_preferences": ["professional", "technology", "networking", "workshops", "exhibitions"],
            "typical_guest_count": 200,
            "budget_ranges": {
                "budget": "₹1,00,000 - ₹3,00,000",
                "standard": "₹3,00,000 - ₹8,00,000",
                "premium": "₹8,00,000 - ₹20,00,000+"
            },
            "essential_vendors": ["venue", "catering", "av_equipment", "registration", "photography"],
            "planning_duration": "8-12 weeks"
        },
        "anniversary": {
            "typical_duration": "3-5 hours",
            "common_preferences": ["elegant", "romantic", "intimate", "dinner", "live music"],
            "typical_guest_count": 75,
            "budget_ranges": {
                "budget": "₹40,000 - ₹1,00,000",
                "standard": "₹1,00,000 - ₹3,00,000",
                "premium": "₹3,00,000 - ₹8,00,000+"
            },
            "essential_vendors": ["venue", "catering", "decoration", "photography", "entertainment"],
            "planning_duration": "3-6 weeks"
        }
    }
    
    return {
        "templates": templates,
        "status": "success",
        "message": "Event templates retrieved successfully"
    }

@router.get("/venues/{location}")
async def get_venues_by_location(location: str, event_type: str = "general", capacity: int = 50):
    """
    Get available venues for a specific location
    """
    try:
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from agents.event_venues import search_venues
        
        venues = await search_venues(location, event_type, capacity, max_results=10)
        
        return {
            "venues": venues,
            "location": location,
            "event_type": event_type,
            "capacity": capacity,
            "status": "success"
        }
        
    except Exception as e:
        logging.error(f"Venue search failed: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to search venues: {str(e)}")

@router.get("/vendors/{location}")
async def get_vendors_by_location(location: str, service_types: str = "photography,catering,decoration"):
    """
    Get available vendors for a specific location and service types
    """
    try:
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from agents.event_vendors import search_vendors
        
        service_list = service_types.split(",")
        vendors = await search_vendors(location, service_list, "general", max_results=15)
        
        return {
            "vendors": vendors,
            "location": location,
            "service_types": service_list,
            "status": "success"
        }
        
    except Exception as e:
        logging.error(f"Vendor search failed: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to search vendors: {str(e)}")

@router.post("/save")
async def save_event_plan(plan_data: Dict[str, Any]):
    """
    Save event plan to database (placeholder for future implementation)
    """
    try:
        # TODO: Implement database saving
        plan_id = f"event_{plan_data.get('event_name', 'unknown').replace(' ', '_')}_{hash(str(plan_data)) % 10000}"
        
        return {
            "saved_plan_id": plan_id,
            "status": "success",
            "message": "Event plan saved successfully"
        }
        
    except Exception as e:
        logging.error(f"Save failed: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to save event plan: {str(e)}")

@router.get("/health")
async def event_planner_health():
    """
    Health check endpoint for event planner
    """
    return {
        "service": "Event Planner Agent",
        "status": "healthy",
        "features": ["venue_search", "vendor_search", "ai_planning", "timeline_generation"],
        "version": "1.0.0"
    }