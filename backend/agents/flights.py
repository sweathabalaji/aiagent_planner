import os
import logging
from utils.tavily_search import search_flights as tavily_search_flights

async def search_flights(origin: str, destination: str, departureDate: str, returnDate: str = None, adults: int = 1, currency: str = "INR", max_offers: int = 5):
    """
    Search for flights using only Tavily web search - no dummy data
    """
    try:
        logging.info(f"Searching flights from {origin} to {destination} on {departureDate}")
        
        # Use Tavily for comprehensive flight search
        flights = await tavily_search_flights(origin, destination, departureDate, returnDate)
        
        # Limit results to max_offers
        return flights[:max_offers]
        
    except Exception as e:
        logging.error(f"Flight search failed: {e}")
        raise RuntimeError(f"Unable to search flights: {e}")  # Don't use dummy data
