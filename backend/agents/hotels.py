import os
import logging
from utils.tavily_search import search_hotels as tavily_search_hotels

async def search_hotels(city_code: str, check_in: str, check_out: str, currency: str = "INR", max_results: int = 5):
    """
    Search for hotels using only Tavily web search - no dummy data
    """
    try:
        logging.info(f"Searching hotels in {city_code} from {check_in} to {check_out}")
        
        # Use Tavily for comprehensive hotel search
        hotels = await tavily_search_hotels(city_code, check_in, check_out)
        
        # Limit results to max_results
        return hotels[:max_results]
        
    except Exception as e:
        logging.error(f"Hotel search failed: {e}")
        raise RuntimeError(f"Unable to search hotels: {e}")  # Don't use dummy data
