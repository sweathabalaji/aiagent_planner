import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any
import asyncio
from langchain.schema import SystemMessage, HumanMessage
from .llm import get_chat_llm

# Global tracker to prevent POI repetition across days
used_pois_tracker = set()

async def optimize_travel_plan(
    flights: List[Dict], 
    hotels: List[Dict], 
    pois: List[Dict], 
    start_date: str, 
    end_date: str, 
    destination: str,
    budget: float,
    interests: List[str] = None
) -> Dict[str, Any]:
    """
    Create optimized travel plan with three variants using only real API data
    """
    try:
        # Calculate duration
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.strptime(end_date, "%Y-%m-%d")
        duration_days = (end_dt - start_dt).days
        
        if duration_days <= 0:
            duration_days = 3
        
        logging.info(f"Optimizing {duration_days}-day travel plan for {destination}")
        
        # Create three variants with different budget allocations
        variants = await create_plan_variants(
            flights, hotels, pois, start_date, end_date, destination, 
            duration_days, budget, interests
        )
        
        # Generate AI recommendations
        recommendations = await generate_ai_recommendations(
            destination, duration_days, budget, interests, pois
        )
        
        return {
            "destination": destination,
            "duration": f"{duration_days} days",
            "travel_dates": f"{start_date} to {end_date}",
            "variants": variants,
            "recommendations": recommendations,
            "status": "success"
        }
        
    except Exception as e:
        logging.error(f"Error in optimize_travel_plan: {str(e)}")
        return {
            "error": f"Failed to optimize travel plan: {str(e)}",
            "status": "error"
        }

async def create_plan_variants(
    flights: List[Dict], 
    hotels: List[Dict], 
    pois: List[Dict], 
    start_date: str, 
    end_date: str, 
    destination: str,
    duration_days: int,
    budget: float,
    interests: List[str] = None
) -> List[Dict]:
    """
    Create three plan variants: Budget, Standard, Premium using only real data
    """
    variants = []
    
    # Filter and categorize available data
    budget_flights = [f for f in flights if f.get('price', 0) <= budget * 0.4]
    standard_flights = [f for f in flights if budget * 0.3 <= f.get('price', 0) <= budget * 0.6]
    premium_flights = [f for f in flights if f.get('price', 0) >= budget * 0.4]
    
    budget_hotels = [h for h in hotels if h.get('price_per_night', 0) <= budget * 0.2 / duration_days]
    standard_hotels = [h for h in hotels if budget * 0.15 / duration_days <= h.get('price_per_night', 0) <= budget * 0.3 / duration_days]
    premium_hotels = [h for h in hotels if h.get('price_per_night', 0) >= budget * 0.25 / duration_days]
    
    # Create variants
    variant_configs = [
        {
            "name": "Budget Plan",
            "description": "Cost-effective travel with essential experiences",
            "flights": budget_flights[:3] if budget_flights else flights[:3],
            "hotels": budget_hotels[:3] if budget_hotels else hotels[:3],
            "budget_multiplier": 0.7
        },
        {
            "name": "Standard Plan", 
            "description": "Balanced comfort and experiences",
            "flights": standard_flights[:3] if standard_flights else flights[:3],
            "hotels": standard_hotels[:3] if standard_hotels else hotels[:3],
            "budget_multiplier": 1.0
        },
        {
            "name": "Premium Plan",
            "description": "Luxury travel with premium experiences", 
            "flights": premium_flights[:3] if premium_flights else flights[:3],
            "hotels": premium_hotels[:3] if premium_hotels else hotels[:3],
            "budget_multiplier": 1.3
        }
    ]
    
    for config in variant_configs:
        variant = await create_single_variant(
            config, pois, start_date, end_date, destination, 
            duration_days, budget, interests
        )
        if variant:
            variants.append(variant)
    
    return variants

