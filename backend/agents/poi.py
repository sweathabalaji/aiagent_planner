import os
import logging
from utils.tavily_search import search_attractions

async def get_pois_near(city: str, kinds: list = None, radius: int = 5000, limit: int = 20, interests: list = None):
    """
    Get points of interest near a city using Tavily search with interest-based filtering
    """
    try:
        logging.info(f"Searching attractions in {city} with interests: {interests}")
        
        # Enhanced search based on user interests
        attractions = await search_attractions_with_interests(city, interests)
        
        # Filter by kinds if specified  
        if kinds:
            filtered_attractions = []
            for attraction in attractions:
                attraction_kinds = attraction.get("kinds", "").lower()
                if any(kind.lower() in attraction_kinds for kind in kinds):
                    filtered_attractions.append(attraction)
            attractions = filtered_attractions
        
        # Remove duplicates and ensure quality
        unique_attractions = []
        seen_names = set()
        
        for attraction in attractions:
            name_lower = attraction.get("name", "").lower().strip()
            if (name_lower and 
                name_lower not in seen_names and 
                len(name_lower) > 3 and
                not any(skip in name_lower for skip in ['[x]', 'among', 'you can', 'though we'])):
                seen_names.add(name_lower)
                unique_attractions.append(attraction)
        
        # Limit results
        return unique_attractions[:limit]
        
    except Exception as e:
        logging.error(f"POI search failed: {e}")
        raise RuntimeError(f"Unable to search attractions: {e}")

async def search_attractions_with_interests(city: str, interests: list = None):
    """
    Search for attractions based on user interests using Tavily
    """
    from utils.tavily_search import search_attractions
    
    if not interests:
        # Default search if no interests specified
        return await search_attractions(city)
    
    all_attractions = []
    
    # Create interest-specific search queries
    interest_queries = create_interest_based_queries(city, interests)
    
    # Search for each interest category
    for query in interest_queries:
        try:
            attractions = await search_attractions_with_query(city, query)
            all_attractions.extend(attractions)
        except Exception as e:
            logging.warning(f"Interest-based search failed for query '{query}': {e}")
            continue
    
    # Also do a general search to ensure we have comprehensive results
    try:
        general_attractions = await search_attractions(city)
        all_attractions.extend(general_attractions)
    except Exception as e:
        logging.warning(f"General search failed: {e}")
    
    return all_attractions

def create_interest_based_queries(city: str, interests: list) -> list:
    """
    Create specific search queries based on user interests for any destination
    """
    interest_mapping = {
        'historical': f"historical places temples forts monuments heritage sites {city}",
        'religious': f"temples churches mosques religious places worship {city}",
        'nature': f"parks gardens lakes beaches nature outdoor activities {city}",
        'cultural': f"museums art galleries cultural centers exhibitions {city}",
        'adventure': f"adventure sports activities trekking climbing water sports {city}",
        'shopping': f"markets shopping malls bazaars local shopping {city}",
        'food': f"restaurants local cuisine food markets street food {city}",
        'nightlife': f"nightlife clubs bars entertainment venues {city}",
        'family': f"family attractions amusement parks zoos kid-friendly places {city}",
        'photography': f"scenic spots photo locations instagram worthy places {city}",
        'architecture': f"architectural marvels buildings modern ancient structures {city}",
        'wellness': f"spas wellness centers yoga meditation retreats {city}"
    }
    
    queries = []
    
    for interest in interests:
        interest_lower = interest.lower()
        for key, query in interest_mapping.items():
            if key in interest_lower or interest_lower in key:
                queries.append(query)
                break
        else:
            # Generic query for interests not in mapping
            queries.append(f"{interest} places attractions {city}")
    
    return queries[:3]  # Limit to top 3 queries for performance

async def search_attractions_with_query(city: str, query: str):
    """
    Search attractions with a specific query
    """
    from utils.tavily_search import search_travel_info
    
    try:
        results = await search_travel_info(query, max_results=3)
        attractions = []
        
        for result in results:
            # Use the existing extract_attraction_names function
            from utils.tavily_search import extract_attraction_names
            extracted_attractions = extract_attraction_names(result.get("content", ""), city)
            
            for attraction_info in extracted_attractions:
                attractions.append({
                    "id": f"interest_poi_{len(attractions)+1}",
                    "name": attraction_info.get("name", "Attraction"),
                    "kinds": determine_attraction_kinds(attraction_info.get("name", ""), query),
                    "type": determine_attraction_type_from_query(query),
                    "rate": 4.0 + (len(attractions) * 0.1),
                    "address": attraction_info.get("location", f"{city}"),
                    "location": attraction_info.get("location", f"{city}"),
                    "description": attraction_info.get("description", f"Popular attraction in {city}"),
                    "url": result.get("url", ""),
                    "source": "Interest-based Tavily Search",
                    "opening_hours": attraction_info.get("hours", "9:00 AM - 6:00 PM"),
                    "entry_fee": attraction_info.get("fee", "Entry fee may apply"),
                    "ticket_price": determine_ticket_price(attraction_info.get("name", "")),
                    "raw": result
                })
        
        return attractions
        
    except Exception as e:
        logging.error(f"Query-specific search failed: {e}")
        return []

def determine_attraction_kinds(name: str, query: str) -> str:
    """
    Determine attraction kinds based on name and search query
    """
    name_lower = name.lower()
    query_lower = query.lower()
    
    kinds = []
    
    if any(word in name_lower for word in ["temple", "church", "mosque", "gurudwara"]):
        kinds.append("religious")
    if any(word in name_lower for word in ["fort", "palace", "monument", "heritage"]):
        kinds.append("historical")
    if any(word in name_lower for word in ["museum", "gallery", "exhibition"]):
        kinds.append("cultural")
    if any(word in name_lower for word in ["park", "garden", "lake", "beach"]):
        kinds.append("nature")
    if any(word in name_lower for word in ["market", "bazaar", "shopping"]):
        kinds.append("shopping")
    
    # Add kinds based on query context
    if "historical" in query_lower:
        kinds.append("historical")
    if "religious" in query_lower:
        kinds.append("religious")
    if "nature" in query_lower:
        kinds.append("nature")
    if "cultural" in query_lower:
        kinds.append("cultural")
    
    return ",".join(kinds) if kinds else "sightseeing"

def determine_attraction_type_from_query(query: str) -> str:
    """
    Determine the primary attraction type from the search query
    """
    query_lower = query.lower()
    
    if "historical" in query_lower or "heritage" in query_lower:
        return "historical"
    elif "religious" in query_lower or "temple" in query_lower:
        return "religious"
    elif "nature" in query_lower or "park" in query_lower:
        return "nature"
    elif "cultural" in query_lower or "museum" in query_lower:
        return "cultural"
    elif "adventure" in query_lower:
        return "adventure"
    elif "shopping" in query_lower:
        return "shopping"
    else:
        return "sightseeing"

def determine_ticket_price(name: str) -> int:
    """
    Determine realistic ticket price based on attraction name
    """
    name_lower = name.lower()
    
    if any(word in name_lower for word in ["temple", "mosque", "church", "gurudwara"]):
        return 0  # Most religious places are free
    elif any(word in name_lower for word in ["fort", "palace", "monument"]):
        return 250  # Historical monuments
    elif any(word in name_lower for word in ["museum", "gallery"]):
        return 200  # Museums and galleries
    elif any(word in name_lower for word in ["park", "garden"]):
        return 50   # Parks and gardens
    elif any(word in name_lower for word in ["zoo", "aquarium"]):
        return 300  # Zoos and aquariums
    else:
        return 100  # General attractions
