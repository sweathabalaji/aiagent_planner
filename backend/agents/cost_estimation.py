import logging
import json
from typing import Dict, Any, List
from datetime import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.llm import get_chat_llm
from langchain.schema import HumanMessage, SystemMessage

class DynamicCostEstimationAgent:
    def __init__(self):
        """Initialize the Dynamic Cost Estimation Agent using Moonshot LLM"""
        try:
            self.llm = get_chat_llm()
            if self.llm is None:
                logging.warning("LLM not available - using fallback cost estimation")
                self.use_fallback = True
            else:
                self.use_fallback = False
                logging.info("Dynamic Cost Estimation Agent initialized with Moonshot LLM")
        except Exception as e:
            logging.error(f"Failed to initialize Dynamic Cost Estimation Agent: {e}")
            self.llm = None
            self.use_fallback = True
    
    async def analyze_market_costs(self, event_request: Dict[str, Any], venues: List[Dict], vendors: List[Dict]) -> Dict[str, Any]:
        """
        Analyze market costs dynamically based on real venue/vendor data and event requirements
        """
        try:
            if self.use_fallback:
                return await self._get_fallback_cost_analysis(event_request, venues, vendors)
            
            # Prepare data for AI analysis
            event_type = event_request.get("event_type", "")
            location = event_request.get("location", "")
            guest_count = event_request.get("guest_count", 50)
            budget = event_request.get("budget", 100000)
            preferences = event_request.get("preferences", [])
            special_requirements = event_request.get("special_requirements", [])
            
            # Extract real pricing data from venues and vendors
            venue_prices = []
            vendor_prices = {}
            
            for venue in venues:
                if venue.get("price_per_day"):
                    venue_prices.append({
                        "name": venue.get("name"),
                        "price": venue.get("price_per_day"),
                        "capacity": venue.get("capacity"),
                        "type": venue.get("venue_type", "")
                    })
            
            for vendor in vendors:
                service_type = vendor.get("service_type", "unknown")
                if service_type not in vendor_prices:
                    vendor_prices[service_type] = []
                
                price_info = {
                    "name": vendor.get("name"),
                    "price_range": vendor.get("price_range", ""),
                    "contact": vendor.get("contact", ""),
                    "specialties": vendor.get("specialties", [])
                }
                vendor_prices[service_type].append(price_info)
            
            # Create comprehensive prompt for AI analysis
            analysis_prompt = f"""
            You are a professional event planning cost analyst. Analyze the following real market data and provide dynamic cost estimation:

            EVENT DETAILS:
            - Type: {event_type}
            - Location: {location}
            - Guest Count: {guest_count}
            - Budget: ₹{budget}
            - Preferences: {', '.join(preferences)}
            - Special Requirements: {', '.join(special_requirements)}

            REAL VENUE PRICING DATA:
            {json.dumps(venue_prices, indent=2)}

            REAL VENDOR PRICING DATA:
            {json.dumps(vendor_prices, indent=2)}

            ANALYSIS REQUIRED:
            1. Market rate analysis for this specific event type and location
            2. Dynamic cost estimation based on real vendor data
            3. Budget allocation recommendations based on guest count and preferences
            4. Cost optimization strategies
            5. Risk factors that could affect pricing
            6. Seasonal/demand-based pricing adjustments
            7. Value-for-money recommendations

            Provide your analysis in the following JSON format:
            {{
                "market_analysis": {{
                    "average_venue_cost": number,
                    "venue_cost_range": {{"min": number, "max": number}},
                    "catering_cost_per_person": {{"min": number, "max": number}},
                    "photography_cost_range": {{"min": number, "max": number}},
                    "decoration_cost_range": {{"min": number, "max": number}},
                    "entertainment_cost_range": {{"min": number, "max": number}}
                }},
                "dynamic_estimation": {{
                    "optimistic_total": number,
                    "realistic_total": number,
                    "pessimistic_total": number,
                    "confidence_level": "high|medium|low"
                }},
                "budget_allocation": {{
                    "venue_percentage": number,
                    "catering_percentage": number,
                    "photography_percentage": number,
                    "decoration_percentage": number,
                    "entertainment_percentage": number,
                    "miscellaneous_percentage": number
                }},
                "cost_optimization": [
                    "specific optimization strategy 1",
                    "specific optimization strategy 2"
                ],
                "risk_factors": [
                    "risk factor 1",
                    "risk factor 2"
                ],
                "value_recommendations": [
                    "recommendation 1",
                    "recommendation 2"
                ]
            }}
            """
            
            system_msg = SystemMessage(content="""You are an expert event planning cost analyst with deep knowledge of Indian event market pricing. Provide accurate, data-driven cost analysis based on real market data. Be specific with numbers and practical with recommendations.""")
            human_msg = HumanMessage(content=analysis_prompt)
            
            response = self.llm.invoke([system_msg, human_msg])
            
            try:
                # Parse AI response
                cost_analysis = json.loads(response.content)
                
                # Add metadata
                cost_analysis["metadata"] = {
                    "analysis_date": datetime.now().isoformat(),
                    "data_sources": f"{len(venues)} venues, {len(vendors)} vendors",
                    "location_factor": self._get_location_factor(location),
                    "seasonal_factor": self._get_seasonal_factor(),
                    "analysis_engine": "Moonshot LLM + Real Market Data"
                }
                
                # Validate and adjust estimates if needed
                validated_analysis = self._validate_cost_estimates(cost_analysis, budget, guest_count)
                
                return validated_analysis
                
            except json.JSONDecodeError:
                logging.warning("AI response was not valid JSON, using fallback analysis")
                return await self._get_fallback_cost_analysis(event_request, venues, vendors)
                
        except Exception as e:
            logging.error(f"Dynamic cost analysis failed: {e}")
            return await self._get_fallback_cost_analysis(event_request, venues, vendors)
    
    def _get_location_factor(self, location: str) -> float:
        """Get location-based cost factor"""
        location_lower = location.lower()
        
        if any(city in location_lower for city in ["mumbai", "delhi", "bangalore", "chennai"]):
            return 1.2  # Metro cities are 20% more expensive
        elif any(city in location_lower for city in ["pune", "hyderabad", "kolkata", "ahmedabad"]):
            return 1.1  # Tier 1 cities are 10% more expensive
        else:
            return 1.0  # Tier 2/3 cities baseline
    
    def _get_seasonal_factor(self) -> float:
        """Get seasonal cost factor based on current month"""
        current_month = datetime.now().month
        
        # Wedding season (November to February) is more expensive
        if current_month in [11, 12, 1, 2]:
            return 1.15
        # Summer months (April to June) are cheaper
        elif current_month in [4, 5, 6]:
            return 0.95
        else:
            return 1.0
    
    def _validate_cost_estimates(self, analysis: Dict, budget: float, guest_count: int) -> Dict:
        """Validate and adjust cost estimates for reasonableness"""
        try:
            dynamic_est = analysis.get("dynamic_estimation", {})
            realistic_total = dynamic_est.get("realistic_total", budget)
            
            # Ensure estimates are within reasonable bounds
            per_person_cost = realistic_total / guest_count if guest_count > 0 else 0
            
            # Adjust if estimates seem unreasonable
            if per_person_cost < 800:  # Too low for realistic event
                adjustment_factor = 800 * guest_count / realistic_total
                analysis["dynamic_estimation"]["realistic_total"] = int(realistic_total * adjustment_factor)
                analysis["dynamic_estimation"]["optimistic_total"] = int(dynamic_est.get("optimistic_total", realistic_total) * adjustment_factor)
                analysis["dynamic_estimation"]["pessimistic_total"] = int(dynamic_est.get("pessimistic_total", realistic_total) * adjustment_factor)
                analysis["dynamic_estimation"]["confidence_level"] = "medium"
                
            elif per_person_cost > 10000:  # Too high for typical event
                adjustment_factor = 5000 * guest_count / realistic_total
                analysis["dynamic_estimation"]["realistic_total"] = int(realistic_total * adjustment_factor)
                analysis["dynamic_estimation"]["optimistic_total"] = int(dynamic_est.get("optimistic_total", realistic_total) * adjustment_factor)
                analysis["dynamic_estimation"]["pessimistic_total"] = int(dynamic_est.get("pessimistic_total", realistic_total) * adjustment_factor)
                analysis["dynamic_estimation"]["confidence_level"] = "medium"
            
            return analysis
            
        except Exception as e:
            logging.warning(f"Cost validation failed: {e}")
            return analysis
    
    async def _get_fallback_cost_analysis(self, event_request: Dict[str, Any], venues: List[Dict], vendors: List[Dict]) -> Dict[str, Any]:
        """Fallback cost analysis when AI is not available"""
        try:
            guest_count = event_request.get("guest_count", 50)
            budget = event_request.get("budget", 100000)
            location = event_request.get("location", "")
            event_type = event_request.get("event_type", "")
            
            # Basic cost estimation based on guest count and location
            location_factor = self._get_location_factor(location)
            seasonal_factor = self._get_seasonal_factor()
            
            # Base costs per person
            base_costs = {
                "wedding": {"min": 2000, "max": 5000},
                "corporate": {"min": 1200, "max": 3000},
                "birthday": {"min": 800, "max": 2000},
                "anniversary": {"min": 1000, "max": 2500}
            }
            
            event_costs = base_costs.get(event_type.lower(), base_costs["birthday"])
            min_per_person = int(event_costs["min"] * location_factor * seasonal_factor)
            max_per_person = int(event_costs["max"] * location_factor * seasonal_factor)
            
            optimistic_total = min_per_person * guest_count
            realistic_total = int((min_per_person + max_per_person) / 2 * guest_count)
            pessimistic_total = max_per_person * guest_count
            
            return {
                "market_analysis": {
                    "average_venue_cost": realistic_total * 0.35,
                    "venue_cost_range": {"min": optimistic_total * 0.3, "max": pessimistic_total * 0.4},
                    "catering_cost_per_person": {"min": min_per_person * 0.4, "max": max_per_person * 0.4},
                    "photography_cost_range": {"min": 8000, "max": 25000},
                    "decoration_cost_range": {"min": 10000, "max": 40000},
                    "entertainment_cost_range": {"min": 5000, "max": 20000}
                },
                "dynamic_estimation": {
                    "optimistic_total": optimistic_total,
                    "realistic_total": realistic_total,
                    "pessimistic_total": pessimistic_total,
                    "confidence_level": "medium"
                },
                "budget_allocation": {
                    "venue_percentage": 35,
                    "catering_percentage": 30,
                    "photography_percentage": 15,
                    "decoration_percentage": 15,
                    "entertainment_percentage": 5
                },
                "cost_optimization": [
                    "Book venues and vendors in advance for early bird discounts",
                    "Consider package deals for multiple services",
                    "Opt for weekday events for reduced costs",
                    "Negotiate group rates for catering"
                ],
                "risk_factors": [
                    "Peak season pricing (November-February)",
                    "Last-minute bookings incur premium charges",
                    "Weather dependency for outdoor events",
                    "Guest count changes affecting final costs"
                ],
                "value_recommendations": [
                    f"Focus on essential services within ₹{budget} budget",
                    "Prioritize venue and catering as primary cost drivers",
                    "Consider local vendors to reduce transportation costs",
                    "Plan for 10-15% contingency for unexpected expenses"
                ],
                "metadata": {
                    "analysis_date": datetime.now().isoformat(),
                    "data_sources": "Fallback estimation model",
                    "location_factor": location_factor,
                    "seasonal_factor": seasonal_factor,
                    "analysis_engine": "Fallback Cost Model"
                }
            }
            
        except Exception as e:
            logging.error(f"Fallback cost analysis failed: {e}")
            return {
                "dynamic_estimation": {
                    "realistic_total": budget,
                    "confidence_level": "low"
                },
                "error": "Cost analysis unavailable"
            }

# Factory function
async def analyze_event_costs(event_request: Dict[str, Any], venues: List[Dict], vendors: List[Dict]) -> Dict[str, Any]:
    """
    Factory function to create and execute dynamic cost estimation
    """
    agent = DynamicCostEstimationAgent()
    return await agent.analyze_market_costs(event_request, venues, vendors)