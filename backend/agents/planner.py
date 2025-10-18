import logging
from typing import Dict, Any, List
from agents.flights import search_flights
from agents.hotels import search_hotels  
from agents.poi import get_pois_near
from utils.optimizer import optimize_travel_plan

class TravelPlannerAgent:
    def __init__(self):
        # Use the existing function-based agents
        pass
        
    async def create_travel_plan(self, user_request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a comprehensive travel plan using enhanced Tavily search and LangChain optimization
        """
        try:
            # Extract user requirements
            destination = user_request.get("destination", "")
            start_date = user_request.get("start_date", "")
            end_date = user_request.get("end_date", "")
            origin = user_request.get("origin", "Delhi")
            budget = user_request.get("budget", 50000)
            travelers = user_request.get("travelers", 2)
            interests = user_request.get("interests", [])  # Get user interests
            
            logging.info(f"Creating enhanced travel plan for {destination} from {origin} with interests: {interests}")
            
            # Get comprehensive travel data using parallel Tavily calls for faster processing
            import asyncio
            
            # Run all searches in parallel for faster results
            search_tasks = [
                search_flights(
                    origin=origin,
                    destination=destination,
                    departureDate=start_date,
                    returnDate=end_date,
                    adults=travelers
                ),
                search_hotels(
                    city_code=destination,
                    check_in=start_date,
                    check_out=end_date
                ),
                get_pois_near(
                    city=destination,
                    limit=15,  # Increased to get more variety
                    interests=interests  # Pass user interests
                )
            ]
            
            # Wait for all searches to complete
            flights_data, hotels_data, pois_data = await asyncio.gather(*search_tasks, return_exceptions=True)
            
            # Handle exceptions from parallel tasks
            if isinstance(flights_data, Exception):
                logging.error(f"Flight search failed: {flights_data}")
                flights_data = []
            
            if isinstance(hotels_data, Exception):
                logging.error(f"Hotel search failed: {hotels_data}")
                hotels_data = []
                
            if isinstance(pois_data, Exception):
                logging.error(f"POI search failed: {pois_data}")
                pois_data = []
            
            # Log search results
            logging.info(f"Found {len(flights_data)} flights, {len(hotels_data)} hotels, {len(pois_data)} POIs")
            
            # Use the new optimizer for creating travel plan with variants  
            travel_plan = await optimize_travel_plan(
                flights=flights_data,
                hotels=hotels_data,
                pois=pois_data,
                start_date=start_date,
                end_date=end_date,
                destination=destination,
                budget=budget,
                interests=interests
            )
            
            # Add metadata and user request info
            travel_plan.update({
                "planning_metadata": {
                    "total_flights_found": len(flights_data),
                    "total_hotels_found": len(hotels_data),
                    "total_attractions_found": len(pois_data),
                    "planning_engine": "Tavily + LangChain (Real Data Only)",
                    "data_sources": "Real-time web search",
                    "currency": "INR",
                    "last_updated": "Real-time data",
                    "processing_time": "Fast parallel search"
                },
                "user_request": {
                    "destination": destination,
                    "origin": origin,
                    "budget": budget,
                    "travelers": travelers,
                    "start_date": start_date,
                    "end_date": end_date,
                    "interests": interests
                }
            })
            
            logging.info(f"Successfully created travel plan using new optimizer")
            return travel_plan
            
        except Exception as e:
            logging.error(f"Error creating travel plan: {e}")
            return {
                "error": "Failed to create travel plan",
                "message": str(e),
                "trip_summary": {
                    "destination": destination,
                    "start_date": start_date,
                    "end_date": end_date,
                    "status": "error"
                }
            }
    
    async def create_budget_variants(self, flights: List[Dict], hotels: List[Dict], pois: List[Dict], 
                                   start_date: str, end_date: str, destination: str, 
                                   budget: int, travelers: int) -> List[Dict]:
        """
        Create three budget-based variants: Budget, Mid-range, and Luxury
        """
        try:
            from datetime import datetime, timedelta
            
            # Calculate trip duration
            try:
                start_dt = datetime.strptime(start_date, "%Y-%m-%d")
                end_dt = datetime.strptime(end_date, "%Y-%m-%d")
                duration_days = max(1, (end_dt - start_dt).days)
            except ValueError:
                duration_days = 3
            
            # Sort options by price for selection
            sorted_flights = sorted(flights, key=lambda x: x.get('price', 0))
            sorted_hotels = sorted(hotels, key=lambda x: x.get('price_per_night', 0))
            
            variants = []
            
            # Budget Variant (30% below requested budget)
            budget_limit = int(budget * 0.7)
            budget_variant = await self.create_variant(
                variant_type="budget",
                flights=sorted_flights[:2],  # Cheapest flights
                hotels=[h for h in sorted_hotels if h.get('price_per_night', 0) <= 3000][:2],
                pois=pois[:8],  # Fewer activities
                start_date=start_date,
                end_date=end_date,
                destination=destination,
                budget_limit=budget_limit,
                duration_days=duration_days
            )
            variants.append(budget_variant)
            
            # Mid-range Variant (around requested budget)
            midrange_variant = await self.create_variant(
                variant_type="standard",
                flights=sorted_flights[1:4] if len(sorted_flights) > 1 else sorted_flights,  # Mid-price flights
                hotels=[h for h in sorted_hotels if 2500 <= h.get('price_per_night', 0) <= 6000][:3],
                pois=pois[:12],  # More activities
                start_date=start_date,
                end_date=end_date,
                destination=destination,
                budget_limit=budget,
                duration_days=duration_days
            )
            variants.append(midrange_variant)
            
            # Luxury Variant (50% above requested budget)
            luxury_limit = int(budget * 1.5)
            luxury_variant = await self.create_variant(
                variant_type="premium",
                flights=sorted_flights[-2:] if len(sorted_flights) > 1 else sorted_flights,  # Most expensive flights
                hotels=[h for h in sorted_hotels if h.get('price_per_night', 0) >= 4000][:3],
                pois=pois,  # All activities
                start_date=start_date,
                end_date=end_date,
                destination=destination,
                budget_limit=luxury_limit,
                duration_days=duration_days
            )
            variants.append(luxury_variant)
            
            return variants
            
        except Exception as e:
            logging.error(f"Error creating budget variants: {e}")
            # Return single default variant on error
            return [await self.create_variant(
                "standard", flights[:3], hotels[:3], pois[:10], 
                start_date, end_date, destination, budget, 3
            )]
    
    async def create_variant(self, variant_type: str, flights: List[Dict], hotels: List[Dict], 
                           pois: List[Dict], start_date: str, end_date: str, 
                           destination: str, budget_limit: int, duration_days: int) -> Dict:
        """
        Create a single travel plan variant
        """
        from utils.optimizer import create_basic_daily_itinerary
        
        # Select best options within budget
        selected_flight = flights[0] if flights else {}
        selected_hotel = hotels[0] if hotels else {}
        
        # Create itinerary based on variant type
        if variant_type == "budget":
            # Basic itinerary with essential attractions
            daily_itinerary = create_basic_daily_itinerary(pois[:6], duration_days, start_date)
            activities_per_day = 2
        elif variant_type == "premium":
            # Comprehensive itinerary with premium experiences
            daily_itinerary = create_basic_daily_itinerary(pois, duration_days, start_date)
            activities_per_day = 4
        else:  # standard
            # Balanced itinerary
            daily_itinerary = create_basic_daily_itinerary(pois[:10], duration_days, start_date)
            activities_per_day = 3
        
        # Calculate costs
        flight_cost = selected_flight.get('price', 0) * 2  # Round trip
        hotel_cost = selected_hotel.get('total_price', 0) or (selected_hotel.get('price_per_night', 0) * duration_days)
        activity_cost = sum(day.get('estimated_cost', 0) for day in daily_itinerary)
        
        # Add daily expenses based on variant type
        daily_expenses_map = {
            "budget": 1200,     # Basic meals and transport
            "standard": 2000,   # Comfortable dining and transport
            "premium": 3500     # Premium dining and private transport
        }
        daily_expenses = daily_expenses_map.get(variant_type, 2000) * duration_days
        
        total_cost = flight_cost + hotel_cost + activity_cost + daily_expenses
        
        return {
            "variant": variant_type,
            "flights": flights[:3],
            "hotels": hotels[:3], 
            "itinerary": daily_itinerary,
            "estimated_cost": total_cost,
            "selected_flight": selected_flight,
            "selected_hotel": selected_hotel,
            "cost_breakdown": {
                "flights": flight_cost,
                "accommodation": hotel_cost,
                "activities": activity_cost,
                "daily_expenses": daily_expenses,
                "total": total_cost
            },
            "features": self.get_variant_features(variant_type),
            "within_budget": total_cost <= budget_limit,
            "savings": max(0, budget_limit - total_cost)
        }
    
    def get_variant_features(self, variant_type: str) -> List[str]:
        """
        Get features for each variant type
        """
        features_map = {
            "budget": [
                "Budget-friendly accommodation",
                "Economy flight options",
                "Essential attractions covered",
                "Local transport recommendations",
                "Basic meal suggestions"
            ],
            "standard": [
                "Comfortable accommodation", 
                "Good flight options with preferred airlines",
                "Popular attractions and hidden gems",
                "Mix of local and private transport",
                "Restaurant recommendations"
            ],
            "premium": [
                "Luxury accommodation options",
                "Premium airlines and flexible timings", 
                "Comprehensive attraction coverage",
                "Private transport options",
                "Fine dining recommendations",
                "Concierge service suggestions"
            ]
        }
        return features_map.get(variant_type, [])
    
    async def generate_travel_recommendations(self, destination: str, budget: int, 
                                            variants: List[Dict], travelers: int) -> Dict:
        """
        Generate AI-powered travel recommendations and summary
        """
        try:
            # Analyze the variants
            best_value_variant = min(variants, key=lambda v: v['estimated_cost'] / len(v.get('features', [1])))
            most_comprehensive = max(variants, key=lambda v: len(v.get('itinerary', [])))
            
            # Calculate budget efficiency
            budget_utilization = {}
            for variant in variants:
                efficiency = (variant['estimated_cost'] / budget) * 100
                budget_utilization[variant['variant']] = round(efficiency, 1)
            
            # Generate season-based recommendations
            season_advice = self.get_seasonal_advice(destination)
            
            # Create recommendations
            recommendations = {
                "summary": {
                    "destination_overview": f"Exploring {destination} with {travelers} travelers",
                    "budget_analysis": f"Your budget of ₹{budget:,} offers great flexibility for this destination",
                    "best_time_insight": season_advice,
                    "trip_highlights": self.get_destination_highlights(destination)
                },
                "variant_analysis": {
                    "best_value": {
                        "variant": best_value_variant['variant'],
                        "reason": "Offers the most features and experiences per rupee spent",
                        "cost": best_value_variant['estimated_cost']
                    },
                    "most_comprehensive": {
                        "variant": most_comprehensive['variant'], 
                        "reason": "Includes the most attractions and detailed itinerary",
                        "activities": len(most_comprehensive.get('itinerary', []))
                    },
                    "budget_efficiency": budget_utilization
                },
                "personalized_tips": [
                    f"For {travelers} travelers, consider the {best_value_variant['variant']} variant for best value",
                    f"Book flights and hotels at least 2-3 weeks in advance for better prices",
                    f"Local transport in {destination} is cost-effective and authentic",
                    f"Try local street food and markets for budget-friendly dining",
                    "Keep some budget for spontaneous experiences and shopping"
                ],
                "smart_savings": [
                    "Book accommodation slightly outside city center for better rates",
                    "Use public transport or ride-sharing for cost efficiency", 
                    "Look for combo tickets for multiple attractions",
                    "Eat at local restaurants instead of hotel dining",
                    "Shop at local markets for souvenirs"
                ],
                "safety_tips": [
                    "Keep copies of important documents",
                    "Share your itinerary with family/friends",
                    "Use registered taxis or ride-sharing apps",
                    "Drink bottled water and eat at hygienic places",
                    "Keep emergency contacts handy"
                ]
            }
            
            return recommendations
            
        except Exception as e:
            logging.error(f"Error generating recommendations: {e}")
            return {
                "summary": {
                    "destination_overview": f"Exploring {destination}",
                    "budget_analysis": "Budget analysis available",
                    "trip_highlights": ["Great destination for travelers"]
                },
                "personalized_tips": ["Enjoy your trip!", "Stay safe and have fun!"]
            }
    
    def get_seasonal_advice(self, destination: str) -> str:
        """
        Get seasonal travel advice for destination
        """
        import datetime
        current_month = datetime.datetime.now().month
        
        # General seasonal advice
        if current_month in [12, 1, 2]:  # Winter
            return "Winter season - generally pleasant weather for most Indian destinations"
        elif current_month in [3, 4, 5]:  # Summer
            return "Summer season - consider hill stations or coastal areas for better weather"
        elif current_month in [6, 7, 8, 9]:  # Monsoon
            return "Monsoon season - perfect for hill stations but check local weather conditions"
        else:  # Post-monsoon
            return "Post-monsoon season - excellent time for most destinations with clear skies"
    
    def get_destination_highlights(self, destination: str) -> List[str]:
        """
        Get key highlights for the destination
        """
        highlights_map = {
            "mumbai": ["Bollywood capital", "Street food paradise", "Colonial architecture", "Marine Drive"],
            "delhi": ["Rich historical heritage", "Mughal monuments", "Street food culture", "Shopping hubs"],
            "bangalore": ["IT capital", "Pleasant weather", "Pub culture", "Gardens and parks"],
            "chennai": ["Cultural capital", "Temples and heritage", "Marina Beach", "South Indian cuisine"],
            "goa": ["Beautiful beaches", "Portuguese heritage", "Vibrant nightlife", "Water sports"],
            "kerala": ["Backwaters", "Spice plantations", "Ayurveda", "Hill stations"]
        }
        
        destination_lower = destination.lower()
        for key, highlights in highlights_map.items():
            if key in destination_lower:
                return highlights
        
        return ["Rich cultural heritage", "Local cuisine", "Historical sites", "Natural beauty"]

# Legacy function for backward compatibility with the existing FastAPI endpoints
async def create_plan_agent(request: dict):
    """
    Enhanced legacy function using new TravelPlannerAgent with Tavily + LangChain
    """
    try:
        # Convert legacy request format to new format
        user_request = {
            "destination": request.get("destination", ""),
            "start_date": request.get("start_date", ""),
            "end_date": request.get("end_date", ""), 
            "origin": request.get("origin", "Delhi"),
            "budget": request.get("budget", 50000),
            "travelers": request.get("travellers", 2),  # Note: legacy uses 'travellers'
            "interests": request.get("interests", [])
        }
        
        # Create planner and get travel plan
        planner = TravelPlannerAgent()
        travel_plan = await planner.create_travel_plan(user_request)
        
        # Convert to legacy format for existing frontend
        if "error" in travel_plan:
            return {"variants": [], "error": travel_plan["error"]}
        
        # Return the new multi-variant structure directly
        return {
            "variants": travel_plan.get("variants", []),
            "recommendations": travel_plan.get("recommendations", {}),
            "user_request": travel_plan.get("user_request", {}),
            "planning_metadata": travel_plan.get("planning_metadata", {})
        }
        
    except Exception as e:
        logging.error(f"Error in legacy create_plan_agent: {e}")
        return {"variants": [], "error": str(e)}
