import json
import logging
import re
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import asyncio
from langchain.schema import SystemMessage, HumanMessage
from .llm import get_chat_llm
from .tavily_search import is_valid_hotel_name


async def optimize_travel_plan(
    flights: List[Dict],
    hotels: List[Dict],
    pois: List[Dict],
    start_date: str,
    end_date: str,
    destination: str,
    budget: float,
    interests: List[str] = None,
    origin: str = "",
    travelers: int = 1
) -> Dict[str, Any]:
    """
    Create optimized travel plan using LLM as the primary planning agent.
    Generates 3 budget-aware variants with 5 places per day, proper budget splits,
    and detailed itineraries matching the user's input.
    """
    try:
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.strptime(end_date, "%Y-%m-%d")
        duration_days = (end_dt - start_dt).days
        if duration_days <= 0:
            duration_days = 3

        logging.info(
            f"Planning {duration_days}-day trip to {destination} | "
            f"Budget: ₹{budget:,.0f} | Travelers: {travelers} | Origin: {origin}"
        )

        # Primary: LLM agent generates the complete travel plan
        variants = await generate_llm_travel_plan(
            flights=flights,
            hotels=hotels,
            pois=pois,
            start_date=start_date,
            end_date=end_date,
            destination=destination,
            duration_days=duration_days,
            budget=budget,
            interests=interests or [],
            origin=origin,
            travelers=travelers
        )

        # Generate structured recommendations for the UI
        recommendations = generate_recommendations(
            destination=destination,
            budget=budget,
            duration_days=duration_days,
            interests=interests or [],
            variants=variants,
            origin=origin,
            travelers=travelers
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
            "status": "error",
            "variants": [],
            "recommendations": {}
        }