async def create_single_variant(
    config: Dict,
    pois: List[Dict], 
    start_date: str, 
    end_date: str, 
    destination: str,
    duration_days: int,
    budget: float,
    interests: List[str] = None
) -> Dict:
    """
    Create a single travel plan variant using only real data
    """
    try:
        # Create itinerary using only real POI data
        itinerary = create_basic_daily_itinerary(pois, duration_days, start_date)
        
        # Only proceed if we have real itinerary data
        if not itinerary:
            logging.warning(f"No real POI data available for {config['name']}")
            return None
            
        # Calculate costs
        flight_cost = sum(f.get('price', 0) for f in config['flights'][:1]) if config['flights'] else 0
        hotel_cost = sum(h.get('price_per_night', 0) for h in config['hotels'][:1]) * duration_days if config['hotels'] else 0
        activity_cost = sum(day.get('estimated_cost', 0) for day in itinerary)
        
        total_cost = (flight_cost + hotel_cost + activity_cost) * config['budget_multiplier']
        
        return {
            "variant": config['name'],
            "description": config['description'],
            "estimated_cost": round(total_cost, 2),
            "cost_breakdown": {
                "flights": round(flight_cost * config['budget_multiplier'], 2),
                "accommodation": round(hotel_cost * config['budget_multiplier'], 2),
                "activities": round(activity_cost * config['budget_multiplier'], 2)
            },
            "flights": config['flights'],
            "hotels": config['hotels'],
            "itinerary": itinerary,
            "days": duration_days
        }
        
    except Exception as e:
        logging.error(f"Error creating variant {config['name']}: {str(e)}")
        return None

def create_basic_daily_itinerary(pois: List[Dict], duration_days: int, start_date: str) -> List[Dict]:
    """
    Create daily itinerary only using real POI data - no dummy data
    """
    daily_itinerary = []
    
    # Reset the global POI tracker for a new itinerary
    global used_pois_tracker
    used_pois_tracker = set()
    
    # Ensure minimum duration
    if duration_days <= 0:
        duration_days = 3
    
    try:
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    except ValueError:
        start_dt = datetime.now()
    
    # If no POIs available, return empty itinerary rather than dummy data
    if not pois:
        logging.warning("No POIs available - cannot create itinerary without real data")
        return []
    
    # Remove duplicates from POIs and clean data
    unique_pois = []
    seen_names = set()
    
    for poi in pois:
        poi_name = poi.get('name', '').lower().strip()
        # Clean and filter POI names with stricter criteria
        if (poi_name and 
            poi_name not in seen_names and 
            len(poi_name) > 3 and
            not any(skip in poi_name for skip in ['[x]', 'among', 'you can', 'though we', '...', 'visit', 'explore'])):
            
            # Clean the POI data
            cleaned_poi = clean_poi_data(poi)
            if cleaned_poi and cleaned_poi['name']:
                seen_names.add(poi_name)
                unique_pois.append(cleaned_poi)
    
    # Log the number of unique POIs found
    logging.info(f"Found {len(unique_pois)} unique POIs for {duration_days} days")
    
    # If we don't have enough unique POIs, work with what we have
    if len(unique_pois) < duration_days:
        logging.warning(f"Limited POI data: {len(unique_pois)} POIs for {duration_days} days")
    
    # Group POIs by type for better distribution
    poi_groups = categorize_pois(unique_pois)
    
    # Log categorization
    for category, pois_in_cat in poi_groups.items():
        if pois_in_cat:
            logging.info(f"Category '{category}': {len(pois_in_cat)} POIs")
    
    # Create balanced daily itineraries with strict no-repeat policy
    for day in range(duration_days):
        day_date = (start_dt + timedelta(days=day)).strftime("%Y-%m-%d")
        
        # Get diverse activities for this day (ensures no repetitions)
        day_activities = create_diverse_day_activities(poi_groups, day, duration_days)
        
        # Only create days if we have real activities
        if day_activities:
            # Calculate day theme based on activities
            day_theme = determine_day_theme(day_activities, day + 1)
            
            daily_itinerary.append({
                "day": day + 1,
                "date": day_date,
                "theme": day_theme,
                "activities": day_activities,
                "estimated_cost": sum(activity.get('cost', 0) for activity in day_activities),
                "total_duration": "Full Day (9 AM - 8 PM)"
            })
            
            logging.info(f"Created {day_theme} with {len(day_activities)} activities")
        else:
            logging.warning(f"No activities available for day {day + 1}")
    
    return daily_itinerary

