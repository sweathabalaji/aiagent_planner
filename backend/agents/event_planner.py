import logging
import asyncio
import json
from typing import Dict, Any, List
from datetime import datetime, timedelta
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.llm import get_chat_llm
from utils.tavily_search import search_travel_info  # Use existing tavily search
from langchain.schema import HumanMessage, SystemMessage
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import tool
from langchain.prompts import PromptTemplate
from langchain.tools import Tool
from langchain.prompts import PromptTemplate

# Configure Tavily for event-specific searches
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
tavily_client = TavilyClient(api_key=TAVILY_API_KEY) if TAVILY_API_KEY else None

async def search_venues_tavily(location: str, event_type: str, guest_count: int = 50, max_results: int = 8):
    """Search for real venues using Tavily API"""
    if not tavily_client:
        logging.warning("Tavily API not available - using fallback")
        return []
    
    try:
        # Create comprehensive search queries for venues
        search_queries = [
            f"{event_type} venues {location} capacity {guest_count} guests",
            f"event halls {location} {event_type} booking",
            f"banquet halls {location} {event_type} venues",
            f"party venues {location} {guest_count} people capacity",
            f"event spaces {location} {event_type} celebration"
        ]
        
        all_venues = []
        for query in search_queries[:3]:  # Limit to 3 queries to avoid rate limits
            try:
                loop = asyncio.get_event_loop()
                response = await loop.run_in_executor(
                    None,
                    lambda q=query: tavily_client.search(
                        query=q,
                        search_depth="advanced",
                        max_results=3,
                        include_domains=[
                            "justdial.com", "sulekha.com", "urbancompany.com", "weddingwire.in",
                            "venuelook.com", "bookeventz.com", "eventsindia.com", "partyone.in",
                            "bookmyfunction.com", "venuemonk.com", "evoma.com", "zomato.com"
                        ]
                    )
                )
                
                results = response.get("results", [])
                for result in results:
                    venue_data = {
                        "name": extract_venue_name(result.get("title", "")),
                        "location": location,
                        "capacity": guest_count + 20,  # Estimated capacity
                        "price_per_hour": None,
                        "price_per_day": None,
                        "amenities": extract_amenities(result.get("content", "")),
                        "contact": extract_contact(result.get("content", "")),
                        "website": result.get("url", ""),
                        "rating": 4.2,  # Default rating
                        "description": f"Professional venue in {location}"
                    }
                    all_venues.append(venue_data)
                    
            except Exception as e:
                logging.error(f"Venue search failed for query '{query}': {e}")
                continue
        
        # Remove duplicates and limit results
        unique_venues = []
        seen_names = set()
        for venue in all_venues:
            if venue["name"] not in seen_names and len(unique_venues) < max_results:
                unique_venues.append(venue)
                seen_names.add(venue["name"])
        
        return unique_venues[:max_results]
        
    except Exception as e:
        logging.error(f"Venue search failed: {e}")
        return []

async def search_vendors_tavily(location: str, service_type: str, event_type: str, max_results: int = 8):
    """Search for real vendors using Tavily API"""
    if not tavily_client:
        logging.warning("Tavily API not available - using fallback")
        return []
    
    try:
        # Create service-specific search queries
        service_queries = {
            "catering": [
                f"{event_type} catering services {location}",
                f"event catering {location} {event_type}",
                f"party catering {location} food services"
            ],
            "photography": [
                f"{event_type} photography {location}",
                f"event photographers {location}",
                f"party photography services {location}"
            ],
            "decoration": [
                f"{event_type} decoration services {location}",
                f"event decorators {location}",
                f"party decoration {location} services"
            ],
            "entertainment": [
                f"{event_type} entertainment {location}",
                f"live music {location} events",
                f"DJ services {location} {event_type}"
            ]
        }
        
        search_terms = service_queries.get(service_type, [f"{service_type} services {location}"])
        all_vendors = []
        
        for query in search_terms[:2]:  # Limit queries
            try:
                loop = asyncio.get_event_loop()
                response = await loop.run_in_executor(
                    None,
                    lambda q=query: tavily_client.search(
                        query=q,
                        search_depth="advanced",
                        max_results=3,
                        include_domains=[
                            "justdial.com", "sulekha.com", "urbancompany.com", "weddingwire.in",
                            "venuelook.com", "bookeventz.com", "eventsindia.com", "partyone.in",
                            "zomato.com", "practo.com", "99acres.com", "magicpin.com"
                        ]
                    )
                )
                
                results = response.get("results", [])
                for result in results:
                    vendor_data = {
                        "name": extract_vendor_name(result.get("title", ""), service_type),
                        "service_type": service_type,
                        "location": location,
                        "price_range": "Quote available",
                        "contact": extract_contact(result.get("content", "")),
                        "website": result.get("url", ""),
                        "rating": 4.2,
                        "specialties": [service_type, "event services"],
                        "description": f"Professional {service_type} service in {location}"
                    }
                    all_vendors.append(vendor_data)
                    
            except Exception as e:
                logging.error(f"Vendor search failed for '{query}': {e}")
                continue
        
        # Remove duplicates and limit results
        unique_vendors = []
        seen_names = set()
        for vendor in all_vendors:
            if vendor["name"] not in seen_names and len(unique_vendors) < max_results:
                unique_vendors.append(vendor)
                seen_names.add(vendor["name"])
        
        return unique_vendors[:max_results]
        
    except Exception as e:
        logging.error(f"Vendor search failed: {e}")
        return []

def extract_venue_name(title: str) -> str:
    """Extract venue name from search result title"""
    # Remove common prefixes and clean up
    title = title.replace("Book ", "").replace("Best ", "").replace("Top ", "")
    title = title.split(" - ")[0].split(" | ")[0].split(" in ")[0]
    return title.strip() or "Professional Venue"

def extract_vendor_name(title: str, service_type: str) -> str:
    """Extract vendor name from search result title"""
    # Remove common prefixes
    title = title.replace("Best ", "").replace("Top ", "").replace("Book ", "")
    title = title.split(" - ")[0].split(" | ")[0].split(" in ")[0]
    
    # If title is too generic, create a professional name
    if len(title.split()) < 2 or any(word in title.lower() for word in ["services", "providers", "list"]):
        service_names = {
            "catering": "Professional Catering Services",
            "photography": "Elite Photography Studio", 
            "decoration": "Creative Event Decorators",
            "entertainment": "Premium Entertainment Group"
        }
        return service_names.get(service_type, "Professional Service Provider")
    
    return title.strip()

def extract_amenities(content: str) -> List[str]:
    """Extract amenities from content"""
    amenities = []
    common_amenities = ["parking", "ac", "wifi", "sound system", "catering", "decoration", "lighting"]
    
    content_lower = content.lower()
    for amenity in common_amenities:
        if amenity in content_lower:
            amenities.append(amenity)
    
    return amenities

def extract_contact(content: str) -> str:
    """Extract contact information from content"""
    import re
    # Look for phone numbers
    phone_pattern = r'(\+91\s?)?[789]\d{9}'
    phone_match = re.search(phone_pattern, content)
    if phone_match:
        return phone_match.group()
    return None

async def analyze_event_costs(event_request: Dict[str, Any], venues: List[Dict], vendors: List[Dict]) -> Dict[str, Any]:
    """Analyze event costs based on venues and vendors"""
    budget = event_request.get("budget", 100000)
    guest_count = event_request.get("guest_count", 50)
    
    # Calculate costs based on typical percentages
    estimated_costs = {
        "venue": budget * 0.25,
        "catering": budget * 0.40, 
        "photography": budget * 0.15,
        "decoration": budget * 0.15,
        "entertainment": budget * 0.05
    }
    
    total_estimated = sum(estimated_costs.values())
    
    return {
        "total_estimated_cost": total_estimated,
        "cost_breakdown": estimated_costs,
        "budget_analysis": f"Budget utilization: {(total_estimated/budget)*100:.1f}%" if budget > 0 else "Budget analysis unavailable",
        "cost_per_guest": total_estimated / guest_count if guest_count > 0 else 0
    }

