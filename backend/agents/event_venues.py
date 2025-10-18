import logging
from typing import Dict, List, Any
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.tavily_search import search_event_venues

async def search_venues(location: str, event_type: str, capacity: int, budget: float = None, max_results: int = 5) -> List[Dict[str, Any]]:
    """
    Search for event venues using Tavily API with real-time data
    """
    try:
        logging.info(f"Searching venues in {location} for {event_type} with capacity {capacity}")
        
        # Use Tavily for comprehensive venue search
        venues = await search_event_venues(location, event_type, capacity, budget, max_results)
        
        # Enhance venue data with additional processing
        enhanced_venues = []
        for venue in venues:
            enhanced_venue = {
                "name": venue.get("name", ""),
                "location": venue.get("location", location),
                "capacity": venue.get("capacity", capacity),
                "price_per_day": venue.get("price_per_day"),
                "amenities": venue.get("amenities", []),
                "rating": venue.get("rating"),
                "description": venue.get("description", ""),
                "website": venue.get("url", ""),
                "contact": venue.get("contact", "Contact venue directly"),
                "suitable_for": [event_type],
                "booking_contact": "Contact venue directly"
            }
            enhanced_venues.append(enhanced_venue)
        
        logging.info(f"Found {len(enhanced_venues)} venues for {event_type}")
        return enhanced_venues
        
    except Exception as e:
        logging.error(f"Venue search failed: {e}")
        raise RuntimeError(f"Unable to search venues: {e}")