def clean_poi_data(poi: Dict) -> Dict:
    """
    Clean and validate POI data
    """
    if not poi or not poi.get('name'):
        return None
        
    # Clean the name
    name = poi.get('name', '').strip()
    if not name or len(name) < 3:
        return None
    
    # Remove problematic entries
    problematic_phrases = ['[x]', 'among', 'you can', 'though we', '...', 'explore the', 'visit the']
    if any(phrase in name.lower() for phrase in problematic_phrases):
        return None
    
    return {
        'name': name,
        'description': poi.get('description', f'Visit {name}'),
        'location': poi.get('location', 'Location TBD'),
        'type': poi.get('type', 'attraction'),
        'ticket_price': poi.get('ticket_price', 0),
        'rating': poi.get('rating', 4.0),
        'duration': poi.get('duration', '2-3 hours'),
        'url': poi.get('url', ''),
        'opening_hours': poi.get('opening_hours', '9:00 AM - 6:00 PM')
    }

def categorize_pois(pois: List[Dict]) -> Dict[str, List[Dict]]:
    """
    Categorize POIs by type for better distribution
    """
    categories = {
        'historic': [],
        'nature': [],
        'cultural': [],
        'shopping': [],
        'food': [],
        'general': []
    }
    
    for poi in pois:
        poi_type = poi.get('type', '').lower()
        poi_name = poi.get('name', '').lower()
        
        if any(word in poi_type + poi_name for word in ['temple', 'fort', 'palace', 'historic', 'monument']):
            categories['historic'].append(poi)
        elif any(word in poi_type + poi_name for word in ['park', 'garden', 'beach', 'nature', 'lake']):
            categories['nature'].append(poi)
        elif any(word in poi_type + poi_name for word in ['museum', 'gallery', 'cultural', 'art']):
            categories['cultural'].append(poi)
        elif any(word in poi_type + poi_name for word in ['market', 'shop', 'mall', 'bazar']):
            categories['shopping'].append(poi)
        elif any(word in poi_type + poi_name for word in ['restaurant', 'food', 'cafe', 'dining']):
            categories['food'].append(poi)
        else:
            categories['general'].append(poi)
    
    return categories

def create_diverse_day_activities(poi_groups: Dict[str, List[Dict]], day_index: int, total_days: int) -> List[Dict]:
    """
    Create diverse activities for a single day using only real POI data - no dummy activities
    """
    activities = []
    time_slots = [
        {"time": "9:00 AM - 12:00 PM", "period": "Morning"},
        {"time": "1:00 PM - 4:00 PM", "period": "Afternoon"}, 
        {"time": "5:00 PM - 8:00 PM", "period": "Evening"}
    ]
    
    # Create a unique key for tracking used POIs globally
    global used_pois_tracker
    if 'used_pois_tracker' not in globals():
        used_pois_tracker = set()
    
    # Strategy: Different categories for different time slots to ensure variety
    time_category_mapping = {
        0: ['historic', 'cultural'],      # Morning: Historical and cultural sites
        1: ['nature', 'shopping'],        # Afternoon: Nature and shopping
        2: ['general', 'cultural']        # Evening: General attractions and cultural sites
    }
    
    for i, slot in enumerate(time_slots):
        activity = None
        preferred_categories = time_category_mapping.get(i, ['general'])
        
        # Try preferred categories first, then any available
        all_categories = preferred_categories + [cat for cat in poi_groups.keys() if cat not in preferred_categories]
        
        for category in all_categories:
            available_pois = poi_groups.get(category, [])
            
            # Find an unused POI in this category
            for poi in available_pois:
                poi_name = poi.get('name', '').lower().strip()
                if poi_name and poi_name not in used_pois_tracker:
                    # Mark this POI as used
                    used_pois_tracker.add(poi_name)
                    
                    activity = {
                        "time": slot["time"],
                        "activity": f"Visit {poi['name']}",
                        "name": poi['name'],
                        "location": poi['location'],
                        "description": poi['description'],
                        "cost": poi.get('ticket_price', 0),
                        "duration": "2-3 hours",
                        "type": poi['type'],
                        "url": poi.get('url', ''),
                        "rating": poi.get('rating', 4.0),
                        "tips": f"Best visited during {slot['period'].lower()}. {poi.get('opening_hours', 'Check opening hours.')}"
                    }
                    break
            
            if activity:
                break
        
        # Only add activity if we found a real POI
        if activity:
            activities.append(activity)
    
    return activities

