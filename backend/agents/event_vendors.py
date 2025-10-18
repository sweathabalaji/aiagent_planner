import logging
from typing import Dict, List, Any
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.tavily_search import search_event_vendors

async def search_vendors(location: str, service_types: List[str], event_type: str, budget: float = None, max_results: int = 5) -> List[Dict[str, Any]]:
    """
    Search for event vendors (photography, decoration, entertainment, etc.) using Tavily API
    """
    try:
        logging.info(f"Searching {service_types} vendors in {location} for {event_type}")
        
        # Use Tavily for comprehensive vendor search
        vendors = await search_event_vendors(location, service_types, event_type, budget, max_results)
        
        # Enhance vendor data with additional processing
        enhanced_vendors = []
        for vendor in vendors:
            enhanced_vendor = {
                "name": vendor.get("name", ""),
                "service_type": vendor.get("service_type", ""),
                "location": vendor.get("location", location),
                "price_range": vendor.get("price_range", "Contact for pricing"),
                "specialties": vendor.get("specialties", []),
                "rating": vendor.get("rating"),
                "description": vendor.get("description", ""),
                "website": vendor.get("url", ""),
                "contact": "Contact vendor directly",
                "availability": "Check with vendor",
                "portfolio": vendor.get("url", "")
            }
            enhanced_vendors.append(enhanced_vendor)
        
        logging.info(f"Found {len(enhanced_vendors)} vendors for {event_type}")
        return enhanced_vendors
        
    except Exception as e:
        logging.error(f"Vendor search failed: {e}")
        raise RuntimeError(f"Unable to search vendors: {e}")

async def search_photographers(location: str, event_type: str, budget: float = None, max_results: int = 3) -> List[Dict[str, Any]]:
    """
    Search specifically for event photographers
    """
    return await search_vendors(location, ["photography"], event_type, budget, max_results)

async def search_decorators(location: str, event_type: str, budget: float = None, max_results: int = 3) -> List[Dict[str, Any]]:
    """
    Search specifically for event decorators
    """
    return await search_vendors(location, ["decoration"], event_type, budget, max_results)

async def search_entertainment(location: str, event_type: str, budget: float = None, max_results: int = 3) -> List[Dict[str, Any]]:
    """
    Search for entertainment services (DJ, band, performers)
    """
    return await search_vendors(location, ["entertainment", "DJ", "band", "music"], event_type, budget, max_results)