async def generate_llm_travel_plan(
    flights: List[Dict],
    hotels: List[Dict],
    pois: List[Dict],
    start_date: str,
    end_date: str,
    destination: str,
    duration_days: int,
    budget: float,
    interests: List[str],
    origin: str,
    travelers: int
) -> List[Dict]:
    """
    Use LLM as the primary travel planning agent.
    Generates 3 complete, budget-aware variants with 5 activities per day.
    Falls back to deterministic generation if LLM fails.
    """
    # Budget allocations
    b_budget = round(budget * 0.7)
    s_budget = round(budget * 1.0)
    p_budget = round(budget * 1.3)

    interests_str = ", ".join(interests) if interests else "sightseeing, local culture, food"

    # Build date list
    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    dates = [(start_dt + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(duration_days)]

    # Format real data for LLM context
    flights_text = _format_flights_for_prompt(flights[:5])
    hotels_text = _format_hotels_for_prompt(hotels[:5])
    pois_text = _format_pois_for_prompt(pois[:15])

    # Three sequential LLM calls — one variant each — avoids huge JSON / truncation parse errors
    variant_specs = [
        ("Budget Plan", b_budget, round(budget - b_budget), True,
         ["Economy class flights", "Budget-friendly hotel", "Major attractions", "Local transport", "Street food & local dining"]),
        ("Standard Plan", s_budget, 0, True,
         ["Preferred airlines", "Comfortable 3-star hotel", "Popular + hidden gems", "Mixed transport", "Restaurant dining"]),
        ("Premium Plan", p_budget, 0, False,
         ["Premium flights", "Luxury 4–5 star hotel", "Exclusive experiences", "Private transport", "Fine dining"]),
    ]

    try:
        llm = get_chat_llm()
        validated = []
        for vname, vcost, savings, within, feats in variant_specs:
            one = await _llm_single_variant(
                llm=llm,
                variant_name=vname,
                plan_budget=vcost,
                user_budget=budget,
                savings=savings,
                within_budget=within,
                features=feats,
                flights_text=flights_text,
                hotels_text=hotels_text,
                pois_text=pois_text,
                origin=origin,
                destination=destination,
                start_date=start_date,
                dates=dates,
                duration_days=duration_days,
                travelers=travelers,
                interests_str=interests_str,
            )
            if one:
                fixed = _validate_and_fix_variant(
                    one, budget, duration_days, start_date, destination, origin, travelers
                )
                if fixed:
                    validated.append(fixed)

        if validated:
            logging.info(f"LLM generated {len(validated)} travel variant(s) (sequential calls)")
            return validated

        raise ValueError("No valid variants from LLM")

    except Exception as e:
        logging.warning(f"LLM plan generation failed ({e}). Using deterministic fallback.")
        return _create_deterministic_variants(
            flights, hotels, pois, start_date, end_date, destination,
            duration_days, budget, interests, origin, travelers
        )


async def _llm_single_variant(
    llm,
    variant_name: str,
    plan_budget: float,
    user_budget: float,
    savings: float,
    within_budget: bool,
    features: List[str],
    flights_text: str,
    hotels_text: str,
    pois_text: str,
    origin: str,
    destination: str,
    start_date: str,
    dates: List[str],
    duration_days: int,
    travelers: int,
    interests_str: str,
) -> Optional[Dict]:
    """One variant per request — smaller JSON, fewer parse failures."""
    bf = round(plan_budget * 0.35)
    bh = round(plan_budget * 0.35)
    ba = round(plan_budget * 0.15)
    bm = round(plan_budget * 0.15)
    date_str = ", ".join([f"day{i+1}={d}" for i, d in enumerate(dates)])

    prompt = f"""You are a travel agent. Output ONE JSON object only (no markdown, no commentary).

TRIP: {origin or "Origin"} → {destination} | {start_date} + {duration_days} days | {travelers} travellers | Interests: {interests_str}
USER BUDGET (whole trip): ₹{user_budget:,.0f} INR
THIS VARIANT: "{variant_name}" — target total ₹{plan_budget:,.0f} INR
Cost split: flights ₹{bf:,} | hotels ₹{bh:,} | activities ₹{ba:,} | meals/transport ₹{bm:,}

LIVE SEARCH DATA (prefer these real names & prices when present):
--- FLIGHTS ---
{flights_text}
--- HOTELS ---
{hotels_text}
--- PLACES ---
{pois_text}

RULES:
- Include exactly 3 flight objects and 3 hotel objects (use DATA above; if insufficient, use realistic named options for this route).
- itinerary: {duration_days} days, dates {date_str}. EACH day: exactly 5 activities.
- Activity times: "9:00 AM - 10:30 AM", "11:00 AM - 12:30 PM", "2:00 PM - 3:30 PM", "4:30 PM - 6:00 PM", "7:00 PM - 9:00 PM"
- description fields max 120 characters. Use REAL venue names in {destination}.
- Numbers only for prices. INR.

JSON shape (fill all fields):
{{
  "variant": "{variant_name}",
  "description": "short string",
  "estimated_cost": {int(plan_budget)},
  "within_budget": {str(within_budget).lower()},
  "savings": {int(savings)},
  "features": {json.dumps(features)},
  "cost_breakdown": {{"flights": {bf}, "accommodation": {bh}, "activities": {ba}, "daily_expenses": {bm}, "total": {int(plan_budget)}}},
  "flights": [ {{ "airline": "", "price": 0, "departure": "", "arrival": "", "duration": "", "class": "", "stops": "", "route": "", "url": "", "source": "" }} ],
  "hotels": [ {{ "name": "", "price_per_night": 0, "total_price": 0, "rating": 0, "category": "", "location": "", "address": "", "amenities": [], "room_type": "", "url": "", "source": "" }} ],
  "itinerary": [ {{ "day": 1, "date": "", "theme": "", "activities": [ {{ "time": "", "period": "", "name": "", "activity": "", "location": "", "description": "", "cost": 0, "tips": "", "meal_suggestion": "", "transport": "", "type": "", "rating": 0 }} ], "meals": {{ "breakfast": "", "lunch": "", "dinner": "" }}, "estimated_cost": 0 }} ]
}}

Generate all {duration_days} days in "itinerary". Each day has exactly 5 activities. Return ONLY the JSON object."""

    messages = [
        SystemMessage(content=(
            "You output valid JSON only. No markdown fences. Escape quotes inside strings. "
            "Use real business names from DATA when provided."
        )),
        HumanMessage(content=prompt),
    ]
    response = await llm.ainvoke(messages)
    raw = (response.content or "").strip()
    content = _extract_json_from_response(raw)
    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        logging.warning(f"JSON decode for {variant_name}: {e}")
        return None
    return data if isinstance(data, dict) else None


# ---------------------------------------------------------------------------
# JSON extraction helper
# ---------------------------------------------------------------------------

def _extract_json_from_response(content: str) -> str:
    """Extract clean JSON from LLM response, stripping markdown wrappers."""
    if "```json" in content:
        m = re.search(r'```json\s*([\s\S]*?)\s*```', content)
        if m:
            return m.group(1).strip()
    if "```" in content:
        m = re.search(r'```\s*([\s\S]*?)\s*```', content)
        if m:
            return m.group(1).strip()
    start = content.find('{')
    end = content.rfind('}')
    if start != -1 and end != -1 and end > start:
        return content[start:end + 1]
    return content


# ---------------------------------------------------------------------------
# Variant validation and enrichment
# ---------------------------------------------------------------------------

def _validate_and_fix_variant(
    variant: Dict,
    budget: float,
    duration_days: int,
    start_date: str,
    destination: str,
    origin: str = "",
    travelers: int = 1
) -> Optional[Dict]:
    """Validate a single LLM variant and fix missing / malformed fields."""
    try:
        if not isinstance(variant, dict):
            return None

        variant_name = variant.get("variant", "Standard Plan")
        name_lower = variant_name.lower()

        # Determine plan budget multiplier
        if "budget" in name_lower:
            plan_budget = budget * 0.7
        elif "premium" in name_lower or "luxury" in name_lower:
            plan_budget = budget * 1.3
        else:
            plan_budget = budget * 1.0

        # --- cost breakdown ---
        cb = variant.get("cost_breakdown") or {}
        flights_cost = _to_float(cb.get("flights"), round(plan_budget * 0.35))
        accom_cost = _to_float(cb.get("accommodation"), round(plan_budget * 0.35))
        activity_cost = _to_float(cb.get("activities"), round(plan_budget * 0.15))
        daily_exp = _to_float(cb.get("daily_expenses"), round(plan_budget * 0.15))
        total = flights_cost + accom_cost + activity_cost + daily_exp

        estimated_cost = _to_float(variant.get("estimated_cost"), total)
        within_budget = estimated_cost <= budget
        savings = max(0.0, budget - estimated_cost)

        # --- flights ---
        raw_flights = variant.get("flights", [])
        if isinstance(raw_flights, list) and raw_flights and isinstance(raw_flights[0], dict):
            cleaned_flights = [_clean_flight(f, origin, destination, plan_budget) for f in raw_flights[:3]]
        else:
            cleaned_flights = _create_default_flights(destination, origin, flights_cost, name_lower)

        # --- hotels ---
        raw_hotels = variant.get("hotels", [])
        if isinstance(raw_hotels, list) and raw_hotels and isinstance(raw_hotels[0], dict):
            cleaned_hotels = [_clean_hotel(h, destination, duration_days, accom_cost) for h in raw_hotels[:3]]
        else:
            cleaned_hotels = _create_default_hotels(destination, accom_cost, duration_days, name_lower)

        # --- itinerary ---
        raw_itinerary = variant.get("itinerary", [])
        if isinstance(raw_itinerary, list) and raw_itinerary and isinstance(raw_itinerary[0], dict):
            cleaned_itinerary = [
                _clean_day(day, destination, round(plan_budget * 0.15 / max(duration_days, 1)))
                for day in raw_itinerary[:duration_days]
            ]
            # Fill any missing days
            start_dt = datetime.strptime(start_date, "%Y-%m-%d")
            for i in range(len(cleaned_itinerary), duration_days):
                day_date = (start_dt + timedelta(days=i)).strftime("%Y-%m-%d")
                cleaned_itinerary.append(_make_generic_day(i + 1, day_date, destination, round(plan_budget * 0.15 / max(duration_days, 1))))
        else:
            cleaned_itinerary = _make_generic_itinerary(duration_days, start_date, destination, plan_budget)

        # --- features ---
        features = variant.get("features")
        if not features or not isinstance(features, list):
            features = _default_features(name_lower)

        return {
            "variant": variant_name,
            "description": variant.get("description", f"{variant_name} for {destination}"),
            "estimated_cost": round(estimated_cost),
            "within_budget": within_budget,
            "savings": round(savings),
            "features": features,
            "cost_breakdown": {
                "flights": round(flights_cost),
                "accommodation": round(accom_cost),
                "activities": round(activity_cost),
                "daily_expenses": round(daily_exp),
                "total": round(total)
            },
            "flights": cleaned_flights,
            "hotels": cleaned_hotels,
            "itinerary": cleaned_itinerary,
            "days": duration_days
        }
    except Exception as e:
        logging.error(f"Error validating variant '{variant.get('variant')}': {e}")
        return None


def _clean_flight(f: Dict, origin: str, destination: str, plan_budget: float) -> Dict:
    """Clean and normalise a single flight object."""
    price = _to_float(f.get("price"), round(plan_budget * 0.35 / 2))
    return {
        "airline": f.get("airline") or "IndiGo",
        "price": round(price),
        "departure": f.get("departure") or "06:30 AM",
        "arrival": f.get("arrival") or "09:00 AM",
        "duration": f.get("duration") or "2h 30m",
        "class": f.get("class") or "Economy",
        "stops": f.get("stops") or "Direct",
        "route": f.get("route") or f"{origin or 'Origin'} → {destination}",
        "url": f.get("url") or "https://www.makemytrip.com/flights",
        "source": f.get("source") or "MakeMyTrip"
    }


def _clean_hotel(h: Dict, destination: str, duration_days: int, plan_budget: float) -> Dict:
    """Clean and normalise a single hotel object."""
    ppn = _to_float(h.get("price_per_night"), round(plan_budget * 0.35 / max(duration_days, 1)))
    total = _to_float(h.get("total_price"), ppn * duration_days)
    amenities = h.get("amenities")
    if not amenities or not isinstance(amenities, list):
        amenities = ["WiFi", "AC", "TV"]
    return {
        "name": h.get("name") or f"Hotel {destination}",
        "price_per_night": round(ppn),
        "total_price": round(total),
        "rating": min(5.0, max(1.0, _to_float(h.get("rating"), 3.5))),
        "category": h.get("category") or "mid-range",
        "location": h.get("location") or f"City Center, {destination}",
        "address": h.get("address") or f"City Center, {destination}",
        "amenities": amenities,
        "room_type": h.get("room_type") or "Deluxe Room",
        "url": h.get("url") or "https://www.booking.com",
        "source": h.get("source") or "Booking.com"
    }


def _clean_day(day: Dict, destination: str, budget_per_day: int) -> Dict:
    """Clean and normalise a single itinerary day, ensuring 5 activities."""
    time_slots = [
        ("9:00 AM - 10:30 AM", "Morning"),
        ("11:00 AM - 12:30 PM", "Late Morning"),
        ("2:00 PM - 3:30 PM", "Afternoon"),
        ("4:30 PM - 6:00 PM", "Late Afternoon"),
        ("7:00 PM - 9:00 PM", "Evening")
    ]

    raw_activities = day.get("activities", [])
    activities = []

    for idx, (ts, period) in enumerate(time_slots):
        if idx < len(raw_activities) and isinstance(raw_activities[idx], dict):
            a = raw_activities[idx]
            name = a.get("name") or f"{destination} Attraction"
            activities.append({
                "time": a.get("time") or ts,
                "period": a.get("period") or period,
                "name": name,
                "activity": a.get("activity") or f"Visit {name}",
                "location": a.get("location") or f"Central {destination}",
                "description": _ensure_description(a.get("description"), name, destination),
                "cost": _to_int(a.get("cost"), 0),
                "tips": a.get("tips") or f"Best visited during {period.lower()}. Check timings before visit.",
                "meal_suggestion": a.get("meal_suggestion") or f"Try local cuisine near {name}",
                "transport": a.get("transport") or "Take auto-rickshaw or local taxi",
                "type": a.get("type") or "sightseeing",
                "rating": min(5.0, max(1.0, _to_float(a.get("rating"), 4.0))),
                "url": a.get("url") or ""
            })
        else:
            # Pad with a generic activity for missing slots
            activities.append({
                "time": ts,
                "period": period,
                "name": f"{destination} {period} Experience",
                "activity": f"Explore {destination} during {period.lower()} hours",
                "location": f"City Center, {destination}",
                "description": (
                    f"Spend this {period.lower()} exploring the vibrant local culture of {destination}. "
                    f"Visit nearby markets, cafes, and points of interest as you soak in the atmosphere."
                ),
                "cost": 0,
                "tips": "Ask locals for their favourite spots and hidden gems",
                "meal_suggestion": f"Try authentic {destination} street food available nearby",
                "transport": "Walk or use local auto-rickshaw",
                "type": "cultural",
                "rating": 4.0
            })

    meals = day.get("meals") or {}
    return {
        "day": _to_int(day.get("day"), 1),
        "date": day.get("date") or "",
        "theme": day.get("theme") or f"Day {day.get('day', 1)} - City Exploration",
        "activities": activities,
        "meals": {
            "breakfast": meals.get("breakfast") or f"Local breakfast near your hotel in {destination}",
            "lunch": meals.get("lunch") or f"Lunch at a recommended {destination} restaurant",
            "dinner": meals.get("dinner") or f"Dinner featuring {destination} local specialties"
        },
        "estimated_cost": _to_int(day.get("estimated_cost"), budget_per_day)
    }


def _ensure_description(desc: Any, name: str, destination: str) -> str:
    """Ensure description is a non-trivial string."""
    if isinstance(desc, str) and len(desc.strip()) > 30:
        return desc.strip()
    return (
        f"{name} is one of the must-visit attractions in {destination}, offering a unique experience "
        f"for all types of travellers. Visitors can explore the rich heritage, architecture, and stories "
        f"that make this place special."
    )


# ---------------------------------------------------------------------------
# Deterministic fallback (5 activities per day)
# ---------------------------------------------------------------------------

def _create_deterministic_variants(
    flights: List[Dict],
    hotels: List[Dict],
    pois: List[Dict],
    start_date: str,
    end_date: str,
    destination: str,
    duration_days: int,
    budget: float,
    interests: List[str],
    origin: str,
    travelers: int
) -> List[Dict]:
    """Deterministic fallback: 3 variants, 5 activities/day, real Tavily data."""
    sorted_flights = sorted(flights, key=lambda x: x.get('price', 0)) if flights else []
    clean_hotels = [h for h in (hotels or []) if is_valid_hotel_name(str(h.get("name", "")))]
    sorted_hotels = sorted(clean_hotels, key=lambda x: x.get("price_per_night", 0)) if clean_hotels else []

    configs = [
        {
            "name": "Budget Plan",
            "mult": 0.7,
            "fl_slice": slice(0, 3),
            "ht_slice": slice(0, 3),
            "poi_limit": 15,
            "features": ["Economy class flights", "Budget-friendly accommodation", "All major attractions", "Local transport", "Street food & local dining"],
            "cat": "budget"
        },
        {
            "name": "Standard Plan",
            "mult": 1.0,
            "fl_slice": slice(0, 3),
            "ht_slice": slice(0, 3),
            "poi_limit": 20,
            "features": ["Preferred airline flights", "Comfortable 3-star hotel", "Popular attractions & hidden gems", "Mix of transport", "Restaurant dining"],
            "cat": "standard"
        },
        {
            "name": "Premium Plan",
            "mult": 1.3,
            "fl_slice": slice(-3, None),
            "ht_slice": slice(-3, None),
            "poi_limit": 25,
            "features": ["Premium/business flights", "Luxury 4-5 star hotel", "All attractions + exclusive experiences", "Private transport", "Fine dining"],
            "cat": "premium"
        }
    ]

    variants = []
    for cfg in configs:
        pb = round(budget * cfg["mult"])
        fl = sorted_flights[cfg["fl_slice"]] or _create_default_flights(destination, origin, round(pb * 0.35), cfg["cat"])
        ht = sorted_hotels[cfg["ht_slice"]] or _create_default_hotels(destination, round(pb * 0.35), duration_days, cfg["cat"])

        itinerary = _create_poi_based_itinerary(
            pois[:cfg["poi_limit"]], duration_days, start_date, destination,
            round(pb * 0.15 / max(duration_days, 1))
        )

        f_cost = round(pb * 0.35)
        h_cost = round(pb * 0.35)
        a_cost = round(pb * 0.15)
        d_cost = round(pb * 0.15)
        total = f_cost + h_cost + a_cost + d_cost

        variants.append({
            "variant": cfg["name"],
            "description": f"{cfg['name']} for a great {destination} experience",
            "estimated_cost": total,
            "within_budget": total <= budget,
            "savings": max(0, round(budget - total)),
            "features": cfg["features"],
            "cost_breakdown": {
                "flights": f_cost,
                "accommodation": h_cost,
                "activities": a_cost,
                "daily_expenses": d_cost,
                "total": total
            },
            "flights": fl,
            "hotels": ht,
            "itinerary": itinerary,
            "days": duration_days
        })

    return variants


def _create_poi_based_itinerary(
    pois: List[Dict],
    duration_days: int,
    start_date: str,
    destination: str,
    budget_per_day: int
) -> List[Dict]:
    """Build a {duration_days}-day itinerary with 5 activities per day from POI data."""
    start_dt = datetime.strptime(start_date, "%Y-%m-%d")

    time_slots = [
        ("9:00 AM - 10:30 AM", "Morning"),
        ("11:00 AM - 12:30 PM", "Late Morning"),
        ("2:00 PM - 3:30 PM", "Afternoon"),
        ("4:30 PM - 6:00 PM", "Late Afternoon"),
        ("7:00 PM - 9:00 PM", "Evening")
    ]

    day_themes = [
        "Arrival & City Highlights",
        "Historical & Cultural Exploration",
        "Nature & Scenic Wonders",
        "Local Markets, Food & Shopping",
        "Hidden Gems & Leisure Day",
        "Art, Museums & Architecture",
        "Spiritual & Heritage Walk"
    ]

    # Deduplicate POIs
    seen = set()
    unique_pois = []
    for p in pois:
        key = p.get('name', '').strip().lower().replace(' ', '')
        if key and key not in seen and len(key) > 3:
            seen.add(key)
            unique_pois.append(p)

    poi_idx = 0
    itinerary = []

    for day in range(duration_days):
        day_date = (start_dt + timedelta(days=day)).strftime("%Y-%m-%d")
        theme = day_themes[day % len(day_themes)]
        activities = []

        for ts, period in time_slots:
            if poi_idx < len(unique_pois):
                p = unique_pois[poi_idx]
                poi_idx += 1
                name = p.get('name', f'{destination} Attraction')
                loc = p.get('location') or p.get('address') or f"Central {destination}"
                desc = p.get('description') or p.get('content') or ""
                activities.append({
                    "time": ts,
                    "period": period,
                    "name": name,
                    "activity": f"Visit {name}",
                    "location": loc if loc != destination else f"Central {destination}",
                    "description": _ensure_description(desc, name, destination),
                    "cost": _to_int(p.get('ticket_price'), 0),
                    "tips": f"Best visited during {period.lower()}. Check opening hours before visiting.",
                    "meal_suggestion": f"Enjoy local food near {name} — ask locals for best spots",
                    "transport": f"Take local auto/taxi or metro to {name}",
                    "type": p.get('type') or 'sightseeing',
                    "rating": min(5.0, max(1.0, _to_float(p.get('rate') or p.get('rating'), 4.0))),
                    "url": p.get('url') or ""
                })
            else:
                activities.append({
                    "time": ts,
                    "period": period,
                    "name": f"{destination} {period} Exploration",
                    "activity": f"Explore {destination} neighbourhood",
                    "location": f"City Center, {destination}",
                    "description": (
                        f"Wander through the vibrant streets of {destination} during the {period.lower()} "
                        f"and discover the city's authentic charm, local cafes, street art, and everyday life."
                    ),
                    "cost": 0,
                    "tips": "Explore on foot for the best experience; carry water and comfortable shoes",
                    "meal_suggestion": f"Try street food and local snacks available in {destination} markets",
                    "transport": "Walk or use local transport",
                    "type": "cultural",
                    "rating": 4.0
                })

        itinerary.append({
            "day": day + 1,
            "date": day_date,
            "theme": theme,
            "activities": activities,
            "meals": {
                "breakfast": f"Start with a local breakfast at your hotel or a nearby café in {destination}",
                "lunch": f"Lunch at a popular {destination} restaurant near your afternoon activities",
                "dinner": f"Evening dinner featuring authentic {destination} cuisine — explore local specialties"
            },
            "estimated_cost": budget_per_day
        })

    return itinerary


def _make_generic_day(day_num: int, day_date: str, destination: str, budget_per_day: int) -> Dict:
    """Create a fully generic day when no data is available."""
    time_slots = [
        ("9:00 AM - 10:30 AM", "Morning"),
        ("11:00 AM - 12:30 PM", "Late Morning"),
        ("2:00 PM - 3:30 PM", "Afternoon"),
        ("4:30 PM - 6:00 PM", "Late Afternoon"),
        ("7:00 PM - 9:00 PM", "Evening")
    ]
    themes_list = [
        "City Highlights", "Cultural Exploration", "Nature & Parks",
        "Shopping & Food", "Heritage & Leisure"
    ]
    theme = themes_list[(day_num - 1) % len(themes_list)]

    activities = []
    for ts, period in time_slots:
        activities.append({
            "time": ts,
            "period": period,
            "name": f"{destination} — {period} Activity",
            "activity": f"Explore {destination} during the {period.lower()}",
            "location": f"Central {destination}",
            "description": (
                f"A great opportunity to explore {destination} during the {period.lower()}. "
                f"Visit local landmarks, enjoy the atmosphere, and discover what makes {destination} special."
            ),
            "cost": 0,
            "tips": "Carry a travel guide and ask locals for personalised recommendations",
            "meal_suggestion": f"Nearby {destination} eateries for a quick, authentic bite",
            "transport": "Local auto, taxi, or metro",
            "type": "sightseeing",
            "rating": 4.0
        })

    return {
        "day": day_num,
        "date": day_date,
        "theme": f"Day {day_num} — {theme}",
        "activities": activities,
        "meals": {
            "breakfast": f"Hotel breakfast or local café in {destination}",
            "lunch": f"Local {destination} restaurant recommended by hotel staff",
            "dinner": f"Authentic {destination} dinner — try the local specialties"
        },
        "estimated_cost": budget_per_day
    }


def _make_generic_itinerary(duration_days: int, start_date: str, destination: str, plan_budget: float) -> List[Dict]:
    """Fallback itinerary when all else fails."""
    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    bpd = round(plan_budget * 0.15 / max(duration_days, 1))
    return [
        _make_generic_day(
            d + 1,
            (start_dt + timedelta(days=d)).strftime("%Y-%m-%d"),
            destination,
            bpd
        )
        for d in range(duration_days)
    ]


# ---------------------------------------------------------------------------
# Default data creators
# ---------------------------------------------------------------------------

def _create_default_flights(destination: str, origin: str, budget: float, category: str) -> List[Dict]:
    airline_map = {
        "budget": [("IndiGo", "06:30 AM", "09:00 AM", "Economy", 0),
                   ("SpiceJet", "09:15 AM", "11:45 AM", "Economy", 500),
                   ("AirAsia India", "02:00 PM", "04:30 PM", "Economy", 800)],
        "standard": [("Air India", "07:00 AM", "09:30 AM", "Economy", 0),
                     ("Vistara", "11:00 AM", "01:30 PM", "Economy", 1000),
                     ("IndiGo", "04:00 PM", "06:30 PM", "Economy", 500)],
        "premium": [("Vistara", "06:00 AM", "08:30 AM", "Business", 0),
                    ("Air India", "10:00 AM", "12:30 PM", "Business", 2000),
                    ("Emirates", "02:30 PM", "05:00 PM", "Business", 3000)]
    }
    cat = "budget" if "budget" in category else ("premium" if "premium" in category else "standard")
    base_price = round(budget / 2)
    return [
        {
            "airline": al, "price": max(500, base_price + var),
            "departure": dep, "arrival": arr, "duration": "2h 30m",
            "class": cls, "stops": "Direct",
            "route": f"{origin or 'Origin'} → {destination}",
            "url": "https://www.makemytrip.com/flights", "source": "MakeMyTrip"
        }
        for al, dep, arr, cls, var in airline_map[cat]
    ]


def _create_default_hotels(destination: str, budget: float, duration_days: int, category: str) -> List[Dict]:
    hotel_map = {
        "budget": [
            (f"OYO Rooms {destination}", 3.2, ["WiFi", "AC", "TV", "24hr Desk"], "Standard Room"),
            (f"Zostel {destination}", 3.4, ["WiFi", "AC", "Common Area", "Lockers"], "Dorm/Private Room"),
            (f"City Lodge {destination}", 3.5, ["WiFi", "AC", "TV"], "Standard Room")
        ],
        "standard": [
            (f"Lemon Tree Hotel {destination}", 4.0, ["WiFi", "AC", "Restaurant", "Gym", "Parking"], "Deluxe Room"),
            (f"Sarovar Portico {destination}", 4.1, ["WiFi", "AC", "Pool", "Restaurant", "Gym"], "Deluxe Room"),
            (f"The Fern {destination}", 4.2, ["WiFi", "AC", "Restaurant", "Room Service", "Parking"], "Superior Room")
        ],
        "premium": [
            (f"Taj Hotel {destination}", 4.8, ["WiFi", "Spa", "Pool", "Gym", "Restaurant", "Bar", "Concierge", "Valet"], "Executive Suite"),
            (f"Marriott {destination}", 4.7, ["WiFi", "Spa", "Pool", "Gym", "Restaurant", "Bar", "Concierge"], "Deluxe Suite"),
            (f"Hyatt Regency {destination}", 4.6, ["WiFi", "Spa", "Pool", "Gym", "Restaurant", "Lounge"], "King Room")
        ]
    }
    cat = "budget" if "budget" in category else ("premium" if "premium" in category else "standard")
    ppn = max(300, round(budget / max(duration_days, 1)))
    return [
        {
            "name": name,
            "price_per_night": round(ppn * (1 + i * 0.1)),
            "total_price": round(ppn * (1 + i * 0.1)) * duration_days,
            "rating": rating,
            "category": cat,
            "location": f"City Center, {destination}",
            "address": f"City Center, {destination}",
            "amenities": amenities,
            "room_type": room,
            "url": "https://www.booking.com",
            "source": "Booking.com"
        }
        for i, (name, rating, amenities, room) in enumerate(hotel_map[cat])
    ]


# ---------------------------------------------------------------------------
# Recommendations (structured for frontend)
# ---------------------------------------------------------------------------

def generate_recommendations(
    destination: str,
    budget: float,
    duration_days: int,
    interests: List[str],
    variants: List[Dict],
    origin: str = "",
    travelers: int = 1
) -> Dict[str, Any]:
    """Generate structured travel recommendations matching the frontend's expected format."""
    try:
        if not variants:
            raise ValueError("No variants")

        def activity_count(v):
            return sum(len(d.get('activities', [])) for d in v.get('itinerary', []))

        best_value = min(variants, key=lambda v: v.get('estimated_cost', budget) / max(activity_count(v), 1))
        most_comprehensive = max(variants, key=activity_count)

        budget_efficiency = {
            v.get('variant', 'Plan'): round((v.get('estimated_cost', 0) / budget) * 100, 1)
            for v in variants
        }

        highlights = get_destination_highlights(destination)
        best_time = get_seasonal_advice(destination)

        interest_tips = []
        for interest in (interests or [])[:2]:
            interest_tips.append(
                f"For {interest.lower()} enthusiasts: {destination} has excellent {interest.lower()} spots worth exploring"
            )

        return {
            "summary": {
                "destination_overview": (
                    f"Exploring {destination} with {travelers} traveler(s) for {duration_days} days "
                    f"departing from {origin or 'your city'}"
                ),
                "budget_analysis": (
                    f"Your budget of ₹{budget:,.0f} has been split across flights (35%), accommodation (35%), "
                    f"activities (15%), and meals & transport (15%) for optimal value"
                ),
                "best_time_insight": best_time,
                "trip_highlights": highlights
            },
            "variant_analysis": {
                "best_value": {
                    "variant": best_value.get('variant', 'Budget Plan'),
                    "reason": "Provides the highest number of experiences per rupee spent",
                    "cost": best_value.get('estimated_cost', 0)
                },
                "most_comprehensive": {
                    "variant": most_comprehensive.get('variant', 'Premium Plan'),
                    "reason": f"Covers the maximum attractions across all {duration_days} days in {destination}",
                    "activities": activity_count(most_comprehensive)
                },
                "budget_efficiency": budget_efficiency
            },
            "personalized_tips": [
                f"For {travelers} traveler(s), the '{best_value.get('variant')}' offers the best value-for-money",
                f"Book {origin} to {destination} flights 3–4 weeks in advance for best fares",
                f"Local transport in {destination} (metro/auto/bus) is affordable — use it to save on transport",
                "Download Google Maps offline for {destination} to navigate without data",
                "Carry local currency for markets, street food, and small vendors"
            ] + interest_tips,
            "smart_savings": [
                f"Compare flight prices across MakeMyTrip, Goibibo, and Ixigo for {origin} → {destination}",
                "Book accommodation 1–2 km from the main tourist area for better rates",
                "Many {destination} attractions have discounted or free entry on certain days",
                "Street food and local restaurants in {destination} are authentic and budget-friendly",
                "Use Ola/Uber instead of tourist taxis for significant savings on local transport"
            ],
            "safety_tips": [
                "Keep digital and physical copies of all travel documents (passport, ID, tickets)",
                "Share your complete itinerary with family or friends back home",
                f"Use only registered taxis or ride-sharing apps in {destination}",
                f"Stay in well-reviewed, centrally located accommodation in {destination}",
                "Keep emergency contacts: local police (100), ambulance (108), and your hotel's number"
            ]
        }
    except Exception as e:
        logging.error(f"Error generating recommendations: {e}")
        return {
            "summary": {
                "destination_overview": f"Exploring {destination}",
                "budget_analysis": f"Budget of ₹{budget:,.0f} allocated across the trip",
                "best_time_insight": "Check local weather before your visit",
                "trip_highlights": [f"{destination} cultural highlights", "Local cuisine", "Historical sites"]
            },
            "personalized_tips": ["Plan in advance for the best experience", "Stay safe and enjoy your trip"],
            "smart_savings": ["Compare prices across platforms", "Book accommodation in advance"],
            "safety_tips": ["Keep documents safe", "Stay in touch with family"]
        }


# ---------------------------------------------------------------------------
# Destination helpers
# ---------------------------------------------------------------------------

def get_destination_highlights(destination: str) -> List[str]:
    highlights_map = {
        "mumbai": ["Gateway of India", "Marine Drive", "Bollywood Film City", "Elephanta Caves", "Juhu Beach"],
        "delhi": ["Red Fort", "Qutub Minar", "India Gate", "Humayun's Tomb", "Chandni Chowk Market"],
        "bangalore": ["Lalbagh Botanical Garden", "Cubbon Park", "ISKCON Temple", "Nandi Hills", "Commercial Street"],
        "chennai": ["Marina Beach", "Kapaleeshwarar Temple", "Fort St. George", "Mahabalipuram", "Government Museum"],
        "goa": ["Baga Beach", "Fort Aguada", "Basilica of Bom Jesus", "Dudhsagar Falls", "Anjuna Flea Market"],
        "kerala": ["Alleppey Backwaters", "Munnar Tea Gardens", "Periyar Wildlife Sanctuary", "Kovalam Beach", "Fort Kochi"],
        "jaipur": ["Amber Fort", "Hawa Mahal", "City Palace", "Jantar Mantar", "Nahargarh Fort"],
        "agra": ["Taj Mahal", "Agra Fort", "Fatehpur Sikri", "Mehtab Bagh", "Itmad-ud-Daulah Tomb"],
        "kolkata": ["Victoria Memorial", "Howrah Bridge", "Dakshineswar Temple", "Indian Museum", "Eden Gardens"],
        "hyderabad": ["Charminar", "Golconda Fort", "Hussain Sagar Lake", "Salar Jung Museum", "Ramoji Film City"],
        "varanasi": ["Dashashwamedh Ghat", "Kashi Vishwanath Temple", "Sarnath", "Manikarnika Ghat", "Ramnagar Fort"],
        "dubai": ["Burj Khalifa", "Dubai Mall", "Palm Jumeirah", "Dubai Creek & Gold Souk", "Desert Safari"],
        "singapore": ["Marina Bay Sands", "Gardens by the Bay", "Sentosa Island", "Universal Studios", "Orchard Road"],
        "bangkok": ["Grand Palace", "Wat Pho", "Chatuchak Weekend Market", "Floating Markets", "Khao San Road"],
        "paris": ["Eiffel Tower", "Louvre Museum", "Notre-Dame Cathedral", "Champs-Élysées", "Palace of Versailles"],
        "london": ["Big Ben & Westminster", "Tower of London", "Buckingham Palace", "British Museum", "Hyde Park"],
        "new york": ["Statue of Liberty", "Times Square", "Central Park", "Empire State Building", "Metropolitan Museum"],
        "tokyo": ["Senso-ji Temple", "Shibuya Crossing", "Mount Fuji Day Trip", "Shinjuku Gyoen", "teamLab Borderless"]
    }
    dest_lower = destination.lower()
    for key, hl in highlights_map.items():
        if key in dest_lower:
            return hl
    return [
        f"{destination} Historical Landmarks",
        f"{destination} Local Cuisine & Street Food",
        f"{destination} Cultural Heritage Sites",
        "Local Markets & Shopping",
        "Natural Scenic Attractions"
    ]


def get_seasonal_advice(destination: str) -> str:
    import datetime as dt
    m = dt.datetime.now().month
    if m in [12, 1, 2]:
        season, advice = "Winter (Dec–Feb)", "pleasant and cool weather — ideal for outdoor sightseeing"
    elif m in [3, 4, 5]:
        season, advice = "Summer (Mar–May)", "warmer temperatures — carry sunscreen and stay hydrated"
    elif m in [6, 7, 8, 9]:
        season, advice = "Monsoon (Jun–Sep)", "lush greenery with occasional rains — carry an umbrella"
    else:
        season, advice = "Post-Monsoon (Oct–Nov)", "excellent clear weather — one of the best times to visit"
    return f"{season}: {destination} currently has {advice}"


def get_destination_currency(destination: str) -> str:
    currency_map = {
        'india': 'INR', 'mumbai': 'INR', 'delhi': 'INR', 'bangalore': 'INR',
        'chennai': 'INR', 'kolkata': 'INR', 'goa': 'INR', 'jaipur': 'INR',
        'hyderabad': 'INR', 'kerala': 'INR', 'agra': 'INR', 'varanasi': 'INR',
        'dubai': 'AED', 'singapore': 'SGD', 'bangkok': 'THB', 'kuala lumpur': 'MYR',
        'london': 'GBP', 'paris': 'EUR', 'rome': 'EUR', 'amsterdam': 'EUR',
        'new york': 'USD', 'los angeles': 'USD', 'tokyo': 'JPY', 'sydney': 'AUD'
    }
    dest_lower = destination.lower()
    for key, currency in currency_map.items():
        if key in dest_lower:
            return currency
    return 'INR'


# ---------------------------------------------------------------------------
# LLM prompt formatters
# ---------------------------------------------------------------------------

def _fmt(n) -> str:
    """Format a number with Indian comma grouping, no decimals."""
    try:
        return f"{int(round(float(str(n).replace(',', '').replace('₹', '')))):,}"
    except (TypeError, ValueError):
        return "0"


def _format_flights_for_prompt(flights: List[Dict]) -> str:
    """Format flight list as readable text for the LLM prompt."""
    if not flights:
        return "No flight data available from search — generate realistic options based on the route."
    lines = []
    for i, f in enumerate(flights, 1):
        airline   = f.get('airline', 'Unknown')
        price     = f.get('price', 0)
        departure = f.get('departure', '')
        duration  = f.get('duration', '')
        route     = f.get('route', '')
        source    = f.get('source', 'Web Search')
        lines.append(
            f"{i}. {airline} | Rs.{_fmt(price)}/person | Departs: {departure} | "
            f"Duration: {duration} | Route: {route} | Source: {source}"
        )
    return "\n".join(lines)


def _format_hotels_for_prompt(hotels: List[Dict]) -> str:
    """Format hotel list as readable text for the LLM prompt."""
    if not hotels:
        return "No hotel data available from search — generate realistic options matching the budget."
    lines = []
    for i, h in enumerate(hotels, 1):
        name     = h.get('name', 'Unknown Hotel')
        ppn      = h.get('price_per_night', h.get('price', 0))
        rating   = h.get('rating', 0)
        location = h.get('location', '')
        source   = h.get('source', 'Web Search')
        lines.append(
            f"{i}. {name} | Rs.{_fmt(ppn)}/night | Rating: {rating} stars | "
            f"Location: {location} | Source: {source}"
        )
    return "\n".join(lines)


def _format_pois_for_prompt(pois: List[Dict]) -> str:
    """Format POI list as readable text for the LLM prompt."""
    if not pois:
        return "No attraction data available from search — use well-known places at the destination."
    lines = []
    for i, p in enumerate(pois, 1):
        name     = p.get('name', 'Unknown')
        location = p.get('location') or p.get('address', '')
        ptype    = p.get('type', 'attraction')
        fee      = p.get('ticket_price', 0)
        desc     = (p.get('description') or p.get('content') or '')[:80]
        lines.append(
            f"{i}. {name} ({ptype}) | Location: {location} | Entry: Rs.{_fmt(fee)} | {desc}"
        )
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Utility helpers
# ---------------------------------------------------------------------------

def _to_float(val: Any, default: float = 0.0) -> float:
    try:
        return float(str(val).replace(',', '').replace('₹', '').strip())
    except (TypeError, ValueError):
        return default


def _to_int(val: Any, default: int = 0) -> int:
    return int(round(_to_float(val, default)))


def _default_features(name_lower: str) -> List[str]:
    if "budget" in name_lower:
        return ["Economy class flights", "Budget accommodation", "All major attractions", "Local transport", "Street food & local restaurants"]
    elif "premium" in name_lower:
        return ["Business/premium class flights", "Luxury 4-5 star hotel", "All attractions + exclusive tours", "Private transport", "Fine dining included"]
    return ["Economy flights", "Comfortable 3-star hotel", "Popular attractions & hidden gems", "Mix of transport", "Restaurant dining"]


# ---------------------------------------------------------------------------
# Legacy compatibility — kept so existing imports don't break
# ---------------------------------------------------------------------------

def create_basic_daily_itinerary(pois: List[Dict], duration_days: int, start_date: str) -> List[Dict]:
    """Legacy function — delegates to the new 5-activity implementation."""
    return _create_poi_based_itinerary(pois, duration_days, start_date, "destination", 1000)