def determine_day_theme(activities: List[Dict], day_num: int) -> str:
    """
    Determine day theme based on activities
    """
    if not activities:
        return f"Day {day_num} - Exploration"
    
    activity_types = [activity.get('type', 'general') for activity in activities]
    
    if 'historic' in activity_types:
        return f"Day {day_num} - Historical Heritage"
    elif 'cultural' in activity_types:
        return f"Day {day_num} - Cultural Immersion"
    elif 'nature' in activity_types:
        return f"Day {day_num} - Nature & Outdoors"
    elif 'shopping' in activity_types:
        return f"Day {day_num} - Shopping & Markets"
    else:
        return f"Day {day_num} - City Exploration"

async def generate_ai_recommendations(
    destination: str, 
    duration_days: int, 
    budget: float, 
    interests: List[str], 
    pois: List[Dict]
) -> Dict[str, Any]:
    """
    Generate AI-powered travel recommendations using real data
    """
    try:
        # Base recommendations on actual POI data
        poi_names = [poi.get('name', '') for poi in pois[:10] if poi.get('name')]
        
        prompt = f"""
        Based on the following real attractions and places in {destination}:
        {', '.join(poi_names)}
        
        Provide travel recommendations for a {duration_days}-day trip with a budget of ${budget}.
        User interests: {', '.join(interests) if interests else 'General travel'}
        
        Return practical advice in the following format:
        - Best time to visit
        - Local transportation tips
        - Cultural etiquette
        - Must-try local food
        - Budget-saving tips
        """
        
        llm = get_chat_llm()
        
        messages = [
            SystemMessage(content="You are a knowledgeable travel advisor providing practical, real-world advice."),
            HumanMessage(content=prompt)
        ]
        
        response = await llm.ainvoke(messages)
        
        return {
            "ai_advice": response.content,
            "based_on_real_data": True,
            "poi_count": len(pois),
            "destination_currency": get_destination_currency(destination)
        }
        
    except Exception as e:
        logging.error(f"Error generating AI recommendations: {str(e)}")
        return {
            "ai_advice": "Please explore the provided attractions and enjoy your trip!",
            "based_on_real_data": False,
            "error": str(e)
        }

def get_destination_currency(destination: str) -> str:
    """
    Get the local currency for the destination
    """
    currency_map = {
        'india': 'INR',
        'mumbai': 'INR',
        'delhi': 'INR',
        'bangalore': 'INR',
        'usa': 'USD',
        'uk': 'GBP',
        'japan': 'JPY',
        'thailand': 'THB',
        'singapore': 'SGD',
        'malaysia': 'MYR',
        'france': 'EUR',
        'germany': 'EUR',
        'italy': 'EUR',
        'spain': 'EUR'
    }
    
    destination_lower = destination.lower()
    for country, currency in currency_map.items():
        if country in destination_lower:
            return currency
    
    return 'USD'  # Default currency
