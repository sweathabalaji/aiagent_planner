import logging
from typing import Dict, List, Any
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.tavily_search import search_event_catering

async def search_caterers(location: str, cuisine_type: str, guest_count: int, event_type: str, budget: float = None, max_results: int = 5) -> List[Dict[str, Any]]:
    """
    Search for catering services using Tavily API with real-time data
    """
    try:
        logging.info(f"Searching caterers in {location} for {cuisine_type} cuisine, {guest_count} guests")
        
        # Use Tavily for comprehensive catering search
        caterers = await search_event_catering(location, cuisine_type, guest_count, event_type, budget, max_results)
        
        # Enhance catering data with additional processing
        enhanced_caterers = []
        for caterer in caterers:
            enhanced_caterer = {
                "name": caterer.get("name", ""),
                "service_type": "catering",
                "location": caterer.get("location", location),
                "cuisine_type": caterer.get("cuisine_type", cuisine_type),
                "price_per_person": caterer.get("price_per_person"),
                "menu_highlights": caterer.get("menu_highlights", []),
                "description": caterer.get("description", ""),
                "website": caterer.get("url", ""),
                "contact": caterer.get("contact", "Contact caterer directly"),
                "specialties": caterer.get("menu_highlights", []),
                "dietary_options": get_dietary_options(cuisine_type),
                "minimum_order": guest_count
            }
            enhanced_caterers.append(enhanced_caterer)
        
        logging.info(f"Found {len(enhanced_caterers)} caterers for {event_type}")
        return enhanced_caterers
        
    except Exception as e:
        logging.error(f"Catering search failed: {e}")
        raise RuntimeError(f"Unable to search caterers: {e}")

def get_dietary_options(cuisine_type: str) -> List[str]:
    """
    Get common dietary options based on cuisine type
    """
    dietary_options = ["Vegetarian", "Non-Vegetarian"]
    
    if "indian" in cuisine_type.lower():
        dietary_options.extend(["Pure Vegetarian", "Jain Food", "Vegan Options"])
    elif "continental" in cuisine_type.lower():
        dietary_options.extend(["Gluten-Free", "Vegan", "Keto-Friendly"])
    elif "chinese" in cuisine_type.lower():
        dietary_options.extend(["Vegan Options", "Low-Sodium"])
    
    return dietary_options

async def get_menu_suggestions(event_type: str, guest_count: int, cuisine_type: str) -> Dict[str, List[str]]:
    """
    Get menu suggestions based on event type and preferences
    """
    try:
        base_menu = {
            "appetizers": [],
            "main_course": [],
            "desserts": [],
            "beverages": []
        }
        
        if "indian" in cuisine_type.lower():
            base_menu["appetizers"] = ["Samosa", "Pakora", "Paneer Tikka", "Chicken Tikka"]
            base_menu["main_course"] = ["Dal Makhani", "Paneer Butter Masala", "Chicken Curry", "Biryani", "Roti/Naan"]
            base_menu["desserts"] = ["Gulab Jamun", "Rasmalai", "Ice Cream"]
            base_menu["beverages"] = ["Tea", "Coffee", "Fresh Lime Water", "Lassi"]
            
        elif "continental" in cuisine_type.lower():
            base_menu["appetizers"] = ["Bruschetta", "Caesar Salad", "Soup of the Day"]
            base_menu["main_course"] = ["Grilled Chicken", "Pasta", "Steamed Vegetables", "Garlic Bread"]
            base_menu["desserts"] = ["Chocolate Cake", "Fresh Fruits", "Ice Cream"]
            base_menu["beverages"] = ["Coffee", "Tea", "Fresh Juices", "Soft Drinks"]
            
        elif "chinese" in cuisine_type.lower():
            base_menu["appetizers"] = ["Spring Rolls", "Manchow Soup", "Honey Chili Potatoes"]
            base_menu["main_course"] = ["Fried Rice", "Hakka Noodles", "Sweet & Sour Chicken", "Szechuan Vegetables"]
            base_menu["desserts"] = ["Date Pancake", "Ice Cream"]
            base_menu["beverages"] = ["Green Tea", "Fresh Juices", "Soft Drinks"]
        
        # Adjust portions based on guest count
        if guest_count > 100:
            base_menu["additional_options"] = ["Live Counters", "Buffet Setup", "Multiple Cuisine Stations"]
        
        return base_menu
        
    except Exception as e:
        logging.error(f"Menu suggestion failed: {e}")
        return {"error": "Unable to generate menu suggestions"}