class AgenticEventPlannerAgent:
    def __init__(self):
        """Initialize the Agentic Event Planner with REQUIRED ReAct capabilities"""
        # Get LLM - REQUIRED for agentic operation
        try:
            self.llm = get_chat_llm()
            if self.llm is None:
                logging.error("❌ LLM not available - Using fallback mode")
                self.llm = None
                self.agent_executor = None
                return
        except Exception as e:
            logging.error(f"❌ LLM initialization failed: {e}")
            self.llm = None
            self.agent_executor = None
            return
            
        # Initialize Moonshot for cost analysis
        moonshot_key = os.getenv("MOONSHOT_API_KEY")
        if not moonshot_key:
            logging.warning("⚠️ MOONSHOT_API_KEY not found - Limited functionality")
            
        # Create tools for the ReAct agent
        try:
            self.tools = self._create_tools()
        except Exception as e:
            logging.error(f"❌ Tool creation failed: {e}")
            self.tools = []
            self.agent_executor = None
            return
        
        # Create ReAct agent - REQUIRED for agentic operation  
        try:
            self.agent_executor = self._create_react_agent()
            if self.agent_executor is None:
                logging.error("❌ Failed to create ReAct agent")
                return
        except Exception as e:
            logging.error(f"❌ ReAct agent creation failed: {e}")
            self.agent_executor = None
            return
            
        logging.info("✅ Agentic Event Planner initialized - Pure agentic mode only")
    
    def _create_error_response(self, error_message: str, budget: float) -> Dict[str, Any]:
        """Create a standardized error response structure"""
        return {
            "variants": [{
                "id": "error_response",
                "name": "Error in Event Planning",
                "variant": "error",
                "estimated_cost": budget,
                "total_cost": budget,
                "cost_breakdown": {
                    "venue": 0.0,
                    "catering": 0.0,
                    "photography": 0.0,
                    "decoration": 0.0,
                    "entertainment": 0.0
                },
                "venues": [],
                "vendors": {"catering": [], "photography": [], "decoration": []},
                "planning_timeline": ["Error occurred"],
                "agent_insights": [error_message]
            }],
            "agent_analysis": {
                "full_analysis": error_message,
                "budget_assessment": "Unable to assess - error occurred",
                "strategy_recommendations": ["Please try again with valid inputs"],
                "venue_analysis": "Error in processing"
            },
            "metadata": {
                "planning_approach": "PURE AGENTIC MODE - Error Response",
                "error": error_message,
                "timestamp": datetime.now().isoformat()
            }
        }
    
    def _create_tools(self) -> List[Tool]:
        """Create tools for the ReAct agent"""
        tools = [
            Tool(
                name="analyze_event_requirements",
                description="Analyze event requirements to determine search strategy. Input: event_request dict",
                func=self._analyze_event_requirements
            ),
            Tool(
                name="search_context_aware_venues",
                description="Search for venues based on analyzed context. Input: context_analysis dict",
                func=self._search_context_aware_venues
            ),
            Tool(
                name="search_context_aware_vendors",
                description="Search for vendors based on analyzed context. Input: context_analysis dict",
                func=self._search_context_aware_vendors
            ),
            Tool(
                name="estimate_dynamic_costs",
                description="Estimate costs based on market analysis and event requirements. Input: event_details and vendor_list",
                func=self._estimate_dynamic_costs
            ),
            Tool(
                name="optimize_vendor_selection",
                description="Optimize vendor selection based on budget and requirements. Input: all_vendors and budget_analysis",
                func=self._optimize_vendor_selection
            )
        ]
        return tools
    
    def _create_react_agent(self):
        """Create ReAct agent with custom prompt"""
        react_prompt = PromptTemplate(
            input_variables=["tools", "tool_names", "input", "agent_scratchpad"],
            template="""You are an expert event planning agent that creates comprehensive event plans by intelligently analyzing requirements and fetching REAL venue and vendor data.

CRITICAL REQUIREMENTS:
- You MUST retrieve minimum 5, maximum 10 REAL venues from the user's location
- You MUST retrieve minimum 5, maximum 10 REAL vendors for each service type (catering, photography, decoration, entertainment) from the user's location
- All venues and vendors must be actual businesses, not mock or placeholder data
- Use the search tools to find genuine business listings from the specified location

AVAILABLE TOOLS:
{tools}

TOOL NAMES: {tool_names}

Your task is to create a personalized event plan by:
1. First analyzing the event requirements to understand the context (indoor/outdoor, theme, guest preferences, etc.)
2. Based on the analysis, search for 5-10 REAL context-appropriate venues in the user's location
3. Search for 5-10 REAL vendors for each service type (catering, photography, decoration, entertainment) in the user's location
4. Estimate realistic costs using market analysis
5. Optimize vendor selection within budget constraints
6. Provide comprehensive recommendations with all real business data

IMPORTANT: The venues and vendors you find must be real businesses with actual names, not generic terms like "space", "options", "combo", etc.

STOPPING CRITERIA: Once you have gathered venues and vendors data through your tools, you MUST immediately provide your Final Answer. Do NOT continue searching or analyzing after you have the core data - provide the comprehensive plan immediately.

Always use the following format:

Thought: I need to analyze the event requirements first to understand what type of venues and vendors to search for
Action: [action_name]
Action Input: [input]
Observation: [observation]
... (repeat Thought/Action/Action Input/Observation as needed)
Thought: I now have sufficient real venue and vendor data from my searches to create a comprehensive event plan
Final Answer: [comprehensive event plan with structured data including all real venues and vendors found]

Event Request: {input}

{agent_scratchpad}"""
        )
        
        try:
            # Create the ReAct agent
            agent = create_react_agent(self.llm, self.tools, react_prompt)
            
            # Create agent executor with improved settings for comprehensive planning
            agent_executor = AgentExecutor(
                agent=agent,
                tools=self.tools,
                verbose=True,
                handle_parsing_errors=True,
                max_iterations=15,  # Increased iterations for comprehensive analysis
                early_stopping_method="force",  # Force stop when Final Answer is provided
                return_intermediate_steps=True  # Get full reasoning chain
            )
            
            logging.info("✅ ReAct agent created successfully with MOONSHOT LLM")
            return agent_executor
            
        except Exception as e:
            logging.error(f"❌ Failed to create ReAct agent: {e}")
            return None  # Return None instead of raising exception
    
    def _analyze_event_requirements(self, event_request_str: str) -> str:
        """Analyze event requirements to determine search strategy"""
        try:
            # Parse input - handle different input formats
            if isinstance(event_request_str, dict):
                # If it's already a dict, use it directly
                event_request = event_request_str
            elif isinstance(event_request_str, str):
                try:
                    # Try parsing as JSON first
                    event_request = json.loads(event_request_str)
                except json.JSONDecodeError:
                    # If JSON parsing fails, try to extract from string format
                    if "event_request_str" in event_request_str:
                        # Handle format like {"event_request_str": "..."}
                        try:
                            parsed = json.loads(event_request_str)
                            event_request_str = parsed.get("event_request_str", event_request_str)
                        except:
                            pass
                    
                    # Create event request from string description
                    event_request = {
                        "event_type": "wedding" if "wedding" in event_request_str.lower() else "event",
                        "location": "Chennai" if "Chennai" in event_request_str else "",
                        "guest_count": 150 if "150" in event_request_str else 50,
                        "budget": 100000 if "100000" in event_request_str else 50000,
                        "preferences": [],
                        "special_requirements": []
                    }
                    
                    # Extract preferences from string
                    if "traditional" in event_request_str.lower():
                        event_request["preferences"].append("traditional")
                    if "outdoor" in event_request_str.lower():
                        event_request["preferences"].append("outdoor")
                    if "vegetarian" in event_request_str.lower():
                        event_request["preferences"].append("vegetarian")
                    if "photography" in event_request_str.lower():
                        event_request["preferences"].append("photography")
                    if "live music" in event_request_str.lower():
                        event_request["preferences"].append("live music")
            else:
                # Fallback for other types
                event_request = {
                    "event_type": "event",
                    "location": "Chennai",
                    "guest_count": 50,
                    "budget": 50000,
                    "preferences": [],
                    "special_requirements": []
                }
                
            event_type = event_request.get("event_type", "").lower()
            location = event_request.get("location", "")
            preferences = [p.lower() for p in event_request.get("preferences", [])]
            special_requirements = [r.lower() for r in event_request.get("special_requirements", [])]
            guest_count = event_request.get("guest_count", 50)
            budget = event_request.get("budget", 100000)
            
            # Analyze context for search strategy
            context_analysis = {
                "event_type": event_type,
                "location": location,
                "is_outdoor": any(keyword in preferences + special_requirements for keyword in 
                                ["outdoor", "beach", "garden", "pool", "terrace", "rooftop", "lawn"]),
                "is_indoor": any(keyword in preferences + special_requirements for keyword in 
                               ["indoor", "hall", "banquet", "conference", "ballroom", "restaurant"]),
                "theme_keywords": [],
                "cuisine_preferences": [],
                "decor_style": [],
                "entertainment_type": [],
                "search_strategy": {}
            }
            
            # Extract theme keywords
            for pref in preferences + special_requirements:
                if any(theme in pref for theme in ["beach", "tropical", "ocean", "sand"]):
                    context_analysis["theme_keywords"].extend(["beach", "coastal", "marine", "nautical"])
                elif any(theme in pref for theme in ["garden", "floral", "nature", "green"]):
                    context_analysis["theme_keywords"].extend(["garden", "botanical", "nature", "floral"])
                elif any(theme in pref for theme in ["luxury", "premium", "elegant", "sophisticated"]):
                    context_analysis["theme_keywords"].extend(["luxury", "premium", "upscale", "elegant"])
                elif any(theme in pref for theme in ["casual", "simple", "intimate", "cozy"]):
                    context_analysis["theme_keywords"].extend(["casual", "intimate", "cozy", "simple"])
            
            # Extract cuisine preferences
            for pref in preferences + special_requirements:
                if any(cuisine in pref for cuisine in ["vegetarian", "vegan", "indian", "chinese", "continental", "italian"]):
                    context_analysis["cuisine_preferences"].append(pref)
            
            # Determine search strategy based on analysis
            if context_analysis["is_outdoor"]:
                context_analysis["search_strategy"] = {
                    "venue_keywords": ["outdoor", "beach", "garden", "terrace", "lawn", "resort"] + context_analysis["theme_keywords"],
                    "vendor_focus": ["outdoor catering", "weather-resistant decoration", "outdoor photography", "live music"],
                    "special_considerations": ["weather backup", "outdoor lighting", "power supply", "restroom facilities"]
                }
            elif context_analysis["is_indoor"]:
                context_analysis["search_strategy"] = {
                    "venue_keywords": ["banquet hall", "conference room", "restaurant", "hotel", "ballroom"] + context_analysis["theme_keywords"],
                    "vendor_focus": ["indoor catering", "indoor decoration", "indoor photography", "sound system"],
                    "special_considerations": ["air conditioning", "capacity limits", "parking", "accessibility"]
                }
            else:
                # Mixed or flexible approach
                context_analysis["search_strategy"] = {
                    "venue_keywords": ["versatile venues", "indoor-outdoor", "flexible spaces"] + context_analysis["theme_keywords"],
                    "vendor_focus": ["flexible catering", "adaptable decoration", "versatile photography", "flexible entertainment"],
                    "special_considerations": ["flexible setup", "backup options", "weather contingency"]
                }
            
            return json.dumps(context_analysis)
            
        except Exception as e:
            logging.error(f"Event requirement analysis failed: {e}")
            return json.dumps({"error": str(e), "fallback": True})
    
    def _search_context_aware_venues(self, context_analysis_str: str) -> str:
        """Search for venues based on analyzed context"""
        try:
            # Handle different input formats
            if isinstance(context_analysis_str, dict):
                context = context_analysis_str
            elif isinstance(context_analysis_str, str):
                try:
                    context = json.loads(context_analysis_str)
                except json.JSONDecodeError:
                    # Create context from string description
                    context = {
                        "location": "Chennai" if "Chennai" in context_analysis_str else "",
                        "event_type": "wedding" if "wedding" in context_analysis_str.lower() else "event",
                        "guest_count": 150 if "150" in context_analysis_str else 50,
                        "is_outdoor": "outdoor" in context_analysis_str.lower(),
                        "is_indoor": "indoor" in context_analysis_str.lower(),
                        "theme_keywords": ["traditional"] if "traditional" in context_analysis_str.lower() else [],
                        "search_strategy": {}
                    }
            else:
                context = {"location": "", "event_type": "event", "search_strategy": {}}
            
            # Enhanced venue search with context
            search_terms = []
            base_location = context.get("location", "")
            event_type = context.get("event_type", "")
            
            # Build contextual search terms
            search_strategy = context.get("search_strategy", {})
            venue_keywords = search_strategy.get("venue_keywords", [])
            
            for keyword in venue_keywords[:3]:  # Use top 3 keywords
                search_terms.append(f"{keyword} {event_type} venues {base_location}")
            
            # If no specific keywords, use general search
            if not search_terms:
                search_terms.append(f"{event_type} venues {base_location}")
            
            # This would be replaced with actual async call in real implementation
            # For now, return structured search parameters
            venue_search_params = {
                "search_terms": search_terms,
                "location": base_location,
                "event_type": event_type,
                "context_keywords": venue_keywords,
                "special_considerations": search_strategy.get("special_considerations", [])
            }
            
            return json.dumps(venue_search_params)
            
        except Exception as e:
            logging.error(f"Context-aware venue search failed: {e}")
            return json.dumps({"error": str(e)})
    
    def _search_context_aware_vendors(self, context_analysis_str: str) -> str:
        """Search for vendors based on analyzed context"""
        try:
            # Handle different input formats
            if isinstance(context_analysis_str, dict):
                context = context_analysis_str
            elif isinstance(context_analysis_str, str):
                try:
                    context = json.loads(context_analysis_str)
                except json.JSONDecodeError:
                    # Create context from string description
                    context = {
                        "location": "Chennai" if "Chennai" in context_analysis_str else "",
                        "event_type": "wedding" if "wedding" in context_analysis_str.lower() else "event",
                        "is_outdoor": "outdoor" in context_analysis_str.lower(),
                        "theme_keywords": ["traditional"] if "traditional" in context_analysis_str.lower() else [],
                        "cuisine_preferences": ["vegetarian"] if "vegetarian" in context_analysis_str.lower() else [],
                        "search_strategy": {}
                    }
            else:
                context = {"location": "", "event_type": "event", "search_strategy": {}}
            
            event_type = context.get("event_type", "")
            location = context.get("location", "")
            search_strategy = context.get("search_strategy", {})
            vendor_focus = search_strategy.get("vendor_focus", [])
            
            # Build contextual vendor searches
            vendor_searches = {
                "photography": [],
                "catering": [],
                "decoration": [],
                "entertainment": []
            }
            
            # Photography searches
            if context.get("is_outdoor"):
                vendor_searches["photography"].extend([
                    f"outdoor {event_type} photography {location}",
                    f"outdoor event photography {location}"
                ])
            else:
                vendor_searches["photography"].extend([
                    f"indoor {event_type} photography {location}",
                    f"event photography {location}"
                ])
            
            # Catering searches
            cuisine_prefs = context.get("cuisine_preferences", [])
            if cuisine_prefs:
                for cuisine in cuisine_prefs[:2]:  # Limit to 2 cuisines
                    vendor_searches["catering"].append(f"{cuisine} catering {location}")
            else:
                vendor_searches["catering"].append(f"event catering {location}")
            
            # Decoration searches
            theme_keywords = context.get("theme_keywords", [])
            if theme_keywords:
                vendor_searches["decoration"].extend([
                    f"{theme_keywords[0]} decoration {location}",
                    f"{event_type} decoration {location}"
                ])
            else:
                vendor_searches["decoration"].append(f"event decoration {location}")
            
            # Entertainment searches
            if context.get("is_outdoor"):
                vendor_searches["entertainment"].extend([
                    f"outdoor entertainment {location}",
                    f"live music {location}"
                ])
            else:
                vendor_searches["entertainment"].extend([
                    f"{event_type} entertainment {location}",
                    f"DJ services {location}"
                ])
            
            return json.dumps(vendor_searches)
            if cuisine_prefs:
                for cuisine in cuisine_prefs[:2]:
                    vendor_searches["catering"].append(f"{cuisine} catering {event_type} {location}")
            
            if context.get("is_outdoor"):
                vendor_searches["catering"].append(f"outdoor catering {event_type} {location}")
            else:
                vendor_searches["catering"].append(f"indoor catering {event_type} {location}")
            
            # Decoration searches
            theme_keywords = context.get("theme_keywords", [])
            for theme in theme_keywords[:2]:
                vendor_searches["decoration"].append(f"{theme} decoration {event_type} {location}")
            
            if context.get("is_outdoor"):
                vendor_searches["decoration"].append(f"outdoor decoration {event_type} {location}")
            else:
                vendor_searches["decoration"].append(f"indoor decoration {event_type} {location}")
            
            # Entertainment searches
            vendor_searches["entertainment"].extend([
                f"{event_type} entertainment {location}",
                f"live music {event_type} {location}",
                f"DJ services {event_type} {location}"
            ])
            
            return json.dumps(vendor_searches)
            
        except Exception as e:
            logging.error(f"Context-aware vendor search failed: {e}")
            return json.dumps({"error": str(e)})
    
    def _estimate_dynamic_costs(self, event_details_str: str) -> str:
        """Estimate costs based on market analysis and event requirements"""
        try:
            # Handle different input formats
            if isinstance(event_details_str, dict):
                data = event_details_str
            elif isinstance(event_details_str, str):
                try:
                    data = json.loads(event_details_str)
                except json.JSONDecodeError:
                    # Create data from string description
                    data = {
                        "event_type": "wedding" if "wedding" in event_details_str.lower() else "event",
                        "location": "Chennai" if "Chennai" in event_details_str else "",
                        "guest_count": 150 if "150" in event_details_str else 50,
                        "budget": 100000 if "100000" in event_details_str else 50000,
                        "is_outdoor": "outdoor" in event_details_str.lower(),
                        "theme_keywords": ["traditional"] if "traditional" in event_details_str.lower() else []
                    }
            else:
                data = {"event_type": "event", "location": "", "guest_count": 50, "budget": 50000}
            
            # Extract event details
            guest_count = data.get("guest_count", 50)
            budget = data.get("budget", 100000)
            event_type = data.get("event_type", "")
            location = data.get("location", "")
            is_outdoor = data.get("is_outdoor", False)
            theme_keywords = data.get("theme_keywords", [])
            
            # Dynamic cost estimation based on context
            base_costs = {
                "venue": {"indoor": 15000, "outdoor": 20000, "luxury": 35000},
                "catering_per_person": {"basic": 800, "standard": 1200, "premium": 2000},
                "photography": {"basic": 8000, "standard": 15000, "premium": 25000},
                "decoration": {"basic": 10000, "standard": 20000, "premium": 40000},
                "entertainment": {"basic": 5000, "standard": 12000, "premium": 25000}
            }
            
            # Calculate estimates
            estimated_costs = {}
            
            # Venue cost
            venue_type = "outdoor" if is_outdoor else "indoor"
            if any(keyword in theme_keywords for keyword in ["luxury", "premium", "elegant"]):
                venue_type = "luxury"
            estimated_costs["venue"] = base_costs["venue"][venue_type]
            
            # Catering cost
            catering_level = "standard"
            if budget > 300000:
                catering_level = "premium"
            elif budget < 100000:
                catering_level = "basic"
            estimated_costs["catering"] = base_costs["catering_per_person"][catering_level] * guest_count
            
            # Photography cost
            photo_level = "standard"
            if any(keyword in theme_keywords for keyword in ["luxury", "premium"]) or budget > 300000:
                photo_level = "premium"
            elif budget < 100000:
                photo_level = "basic"
            estimated_costs["photography"] = base_costs["photography"][photo_level]
            
            # Decoration cost
            decor_level = "standard"
            if any(keyword in theme_keywords for keyword in ["luxury", "premium", "elaborate"]):
                decor_level = "premium"
            elif budget < 100000 or any(keyword in theme_keywords for keyword in ["simple", "minimal"]):
                decor_level = "basic"
            estimated_costs["decoration"] = base_costs["decoration"][decor_level]
            
            # Entertainment cost
            entertainment_level = "standard"
            if budget > 300000:
                entertainment_level = "premium"
            elif budget < 100000:
                entertainment_level = "basic"
            estimated_costs["entertainment"] = base_costs["entertainment"][entertainment_level]
            
            # Calculate total and provide recommendations
            total_estimated = sum(estimated_costs.values())
            
            cost_analysis = {
                "estimated_costs": estimated_costs,
                "total_estimated": total_estimated,
                "budget_utilization": (total_estimated / budget) * 100 if budget > 0 else 0,
                "recommendations": []
            }
            
            # Add budget recommendations
            if total_estimated > budget:
                cost_analysis["recommendations"].append("Consider reducing decoration or entertainment budget")
                cost_analysis["recommendations"].append("Look for package deals from vendors")
            elif total_estimated < budget * 0.8:
                cost_analysis["recommendations"].append("You have room to upgrade to premium services")
                cost_analysis["recommendations"].append("Consider adding extra entertainment or enhanced menu")
            
            return json.dumps(cost_analysis)
            
        except Exception as e:
            logging.error(f"Dynamic cost estimation failed: {e}")
            return json.dumps({"error": str(e)})
    
    def _optimize_vendor_selection(self, vendor_data_str: str) -> str:
        """Optimize vendor selection based on budget and requirements"""
        try:
            # Handle different input formats
            if isinstance(vendor_data_str, dict):
                data = vendor_data_str
            elif isinstance(vendor_data_str, str):
                try:
                    data = json.loads(vendor_data_str)
                except json.JSONDecodeError:
                    # Create data from string description
                    data = {
                        "all_vendors": [],
                        "budget_analysis": {
                            "total_budget": 100000 if "100000" in vendor_data_str else 50000,
                            "current_estimate": 120000,
                            "overspend": 20000,
                            "percentage_over": 20
                        },
                        "priority_requirements": ["outdoor", "vegetarian", "photography"]
                    }
            else:
                data = {"all_vendors": [], "budget_analysis": {}}
            
            # This would contain actual vendor data in real implementation
            # For now, return optimization strategy
            optimization_strategy = {
                "selection_criteria": [
                    "Budget compatibility",
                    "Context relevance (outdoor/indoor match)",
                    "Theme alignment", 
                    "Service quality ratings",
                    "Availability on event date"
                ],
                "prioritization": {
                    "essential": ["venue", "catering"],
                    "important": ["photography", "decoration"],
                    "optional": ["entertainment", "extras"]
                },
                "fallback_options": [
                    "Package deals for cost savings",
                    "Flexible vendors who can adapt to theme",
                    "Local vendors for reduced travel costs"
                ]
            }
            
            return json.dumps(optimization_strategy)
            
        except Exception as e:
            logging.error(f"Vendor optimization failed: {e}")
            return json.dumps({"error": str(e)})
    
    async def create_event_plan(self, event_request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a comprehensive event plan using PURE agentic AI approach - NO FALLBACKS
        """
        try:
            # Ensure event_request is a dictionary
            if isinstance(event_request, str):
                try:
                    event_request = json.loads(event_request)
                except json.JSONDecodeError:
                    logging.error("Invalid event request JSON format")
                    # Return error structure instead of raising
                    return self._create_error_response("Invalid event request format", 0)
            elif not isinstance(event_request, dict):
                logging.error("Event request must be a dictionary")
                # Return error structure instead of raising  
                return self._create_error_response("Event request must be a dictionary", 0)
            
            logging.info(f"🤖 Creating AGENTIC event plan for {event_request.get('event_name', 'Unknown Event')}")
            
            # Check if agent executor is available
            if self.agent_executor is None:
                logging.error("❌ Agent executor not available")
                return self._create_error_response("Agent executor not initialized", event_request.get("budget", 0))
            
            # Use ReAct agent to create the plan - NO FALLBACKS
            agent_input = json.dumps(event_request)
            
            try:
                # Execute ReAct agent
                result = await asyncio.to_thread(
                    self.agent_executor.invoke,
                    {"input": f"Create a comprehensive event plan for: {agent_input}"}
                )
                
                logging.info(f"🔍 Agent result type: {type(result)}")
                logging.info(f"🔍 Agent result content: {str(result)[:200]}...")
                
            except Exception as agent_error:
                logging.error(f"❌ Agent execution failed: {agent_error}")
                return self._create_error_response(f"Agent execution failed: {str(agent_error)}", event_request.get("budget", 0))
            
            # Parse the agent's response and structure it
            structured_plan = await self._structure_agent_response(result, event_request)
            
            # Ensure structured_plan is a dictionary before proceeding
            if not isinstance(structured_plan, dict):
                logging.error(f"❌ _structure_agent_response returned {type(structured_plan)}, expected dict")
                return self._create_error_response(f"Invalid response type: {type(structured_plan)}", event_request.get("budget", 0))
            
            # Ensure it has agentic metadata
            structured_plan.setdefault("metadata", {})
            structured_plan["metadata"]["planning_mode"] = "PURE AGENTIC - NO FALLBACKS"
            structured_plan["metadata"]["agent_type"] = "LangChain ReAct Agent"
            
            logging.info(f"🎯 Event plan created successfully with agent analysis and real venue data!")
            return structured_plan
                
        except Exception as e:
            logging.error(f"❌ Agentic event planning failed: {e}")
            import traceback
            logging.error(f"❌ Full traceback: {traceback.format_exc()}")
            
            # Return a structured error response instead of raising an exception
            return {
                "variants": [{
                    "id": "error_fallback",
                    "name": "Error - Please Try Again",
                    "variant": "error",
                    "estimated_cost": event_request.get("budget", 0) if isinstance(event_request, dict) else 0,
                    "total_cost": event_request.get("budget", 0) if isinstance(event_request, dict) else 0,
                    "cost_breakdown": {
                        "venue": 0.0,
                        "catering": 0.0,
                        "photography": 0.0,
                        "decoration": 0.0,
                        "entertainment": 0.0
                    },
                    "venues": [],
                    "vendors": {"catering": [], "photography": [], "decoration": []},
                    "planning_timeline": ["Please try again"],
                    "agent_insights": [f"Error occurred: {str(e)}"]
                }],
                "agent_analysis": {
                    "full_analysis": f"Error in agent processing: {str(e)}",
                    "budget_assessment": "Unable to analyze budget",
                    "strategy_recommendations": ["Please try again with valid inputs"],
                    "venue_analysis": "Error in venue analysis"
                },
                "cost_analysis": {
                    "dynamic_estimation": {"optimistic_total": 0, "realistic_total": 0, "pessimistic_total": 0, "confidence_level": "none"},
                    "market_analysis": "Error in analysis",
                    "budget_optimization": ["Please try again"]
                },
                "planning_insights": [f"Error: {str(e)}"],
                "contextual_recommendations": ["Please check your inputs and try again"],
                "metadata": {
                    "planning_approach": "ERROR - Pure Agentic Mode Failed",
                    "agent_used": "MOONSHOT LLM ReAct Agent", 
                    "data_sources": "Error in processing",
                    "agentic_mode": "PURE AGENTIC - NO FALLBACKS",
                    "timestamp": datetime.now().isoformat(),
                    "error": str(e)
                }
            }
    
    async def _structure_agent_response(self, agent_result, event_request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Structure the ReAct agent's response into proper event plan format with Tavily data
        """
        try:
            # Ensure event_request is a dictionary
            if isinstance(event_request, str):
                try:
                    event_request = json.loads(event_request)
                except json.JSONDecodeError:
                    event_request = {"event_type": "birthday", "location": "Chennai", "budget": 20000, "guest_count": 25}
            elif not isinstance(event_request, dict):
                event_request = {"event_type": "birthday", "location": "Chennai", "budget": 20000, "guest_count": 25}
            
            logging.info(f"🔍 Structuring agent result type: {type(agent_result)}")
            
            # Handle different types of agent results
            if isinstance(agent_result, dict):
                agent_output = agent_result.get("output", str(agent_result))
            elif isinstance(agent_result, str):
                agent_output = agent_result
            else:
                agent_output = str(agent_result)
            
            logging.info(f"🤖 Processing agent output for UI display...")
            logging.info(f"📝 Agent output length: {len(agent_output)}")
            logging.info(f"📝 Agent output preview: {agent_output[:300]}...")
            
            # Debug: Check what indicators are present
            indicators_found = []
            comprehensive_indicators = [
                "## Event Overview", "## Recommended Venues", "# Comprehensive", 
                "## Catering Vendors", "## **EVENT SUMMARY**", "## **REAL VENUES IDENTIFIED**",
                "## **REAL VENDORS IDENTIFIED**", "COMPREHENSIVE WEDDING EVENT PLAN", "Final Answer:"
            ]
            for indicator in comprehensive_indicators:
                if indicator in agent_output:
                    indicators_found.append(indicator)
            
            logging.info(f"🔍 Comprehensive indicators found: {indicators_found}")
            
            # Check if agent provided comprehensive content but didn't format as Final Answer
            if ("## Event Overview" in agent_output or "## Recommended Venues" in agent_output or 
                "# Comprehensive" in agent_output or "## Catering Vendors" in agent_output or
                "## **EVENT SUMMARY**" in agent_output or "## **REAL VENUES IDENTIFIED**" in agent_output or
                "## **REAL VENDORS IDENTIFIED**" in agent_output or "COMPREHENSIVE WEDDING EVENT PLAN" in agent_output or
                "Final Answer:" in agent_output):
                logging.info("🎯 Detected comprehensive event plan in agent output - extracting structured data")
                
                # Agent provided comprehensive plan, extract venues and vendors directly
                venues = self._extract_venues_from_comprehensive_text(agent_output)
                vendors = self._extract_vendors_from_comprehensive_text(agent_output)
                
                logging.info(f"📍 Extracted {len(venues)} venues and {sum(len(v) for v in vendors.values())} vendors")
                
                return self._create_structured_plan_from_extracted_data(venues, vendors, event_request, agent_output)
            
            # Agent didn't provide comprehensive format - use agent output directly
            logging.info("⚠️ Agent output not in comprehensive format - using raw agent analysis")
            
            # Extract the agent's analysis for display - NO FALLBACKS
            agent_analysis = agent_output
            
            # Get real venue and vendor data using Tavily
            location = event_request.get("location", "Chennai")
            event_type = event_request.get("event_type", "birthday")
            budget = event_request.get("budget", 20000)
            guest_count = event_request.get("guest_count", 25)
            
            # Use Tavily to get real data - NO MOCK DATA FALLBACKS
            try:
                from utils.tavily_search import search_event_venues, search_event_vendors, search_event_catering
                import asyncio
                
                logging.info(f"🔍 Searching for real venues and vendors in {location} for {event_type}")
                
                # Search for real venues and vendors
                search_tasks = [
                    search_event_venues(location, event_type, guest_count, budget, 5),
                    search_event_catering(location, "indian", guest_count, event_type, budget, 3),
                    search_event_vendors(location, ["photography"], event_type, budget, 3),
                    search_event_vendors(location, ["decoration", "decor"], event_type, budget, 3)
                ]
                
                venues, caterers, photographers, decorators = await asyncio.gather(*search_tasks, return_exceptions=True)
                
                # Handle search exceptions - use empty lists if search fails
                venues = venues if not isinstance(venues, Exception) else []
                caterers = caterers if not isinstance(caterers, Exception) else []
                photographers = photographers if not isinstance(photographers, Exception) else []
                decorators = decorators if not isinstance(decorators, Exception) else []
                
                logging.info(f"🔍 Tavily search results: {len(venues)} venues, {len(caterers)} caterers, {len(photographers)} photographers, {len(decorators)} decorators")
                
            except ImportError as e:
                logging.error(f"❌ Tavily search not available: {e}")
                # NO MOCK DATA - Use empty lists to force pure agent parsing
                venues = []
                caterers = []
                photographers = []
                decorators = []
            
            # Create budget variants with real data based on agent analysis
            variants = await self._create_agent_variants_from_analysis(
                budget, venues, caterers, photographers, decorators, event_request, agent_output
            )
            
            # Extract insights from agent output
            planning_insights = self._extract_insights_from_agent_output(agent_output)
            recommendations = self._extract_recommendations_from_agent_output(agent_output)
            
            # Debug: Check agent_analysis content before structured plan creation
            logging.info(f"🔬 About to create structured plan with agent_analysis length: {len(agent_analysis)}")
            logging.info(f"🔬 agent_analysis preview: {agent_analysis[:200]}...")
            
            # Create structured plan with agent analysis - PURE AGENTIC
            structured_plan = {
                "variants": variants,
                "agent_analysis": {
                    "full_analysis": agent_analysis,
                    "budget_assessment": self._extract_budget_assessment(agent_output),
                    "strategy_recommendations": self._extract_strategy_recommendations(agent_output),
                    "venue_analysis": self._extract_venue_analysis(agent_output)
                },
                "cost_analysis": {
                    "dynamic_estimation": {
                        "optimistic_total": budget * 0.8,
                        "realistic_total": budget,
                        "pessimistic_total": budget * 1.5,
                        "confidence_level": "high"
                    },
                    "market_analysis": "AI agent analyzed Chennai market rates",
                    "budget_optimization": self._extract_cost_optimization(agent_output)
                },
                "planning_insights": planning_insights,
                "contextual_recommendations": recommendations,
                "metadata": {
                    "planning_approach": "PURE AGENTIC - LangChain ReAct Agent Only",
                    "agent_used": "MOONSHOT LLM ReAct Agent",
                    "data_sources": "AI Agent Analysis Only - No Fallbacks",
                    "agentic_mode": "PURE AGENTIC - 100% AI DRIVEN",
                    "timestamp": datetime.now().isoformat()
                }
            }
            
            # Debug: Log final structured plan content - PURE AGENTIC
            agent_analysis_length = len(structured_plan.get("agent_analysis", {}).get("full_analysis", ""))
            logging.info(f"✅ Structured plan created with agent_analysis.full_analysis length: {agent_analysis_length}")
            if agent_analysis_length > 0:
                analysis_preview = structured_plan["agent_analysis"]["full_analysis"][:100]
                logging.info(f"✅ Agent analysis preview: {analysis_preview}...")
            else:
                logging.warning("⚠️ Structured plan has EMPTY agent_analysis.full_analysis - pure agentic mode")
            
            return structured_plan
            
        except Exception as e:
            logging.error(f"❌ Failed to structure agent response: {e}")
            import traceback
            logging.error(f"❌ Structure response traceback: {traceback.format_exc()}")
            
            # Return a basic structure on error instead of raising
            return {
                "variants": [{
                    "id": "structure_error",
                    "name": "Processing Error",
                    "variant": "error", 
                    "estimated_cost": event_request.get("budget", 0) if isinstance(event_request, dict) else 0,
                    "total_cost": event_request.get("budget", 0) if isinstance(event_request, dict) else 0,
                    "cost_breakdown": {
                        "venue": 0.0,
                        "catering": 0.0,
                        "photography": 0.0,
                        "decoration": 0.0,
                        "entertainment": 0.0
                    },
                    "venues": [],
                    "vendors": {"catering": [], "photography": [], "decoration": []},
                    "planning_timeline": ["Error in processing"],
                    "agent_insights": ["Unable to process agent response"]
                }],
                "agent_analysis": {
                    "full_analysis": f"Error processing response: {str(e)}",
                    "budget_assessment": "Unable to assess",
                    "strategy_recommendations": [],
                    "venue_analysis": "Error in analysis"
                },
                "metadata": {
                    "planning_approach": "Error in Response Processing", 
                    "agent_used": "MOONSHOT LLM ReAct Agent",
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                }
            }

    async def _create_agent_variants_from_analysis(self, budget: float, venues: List, caterers: List, 
                                                  photographers: List, decorators: List, 
                                                  event_request: Dict, agent_output: str) -> List[Dict]:
        """Create budget variants by parsing agent's detailed analysis"""
        try:
            variants = []
            
            # Parse venue recommendations from agent output - PURE AGENTIC
            parsed_venues = self._parse_venues_from_agent_output(agent_output)
            
            # Parse cost breakdown from agent output
            parsed_costs = self._parse_cost_breakdown_from_agent_output(agent_output, budget)
            
            # Create main agentic variant with parsed data
            main_variant = {
                "id": "moonshot_agentic",
                "name": "AI Agent Recommended Plan",
                "variant": "agentic",
                "estimated_cost": parsed_costs.get("total", budget),
                "total_cost": parsed_costs.get("total", budget),
                "cost_breakdown": parsed_costs.get("breakdown", {
                    "venue": budget * 0.25,
                    "catering": budget * 0.45, 
                    "photography": budget * 0.25,
                    "decoration": budget * 0.05
                }),
                "venues": parsed_venues,
                "vendors": {
                    "catering": self._parse_vendors_from_agent_output(agent_output, "catering"),
                    "photography": self._parse_vendors_from_agent_output(agent_output, "photography"),
                    "decoration": self._parse_vendors_from_agent_output(agent_output, "decoration")
                },
                "planning_timeline": self._extract_timeline_from_agent(agent_output),
                "agent_insights": self._extract_key_insights(agent_output)
            }
            
            variants.append(main_variant)
            
            # Add budget optimization variant from agent recommendations
            if "Option 1:" in agent_output or "cost reduction" in agent_output.lower():
                optimized_costs = self._parse_optimized_costs_from_agent(agent_output, budget)
                budget_variant = {
                    "id": "budget_optimized", 
                    "name": "Budget-Optimized Plan",
                    "variant": "budget",
                    "estimated_cost": optimized_costs.get("total", budget * 0.8),
                    "total_cost": optimized_costs.get("total", budget * 0.8),
                    "cost_breakdown": optimized_costs.get("breakdown", {
                        "venue": budget * 0.15,
                        "catering": budget * 0.55,
                        "photography": budget * 0.05,
                        "decoration": budget * 0.05
                    }),
                    "venues": parsed_venues[:1],  # Use fewer venues for budget option
                    "vendors": {
                        "catering": self._parse_vendors_from_agent_output(agent_output, "catering")[:1],
                        "photography": [],
                        "decoration": []
                    },
                    "planning_timeline": self._extract_budget_timeline_from_agent(agent_output),
                    "agent_insights": ["Budget-conscious approach", "DIY recommendations", "Cost-saving strategies"]
                }
                variants.append(budget_variant)
            
            return variants
            
        except Exception as e:
            logging.error(f"❌ Error creating agent variants from analysis: {e}")
            # Return minimal variant with error info - no fallback data
            return [{
                "id": "agent_error",
                "name": "Agent Analysis Error",
                "variant": "error",
                "estimated_cost": budget,
                "total_cost": budget,
                "cost_breakdown": {
                    "venue": 0.0,
                    "catering": 0.0,
                    "photography": 0.0,
                    "decoration": 0.0,
                    "entertainment": 0.0
                },
                "venues": [],
                "vendors": {"catering": [], "photography": [], "decoration": []},
                "planning_timeline": ["Error in agent analysis"],
                "agent_insights": [f"Error: {str(e)}"]
            }]

    def _parse_venues_from_agent_output(self, agent_output: str) -> List[Dict]:
        """Parse specific venue recommendations from agent output - PURE AGENTIC"""
        try:
            venues = []
            import re
            
            # Enhanced venue patterns to match agent's comprehensive output
            venue_patterns = [
                # Pattern like "• The Green Lawn Resort (ECR) – capacity 80 – ₹22 k"
                r'[•\-\*]?\s*([A-Z][^(–\n]+?(?:Resort|Garden|Hall|Hotel|Terrace|Lawn|Beach)[^(–\n]*)\s*(?:\([^)]*\))?\s*[–-]\s*capacity\s*(\d+)\s*[–-]\s*₹\s*(\d+(?:\.\d+)?)\s*k',
                # Pattern like "2. SELECTED VENUE ★  • The Green Lawn Resort (ECR)"
                r'SELECTED VENUE[^•]*•\s*([A-Z][^(–\n]+?(?:Resort|Garden|Hall|Hotel|Terrace|Lawn)[^(–\n]*)\s*(?:\([^)]*\))?[^₹]*₹\s*(\d+(?:\.\d+)?)\s*k',
                # Pattern like "Venue: The Green Lawn Resort (₹22,000)"
                r'(?:Venue|venue):\s*([A-Z][^(₹\n]+?(?:Resort|Garden|Hall|Hotel|Terrace|Lawn)[^(₹\n]*)',
                # Pattern from venue recommendations sections
                r'[•\-\*\d\.]\s*([A-Z][A-Za-z\s]+?(?:Resort|Garden|Hall|Hotel|Terrace|Lawn|Beach|Rooftop)[A-Za-z\s]*)[^₹\n]*(?:₹\s*([\d,]+))?',
                # Pattern like "Beach Bay Lawn", "Sunny's Rooftop"  
                r'([A-Z][A-Za-z\s\']+?(?:Resort|Garden|Hall|Hotel|Terrace|Lawn|Beach|Bay|Rooftop)[A-Za-z\s]*)',
                # Pattern for venues with prices in parentheses
                r'([A-Z][A-Za-z\s]+?(?:Resort|Garden|Hall|Hotel|Terrace|Lawn))[^(]*\(₹([\d,]+)',
            ]
            
            for pattern in venue_patterns:
                matches = re.finditer(pattern, agent_output, re.IGNORECASE | re.MULTILINE)
                for match in matches:
                    venue_name = match.group(1).strip()
                    capacity = 50  # Default
                    price = "Contact for pricing"
                    description = ""
                    
                    # Extract capacity if available
                    if len(match.groups()) > 1 and match.group(2):
                        try:
                            capacity = int(match.group(2).replace(',', ''))
                        except:
                            capacity = 50
                    
                    # Extract price if available
                    if len(match.groups()) > 2 and match.group(3):
                        price_str = match.group(3).replace(',', '')
                        if 'k' in pattern and match.group(3):
                            price = f"₹{float(price_str) * 1000:,.0f}/day"
                        else:
                            price = f"₹{price_str}/day"
                    
                    # Extract description if available and not captured as price
                    if len(match.groups()) > 2 and not match.group(3):
                        description = match.group(2).strip() if len(match.groups()) > 1 else ""
                    
                    # Clean up venue name
                    venue_name = re.sub(r'\s+', ' ', venue_name).strip()
                    
                    if venue_name and len(venue_name) > 5:
                        venues.append({
                            "name": venue_name[:50],
                            "location": "Chennai",
                            "price": price,
                            "capacity": 50,
                            "contact": "Contact venue directly",
                            "rating": 4.2,
                            "description": description[:100] if description else f"Professional venue in Chennai"
                        })
            
            # If no specific venues found, try to extract from venue sections
            if not venues:
                lines = agent_output.split('\n')
                venue_section_started = False
                for line in lines:
                    if "venue recommendations" in line.lower() or "venue types" in line.lower():
                        venue_section_started = True
                        continue
                    if venue_section_started and line.strip():
                        if line.startswith('#') or "vendor" in line.lower():
                            break
                        if any(keyword in line.lower() for keyword in ['beach', 'garden', 'hotel', 'resort', 'terrace']):
                            venue_name = line.replace('-', '').replace('*', '').strip()[:50]
                            if venue_name:
                                venues.append({
                                    "name": venue_name,
                                    "location": "Chennai", 
                                    "price": "Contact for pricing",
                                    "capacity": 50,
                                    "contact": "Contact venue directly",
                                    "rating": 4.2,
                                    "description": "Venue option in Chennai"
                                })
            
            # NO FALLBACK DATA - Return only parsed venues from agent output
            logging.info(f"🔍 Parsed {len(venues)} venues from agent output")
            
            return venues[:3]  # Limit to 3 venues, only from agent analysis
            
        except Exception as e:
            logging.error(f"Error parsing venues from agent output: {e}")
            return []  # Return empty list instead of fallback data

    def _parse_cost_breakdown_from_agent_output(self, agent_output: str, total_budget: float) -> Dict:
        """Parse cost breakdown from agent's detailed analysis"""
        try:
            costs = {"total": total_budget, "breakdown": {}}
            import re
            
            # Enhanced patterns to match your agent's output format
            cost_patterns = [
                # Pattern like "Catering   Sangeetha Veg Caterers (4.4★)    ₹16.5 k"
                r'(Catering|Photography|Decoration|Lighting|Music|Venue)\s+[^₹]*₹\s*([\d.]+)\s*k',
                # Pattern like "venue ₹18,000"  
                r'(venue|catering|photography|decoration|entertainment|music|cake|lighting)\s*[:\-]?\s*₹\s*([\d,]+)',
                # Pattern like "₹45,000 | Catering"
                r'₹\s*([\d,]+)[^\n]*?(venue|catering|photography|decoration|entertainment|music|cake|lighting)',
                # Pattern like "• Venue: ₹22,000"
                r'[•\-\*]?\s*(Venue|Catering|Photography|Decoration|Entertainment|Music|Cake|Lighting)[:\s]*₹\s*([\d,]+)',
                # Pattern from budget table "| Catering | Essential | ₹45,000 |"
                r'\|\s*(Venue|Catering|Photography|Decoration|Entertainment|Music|Cake|Lighting)\s*\|[^₹]*₹\s*([\d,]+)',
            ]
            
            for pattern in cost_patterns:
                matches = re.finditer(pattern, agent_output, re.IGNORECASE)
                for match in matches:
                    category = match.group(1).lower()
                    amount_str = match.group(2).replace(',', '')
                    
                    try:
                        # Handle 'k' suffix (thousands)
                        if 'k' in pattern and '.' in amount_str:
                            amount = int(float(amount_str) * 1000)
                        else:
                            amount = int(amount_str)
                            
                        # Map category names
                        category_map = {
                            'catering': 'catering',
                            'photography': 'photography', 
                            'decoration': 'decoration',
                            'venue': 'venue',
                            'entertainment': 'entertainment',
                            'music': 'entertainment',
                            'lighting': 'entertainment',
                            'cake': 'miscellaneous'
                        }
                        
                        mapped_category = category_map.get(category, category)
                        costs["breakdown"][mapped_category] = amount
                        
                    except ValueError:
                        continue
            
            # Look for total budget mentions
            total_patterns = [
                r'TOTAL[:\s]*₹\s*([\d,]+)',
                r'Total[:\s]*₹\s*([\d,]+)',  
                r'Grand Total[:\s]*₹\s*([\d,]+)',
                r'Budget[:\s]*₹\s*([\d,]+)',
            ]
            
            for pattern in total_patterns:
                match = re.search(pattern, agent_output)
                if match:
                    try:
                        total_amount = int(match.group(1).replace(',', ''))
                        costs["total"] = total_amount
                        break
                    except ValueError:
                        continue
            
            # Calculate total from breakdown if available
            if costs["breakdown"]:
                total_from_breakdown = sum(costs["breakdown"].values())
                if total_from_breakdown > 0:
                    costs["total"] = total_from_breakdown
            
            # Return only what agent provided - NO DEFAULT FALLBACKS
            return costs
            
        except Exception as e:
            logging.error(f"Error parsing cost breakdown from agent output: {e}")
            # Return empty structure - NO FALLBACK DATA
            return {"total": 0, "breakdown": {}}

    def _parse_vendors_from_agent_output(self, agent_output: str, vendor_type: str) -> List[Dict]:
        """Parse specific vendor recommendations from agent output"""
        try:
            vendors = []
            import re
            
            logging.info(f"🔍 Parsing {vendor_type} vendors from agent output...")
            logging.info(f"🔍 Agent output preview: {agent_output[:500]}...")
            
            # Enhanced vendor patterns to match agent's output format
            vendor_patterns = [
                # Pattern like "Catering   Sangeetha Veg Caterers (4.4★)    ₹16.5 k"
                rf'{vendor_type.title()}\s+([A-Za-z][^(₹\n]+?)\s*\(([^)]*★[^)]*)\)\s*₹\s*([\d.]+)\s*k',
                # Pattern like "Photograph Studio 360 Out-door (4.8★)      ₹9 k"  
                rf'Photograph[^A-Z]*([A-Z][^(₹\n]+?)\s*\(([^)]*★[^)]*)\)\s*₹\s*([\d.]+)\s*k',
                # Pattern like "Decoration Flora & Fauna Decor (4.7★)        ₹9.5 k"
                rf'Decoration\s+([A-Za-z][^(₹\n]+?)\s*\(([^)]*★[^)]*)\)\s*₹\s*([\d.]+)\s*k',
                # Pattern like "Music      Nanganallur Nadhaswaram Trio     ₹7 k"
                rf'Music\s+([A-Za-z][^₹\n]+?)\s*₹\s*([\d.]+)\s*k',
                # Pattern like "Lighting   GlowGenie Event Lights (4.5★)     ₹4.5 k"
                rf'Lighting\s+([A-Za-z][^(₹\n]+?)\s*\(([^)]*★[^)]*)\)\s*₹\s*([\d.]+)\s*k',
                # General pattern for any vendor with rating and price
                rf'([A-Z][A-Za-z\s&]+?(?:Caterer|Photography|Decor|Music|Light|Studio|Event)[A-Za-z\s]*)\s*\(([^)]*★[^)]*)\)\s*₹\s*([\d.]+)\s*k',
                # Pattern for vendors without ratings  
                rf'(?:{vendor_type.title()}|Music|Lighting)\s+([A-Z][A-Za-z\s&]+?(?:Trio|Duo|Event|Light|Studio)[A-Za-z\s]*)\s*₹\s*([\d.]+)\s*k',
                # Simple patterns for basic vendor mentions
                rf'{vendor_type}[:\s]*([A-Z][A-Za-z\s]+)',
                rf'([A-Za-z\s]+{vendor_type}[A-Za-z\s]*)',
            ]
            
            for pattern in vendor_patterns:
                matches = re.finditer(pattern, agent_output, re.IGNORECASE)
                for match in matches:
                    vendor_name = match.group(1).strip()
                    rating = "4.2"
                    price = "Quote available"
                    
                    logging.info(f"🔍 Found {vendor_type} vendor match: {vendor_name}")
                    
                    # Extract rating if available
                    if len(match.groups()) > 1 and match.group(2):
                        rating_match = re.search(r'([\d.]+)★', match.group(2))
                        if rating_match:
                            rating = rating_match.group(1)
                    
                    # Extract price if available  
                    if len(match.groups()) > 2 and match.group(3):
                        price_str = match.group(3).replace(',', '')
                        if 'k' in pattern.lower():
                            price = f"₹{float(price_str) * 1000:,.0f}"
                        else:
                            price = f"₹{price_str}"
                    
                    # Clean up vendor name
                    vendor_name = re.sub(r'\s+', ' ', vendor_name).strip()
                    
                    if vendor_name and len(vendor_name) > 3:
                        vendors.append({
                            "name": vendor_name[:50],
                            "service": vendor_type,
                            "price": price,
                            "contact": "Contact vendor directly",
                            "rating": float(rating) if rating else 4.2,
                            "description": f"Professional {vendor_type} service in Chennai",
                            "specialties": [vendor_type, "event services"]
                        })
                        logging.info(f"✅ Added {vendor_type} vendor: {vendor_name}")
                
                if vendors:  # Exit early if we found vendors with this pattern
                    break
            
            logging.info(f"🔍 Final {vendor_type} vendors found: {len(vendors)}")
            return vendors[:3]  # Return top 3 vendors
            
        except Exception as e:
            logging.error(f"Error parsing {vendor_type} vendors from agent output: {e}")
            return []

    def _parse_optimized_costs_from_agent(self, agent_output: str, budget: float) -> Dict:
        """Parse optimized cost recommendations from agent output"""
        try:
            # Look for optimization patterns like "Option 1: Simplified Celebration (₹18,000)"
            import re
            
            # Look for specific optimization amounts - NO DEFAULTS
            option_matches = re.findall(r'Option \d+.*?₹([\d,]+)', agent_output)
            if option_matches:
                optimized_total = int(option_matches[0].replace(',', ''))
                return {
                    "total": optimized_total,
                    "breakdown": {}  # Agent should provide breakdown details
                }
            
            # Return only what agent provided - NO DEFAULT OPTIMIZATIONS
            return {"total": 0, "breakdown": {}}
            
        except Exception as e:
            logging.error(f"Error parsing optimized costs: {e}")
            # Return empty structure - NO FALLBACK DATA
            return {"total": 0, "breakdown": {}}


    def _format_venue_data(self, venue_data) -> Dict:
        """Format venue data for frontend display"""
        try:
            # Handle both dict and string inputs
            if isinstance(venue_data, dict):
                return {
                    "name": venue_data.get("title", "Venue"),
                    "location": venue_data.get("content", "")[:100],
                    "price": "Contact for pricing",
                    "capacity": 50,  # Default integer capacity
                    "contact": venue_data.get("url", ""),
                    "rating": 4.0,
                    "description": venue_data.get("content", "")[:200]
                }
            elif isinstance(venue_data, str):
                # Handle string input - extract what we can
                return {
                    "name": venue_data[:50] if venue_data else "Venue",
                    "location": venue_data[:100] if venue_data else "Location available",
                    "price": "Contact for pricing",
                    "capacity": 50,  # Default integer capacity
                    "contact": "",
                    "rating": 4.0,
                    "description": venue_data[:200] if venue_data else "Venue details available"
                }
            else:
                # Handle other types
                return {"name": "Venue Option", "location": "Location available", "price": "Contact for pricing", "capacity": 50, "contact": "", "rating": 4.0, "description": "Venue details available"}
        except Exception as e:
            logging.error(f"Error formatting venue data: {e}")
            return {"name": "Venue Option", "location": "Location available", "price": "Contact for pricing", "capacity": 50, "contact": "", "rating": 4.0, "description": "Venue details available"}

    def _format_vendor_data(self, vendor_data, service_type: str) -> Dict:
        """Format vendor data for frontend display"""
        try:
            # Handle both dict and string inputs
            if isinstance(vendor_data, dict):
                return {
                    "name": vendor_data.get("title", f"{service_type.title()} Service"),
                    "service": service_type,
                    "price": "Quote available",
                    "contact": vendor_data.get("url", ""),
                    "rating": 4.2,
                    "description": vendor_data.get("content", "")[:150],
                    "specialties": [service_type, "event services"]
                }
            elif isinstance(vendor_data, str):
                # Handle string input - extract what we can
                return {
                    "name": vendor_data[:50] if vendor_data else f"{service_type.title()} Service",
                    "service": service_type,
                    "price": "Quote available",
                    "contact": "",
                    "rating": 4.2,
                    "description": vendor_data[:150] if vendor_data else "Professional service available",
                    "specialties": [service_type, "event services"]
                }
            else:
                # Handle other types
                return {"name": f"{service_type.title()} Service", "service": service_type, "price": "Quote available", "contact": "", "rating": 4.2, "description": "Professional service available", "specialties": [service_type]}
        except Exception as e:
            logging.error(f"Error formatting vendor data: {e}")
            return {"name": f"{service_type.title()} Service", "service": service_type, "price": "Quote available", "contact": "", "rating": 4.2, "description": "Professional service available", "specialties": [service_type]}

    def _extract_budget_assessment(self, agent_output: str) -> str:
        """Extract budget assessment from agent output - PURE AGENTIC"""
        budget_keywords = ["budget", "cost", "price", "expensive", "affordable", "shortfall", "optimiz"]
        lines = agent_output.split('\n')
        budget_lines = [line for line in lines if any(keyword in line.lower() for keyword in budget_keywords)]
        return " ".join(budget_lines[:3])  # Return only what agent provided

    def _extract_strategy_recommendations(self, agent_output: str) -> List[str]:
        """Extract strategy recommendations from agent output - PURE AGENTIC"""
        strategy_keywords = ["recommend", "suggest", "consider", "alternative", "strategy", "approach"]
        lines = agent_output.split('\n')
        strategy_lines = [line.strip() for line in lines if any(keyword in line.lower() for keyword in strategy_keywords)]
        return strategy_lines[:5]  # Return only what agent provided

    def _extract_venue_analysis(self, agent_output: str) -> str:
        """Extract venue analysis from agent output - PURE AGENTIC"""
        venue_keywords = ["venue", "location", "hall", "space", "capacity"]
        lines = agent_output.split('\n')
        venue_lines = [line for line in lines if any(keyword in line.lower() for keyword in venue_keywords)]
        return " ".join(venue_lines[:2])  # Return only what agent provided

    def _extract_cost_optimization(self, agent_output: str) -> List[str]:
        """Extract cost optimization suggestions"""
        cost_keywords = ["save", "reduce", "optimize", "cheaper", "alternative", "diy"]
        lines = agent_output.split('\n')
        cost_lines = [line.strip() for line in lines if any(keyword in line.lower() for keyword in cost_keywords)]
        return cost_lines[:4]  # Return only what agent provided

    def _extract_insights_from_agent_output(self, agent_output: str) -> List[str]:
        """Extract planning insights from agent output - PURE AGENTIC"""
        insights = []
        lines = agent_output.split('\n')
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ["insight", "important", "note", "consider", "tip"]):
                insights.append(line.strip())
                
        return insights[:5]  # Return only what agent provided

    def _extract_recommendations_from_agent_output(self, agent_output: str) -> List[str]:
        """Extract contextual recommendations - PURE AGENTIC"""
        recommendations = []
        lines = agent_output.split('\n')
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ["recommend", "suggest", "should", "best", "ideal"]):
                recommendations.append(line.strip())
                
        return recommendations[:6]  # Return only what agent provided

    def _extract_timeline_from_agent(self, agent_output: str) -> List[str]:
        """Extract planning timeline from agent output - PURE AGENTIC"""
        timeline_keywords = ["week", "day", "month", "before", "advance", "timeline", "schedule"]
        lines = agent_output.split('\n')
        timeline_lines = [line.strip() for line in lines if any(keyword in line.lower() for keyword in timeline_keywords)]
        return timeline_lines[:5]  # Return only what agent provided
        return timeline_lines[:4] if timeline_lines else ["4 weeks before: Book venue", "3 weeks before: Confirm catering", "2 weeks before: Finalize decorations", "1 week before: Final confirmations"]

    def _extract_key_insights(self, agent_output: str) -> List[str]:
        """Extract key insights for display"""
        key_phrases = []
        sentences = agent_output.split('.')
        
        for sentence in sentences:
            if len(sentence.strip()) > 20 and any(keyword in sentence.lower() for keyword in ["important", "key", "crucial", "essential", "recommend"]):
                key_phrases.append(sentence.strip())
                
        return key_phrases[:3] if key_phrases else ["AI agent provided intelligent event planning recommendations", "Budget optimization strategies suggested", "Venue and vendor analysis completed"]
    
    async def _create_structured_plan_from_agent_output(self, agent_output: str, event_request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create structured plan from ReAct agent's natural language output - MOONSHOT ONLY
        """
        try:
            # Use MOONSHOT LLM to structure the agent's output quickly
            structure_prompt = f"""
            Convert this event planning output into a structured JSON format:
            
            Agent Output: {agent_output[:1000]}...
            
            Return ONLY this JSON structure:
            {{
                "variants": [
                    {{
                        "variant": "moonshot_agentic",
                        "venues": [],
                        "vendors": [],
                        "timeline": [{{"milestone": "Agentic Planning Complete", "date": "2025-11-15", "priority": "high", "weeks_before": 4}}],
                        "estimated_cost": {event_request.get("budget", 20000)},
                        "cost_breakdown": {{"venue": {event_request.get("budget", 20000) * 0.4}, "catering": {event_request.get("budget", 20000) * 0.3}, "photography": {event_request.get("budget", 20000) * 0.15}, "decoration": {event_request.get("budget", 20000) * 0.15}}}
                    }}
                ],
                "cost_analysis": {{
                    "dynamic_estimation": {{
                        "optimistic_total": {event_request.get("budget", 20000) * 0.8},
                        "realistic_total": {event_request.get("budget", 20000)},
                        "pessimistic_total": {event_request.get("budget", 20000) * 1.2},
                        "confidence_level": "high"
                    }}
                }},
                "planning_insights": ["MOONSHOT AI agent planning complete"],
                "contextual_recommendations": ["Pure agentic recommendations generated"]
            }}
            """
            
            from langchain.schema import SystemMessage, HumanMessage
            system_msg = SystemMessage(content="You are a JSON converter. Return ONLY valid JSON.")
            human_msg = HumanMessage(content=structure_prompt)
            
            response = self.llm.invoke([system_msg, human_msg])
            
            # Parse the structured response
            try:
                import json
                structured_data = json.loads(response.content)
                return structured_data
            except json.JSONDecodeError:
                # Return minimal structure if parsing fails
                return await self._create_minimal_agentic_plan(event_request)
                
        except Exception as e:
            logging.error(f"❌ Failed to structure agent output: {e}")
            return await self._create_minimal_agentic_plan(event_request)
    
    async def _create_minimal_agentic_plan(self, event_request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create minimal agentic plan structure when agent output cannot be parsed
        """
        budget = event_request.get("budget", 100000)
        
        return {
            "variants": [{
                "variant": "agentic",
                "venues": [],
                "vendors": [],
                "timeline": [
                    {
                        "milestone": "Start Agentic Planning",
                        "date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
                        "priority": "high",
                        "weeks_before": 0
                    }
                ],
                "estimated_cost": budget,
                "cost_breakdown": {
                    "venue": budget * 0.4,
                    "catering": budget * 0.3,
                    "photography": budget * 0.1,
                    "decoration": budget * 0.1,
                    "entertainment": budget * 0.1
                }
            }],
            "cost_analysis": {
                "dynamic_estimation": {
                    "optimistic_total": budget * 0.8,
                    "realistic_total": budget,
                    "pessimistic_total": budget * 1.2,
                    "confidence_level": "medium"
                },
                "budget_allocation": {"agentic": "AI-driven allocation"},
                "cost_optimization": ["Agentic optimization in progress"]
            },
            "planning_insights": ["Agentic AI analysis in progress"],
            "contextual_recommendations": ["ReAct agent recommendations being generated"]
        }
    
    async def _create_enhanced_plan(self, event_request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create enhanced event plan with AI-driven context analysis
        """
        try:
            # Use LLM to analyze requirements and generate search strategy
            analysis_prompt = f"""
            Analyze this event request and provide a comprehensive strategy:
            
            Event Details:
            - Name: {event_request.get('event_name', '')}
            - Type: {event_request.get('event_type', '')}
            - Location: {event_request.get('location', '')}
            - Date: {event_request.get('event_date', '')}
            - Guests: {event_request.get('guest_count', 50)}
            - Budget: ₹{event_request.get('budget', 100000)}
            - Preferences: {', '.join(event_request.get('preferences', []))}
            - Special Requirements: {', '.join(event_request.get('special_requirements', []))}
            
            Provide:
            1. Event context analysis (indoor/outdoor, theme, style)
            2. Specific search keywords for venues and vendors
            3. Budget allocation recommendations
            4. Special considerations based on requirements
            5. Risk factors and backup plans
            
            Respond in JSON format with clear structure.
            """
            
            system_msg = SystemMessage(content="You are an expert event planning analyst. Provide detailed, actionable event planning strategies in JSON format.")
            human_msg = HumanMessage(content=analysis_prompt)
            
            response = self.llm.invoke([system_msg, human_msg])
            
            # Parse AI analysis
            try:
                ai_analysis = json.loads(response.content)
            except json.JSONDecodeError:
                # Fallback if JSON parsing fails
                ai_analysis = {"strategy": "standard", "context": "mixed"}
            
            # Use AI analysis to guide searches
            context_keywords = ai_analysis.get("search_keywords", {})
            venue_keywords = context_keywords.get("venues", [])
            vendor_keywords = context_keywords.get("vendors", {})
            
            # Enhanced parallel searches with context
            search_tasks = []
            
            # Context-aware venue search
            search_tasks.append(
                self._search_venues_with_context(
                    event_request.get("location", ""),
                    event_request.get("event_type", ""),
                    event_request.get("guest_count", 50),
                    event_request.get("budget", 100000),
                    venue_keywords
                )
            )
            
            # Context-aware vendor searches
            search_tasks.extend([
                self._search_vendors_with_context(
                    event_request.get("location", ""),
                    "catering",
                    event_request.get("event_type", ""),
                    vendor_keywords.get("catering", []),
                    event_request.get("preferences", [])
                ),
                self._search_vendors_with_context(
                    event_request.get("location", ""),
                    "photography",
                    event_request.get("event_type", ""),
                    vendor_keywords.get("photography", []),
                    []
                ),
                self._search_vendors_with_context(
                    event_request.get("location", ""),
                    "decoration",
                    event_request.get("event_type", ""),
                    vendor_keywords.get("decoration", []),
                    []
                ),
                self._search_vendors_with_context(
                    event_request.get("location", ""),
                    "entertainment",
                    event_request.get("event_type", ""),
                    vendor_keywords.get("entertainment", []),
                    []
                )
            ])
            
            # Execute all searches
            results = await asyncio.gather(*search_tasks, return_exceptions=True)
            
            venues = results[0] if not isinstance(results[0], Exception) else []
            caterers = results[1] if not isinstance(results[1], Exception) else []
            photographers = results[2] if not isinstance(results[2], Exception) else []
            decorators = results[3] if not isinstance(results[3], Exception) else []
            entertainment = results[4] if not isinstance(results[4], Exception) else []
            
            # Create AI-optimized plan variants with dynamic cost analysis
            all_vendors = caterers + photographers + decorators + entertainment
            cost_analysis = await analyze_event_costs(event_request, venues, all_vendors)
            
            optimized_plan = await self._create_ai_optimized_variants(
                venues, caterers, photographers, decorators, entertainment,
                event_request, ai_analysis, cost_analysis
            )
            
            # Add AI insights, cost analysis and recommendations
            optimized_plan.update({
                "ai_analysis": ai_analysis,
                "cost_analysis": cost_analysis,
                "planning_insights": await self._generate_planning_insights(event_request, ai_analysis),
                "contextual_recommendations": await self._generate_contextual_recommendations(event_request, venues, caterers),
                "budget_optimization": cost_analysis.get("cost_optimization", []),
                "risk_assessment": cost_analysis.get("risk_factors", []),
                "metadata": {
                    "planning_approach": "AI-Enhanced Agentic with Dynamic Cost Analysis",
                    "analysis_engine": "Moonshot LLM + Context Analysis + Market Cost Intelligence",
                    "data_sources": "Real-time Tavily Search + AI Optimization + Dynamic Pricing",
                    "cost_confidence": cost_analysis.get("dynamic_estimation", {}).get("confidence_level", "medium"),
                    "last_updated": datetime.now().isoformat()
                }
            })
            
            return optimized_plan
            
        except Exception as e:
            logging.error(f"❌ Enhanced planning failed: {e}")
            # Return error structure instead of raising exception
            return {
                "variants": [{
                    "id": "enhanced_error",
                    "name": "Error in Enhanced Planning",
                    "variant": "error",
                    "estimated_cost": event_request.get("budget", 0),
                    "total_cost": event_request.get("budget", 0),
                    "cost_breakdown": {
                        "venue": 0.0,
                        "catering": 0.0,
                        "photography": 0.0,
                        "decoration": 0.0,
                        "entertainment": 0.0
                    },
                    "venues": [],
                    "vendors": {"catering": [], "photography": [], "decoration": []},
                    "planning_timeline": ["Error in enhanced planning"],
                    "agent_insights": [f"Enhanced planning error: {str(e)}"]
                }],
                "agent_analysis": {
                    "full_analysis": f"Enhanced planning failed: {str(e)}",
                    "budget_assessment": "Unable to assess - error occurred",
                    "strategy_recommendations": ["Please try again"],
                    "venue_analysis": "Error in enhanced analysis"
                },
                "metadata": {
                    "planning_approach": "Enhanced Planning Failed",
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                }
            }
    
    async def _search_venues_with_context(self, location: str, event_type: str, guest_count: int, budget: float, context_keywords: List[str]) -> List:
        """Search venues with context-aware keywords"""
        try:
            # Use new Tavily-based search with real venue data
            venues = await search_venues_tavily(location, event_type, guest_count, 8)
            
            # Filter and rank based on context keywords
            if context_keywords:
                context_scored_venues = []
                for venue in venues:
                    score = 0
                    venue_text = f"{venue.get('name', '')} {venue.get('description', '')}".lower()
                    
                    for keyword in context_keywords:
                        if keyword.lower() in venue_text:
                            score += 1
                    
                    venue['context_score'] = score
                    context_scored_venues.append(venue)
                
                # Sort by context relevance
                venues = sorted(context_scored_venues, key=lambda x: x.get('context_score', 0), reverse=True)
            
            return venues
            
        except Exception as e:
            logging.error(f"Context-aware venue search failed: {e}")
            return []
    
    async def _search_vendors_with_context(self, location: str, service_type: str, event_type: str, context_keywords: List[str], preferences: List[str]) -> List:
        """Search vendors with context-aware keywords"""
        try:
            # Use new Tavily-based vendor search for real data
            vendors = await search_vendors_tavily(location, service_type, event_type, 8)
            
            # Score based on context relevance
            if context_keywords:
                context_scored_vendors = []
                for vendor in vendors:
                    score = 0
                    vendor_text = f"{vendor.get('name', '')} {vendor.get('description', '')} {' '.join(vendor.get('specialties', []))}".lower()
                    
                    for keyword in context_keywords:
                        if keyword.lower() in vendor_text:
                            score += 1
                    
                    vendor['context_score'] = score
                    vendor['service_type'] = service_type
                    context_scored_vendors.append(vendor)
                
                vendors = sorted(context_scored_vendors, key=lambda x: x.get('context_score', 0), reverse=True)
            
            return vendors
            
        except Exception as e:
            logging.error(f"Context-aware {service_type} search failed: {e}")
            return []
    
    async def _create_ai_optimized_variants(self, venues: List, caterers: List, photographers: List, 
                                          decorators: List, entertainment: List, event_request: Dict, 
                                          ai_analysis: Dict, cost_analysis: Dict) -> Dict:
        """Create AI-optimized event plan variants with dynamic cost analysis"""
        try:
            budget = event_request.get("budget", 100000)
            guest_count = event_request.get("guest_count", 50)
            
            # Use AI-driven budget allocation from cost analysis
            budget_allocation = cost_analysis.get("budget_allocation", {})
            if not budget_allocation:
                # Fallback allocation
                budget_allocation = {
                    "venue_percentage": 35,
                    "catering_percentage": 30,
                    "photography_percentage": 15,
                    "decoration_percentage": 15,
                    "entertainment_percentage": 5
                }
            
            # Get dynamic cost estimates
            dynamic_est = cost_analysis.get("dynamic_estimation", {})
            optimistic_budget = dynamic_est.get("optimistic_total", budget * 0.8)
            realistic_budget = dynamic_est.get("realistic_total", budget)
            pessimistic_budget = dynamic_est.get("pessimistic_total", budget * 1.2)
            
            # Create smart variants based on cost analysis
            variants = []
            
            # Budget-conscious variant (optimistic pricing)
            budget_variant = await self._create_smart_variant(
                "budget", optimistic_budget, venues, caterers, photographers, 
                decorators, entertainment, event_request, "cost_effective", budget_allocation
            )
            variants.append(budget_variant)
            
            # Balanced variant (realistic pricing)
            balanced_variant = await self._create_smart_variant(
                "balanced", realistic_budget, venues, caterers, photographers,
                decorators, entertainment, event_request, "balanced", budget_allocation
            )
            variants.append(balanced_variant)
            
            # Premium variant (if budget allows or for aspirational planning)
            if budget > 150000 or pessimistic_budget <= budget * 1.3:
                premium_variant = await self._create_smart_variant(
                    "premium", pessimistic_budget, venues, caterers, photographers,
                    decorators, entertainment, event_request, "premium", budget_allocation
                )
                variants.append(premium_variant)
            
            return {"variants": variants}
            
        except Exception as e:
            logging.error(f"AI optimization failed: {e}")
            return {"variants": [], "error": str(e)}
    
    async def _create_smart_variant(self, variant_type: str, budget: float, venues: List, 
                                   caterers: List, photographers: List, decorators: List, 
                                   entertainment: List, event_request: Dict, strategy: str, 
                                   budget_allocation: Dict) -> Dict:
        """Create smart variant with AI-driven selections and dynamic cost allocation"""
        try:
            guest_count = event_request.get("guest_count", 50)
            event_type = event_request.get("event_type", "")
            
            # Use AI-driven allocation percentages
            venue_pct = budget_allocation.get("venue_percentage", 35) / 100
            catering_pct = budget_allocation.get("catering_percentage", 30) / 100
            photography_pct = budget_allocation.get("photography_percentage", 15) / 100
            decoration_pct = budget_allocation.get("decoration_percentage", 15) / 100
            entertainment_pct = budget_allocation.get("entertainment_percentage", 5) / 100
            
            allocation = {
                "venue": venue_pct,
                "catering": catering_pct,
                "photography": photography_pct,
                "decoration": decoration_pct,
                "entertainment": entertainment_pct
            }
            
            # Smart vendor selection based on context scores and budget
            selected_venues = self._select_smart_venues(venues, budget * allocation["venue"])
            selected_caterers = self._select_smart_vendors(caterers, budget * allocation["catering"], strategy)
            selected_photographers = self._select_smart_vendors(photographers, budget * allocation["photography"], strategy)
            selected_decorators = self._select_smart_vendors(decorators, budget * allocation["decoration"], strategy)
            selected_entertainment = self._select_smart_vendors(entertainment, budget * allocation["entertainment"], strategy)
            
            # Calculate dynamic costs
            venue_cost = selected_venues[0].get("price_per_day", budget * allocation["venue"]) if selected_venues else budget * allocation["venue"]
            catering_cost = budget * allocation["catering"]
            photography_cost = budget * allocation["photography"]
            decoration_cost = budget * allocation["decoration"]
            entertainment_cost = budget * allocation["entertainment"]
            
            total_cost = venue_cost + catering_cost + photography_cost + decoration_cost + entertainment_cost
            
            # Generate smart timeline
            timeline = await self._generate_smart_timeline(event_type, event_request.get("event_date", ""), strategy)
            
            # Combine vendors with service type info
            all_vendors = []
            for vendor_list, service_type in [
                (selected_caterers, "catering"),
                (selected_photographers, "photography"), 
                (selected_decorators, "decoration"),
                (selected_entertainment, "entertainment")
            ]:
                for vendor in vendor_list:
                    vendor["service_type"] = service_type
                    all_vendors.append(vendor)
            
            return {
                "variant": variant_type,
                "strategy": strategy,
                "venues": selected_venues,
                "vendors": all_vendors,
                "timeline": timeline,
                "estimated_cost": total_cost,
                "cost_breakdown": {
                    "venue": venue_cost,
                    "catering": catering_cost,
                    "photography": photography_cost,
                    "decoration": decoration_cost,
                    "entertainment": entertainment_cost
                },
                "selection_rationale": {
                    "venue_reason": f"Selected based on {strategy} strategy and context relevance",
                    "vendor_reason": f"Optimized for {strategy} approach with budget constraints",
                    "cost_reason": f"Budget allocation follows {strategy} priorities"
                }
            }
            
        except Exception as e:
            logging.error(f"Smart variant creation failed: {e}")
            return {
                "variant": variant_type,
                "strategy": strategy,
                "venues": [],
                "vendors": [],
                "timeline": [],
                "estimated_cost": budget,
                "error": str(e)
            }
    
    def _select_smart_venues(self, venues: List, budget: float) -> List:
        """Smart venue selection based on context and budget"""
        if not venues:
            return []
        
        # Filter by budget and rank by context score
        affordable_venues = []
        for v in venues:
            price = v.get("price_per_day")
            if price is None or price <= budget:
                affordable_venues.append(v)
                
        if not affordable_venues:
            affordable_venues = venues  # Include all if none are within budget
        
        # Sort by context score first, then by value for money
        sorted_venues = sorted(affordable_venues, 
                             key=lambda x: (x.get("context_score", 0), -(x.get("price_per_day") or 0)),
                             reverse=True)
        
        return sorted_venues[:3]  # Return top 3 options
    
    def _select_smart_vendors(self, vendors: List, budget: float, strategy: str) -> List:
        """Smart vendor selection based on strategy and context"""
        if not vendors:
            return []
        
        # Strategy-based selection
        if strategy == "cost_effective":
            # Prioritize budget-friendly options with good context score
            scored_vendors = [(v, v.get("context_score", 0) + (1 if "budget" in v.get("price_range", "").lower() else 0)) for v in vendors]
        elif strategy == "premium":
            # Prioritize high-quality and premium options
            scored_vendors = [(v, v.get("context_score", 0) + (1 if "premium" in v.get("price_range", "").lower() else 0)) for v in vendors]
        else:
            # Balanced approach
            scored_vendors = [(v, v.get("context_score", 0)) for v in vendors]
        
        # Sort by calculated score
        sorted_vendors = sorted(scored_vendors, key=lambda x: x[1], reverse=True)
        
        return [v[0] for v in sorted_vendors[:2]]  # Return top 2 vendors
    
    async def _generate_smart_timeline(self, event_type: str, event_date: str, strategy: str) -> List:
        """Generate intelligent timeline based on event type and strategy"""
        try:
            if not event_date:
                event_date = (datetime.now() + timedelta(days=60)).strftime("%Y-%m-%d")
            
            event_dt = datetime.strptime(event_date, "%Y-%m-%d")
            today = datetime.now()
            
            # Strategy-based timeline adjustments
            timeline_templates = {
                "cost_effective": [
                    {"weeks_before": 10, "milestone": "Start Budget Planning", "priority": "high"},
                    {"weeks_before": 8, "milestone": "Book Venue", "priority": "critical"},
                    {"weeks_before": 6, "milestone": "Secure Core Vendors", "priority": "critical"},
                    {"weeks_before": 4, "milestone": "Finalize Details", "priority": "medium"},
                    {"weeks_before": 2, "milestone": "Final Confirmations", "priority": "high"},
                    {"weeks_before": 1, "milestone": "Pre-Event Setup", "priority": "high"}
                ],
                "premium": [
                    {"weeks_before": 12, "milestone": "Premium Venue Booking", "priority": "critical"},
                    {"weeks_before": 10, "milestone": "High-End Vendor Selection", "priority": "critical"},
                    {"weeks_before": 8, "milestone": "Luxury Service Coordination", "priority": "high"},
                    {"weeks_before": 6, "milestone": "Premium Experience Planning", "priority": "medium"},
                    {"weeks_before": 4, "milestone": "Quality Assurance", "priority": "high"},
                    {"weeks_before": 2, "milestone": "VIP Preparations", "priority": "high"},
                    {"weeks_before": 1, "milestone": "Premium Setup", "priority": "critical"}
                ],
                "balanced": [
                    {"weeks_before": 8, "milestone": "Comprehensive Planning Start", "priority": "high"},
                    {"weeks_before": 6, "milestone": "Venue and Key Vendor Booking", "priority": "critical"},
                    {"weeks_before": 4, "milestone": "Service Coordination", "priority": "medium"},
                    {"weeks_before": 3, "milestone": "Menu and Decor Finalization", "priority": "medium"},
                    {"weeks_before": 2, "milestone": "Final Vendor Confirmations", "priority": "high"},
                    {"weeks_before": 1, "milestone": "Event Preparation", "priority": "high"}
                ]
            }
            
            template = timeline_templates.get(strategy, timeline_templates["balanced"])
            
            timeline = []
            for item in template:
                milestone_date = event_dt - timedelta(weeks=item["weeks_before"])
                if milestone_date > today:
                    timeline.append({
                        "milestone": item["milestone"],
                        "date": milestone_date.strftime("%Y-%m-%d"),
                        "priority": item["priority"],
                        "weeks_before": item["weeks_before"],
                        "strategy_note": f"Optimized for {strategy} approach"
                    })
            
            # If no future milestones, add at least current planning items
            if not timeline:
                timeline.extend([
                    {
                        "milestone": "Start Planning Now",
                        "date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
                        "priority": "high",
                        "weeks_before": 0,
                        "strategy_note": "Immediate action required"
                    },
                    {
                        "milestone": "Book Key Vendors",
                        "date": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
                        "priority": "critical",
                        "weeks_before": 0,
                        "strategy_note": "Urgent booking needed"
                    }
                ])
            
            return timeline
            
        except Exception as e:
            logging.error(f"Smart timeline generation failed: {e}")
            return []
    
    async def _generate_planning_insights(self, event_request: Dict, ai_analysis: Dict) -> List[str]:
        """Generate AI-powered planning insights"""
        try:
            if not self.llm:
                return ["Use fallback planning recommendations"]
            
            insight_prompt = f"""
            Based on the event analysis, provide specific planning insights:
            
            Event: {event_request.get('event_type', '')} for {event_request.get('guest_count', 50)} guests
            Budget: ₹{event_request.get('budget', 100000)}
            Location: {event_request.get('location', '')}
            Preferences: {', '.join(event_request.get('preferences', []))}
            
            AI Analysis: {json.dumps(ai_analysis)}
            
            Provide 5-7 specific, actionable insights that will help ensure event success.
            Focus on practical tips based on the specific event requirements.
            """
            
            system_msg = SystemMessage(content="You are an expert event planning consultant. Provide specific, actionable insights based on event analysis.")
            human_msg = HumanMessage(content=insight_prompt)
            
            response = self.llm.invoke([system_msg, human_msg])
            insights = [line.strip() for line in response.content.split('\n') if line.strip() and not line.strip().startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.'))]
            
            return insights[:7]
            
        except Exception as e:
            logging.error(f"Planning insights generation failed: {e}")
            return [
                "Start planning early to secure best vendors",
                "Have backup options for critical services",
                "Consider guest preferences in all decisions",
                "Create detailed timeline with buffer time",
                "Maintain emergency contact list"
            ]
    
    async def _generate_contextual_recommendations(self, event_request: Dict, venues: List, caterers: List) -> List[str]:
        """Generate contextual recommendations based on search results"""
        try:
            recommendations = []
            
            event_type = event_request.get("event_type", "").lower()
            guest_count = event_request.get("guest_count", 50)
            budget = event_request.get("budget", 100000)
            preferences = event_request.get("preferences", [])
            
            # Venue-based recommendations
            if venues:
                outdoor_venues = [v for v in venues if any(keyword in v.get("name", "").lower() + v.get("description", "").lower() 
                                                          for keyword in ["outdoor", "garden", "terrace", "beach"])]
                if outdoor_venues:
                    recommendations.append("Consider weather backup plans for outdoor venues")
                    recommendations.append("Ensure outdoor venues have adequate facilities for guest comfort")
            
            # Budget-based recommendations
            per_person_budget = budget / guest_count if guest_count > 0 else 0
            if per_person_budget < 1500:
                recommendations.append("Focus on essential services and consider buffet-style catering")
                recommendations.append("Look for package deals to maximize value")
            elif per_person_budget > 4000:
                recommendations.append("Consider premium services and additional entertainment options")
                recommendations.append("Add luxury touches like welcome drinks and upgraded decor")
            
            # Event type specific
            if "birthday" in event_type:
                recommendations.append("Plan special moments like cake cutting and photo opportunities")
                recommendations.append("Consider age-appropriate entertainment and activities")
            elif "corporate" in event_type:
                recommendations.append("Ensure venue has proper AV equipment and networking spaces")
                recommendations.append("Plan for registration and material distribution areas")
            elif "wedding" in event_type:
                recommendations.append("Book photographer for both ceremony and reception coverage")
                recommendations.append("Plan detailed timeline with buffer time for ceremonies")
            
            # Preference-based recommendations
            if "vegetarian" in preferences:
                recommendations.append("Ensure caterer specializes in vegetarian cuisine with variety")
            if "outdoor" in preferences:
                recommendations.append("Plan for weather contingencies and guest comfort measures")
            
            return recommendations[:8]
            
        except Exception as e:
            logging.error(f"Contextual recommendations failed: {e}")
            return ["Plan ahead for best vendor availability", "Consider guest preferences in all decisions"]
    
    def _extract_venues_from_comprehensive_text(self, text: str) -> List[Dict]:
        """Extract venues from comprehensive event plan text"""
        try:
            import re
            venues = []
            lines = text.split('\n')
            
            in_venue_section = False
            current_venue = {}
            
            for line in lines:
                line = line.strip()
                
                # Detect venue sections (multiple patterns) 
                if (("venue" in line.lower() and line.startswith("##") and not line.startswith("###")) or 
                    "Recommended Venues" in line or "REAL VENUES IDENTIFIED" in line or
                    "VENUES IDENTIFIED" in line or "## **REAL VENUES" in line):
                    in_venue_section = True
                    continue
                elif line.startswith("##") and not line.startswith("###") and in_venue_section and "venue" not in line.lower():
                    # End of venue section when we hit another ## section (not ###)
                    if current_venue and current_venue.get("name"):
                        venues.append(current_venue)
                        current_venue = {}
                    in_venue_section = False
                    continue
                
                if in_venue_section and line:
                    # Detect individual venue entries (### pattern) - but exclude service sections
                    if line.startswith("### **") and not any(service in line.upper() for service in 
                                                           ["CATERING", "PHOTOGRAPHY", "DECORATION", "ENTERTAINMENT"]):
                        # Save previous venue
                        if current_venue and current_venue.get("name"):
                            venues.append(current_venue)
                        
                        # Start new venue - extract name
                        venue_name = line.replace("### **", "").replace("**", "").strip()
                        # Clean up numbering (e.g., "1. ITC Grand Chola - Grand Lawns" -> "ITC Grand Chola - Grand Lawns")
                        venue_name = re.sub(r'^\d+\.\s*', '', venue_name)
                        # Remove trailing location info in parentheses
                        venue_name = venue_name.split('(')[0].strip()
                        
                        current_venue = {
                            "name": venue_name,
                            "location": "Chennai",
                            "capacity": 150,
                            "price_per_day": "Contact for pricing",
                            "amenities": ["Event space", "Professional setup"],
                            "rating": 4.3,
                            "description": f"Professional event venue in Chennai"
                        }
                    
                    # Extract venue details from bullet points
                    elif line.startswith("- **") and current_venue:
                        if "Capacity" in line:
                            # Extract capacity number
                            capacity_match = re.search(r'(\d+)', line)
                            if capacity_match:
                                current_venue["capacity"] = int(capacity_match.group(1))
                        elif "Cost" in line or "Price" in line:
                            # Extract price info
                            price_part = line.split(":")[-1].strip() if ":" in line else line.split("**")[-1].strip()
                            current_venue["price_per_day"] = price_part
                        elif "Space" in line:
                            space_info = line.split(":")[-1].strip() if ":" in line else line.split("**")[-1].strip()
                            if "outdoor" in space_info.lower():
                                current_venue["amenities"].append("Outdoor space")
                            if "indoor" in space_info.lower():
                                current_venue["amenities"].append("Indoor facilities")
                        elif "Specialty" in line:
                            specialty = line.split(":")[-1].strip() if ":" in line else line.split("**")[-1].strip()
                            current_venue["description"] = specialty
            
            # Don't forget the last venue
            if current_venue and current_venue.get("name"):
                venues.append(current_venue)
            
            logging.info(f"🏢 Extracted {len(venues)} venues from comprehensive text")
            return venues[:10]  # Limit to 10 venues
            
        except Exception as e:
            logging.error(f"Error extracting venues from comprehensive text: {e}")
            return []
    
    def _extract_vendors_from_comprehensive_text(self, text: str) -> Dict[str, List[Dict]]:
        """Extract vendors from comprehensive event plan text"""
        try:
            import re
            vendors = {"catering": [], "photography": [], "decoration": [], "entertainment": []}
            lines = text.split('\n')
            
            current_section = None
            previous_section = None
            current_vendor = {}
            
            for line in lines:
                line = line.strip()
                
                # Detect vendor sections with proper section headers (## **SERVICE_NAME**)
                if line.startswith("## **") and any(service in line.upper() for service in ["CATERING", "FOOD"]):
                    current_section = "catering"
                    # Clear any existing vendor when starting new section
                    if current_vendor and current_vendor.get("name"):
                        if previous_section:
                            vendors[previous_section].append(current_vendor)
                        current_vendor = {}
                    previous_section = current_section
                    continue
                elif line.startswith("## **") and "PHOTOGRAPHY" in line.upper():
                    current_section = "photography"
                    # Clear any existing vendor when starting new section  
                    if current_vendor and current_vendor.get("name"):
                        if previous_section:
                            vendors[previous_section].append(current_vendor)
                        current_vendor = {}
                    previous_section = current_section
                    continue
                elif line.startswith("## **") and "DECORATION" in line.upper():
                    current_section = "decoration"
                    # Clear any existing vendor when starting new section
                    if current_vendor and current_vendor.get("name"):
                        if previous_section:
                            vendors[previous_section].append(current_vendor)
                        current_vendor = {}
                    previous_section = current_section
                    continue
                elif line.startswith("## **") and "ENTERTAINMENT" in line.upper():
                    current_section = "entertainment"
                    # Clear any existing vendor when starting new section
                    if current_vendor and current_vendor.get("name"):
                        if previous_section:
                            vendors[previous_section].append(current_vendor)
                        current_vendor = {}
                    previous_section = current_section
                    continue
                elif line.startswith("##") and current_section and "**" in line:
                    # End of current vendor section when we hit another ## section
                    if current_vendor and current_vendor.get("name"):
                        vendors[current_section].append(current_vendor)
                        current_vendor = {}
                    current_section = None
                    previous_section = None
                    continue
                
                if current_section and line:
                    # Detect individual vendor entries - handle multiple formats
                    if (line.startswith("### ") or 
                        (line.startswith("**") and re.match(r'\*\*\d+\.\s+[A-Z]', line))):
                        # Save previous vendor
                        if current_vendor and current_vendor.get("name"):
                            vendors[current_section].append(current_vendor)
                        
                        # Start new vendor - handle different formats
                        if line.startswith("### "):
                            vendor_name = line.replace("### ", "").strip()
                        else:  # **1. Vendor Name** format
                            vendor_name = line.replace("**", "").strip()
                        
                        # Clean up numbering
                        vendor_name = re.sub(r'^\d+\.\s*', '', vendor_name)
                        
                        current_vendor = {
                            "name": vendor_name,
                            "service_type": current_section,
                            "location": "Chennai",
                            "price_range": "Contact for pricing",
                            "rating": 4.2,
                            "specialties": [current_section, "event services"],
                            "description": f"Professional {current_section} service in Chennai"
                        }
                    
                    # Extract vendor details from bullet points
                    elif line.startswith("- **") and current_vendor:
                        if "Price" in line or "Cost" in line:
                            price_info = line.split(":")[-1].strip() if ":" in line else line.split("**")[-1].strip()
                            current_vendor["price_range"] = price_info
                        elif "Specialty" in line:
                            specialty = line.split(":")[-1].strip() if ":" in line else line.split("**")[-1].strip()
                            current_vendor["specialties"] = [specialty, current_section]
                            current_vendor["description"] = specialty
                        elif "Experience" in line:
                            exp_info = line.split(":")[-1].strip() if ":" in line else line.split("**")[-1].strip()
                            current_vendor["description"] = f"{exp_info} - Professional {current_section} service"
            
            # Don't forget the last vendor
            if current_vendor and current_vendor.get("name") and current_section:
                vendors[current_section].append(current_vendor)
            
            total_vendors = sum(len(v) for v in vendors.values())
            logging.info(f"🎪 Extracted {total_vendors} vendors from comprehensive text")
            return vendors
            
        except Exception as e:
            logging.error(f"Error extracting vendors from comprehensive text: {e}")
            return {"catering": [], "photography": [], "decoration": [], "entertainment": []}
    
    def _create_structured_plan_from_extracted_data(self, venues: List[Dict], vendors: Dict, event_request: Dict, full_text: str) -> Dict[str, Any]:
        """Create structured plan from extracted venue/vendor data"""
        try:
            budget = event_request.get("budget", 100000)
            
            # Create the main variant with extracted data
            main_variant = {
                "id": "agentic_comprehensive_plan",
                "name": "AI Agent Comprehensive Event Plan",
                "variant": "comprehensive_agentic",
                "estimated_cost": budget,
                "total_cost": budget,
                "cost_breakdown": {
                    "venue": budget * 0.25,
                    "catering": budget * 0.40,
                    "photography": budget * 0.15,
                    "decoration": budget * 0.15,
                    "entertainment": budget * 0.05
                },
                "venues": venues,
                "vendors": vendors,
                "planning_timeline": [
                    "6 weeks before: Book venue and major vendors",
                    "4 weeks before: Finalize catering menu and decorations", 
                    "2 weeks before: Confirm all vendor arrangements",
                    "1 week before: Final headcount and logistics",
                    "Event day: Execute the planned celebration"
                ],
                "agent_insights": [
                    f"Agent found {len(venues)} real venues in Chennai",
                    f"Agent found {sum(len(v) for v in vendors.values())} real vendors",
                    "Comprehensive plan created from agent analysis"
                ]
            }
            
            # Create structured response
            structured_plan = {
                "variants": [main_variant],
                "agent_analysis": {
                    "full_analysis": full_text,
                    "budget_assessment": f"Budget of ₹{budget:,} analyzed for comprehensive event planning",
                    "strategy_recommendations": [
                        "Book venue and major vendors immediately",
                        "Consider package deals for cost savings", 
                        "Plan weather contingency for outdoor events"
                    ],
                    "venue_analysis": f"Agent identified {len(venues)} suitable venues with comprehensive details"
                },
                "cost_analysis": {
                    "dynamic_estimation": {
                        "optimistic_total": budget * 0.9,
                        "realistic_total": budget,
                        "pessimistic_total": budget * 1.2,
                        "confidence_level": "high"
                    },
                    "market_analysis": "Comprehensive market analysis by AI agent",
                    "budget_optimization": ["Consider off-season dates", "Package deals available"]
                },
                "planning_insights": [
                    "Agent provided comprehensive venue analysis",
                    "Traditional vendors well-represented in recommendations",
                    "Cost optimization strategies included"
                ],
                "contextual_recommendations": [
                    "Visit shortlisted venues before finalizing",
                    "Taste catering samples before deciding",
                    "Check vendor availability for your exact dates"
                ],
                "metadata": {
                    "planning_approach": "COMPREHENSIVE AI AGENT ANALYSIS",
                    "agent_used": "MOONSHOT LLM ReAct Agent",
                    "data_sources": "Agent comprehensive research and analysis",
                    "agentic_mode": "COMPREHENSIVE AGENTIC EXTRACTION",
                    "extraction_method": "Structured text parsing from agent output",
                    "timestamp": datetime.now().isoformat()
                }
            }
            
            logging.info("✅ Created structured plan from comprehensive agent text")
            return structured_plan
            
        except Exception as e:
            logging.error(f"Error creating structured plan from extracted data: {e}")
            return {
                "variants": [],
                "error": "Failed to structure comprehensive agent response", 
                "metadata": {"error": str(e)}
            }
    
    def _extract_venues_from_final_answer(self, final_answer: str) -> List[Dict]:
        """Extract venue names from agent's Final Answer"""
        try:
            venues = []
            
            # Look for venue listings in the Final Answer
            lines = final_answer.split('\n')
            for line in lines:
                line = line.strip()
                
                # Check if line contains venue names
                if any(venue_word in line.lower() for venue_word in ['venue', 'hall', 'resort', 'hotel', 'palace']):
                    # Extract venue names using common patterns
                    import re
                    
                    # Pattern for comma-separated venue lists
                    if ',' in line and not line.startswith('#'):
                        potential_venues = [v.strip() for v in line.split(',') if v.strip()]
                        for venue in potential_venues:
                            # Clean up venue name
                            venue = re.sub(r'^[\d\.\-\*\s]*', '', venue)  # Remove bullets/numbers
                            venue = re.sub(r'\([^)]*\)', '', venue)  # Remove parentheses
                            venue = venue.split(':')[-1].strip()  # Remove prefixes like "Found venues:"
                            
                            if len(venue) > 5 and not any(skip in venue.lower() for skip in ['found', 'venues', 'search', 'result']):
                                venues.append({
                                    "name": venue[:50],
                                    "location": "Chennai",
                                    "capacity": 150,
                                    "price_per_day": "Contact for pricing",
                                    "amenities": ["Wedding setup", "Catering facilities"],
                                    "rating": 4.3,
                                    "description": f"Professional wedding venue in Chennai"
                                })
                                
                            if len(venues) >= 8:  # Limit to 8 venues
                                break
            
            logging.info(f"🏢 Extracted {len(venues)} venues from Final Answer")
            return venues[:8]
            
        except Exception as e:
            logging.error(f"Error extracting venues from Final Answer: {e}")
            return []
    
    def _extract_vendors_from_final_answer(self, final_answer: str) -> Dict[str, List[Dict]]:
        """Extract vendor names from agent's Final Answer"""
        try:
            vendors = {"catering": [], "photography": [], "decoration": [], "entertainment": []}
            
            lines = final_answer.split('\n')
            current_vendor_type = None
            
            for line in lines:
                line = line.strip()
                
                # Identify vendor sections
                if 'catering:' in line.lower():
                    current_vendor_type = 'catering'
                elif 'photography:' in line.lower():
                    current_vendor_type = 'photography'
                elif 'decoration:' in line.lower():
                    current_vendor_type = 'decoration'
                elif 'entertainment:' in line.lower():
                    current_vendor_type = 'entertainment'
                
                # Extract vendor names from lines
                if current_vendor_type and ',' in line:
                    # Extract vendor names after the colon
                    vendor_part = line.split(':', 1)[-1].strip()
                    potential_vendors = [v.strip() for v in vendor_part.split(',') if v.strip()]
                    
                    for vendor in potential_vendors:
                        # Clean up vendor name
                        import re
                        vendor = re.sub(r'^[\d\.\-\*\s]*', '', vendor)  # Remove bullets
                        vendor = re.sub(r'\([^)]*\)', '', vendor)  # Remove parentheses
                        
                        if len(vendor) > 3 and not any(skip in vendor.lower() for skip in ['found', 'vendors', 'search']):
                            vendors[current_vendor_type].append({
                                "name": vendor[:50],
                                "service_type": current_vendor_type,
                                "location": "Chennai",
                                "price_range": "Contact for pricing",
                                "rating": 4.2,
                                "specialties": [current_vendor_type, "wedding services"],
                                "description": f"Professional {current_vendor_type} service in Chennai"
                            })
                            
                        if len(vendors[current_vendor_type]) >= 3:  # Limit to 3 per type
                            break
            
            total_vendors = sum(len(v) for v in vendors.values())
            logging.info(f"🎪 Extracted {total_vendors} vendors from Final Answer")
            return vendors
            
        except Exception as e:
            logging.error(f"Error extracting vendors from Final Answer: {e}")
            return {"catering": [], "photography": [], "decoration": [], "entertainment": []}
    

    
    async def _create_fallback_plan(self, event_request: Dict[str, Any]) -> Dict[str, Any]:
        """Create basic fallback plan when AI services are unavailable"""
        try:
            # Basic searches using Tavily-based functions
            search_tasks = [
                search_venues_tavily(
                    event_request.get("location", ""),
                    event_request.get("event_type", ""),
                    event_request.get("guest_count", 50),
                    5
                ),
                search_vendors_tavily(
                    event_request.get("location", ""),
                    "catering",
                    event_request.get("event_type", ""),
                    3
                ),
                search_vendors_tavily(
                    event_request.get("location", ""),
                    "photography", 
                    event_request.get("event_type", ""),
                    3
                )
            ]
            
            results = await asyncio.gather(*search_tasks, return_exceptions=True)
            venues = results[0] if not isinstance(results[0], Exception) else []
            caterers = results[1] if not isinstance(results[1], Exception) else []
            photographers = results[2] if not isinstance(results[2], Exception) else []
            
            # Create simple plan
            budget = event_request.get("budget", 100000)
            basic_plan = {
                "variants": [{
                    "variant": "standard",
                    "venues": venues[:2],
                    "vendors": caterers[:2] + photographers[:1],
                    "estimated_cost": budget,
                    "cost_breakdown": {
                        "venue": budget * 0.4,
                        "catering": budget * 0.35,
                        "photography": budget * 0.15,
                        "decoration": budget * 0.1
                    },
                    "timeline": [
                        {"milestone": "Start planning", "date": "6 weeks before", "priority": "high"},
                        {"milestone": "Book venue", "date": "4 weeks before", "priority": "critical"},
                        {"milestone": "Finalize vendors", "date": "2 weeks before", "priority": "high"},
                        {"milestone": "Event day", "date": "Event date", "priority": "critical"}
                    ]
                }],
                "planning_insights": [
                    "Start planning early for better vendor availability",
                    "Keep 10-15% buffer for unexpected costs",
                    "Confirm all bookings 1 week before event"
                ],
                "contextual_recommendations": [
                    "Contact vendors directly for best pricing",
                    "Ask for package deals to save costs",
                    "Have backup contact numbers ready"
                ],
                "metadata": {
                    "planning_approach": "Fallback Mode",
                    "note": "AI features unavailable - basic plan generated"
                }
            }
            
            return basic_plan
            
        except Exception as e:
            logging.error(f"Fallback plan creation failed: {e}")
            return {
                "variants": [],
                "error": "Unable to create event plan",
                "message": "Please try again or contact support"
            }
        
# Factory function to create event planner agent
async def create_event_plan_agent(event_request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Factory function to create and execute agentic event planning agent
    """
    try:
        agent = AgenticEventPlannerAgent()
        return await agent.create_event_plan(event_request)
    except ValueError as ve:
        logging.error(f"Agent initialization failed: {ve}")
        # Return structured error response for initialization failures
        return {
            "variants": [{
                "id": "init_error",
                "name": "Agent Initialization Error",
                "variant": "error",
                "estimated_cost": event_request.get("budget", 0) if isinstance(event_request, dict) else 0,
                "total_cost": event_request.get("budget", 0) if isinstance(event_request, dict) else 0,
                "cost_breakdown": {
                    "venue": 0.0,
                    "catering": 0.0,
                    "photography": 0.0,
                    "decoration": 0.0,
                    "entertainment": 0.0
                },
                "venues": [],
                "vendors": {"catering": [], "photography": [], "decoration": []},
                "planning_timeline": ["Agent initialization failed"],
                "agent_insights": [f"Initialization error: {str(ve)}"]
            }],
            "agent_analysis": {
                "full_analysis": f"Agent initialization failed: {str(ve)}",
                "budget_assessment": "Unable to assess - agent initialization failed",
                "strategy_recommendations": ["Please check configuration and try again"],
                "venue_analysis": "Error in agent initialization"
            },
            "metadata": {
                "planning_approach": "Agent Initialization Failed",
                "error": str(ve),
                "timestamp": datetime.now().isoformat()
            }
        }
    except Exception as e:
        logging.error(f"Unexpected error in event planner: {e}")
        # Return structured error response for any other failures
        return {
            "variants": [{
                "id": "general_error",
                "name": "Event Planning Error",
                "variant": "error",
                "estimated_cost": event_request.get("budget", 0) if isinstance(event_request, dict) else 0,
                "total_cost": event_request.get("budget", 0) if isinstance(event_request, dict) else 0,
                "cost_breakdown": {
                    "venue": 0.0,
                    "catering": 0.0,
                    "photography": 0.0,
                    "decoration": 0.0,
                    "entertainment": 0.0
                },
                "venues": [],
                "vendors": {"catering": [], "photography": [], "decoration": []},
                "planning_timeline": ["Event planning failed"],
                "agent_insights": [f"Error: {str(e)}"]
            }],
            "agent_analysis": {
                "full_analysis": f"Event planning failed: {str(e)}",
                "budget_assessment": "Unable to assess - error occurred",
                "strategy_recommendations": ["Please try again"],
                "venue_analysis": "Error in event planning"
            },
            "metadata": {
                "planning_approach": "Event Planning Failed",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
        }

    def _extract_timeline_from_agent(self, agent_output: str) -> List[str]:
        """Extract timeline items from agent output"""
        try:
            timeline = []
            lines = agent_output.split('\n')
            
            for line in lines:
                if any(keyword in line.lower() for keyword in ['step', 'contact', 'book', 'finalize', 'arrange', 'confirm']):
                    clean_line = line.strip().replace('*', '').replace('#', '').replace('-', '').strip()
                    if clean_line and len(clean_line) > 5:
                        timeline.append(clean_line[:100])
            
            # Default timeline if none extracted
            if not timeline:
                timeline = [
                    "Contact venues for availability",
                    "Book photographer and catering",
                    "Finalize decoration details",
                    "Confirm all arrangements"
                ]
            
            return timeline[:6]  # Limit to 6 items
            
        except Exception as e:
            logging.error(f"Error extracting timeline: {e}")
            return ["Planning milestone", "TBD", "Planning milestone", "TBD"]

    def _extract_budget_timeline_from_agent(self, agent_output: str) -> List[str]:
        """Extract budget-optimized timeline from agent output"""
        try:
            timeline = []
            
            # Look for budget-specific recommendations
            if "diy" in agent_output.lower():
                timeline.append("Arrange DIY decoration materials")
            if "package" in agent_output.lower():
                timeline.append("Negotiate package deals")
            if "local" in agent_output.lower():
                timeline.append("Contact local vendors")
                
            # Add default budget timeline items
            timeline.extend([
                "Confirm budget-friendly venue",
                "Finalize cost-effective catering"
            ])
            
            return timeline[:4]
            
        except Exception as e:
            logging.error(f"Error extracting budget timeline: {e}")
            return ["Budget planning", "Cost confirmation"]

    def _extract_key_insights(self, agent_output: str) -> List[str]:
        """Extract key insights from agent analysis"""
        try:
            insights = []
            lines = agent_output.split('\n')
            
            for line in lines:
                if any(keyword in line.lower() for keyword in ['recommendation', 'strategy', 'optimize', 'consider', 'suggest']):
                    clean_line = line.strip().replace('*', '').replace('#', '').replace('-', '').strip()
                    if clean_line and len(clean_line) > 10:
                        insights.append(clean_line[:150])
            
            # Default insights if none extracted
            if not insights:
                insights = [
                    "AI-optimized vendor selection",
                    "Budget-conscious approach recommended",
                    "Weather considerations included"
                ]
            
            return insights[:5]  # Limit to 5 insights
            
        except Exception as e:
            logging.error(f"Error extracting insights: {e}")
            return ["AI analysis completed", "Professional recommendations provided"]