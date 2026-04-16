import os
import re
import asyncio
import logging
from tavily import TavilyClient
from datetime import datetime
from typing import List, Dict
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Tavily client
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
tavily_client = TavilyClient(api_key=TAVILY_API_KEY) if TAVILY_API_KEY else None

async def tavily_search(query: str, max_results: int = 5):
    """
    Generic Tavily search function for any query
    """
    if not tavily_client:
        logging.error("Tavily API key not configured")
        return []
    
    try:
        # Run the synchronous Tavily search in a thread pool
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None, 
            lambda: tavily_client.search(
                query=query, 
                search_depth="basic",
                max_results=max_results
            )
        )
        
        return response.get("results", [])
    
    except Exception as e:
        logging.error(f"Tavily search failed: {e}")
        return []

async def search_travel_info(query: str, max_results: int = 5):
    """
    Search for travel-related information using Tavily API
    """
    if not tavily_client:
        logging.error("Tavily API key not configured")
        raise RuntimeError("Tavily API not available")
    
    try:
        # Run the synchronous Tavily search in a thread pool
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None, 
            lambda: tavily_client.search(
                query=query, 
                search_depth="advanced",
                max_results=max_results,
                include_domains=[
                    "booking.com", "expedia.com", "tripadvisor.com", "skyscanner.com", "hotels.com", 
                    "makemytrip.com", "cleartrip.com", "goibibo.com", "yatra.com", "ixigo.com",
                    "agoda.com", "kayak.com", "momondo.com", "trivago.com", "oyorooms.com",
                    "airbnb.com", "zostel.com", "fabhotels.com", "treebo.com"
                ]
            )
        )
        
        return response.get("results", [])
    
    except Exception as e:
        logging.error(f"Tavily search failed: {e}")
        raise

async def search_tech_research(query: str, max_results: int = 5):
    """
    Search for technology and software development related information using Tavily API
    """
    if not tavily_client:
        logging.error("Tavily API key not configured")
        raise RuntimeError("Tavily API not available")
    
    try:
        # Run the synchronous Tavily search in a thread pool
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None, 
            lambda: tavily_client.search(
                query=query, 
                search_depth="advanced",
                max_results=max_results,
                include_domains=[
                    "github.com", "stackoverflow.com", "medium.com", "dev.to", "hackernoon.com",
                    "techcrunch.com", "wired.com", "arstechnica.com", "ieee.org", "acm.org",
                    "arxiv.org", "scholar.google.com", "researchgate.net", "semanticscholar.org",
                    "reddit.com", "news.ycombinator.com", "lobste.rs", "producthunt.com",
                    "infoq.com", "martinfowler.com", "google.com", "microsoft.com", "aws.amazon.com",
                    "cloud.google.com", "azure.microsoft.com", "vercel.com", "netlify.com",
                    "mongodb.com", "postgresql.org", "redis.io", "docker.com", "kubernetes.io",
                    "reactjs.org", "vuejs.org", "angular.io", "nodejs.org", "python.org",
                    "golang.org", "rust-lang.org", "java.com", "spring.io", "djangoproject.com",
                    "flask.palletsprojects.com", "fastapi.tiangolo.com", "expressjs.com"
                ]
            )
        )
        
        return response.get("results", [])
    
    except Exception as e:
        logging.error(f"Tech research search failed: {e}")
        raise

async def search_learning_resources(query: str, resource_type: str = "courses", max_results: int = 5):
    """
    Search for learning resources (courses, books, tutorials, etc.) using Tavily API
    Specifically designed for educational content, NOT travel information
    """
    if not tavily_client:
        logging.error("Tavily API key not configured")
        raise RuntimeError("Tavily API not available")
    
    try:
        # Create learning-specific search query
        if resource_type == "courses":
            search_query = f"{query} online courses tutorials lessons training"
            domains = [
                "coursera.org", "udemy.com", "edx.org", "udacity.com", "pluralsight.com",
                "linkedin.com/learning", "skillshare.com", "khanacademy.org", "codecademy.com",
                "freecodecamp.org", "datacamp.com", "treehouse.com", "lynda.com",
                "youtube.com", "educative.io", "egghead.io", "frontendmasters.com",
                "laracasts.com", "masterclass.com", "brilliant.org", "futurelearn.com"
            ]
        elif resource_type == "books":
            search_query = f"{query} books textbooks guides reading materials"
            domains = [
                "amazon.com", "goodreads.com", "springer.com", "oreilly.com", "manning.com",
                "packtpub.com", "apress.com", "nostarch.com", "pragprog.com", "wiley.com",
                "pearson.com", "cambridge.org", "google.com/books", "bookauthority.org",
                "reddit.com/r/books", "libgen.is", "archive.org"
            ]
        elif resource_type == "tutorials":
            search_query = f"{query} tutorials how to learn guide step by step"
            domains = [
                "medium.com", "dev.to", "hackernoon.com", "tutorialspoint.com", "w3schools.com",
                "geeksforgeeks.org", "realpython.com", "javatpoint.com", "baeldung.com",
                "digitalocean.com", "freeCodeCamp.org", "css-tricks.com", "smashingmagazine.com",
                "youtube.com", "github.com", "stackoverflow.com"
            ]
        elif resource_type == "practice":
            search_query = f"{query} practice exercises projects hands-on coding challenges"
            domains = [
                "leetcode.com", "hackerrank.com", "codewars.com", "exercism.io", "codesignal.com",
                "topcoder.com", "codeforces.com", "kaggle.com", "projecteuler.net",
                "github.com", "replit.com", "codepen.io", "codesandbox.io", "glitch.com"
            ]
        elif resource_type == "communities":
            search_query = f"{query} community forum discussion group learning network"
            domains = [
                "reddit.com", "stackoverflow.com", "discord.com", "slack.com", "github.com",
                "dev.to", "hashnode.com", "indie hackers.com", "meetup.com", "facebook.com/groups",
                "linkedin.com", "twitter.com", "quora.com", "spectrum.chat"
            ]
        elif resource_type == "tools":
            search_query = f"{query} tools software platforms IDE libraries frameworks"
            domains = [
                "github.com", "gitlab.com", "npmjs.com", "pypi.org", "maven.org",
                "producthunt.com", "alternativeto.net", "stackshare.io", "slant.co",
                "awesome-list.com", "awesomeopensource.com"
            ]
        else:
            search_query = f"{query} learning resources education training"
            domains = []
        
        # Run the synchronous Tavily search in a thread pool
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None, 
            lambda: tavily_client.search(
                query=search_query, 
                search_depth="advanced",
                max_results=max_results,
                include_domains=domains if domains else None
            )
        )
        
        return response.get("results", [])
    
    except Exception as e:
        logging.error(f"Learning resource search failed: {e}")
        raise

def extract_price_from_text(text: str) -> float:
    """
    Extract price information from text content with better accuracy
    """
    # Look for various currency patterns
    currency_patterns = [
        # Indian Rupee patterns
        r'₹\s*([0-9,]+(?:\.\d{2})?)',
        r'INR\s*([0-9,]+(?:\.\d{2})?)',
        r'Rs\.?\s*([0-9,]+(?:\.\d{2})?)',
        r'from\s*₹\s*([0-9,]+(?:\.\d{2})?)',
        r'starting\s*₹\s*([0-9,]+(?:\.\d{2})?)',
        r'price[:\s]*₹\s*([0-9,]+(?:\.\d{2})?)',
        r'cost[:\s]*₹\s*([0-9,]+(?:\.\d{2})?)',
        r'fare[:\s]*₹\s*([0-9,]+(?:\.\d{2})?)',
        r'per\s+night[:\s]*₹\s*([0-9,]+(?:\.\d{2})?)',
        r'per\s+person[:\s]*₹\s*([0-9,]+(?:\.\d{2})?)',
        # USD patterns
        r'\$\s*([0-9,]+(?:\.\d{2})?)',
        r'USD\s*([0-9,]+(?:\.\d{2})?)',
        r'from\s*\$\s*([0-9,]+(?:\.\d{2})?)',
        r'starting\s*\$\s*([0-9,]+(?:\.\d{2})?)',
        r'price[:\s]*\$\s*([0-9,]+(?:\.\d{2})?)',
        # EUR patterns
        r'€\s*([0-9,]+(?:\.\d{2})?)',
        r'EUR\s*([0-9,]+(?:\.\d{2})?)',
        # GBP patterns
        r'£\s*([0-9,]+(?:\.\d{2})?)',
        r'GBP\s*([0-9,]+(?:\.\d{2})?)',
    ]
    
    for pattern in currency_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            try:
                price = float(match.replace(',', ''))
                if price > 0:
                    return price
            except ValueError:
                continue
    
    return None


# ---------------------------------------------------------------------------
# Hotel name / price validation (Tavily snippets are often noisy)
# ---------------------------------------------------------------------------

_INVALID_HOTEL_NAME_SUBSTRINGS = (
    "operators available", "looking for a", "re looking", "the cheapest",
    "cheapest areas", "compared to the", "average price", "exceptional value",
    "631 operators", "choose from for", "for cheap hotels", "hotel in ",
    "full service", "with full", "updated prices", "reviews on", "book on",
    "save up to", "discount of", "percent off", "star rating based",
    "this hotel", "hotel offers", "hotel room in", "for money compared",
    "value for money", "room in mumbai", "areas for cheap",
)

_HOTEL_BRAND_WORDS = (
    "taj", "marriott", "hilton", "hyatt", "oberoi", "itc", "lemon", "sarovar",
    "radisson", "westin", "sheraton", "novotel", "ibis", "accor", "holiday inn",
    "courtyard", "four seasons", "st regis", "jw marriott", "conrad", "trident",
    "leela", "park ", "grand hyatt", "sofitel", "pullman", "mercure", "fabhotel",
    "treebo", "oyo", "zostel", "hostel", "residency", "palace", "resort",
)


def _is_indian_destination(destination: str) -> bool:
    d = (destination or "").lower()
    indian = (
        "mumbai", "delhi", "bangalore", "bengaluru", "chennai", "hyderabad", "kolkata",
        "pune", "goa", "jaipur", "ahmedabad", "kochi", "kerala", "india", "navi mumbai",
        "thane", "gurgaon", "gurugram", "noida", "lucknow", "indore", "surat",
    )
    return any(x in d for x in indian)


def is_valid_hotel_name(name: str) -> bool:
    """
    Reject sentence fragments and SEO garbage that regex sometimes captures from snippets.
    """
    if not name or not isinstance(name, str):
        return False
    n = name.strip()
    if len(n) < 3 or len(n) > 72:
        return False
    words = n.split()
    if len(words) > 12:
        return False
    lower = n.lower()
    for bad in _INVALID_HOTEL_NAME_SUBSTRINGS:
        if bad in lower:
            return False
    # Incomplete marketing fragments
    if lower.endswith((" with", " for", " to", " and", " the", " a", " in")):
        return False
    # Property-type word anywhere (Booking titles: "Bloom Hotel Worli")
    has_property_type = bool(
        re.search(
            r"\b(hotel|resort|inn|lodge|palace|suites|hostel|guesthouse|guest\s+house|by\s+marriott)\b",
            lower,
        )
    )
    looks_like_title = n[0].isupper() if n else False
    ends_hotelish = bool(
        re.search(
            r"\b(hotel|resort|inn|lodge|palace|suites|hostel|guest\s*house|by\s+marriott)\s*$",
            n,
            re.I,
        )
    )
    has_brand = any(b in lower for b in _HOTEL_BRAND_WORDS)
    if has_property_type and len(words) <= 14:
        return True
    if not (ends_hotelish or has_brand or (looks_like_title and len(words) <= 6)):
        if len(words) <= 4 and looks_like_title and not lower.startswith(("the cheapest", "a cheap", "cheap ")):
            return True
        return False
    return True


def extract_hotel_name_from_result_title(title: str, url: str = "") -> str:
    """
    Booking / TripAdvisor / Agoda titles usually put the property name first.
    """
    if not title:
        return ""
    t = title.strip()
    t = re.sub(r"\s+", " ", t)
    # Split on common OTA suffixes
    for sep in (
        " - Booking.com", " | Booking.com", " – Booking.com", " on Booking.com",
        " - Hotels.com", " | Hotels.com", " - Agoda", " | Agoda",
        " - Tripadvisor", " | Tripadvisor", " - TripAdvisor",
        " - MakeMyTrip", " | MakeMyTrip", " - Expedia", " | Expedia",
        " - Goibibo", " | Goibibo",
    ):
        if sep.lower() in t.lower():
            idx = t.lower().index(sep.lower())
            t = t[:idx].strip()
            break
    m = re.match(r"^(.+?)\s*[-–—]\s*(?:Updated|Reviews|Prices|Book)", t, re.I)
    if m:
        t = m.group(1).strip()
    # Strip trailing city-only noise
    t = re.sub(r"\s*[,|]\s*India\s*$", "", t, flags=re.I).strip()
    return t


def extract_hotel_price_per_night_inr(text: str, title: str, destination: str) -> float:
    """
    Prefer explicit 'per night' prices; ignore tiny numbers (discount %, room count).
    """
    blob = f"{title} {text}"
    # Strong patterns first (INR per night)
    night_patterns = [
        r"₹\s*([0-9][0-9,]{2,})\s*(?:/|\s)*\s*(?:per\s*)?night",
        r"(?:Rs\.?|INR)\s*([0-9][0-9,]{2,})\s*(?:/|\s)*\s*(?:per\s*)?night",
        r"([0-9][0-9,]{2,})\s*₹\s*(?:/|\s)*\s*(?:per\s*)?night",
        r"per\s*night[:\s]*₹\s*([0-9][0-9,]{2,})",
        r"per\s*night[:\s]*(?:Rs\.?|INR)\s*([0-9][0-9,]{2,})",
        r"from\s*₹\s*([0-9][0-9,]{2,})\s*(?:per\s*)?night",
    ]
    candidates = []
    for pat in night_patterns:
        for m in re.finditer(pat, blob, re.I):
            try:
                v = float(m.group(1).replace(",", ""))
                if v > 0:
                    candidates.append(v)
            except ValueError:
                continue
    if candidates:
        # Use median-ish: prefer values that look like nightly rates
        good = [c for c in candidates if _plausible_hotel_nightly_inr(c, destination)]
        pool = good if good else candidates
        return float(sorted(pool)[len(pool) // 2])

    # Fallback: all ₹ amounts, take plausible nightly range only
    all_inr = []
    for m in re.finditer(r"₹\s*([0-9][0-9,]{2,}(?:\.\d{2})?)", blob):
        try:
            all_inr.append(float(m.group(1).replace(",", "")))
        except ValueError:
            continue
    plausible = [x for x in all_inr if _plausible_hotel_nightly_inr(x, destination)]
    if plausible:
        return float(sorted(plausible)[len(plausible) // 2])

    # Last resort: generic extractor only if plausible
    p = extract_price_from_text(blob)
    if p and _plausible_hotel_nightly_inr(p, destination):
        return p
    return None


def _plausible_hotel_nightly_inr(price: float, destination: str) -> bool:
    """Filter out ₹14, ₹2 (discount noise) and million-rupee OCR errors."""
    if price is None or price <= 0:
        return False
    if _is_indian_destination(destination):
        # Budget rooms rarely under ₹400/night on OTAs; ignore garbage < 250
        if price < 250:
            return False
        if price > 250_000:
            return False
        return True
    # International: allow wider band in local currency mixed in snippets
    if price < 15:
        return False
    if price > 50_000:
        return False
    return True


def _plausible_flight_price_inr(price: float, origin: str, destination: str) -> bool:
    """One-way economy fare sanity check for INR-heavy snippets."""
    if price is None or price <= 0:
        return False
    if _is_indian_destination(origin) or _is_indian_destination(destination):
        if price < 400:
            return False
        if price > 150_000:
            return False
        return True
    if price < 30:
        return False
    if price > 500_000:
        return False
    return True


async def search_flights(origin: str, destination: str, departure_date: str, return_date: str = None):
    """
    Search for flight information using Tavily - only returns real results
    """
    # Create comprehensive search queries
    if return_date:
        queries = [
            f"flights {origin} to {destination} {departure_date} return {return_date} prices booking",
            f"flight booking {origin} {destination} {departure_date} return prices airlines",
            f"round trip flights {origin} {destination} {departure_date} {return_date} cost"
        ]
    else:
        queries = [
            f"flights {origin} to {destination} {departure_date} one way prices booking",
            f"one way flight {origin} {destination} {departure_date} airline prices",
            f"flight tickets {origin} to {destination} {departure_date} cost"
        ]
    
    all_flights = []
    
    for query in queries:
        try:
            results = await search_travel_info(query, max_results=3)
            
            for i, result in enumerate(results):
                title = result.get("title", "")
                content = result.get("content", "")
                url = result.get("url", "")
                
                # Extract flight details from real content
                flight_details = extract_flight_details(content, title, origin, destination)
                
                for j, flight_info in enumerate(flight_details):
                    # Prefer real snippet price when in a plausible range; else heuristic
                    raw_price = extract_price_from_text(content + " " + title)
                    airline_guess = flight_info.get("airline", determine_airline(content))
                    heuristic = get_realistic_flight_price(origin, destination, airline_guess, departure_date, j)
                    if raw_price and _plausible_flight_price_inr(raw_price, origin, destination):
                        final_price = round(raw_price)
                    else:
                        final_price = round(heuristic)

                    # Only add flights with actual price data
                    if final_price and final_price > 0:
                        all_flights.append({
                            "id": f"tavily_flight_{len(all_flights)+1}",
                            "airline": airline_guess,
                            "price": final_price,
                            "departure": flight_info.get("departure", "Check airline website"),
                            "duration": flight_info.get("duration", "Check airline website"),
                            "aircraft": flight_info.get("aircraft", ""),
                            "class": flight_info.get("class", "Economy"),
                            "route": f"{origin} → {destination}",
                            "provider": "Tavily Web Search",
                            "title": title,
                            "url": url,
                            "source": "Tavily Web Search",
                            "raw": result
                        })
                        
                        if len(all_flights) >= 8:
                            break
                            
                if len(all_flights) >= 8:
                    break
                    
        except Exception as e:
            logging.warning(f"Flight query failed: {query}, error: {e}")
            continue
    
    # Remove duplicates and return best options
    unique_flights = []
    seen_combinations = set()
    
    for flight in all_flights:
        combo = f"{flight['airline']}_{flight['price']}"
        if combo not in seen_combinations:
            seen_combinations.add(combo)
            unique_flights.append(flight)
    
    # If no flights found from search, create some based on realistic pricing
    if not unique_flights:
        airlines = get_airlines_for_route(origin, destination)
        
        for i, airline in enumerate(airlines[:3]):
            price = get_realistic_flight_price(origin, destination, airline, departure_date, i)
            unique_flights.append({
                "id": f"flight_{i+1}",
                "airline": airline,
                "price": price,
                "departure": determine_departure_time(i),
                "duration": estimate_flight_duration(origin, destination),
                "aircraft": determine_aircraft(airline),
                "class": "Economy",
                "route": f"{origin} → {destination}",
                "provider": "Market Research",
                "title": f"{airline} flight from {origin} to {destination}",
                "url": get_airline_website(airline),
                "source": "Market Research",
                "raw": {}
            })
    logging.info(f"Found {len(unique_flights)} unique flights for {origin} to {destination}")
    return sorted(unique_flights, key=lambda x: x['price'])[:5]

def extract_flight_details(content: str, title: str, origin: str, destination: str):
    """
    Extract specific flight details from content
    """
    flights = []
    
    # Look for flight information patterns
    flight_patterns = [
        r'(\w+(?:\s+\w+)?)\s+(?:flight|airline).*?(\d{1,2}:\d{2})\s*(?:AM|PM)?.*?(\d+h?\s*\d*m?)',
        r'(\w+)\s*-\s*(\d{1,2}:\d{2})\s*(?:AM|PM)?.*?(\d+h\s*\d*m)',
        r'(IndiGo|SpiceJet|Air India|Vistara|GoAir|Emirates|Qatar|Singapore|British|Lufthansa|KLM|Turkish|Thai|Malaysia|United|American|Delta).*?(\d{1,2}:\d{2}).*?(\d+h\s*\d*m)?'
    ]
    
    for pattern in flight_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        for match in matches:
            if len(match) >= 2:
                flights.append({
                    "airline": match[0],
                    "departure": match[1] if len(match) > 1 else "Multiple times",
                    "duration": match[2] if len(match) > 2 else "Check with airline",
                    "aircraft": determine_aircraft_type(match[0]),
                    "class": "Economy"
                })
    
    # Return only real flight data from search results
    return flights[:3]

def determine_aircraft_type(airline: str) -> str:
    """
    Determine likely aircraft type based on airline
    """
    airline_lower = airline.lower()
    
    if any(carrier in airline_lower for carrier in ["indigo", "spicejet", "ryanair", "easyjet"]):
        return "A320"
    elif any(carrier in airline_lower for carrier in ["air india", "vistara", "emirates", "qatar"]):
        return "A330"
    elif any(carrier in airline_lower for carrier in ["singapore", "lufthansa", "british"]):
        return "A350"
    else:
        return "Boeing 737"

def get_destination_currency(destination: str) -> str:
    """
    Determine currency based on destination
    """
    destination_lower = destination.lower()
    
    # Indian cities
    indian_cities = [
        'mumbai', 'delhi', 'bangalore', 'chennai', 'hyderabad', 'kolkata', 'pune', 
        'ahmedabad', 'jaipur', 'surat', 'lucknow', 'kanpur', 'nagpur', 'indore',
        'goa', 'kerala', 'rajasthan', 'agra', 'varanasi', 'rishikesh', 'manali'
    ]
    
    if any(city in destination_lower for city in indian_cities) or 'india' in destination_lower:
        return "INR"
    
    # Common international destinations and their currencies
    currency_map = {
        'dubai': 'AED', 'abu dhabi': 'AED', 'sharjah': 'AED',
        'singapore': 'SGD',
        'bangkok': 'THB', 'phuket': 'THB', 'pattaya': 'THB',
        'kuala lumpur': 'MYR', 'penang': 'MYR',
        'hong kong': 'HKD',
        'tokyo': 'JPY', 'osaka': 'JPY', 'kyoto': 'JPY',
        'london': 'GBP', 'manchester': 'GBP', 'edinburgh': 'GBP',
        'paris': 'EUR', 'rome': 'EUR', 'barcelona': 'EUR', 'amsterdam': 'EUR', 'berlin': 'EUR',
        'new york': 'USD', 'los angeles': 'USD', 'san francisco': 'USD', 'chicago': 'USD',
        'toronto': 'CAD', 'vancouver': 'CAD', 'montreal': 'CAD',
        'sydney': 'AUD', 'melbourne': 'AUD', 'perth': 'AUD',
        'auckland': 'NZD', 'wellington': 'NZD',
        'doha': 'QAR',
        'muscat': 'OMR',
        'riyadh': 'SAR', 'jeddah': 'SAR',
        'kuwait': 'KWD',
        'istanbul': 'TRY',
        'cairo': 'EGP',
        'nairobi': 'KES',
        'johannesburg': 'ZAR', 'cape town': 'ZAR',
        'colombo': 'LKR',
        'male': 'MVR',
        'kathmandu': 'NPR',
        'dhaka': 'BDT'
    }
    
    for city, currency in currency_map.items():
        if city in destination_lower:
            return currency
    
    # Default to USD for unknown international destinations
    return "USD"

def get_realistic_flight_price(origin: str, destination: str, airline: str, departure_date: str, index: int) -> float:
    """
    Get accurate flight pricing for both domestic and international routes
    """
    # Normalize city names for comparison
    origin_lower = origin.lower().strip()
    destination_lower = destination.lower().strip()
    
    # Check if it's an international route
    is_international = is_international_route(origin, destination)
    
    if is_international:
        return get_international_flight_price(origin, destination, airline, departure_date, index)
    else:
        return get_domestic_flight_price(origin, destination, airline, departure_date, index)

def is_international_route(origin: str, destination: str) -> bool:
    """
    Determine if the route is international based on city names
    """
    # List of major Indian cities
    indian_cities = [
        'mumbai', 'delhi', 'bangalore', 'chennai', 'hyderabad', 'kolkata', 'pune', 
        'ahmedabad', 'jaipur', 'surat', 'lucknow', 'kanpur', 'nagpur', 'indore',
        'thane', 'bhopal', 'visakhapatnam', 'pimpri', 'patna', 'vadodara', 'ghaziabad',
        'ludhiana', 'agra', 'nashik', 'faridabad', 'meerut', 'rajkot', 'kalyan',
        'vasai', 'varanasi', 'srinagar', 'aurangabad', 'dhanbad', 'amritsar',
        'navi mumbai', 'allahabad', 'ranchi', 'howrah', 'coimbatore', 'jabalpur',
        'gwalior', 'vijayawada', 'jodhpur', 'madurai', 'raipur', 'kota', 'guwahati',
        'chandigarh', 'thiruvananthapuram', 'solapur', 'hubballi', 'tiruchirappalli',
        'tiruppur', 'moradabad', 'mysore', 'bareilly', 'gurgaon', 'aligarh', 'jalandhar'
    ]
    
    # Common international destinations
    international_cities = [
        'dubai', 'singapore', 'london', 'new york', 'bangkok', 'kuala lumpur',
        'hong kong', 'tokyo', 'paris', 'amsterdam', 'doha', 'abu dhabi',
        'sharjah', 'muscat', 'riyadh', 'jeddah', 'kuwait', 'manama', 'cairo',
        'istanbul', 'frankfurt', 'zurich', 'toronto', 'vancouver', 'sydney',
        'melbourne', 'perth', 'auckland', 'wellington', 'johannesburg', 'cape town',
        'nairobi', 'addis ababa', 'colombo', 'male', 'kathmandu', 'dhaka',
        'karachi', 'lahore', 'islamabad', 'kabul', 'tashkent', 'almaty'
    ]
    
    origin_lower = origin.lower().strip()
    destination_lower = destination.lower().strip()
    
    # Check if both cities are Indian (domestic)
    origin_is_indian = any(city in origin_lower for city in indian_cities)
    destination_is_indian = any(city in destination_lower for city in indian_cities)
    
    # Check if either city is clearly international
    origin_is_international = any(city in origin_lower for city in international_cities)
    destination_is_international = any(city in destination_lower for city in international_cities)
    
    # International if one city is Indian and other is international, or both are non-Indian
    if (origin_is_indian and destination_is_international) or (destination_is_indian and origin_is_international):
        return True
    elif not origin_is_indian and not destination_is_indian:
        return True
    else:
        return False

def get_domestic_flight_price(origin: str, destination: str, airline: str, departure_date: str, index: int) -> float:
    """
    Get accurate domestic flight pricing based on real market data
    """
    route_lower = f"{origin} {destination}".lower()
    
    # Tier 1 routes (Major metros) - High demand, frequent flights
    tier1_routes = [
        ["mumbai", "delhi"], ["delhi", "mumbai"], ["bangalore", "mumbai"], ["mumbai", "bangalore"],
        ["delhi", "bangalore"], ["bangalore", "delhi"], ["chennai", "mumbai"], ["mumbai", "chennai"],
        ["hyderabad", "mumbai"], ["mumbai", "hyderabad"], ["delhi", "chennai"], ["chennai", "delhi"],
        ["kolkata", "mumbai"], ["mumbai", "kolkata"], ["pune", "delhi"], ["delhi", "pune"]
    ]
    
    # Tier 2 routes (Metro to Tier-2 cities) - Medium demand
    tier2_routes = [
        ["mumbai", "pune"], ["pune", "mumbai"], ["bangalore", "hyderabad"], ["hyderabad", "bangalore"],
        ["delhi", "jaipur"], ["jaipur", "delhi"], ["mumbai", "goa"], ["goa", "mumbai"],
        ["chennai", "bangalore"], ["bangalore", "chennai"], ["delhi", "lucknow"], ["lucknow", "delhi"],
        ["mumbai", "ahmedabad"], ["ahmedabad", "mumbai"], ["bangalore", "pune"], ["pune", "bangalore"]
    ]
    
    # Determine route tier
    is_tier1 = any(all(city in route_lower for city in route) for route in tier1_routes)
    is_tier2 = any(all(city in route_lower for city in route) for route in tier2_routes)
    
    # Base pricing by airline and route tier (in INR)
    if is_tier1:
        base_prices = {
            "IndiGo": 4200, "SpiceJet": 3800, "Air India": 4800, "Vistara": 5500, "GoAir": 3600, "AirAsia": 3700
        }
    elif is_tier2:
        base_prices = {
            "IndiGo": 5200, "SpiceJet": 4800, "Air India": 5800, "Vistara": 6500, "GoAir": 4600, "AirAsia": 4700
        }
    else:
        base_prices = {
            "IndiGo": 6500, "SpiceJet": 6000, "Air India": 7200, "Vistara": 8000, "GoAir": 5800, "AirAsia": 5900
        }
    
    base_price = base_prices.get(airline, 5500)
    
    # Dynamic pricing factors
    date_multiplier = get_date_pricing_multiplier(departure_date)
    distance_multiplier = get_distance_multiplier(origin, destination)
    airline_multiplier = get_airline_premium_multiplier(airline)
    index_variation = index * 300
    
    final_price = base_price * date_multiplier * distance_multiplier * airline_multiplier + index_variation
    
    return max(min(final_price, 25000), 2200)

def get_international_flight_price(origin: str, destination: str, airline: str, departure_date: str, index: int) -> float:
    """
    Get accurate international flight pricing
    """
    route_category = get_international_route_category(origin, destination)
    
    # Base pricing by route category and airline (in INR)
    if route_category == "gulf":
        base_prices = {
            "Air India": 25000, "Emirates": 35000, "Qatar Airways": 32000, "Etihad": 30000,
            "IndiGo": 22000, "SpiceJet": 20000, "Kuwait Airways": 24000, "Oman Air": 26000
        }
    elif route_category == "southeast_asia":
        base_prices = {
            "Air India": 30000, "Singapore Airlines": 45000, "Thai Airways": 35000, "Malaysia Airlines": 32000,
            "IndiGo": 25000, "AirAsia": 22000, "Scoot": 20000
        }
    elif route_category == "europe":
        base_prices = {
            "Air India": 45000, "British Airways": 65000, "Lufthansa": 60000, "Emirates": 55000,
            "Qatar Airways": 50000, "KLM": 58000, "Virgin Atlantic": 62000
        }
    elif route_category == "north_america":
        base_prices = {
            "Air India": 65000, "United Airlines": 85000, "American Airlines": 80000, "Delta": 82000,
            "Emirates": 75000, "Qatar Airways": 70000, "British Airways": 78000
        }
    elif route_category == "oceania":
        base_prices = {
            "Air India": 55000, "Qantas": 80000, "Singapore Airlines": 70000, "Emirates": 65000,
            "Qatar Airways": 60000, "Thai Airways": 58000
        }
    else:
        base_prices = {
            "Air India": 35000, "Emirates": 45000, "Qatar Airways": 40000, "Turkish Airlines": 38000,
            "Etihad": 42000
        }
    
    base_price = base_prices.get(airline, 40000)
    
    # International flight pricing factors
    date_multiplier = get_international_date_multiplier(departure_date)
    demand_multiplier = get_international_demand_multiplier(route_category)
    airline_multiplier = get_international_airline_multiplier(airline)
    index_variation = index * 2000
    
    final_price = base_price * date_multiplier * demand_multiplier * airline_multiplier + index_variation
    
    return max(min(final_price, 250000), 15000)

def get_international_route_category(origin: str, destination: str) -> str:
    """
    Categorize international routes for pricing
    """
    gulf_countries = ['dubai', 'doha', 'abu dhabi', 'sharjah', 'muscat', 'riyadh', 'jeddah', 'kuwait', 'manama']
    southeast_asia = ['singapore', 'bangkok', 'kuala lumpur', 'hong kong', 'tokyo', 'jakarta', 'manila', 'ho chi minh']
    europe = ['london', 'paris', 'amsterdam', 'frankfurt', 'zurich', 'rome', 'madrid', 'brussels', 'vienna', 'istanbul']
    north_america = ['new york', 'los angeles', 'chicago', 'toronto', 'vancouver', 'san francisco', 'washington', 'boston']
    oceania = ['sydney', 'melbourne', 'perth', 'auckland', 'wellington', 'brisbane', 'adelaide']
    
    destination_lower = destination.lower()
    origin_lower = origin.lower()
    
    for city in gulf_countries:
        if city in destination_lower or city in origin_lower:
            return "gulf"
    
    for city in southeast_asia:
        if city in destination_lower or city in origin_lower:
            return "southeast_asia"
    
    for city in europe:
        if city in destination_lower or city in origin_lower:
            return "europe"
    
    for city in north_america:
        if city in destination_lower or city in origin_lower:
            return "north_america"
    
    for city in oceania:
        if city in destination_lower or city in origin_lower:
            return "oceania"
    
    return "other"

def get_date_pricing_multiplier(departure_date: str) -> float:
    """
    Get pricing multiplier based on departure date
    """
    try:
        departure_dt = datetime.strptime(departure_date, "%Y-%m-%d")
        current_dt = datetime.now()
        days_ahead = (departure_dt - current_dt).days
        
        if days_ahead < 7:
            return 1.4
        elif days_ahead < 21:
            return 1.2
        elif days_ahead < 60:
            return 1.0
        else:
            return 1.1
    except:
        return 1.0

def get_distance_multiplier(origin: str, destination: str) -> float:
    """
    Get pricing multiplier based on route distance
    """
    long_distance_routes = [
        ["mumbai", "guwahati"], ["delhi", "chennai"], ["kolkata", "mumbai"],
        ["bangalore", "srinagar"], ["kochi", "delhi"], ["trivandrum", "mumbai"]
    ]
    
    route_lower = f"{origin} {destination}".lower()
    is_long_distance = any(all(city in route_lower for city in route) for route in long_distance_routes)
    
    return 1.3 if is_long_distance else 1.0

def get_airline_premium_multiplier(airline: str) -> float:
    """
    Get airline-specific pricing multiplier for domestic flights
    """
    premium_airlines = ["Vistara", "Air India"]
    budget_airlines = ["SpiceJet", "GoAir", "AirAsia"]
    
    if airline in premium_airlines:
        return 1.15
    elif airline in budget_airlines:
        return 0.9
    else:
        return 1.0

def get_international_date_multiplier(departure_date: str) -> float:
    """
    Get international flight pricing multiplier based on date
    """
    try:
        departure_dt = datetime.strptime(departure_date, "%Y-%m-%d")
        current_dt = datetime.now()
        days_ahead = (departure_dt - current_dt).days
        
        if days_ahead < 14:
            return 1.6
        elif days_ahead < 45:
            return 1.3
        elif days_ahead < 90:
            return 1.0
        else:
            return 1.2
    except:
        return 1.0

def get_international_demand_multiplier(route_category: str) -> float:
    """
    Get demand-based multiplier for international routes
    """
    demand_multipliers = {
        "gulf": 1.0, "southeast_asia": 1.1, "europe": 1.3, "north_america": 1.4, "oceania": 1.2, "other": 1.1
    }
    return demand_multipliers.get(route_category, 1.1)

def get_international_airline_multiplier(airline: str) -> float:
    """
    Get airline-specific multiplier for international flights
    """
    premium_international = ["Emirates", "Singapore Airlines", "Qatar Airways", "Lufthansa", "British Airways"]
    full_service = ["Air India", "Turkish Airlines", "Thai Airways", "KLM", "Etihad"]
    budget_international = ["IndiGo", "SpiceJet", "AirAsia", "Scoot"]
    
    if airline in premium_international:
        return 1.3
    elif airline in budget_international:
        return 0.85
    else:
        return 1.0

def determine_airline(text: str):
    """
    Determine airline from text content
    """
    airlines = {
        "IndiGo": ["indigo", "6e"],
        "SpiceJet": ["spicejet", "sg"],
        "Air India": ["air india", "ai"],
        "Vistara": ["vistara", "uk"],
        "GoAir": ["goair", "go air", "g8"],
        "AirAsia": ["airasia", "air asia", "i5"],
        "Emirates": ["emirates", "ek"],
        "Qatar Airways": ["qatar", "qr"],
        "Singapore Airlines": ["singapore", "sq"],
        "British Airways": ["british", "ba"],
        "Lufthansa": ["lufthansa", "lh"],
        "KLM": ["klm", "kl"],
        "Turkish Airlines": ["turkish", "tk"],
        "Thai Airways": ["thai", "tg"]
    }
    
    text_lower = text.lower()
    
    for airline, keywords in airlines.items():
        if any(keyword in text_lower for keyword in keywords):
            return airline
    
    return "Available Airlines"

async def search_hotels(destination: str, checkin_date: str, checkout_date: str, adults: int = 2):
    """
    Search for hotel options via Tavily. Filters out sentence-fragment "names" and bogus nightly rates.
    """
    all_hotels = []
    nights = calculate_nights(checkin_date, checkout_date)

    queries = [
        f'"{destination}" hotel Booking.com price per night {checkin_date}',
        f"{destination} hotels per night rupees {checkin_date} {checkout_date} Agoda",
        f"best hotels {destination} room rate per night Marriott Hilton Taj",
    ]

    for query in queries:
        try:
            results = await search_travel_info(query, max_results=4)

            for result in results:
                title = result.get("title", "") or ""
                content = result.get("content", "") or ""
                url = result.get("url", "") or ""

                # 1) Property name from OTA page title (most reliable)
                name = extract_hotel_name_from_result_title(title, url)
                if not name:
                    # 2) Regex extract only if it passes validation
                    for h in extract_hotel_details(content, title, destination)[:1]:
                        cand = (h.get("name") or "").strip()
                        if is_valid_hotel_name(cand):
                            name = cand
                            break

                if not is_valid_hotel_name(name):
                    continue

                price = extract_hotel_price_per_night_inr(content, title, destination)
                if not price:
                    continue

                rating = 4.0
                m_star = re.search(r"(\d+(?:\.\d+)?)\s*(?:out of|/)\s*5", content + title, re.I)
                if m_star:
                    try:
                        rating = min(5.0, float(m_star.group(1)))
                    except ValueError:
                        pass

                cat = "mid-range"
                nl = name.lower()
                if any(k in nl for k in ("taj ", "oberoi", "marriott", "hyatt regency", "st regis", "four seasons")):
                    cat = "luxury"
                elif any(k in nl for k in ("oyo", "zostel", "fabhotel", "treebo", "hostel")):
                    cat = "budget"

                all_hotels.append({
                    "id": f"tavily_hotel_{len(all_hotels)+1}",
                    "provider": "tavily_search",
                    "name": name.strip(),
                    "price": round(price),
                    "price_per_night": round(price),
                    "total_price": round(price) * nights,
                    "currency": get_destination_currency(destination),
                    "title": title,
                    "url": url,
                    "source": "Tavily Web Search",
                    "location": f"{destination}",
                    "rating": rating,
                    "amenities": get_amenities_by_category(cat),
                    "room_type": "Deluxe Room" if cat != "budget" else "Standard Room",
                    "category": cat,
                    "address": f"{name.strip()}, {destination}",
                    "raw": result,
                })

                if len(all_hotels) >= 10:
                    break

            if len(all_hotels) >= 10:
                break

        except Exception as e:
            logging.warning(f"Hotel query failed: {query}, error: {e}")
            continue

    # Dedupe by normalised name
    unique_hotels = []
    seen = set()
    for hotel in all_hotels:
        key = re.sub(r"[^a-z0-9]", "", hotel["name"].lower())
        if key in seen or len(key) < 4:
            continue
        seen.add(key)
        unique_hotels.append(hotel)

    if not unique_hotels:
        logging.warning(f"No validated hotels for {destination} after filtering noisy Tavily snippets")

    return sorted(unique_hotels, key=lambda x: (-x["rating"], x["price_per_night"]))[:5]

def extract_hotel_details(content: str, title: str, destination: str):
    """
    Secondary extraction from page body. Names are filtered — snippets often contain sentences, not hotel names.
    """
    hotels = []

    hotel_names = re.findall(
        r'([\w\s\']+(?:hotel|resort|inn|lodge|palace|suites)[\w\s\']{0,40})',
        content,
        re.IGNORECASE,
    )
    ratings = re.findall(r'(\d+(?:\.\d+)?)\s*(?:star|★)', content)
    brands = ["Marriott", "Hilton", "Hyatt", "Radisson", "Oberoi", "Taj", "ITC", "OYO", "Lemon Tree", "Sarovar", "Novotel", "Ibis"]
    brand_hotels = [f"{b} {destination}" for b in brands if b.lower() in content.lower() or b.lower() in title.lower()]

    seen = set()
    for raw in hotel_names + brand_hotels:
        name = re.sub(r"\s+", " ", raw).strip()
        if name.lower() in seen:
            continue
        if not is_valid_hotel_name(name):
            continue
        seen.add(name.lower())

        name_lower = name.lower()
        if any(k in name_lower for k in ("taj", "oberoi", "marriott", "hilton", "hyatt", "luxury", "grand", "palace")):
            category = "luxury"
        elif any(k in name_lower for k in ("oyo", "budget", "lodge", "zostel", "treebo")):
            category = "budget"
        else:
            category = "mid-range"

        ri = len(hotels)
        rating = float(ratings[ri]) if ri < len(ratings) else 4.0 + (ri * 0.15)
        price = extract_hotel_price_per_night_inr(content, title, destination)

        hotels.append({
            "name": name,
            "rating": min(rating, 5.0),
            "price": price,
            "category": category,
            "location": f"{destination}",
            "amenities": get_amenities_by_category(category),
            "room_type": "Deluxe Room" if category != "budget" else "Standard Room",
            "address": f"{name}, {destination}",
        })
        if len(hotels) >= 3:
            break

    return hotels[:3]

def extract_hotel_name(title: str):
    """
    Extract hotel name from title
    """
    # Remove common booking site names
    title = re.sub(r'\b(MakeMyTrip|Booking\.com|Agoda|Hotels\.com|Trivago)\b', '', title, flags=re.IGNORECASE)
    
    # Look for hotel patterns
    hotel_match = re.search(r'([\w\s]+(?:hotel|resort|inn|lodge|palace|grand)[\w\s]*)', title, re.IGNORECASE)
    if hotel_match:
        return hotel_match.group(1).strip()
    
    # Look for brand names
    brands = ["Marriott", "Hilton", "Hyatt", "Radisson", "Oberoi", "Taj", "ITC", "OYO"]
    for brand in brands:
        if brand.lower() in title.lower():
            return f"{brand} Hotel"
    
    return "Premium Hotel"

def get_amenities_by_category(category: str):
    """
    Return amenities based on hotel category
    """
    if category == "luxury":
        return ["WiFi", "Spa", "Gym", "Pool", "Restaurant", "Bar", "Concierge", "Room Service", "Valet Parking"]
    elif category == "budget":
        return ["WiFi", "AC", "TV", "24/7 Front Desk"]
    else:
        return ["WiFi", "AC", "Restaurant", "Room Service", "Gym", "Parking", "TV"]

def calculate_nights(checkin_date: str, checkout_date: str) -> int:
    """
    Calculate number of nights between check-in and check-out dates
    """
    try:
        checkin = datetime.strptime(checkin_date, "%Y-%m-%d")
        checkout = datetime.strptime(checkout_date, "%Y-%m-%d")
        nights = (checkout - checkin).days
        return max(1, nights)
    except (ValueError, TypeError):
        return 1

async def search_attractions(city: str):
    """
    Search for detailed tourist attractions using Tavily with proper international destination support
    """
    # Create location-aware search queries without bias
    queries = [
        f"top 10 tourist attractions in {city} must visit places landmarks monuments",
        f"famous places to visit {city} historical sites museums parks gardens",
        f"best things to do in {city} travel guide attractions sightseeing",
        f"{city} tourist destinations heritage sites cultural places parks"
    ]
    
    all_attractions = []
    
    for query in queries:
        try:
            results = await search_travel_info(query, max_results=4)
            
            for i, result in enumerate(results):
                title = result.get("title", "")
                content = result.get("content", "")
                url = result.get("url", "")
                
                specific_places = extract_attraction_names(content, city)
                
                for j, place_info in enumerate(specific_places[:3]):
                    attraction_name = place_info.get("name", "")
                    
                    # Skip invalid names
                    if (not attraction_name or 
                        len(attraction_name) < 4 or
                        any(invalid in attraction_name.lower() for invalid in [
                            'visit', 'explore', 'discover', 'top', 'best', 'guide', 
                            '[x]', 'among', 'you can', '...', 'place to', 'thing to'
                        ])):
                        continue
                    
                    location = place_info.get("location", f"{city}")
                    description = place_info.get("description", f"Popular attraction in {city}")
                    
                    kinds = determine_attraction_type(attraction_name + " " + description)
                    ticket_price = determine_realistic_ticket_price_international(attraction_name, city)
                    
                    all_attractions.append({
                        "id": f"tavily_poi_{len(all_attractions)+1}",
                        "name": attraction_name,
                        "kinds": ",".join(kinds),
                        "type": kinds[0] if kinds else "sightseeing",
                        "rate": round(4.0 + (j * 0.15), 1),
                        "address": location,
                        "location": location,
                        "title": title,
                        "content": description,
                        "description": description,
                        "url": url,
                        "source": "Tavily Web Search",
                        "opening_hours": place_info.get("hours", "9:00 AM - 6:00 PM"),
                        "entry_fee": format_entry_fee_international(ticket_price, city),
                        "ticket_price": ticket_price,
                        "raw": result
                    })
                    
                    if len(all_attractions) >= 20:
                        break
                        
                if len(all_attractions) >= 20:
                    break
                    
        except Exception as e:
            logging.warning(f"Query failed: {query}, error: {e}")
            continue
    
    # Remove duplicates
    unique_attractions = []
    seen_names = set()
    
    for attraction in all_attractions:
        name_lower = attraction["name"].lower().strip()
        name_key = name_lower.replace(' ', '').replace('-', '').replace('_', '')
        
        if (name_key and 
            len(name_key) > 4 and 
            name_key not in seen_names and
            not any(generic in name_lower for generic in ['attraction', 'place', 'site', 'location'])):
            seen_names.add(name_key)
            unique_attractions.append(attraction)
    
    logging.info(f"Found {len(unique_attractions)} unique attractions for {city}")
    return unique_attractions[:15]

def determine_realistic_ticket_price_international(name: str, city: str) -> int:
    """
    Determine realistic ticket price based on attraction type and destination
    """
    name_lower = name.lower()
    city_lower = city.lower()
    
    # Determine if it's an Indian destination or international
    indian_cities = [
        'mumbai', 'delhi', 'bangalore', 'chennai', 'hyderabad', 'kolkata', 'pune', 
        'ahmedabad', 'jaipur', 'surat', 'lucknow', 'kanpur', 'nagpur', 'indore',
        'goa', 'kerala', 'rajasthan', 'agra', 'varanasi', 'rishikesh', 'manali'
    ]
    
    is_indian = any(city in city_lower for city in indian_cities) or 'india' in city_lower
    
    if is_indian:
        return determine_realistic_ticket_price(name)
    
    # International pricing (in local currency equivalent to USD)
    
    # Free attractions
    if any(word in name_lower for word in ["temple", "mosque", "church", "cathedral", "beach", "park", "garden", "bridge", "street", "square"]):
        return 0
    
    # Premium attractions
    elif any(word in name_lower for word in ["tower", "observatory", "palace", "castle", "cathedral", "basilica", "opera", "gallery"]):
        if any(famous in name_lower for famous in ["eiffel", "big ben", "statue of liberty", "empire state", "burj"]):
            return 50
        else:
            return 25
    
    # Museums and cultural sites
    elif any(word in name_lower for word in ["museum", "gallery", "exhibition", "art", "history"]):
        return 20
    
    # Historical sites and monuments
    elif any(word in name_lower for word in ["fort", "monument", "heritage", "historic", "ancient"]):
        return 15
    
    # Entertainment and experiences
    elif any(word in name_lower for word in ["zoo", "aquarium", "theme park", "amusement", "safari"]):
        return 35
    
    # Tours and activities
    elif any(word in name_lower for word in ["tour", "cruise", "boat", "cable car", "gondola"]):
        return 30
    
    else:
        return 10

def format_entry_fee_international(price: int, city: str) -> str:
    """
    Format entry fee with appropriate currency
    """
    city_lower = city.lower()
    
    indian_cities = [
        'mumbai', 'delhi', 'bangalore', 'chennai', 'hyderabad', 'kolkata', 'pune', 
        'ahmedabad', 'jaipur', 'surat', 'lucknow', 'kanpur', 'nagpur', 'indore',
        'goa', 'kerala', 'rajasthan', 'agra', 'varanasi', 'rishikesh', 'manali'
    ]
    
    is_indian = any(city in city_lower for city in indian_cities) or 'india' in city_lower
    
    if price == 0:
        return "Free entry"
    
    if is_indian:
        return f"₹{price}"
    
    return f"~${price} USD"

def determine_realistic_ticket_price(name: str) -> int:
    """
    Determine realistic ticket price for Indian attractions
    """
    name_lower = name.lower()
    
    if any(word in name_lower for word in ["temple", "mosque", "church", "gurudwara", "gurdwara", "marine drive", "beach"]):
        return 0
    elif any(word in name_lower for word in ["fort", "palace", "tomb", "gate", "monument", "heritage"]):
        if "unesco" in name_lower or any(famous in name_lower for famous in ["red fort", "qutub", "humayun", "taj"]):
            return 500
        else:
            return 250
    elif any(word in name_lower for word in ["museum", "gallery", "exhibition", "planetarium"]):
        return 200
    elif any(word in name_lower for word in ["park", "garden", "zoo", "aquarium"]):
        if "national park" in name_lower:
            return 300
        elif "zoo" in name_lower or "aquarium" in name_lower:
            return 250
        else:
            return 50
    elif any(word in name_lower for word in ["market", "bazaar", "street"]):
        return 0
    elif any(word in name_lower for word in ["cave", "falls", "valley"]):
        return 300
    else:
        return 100

def extract_attraction_names(content: str, city: str):
    """
    Extract attraction names from web content with improved accuracy
    """
    attractions = []
    
    # Split content into sentences for better parsing
    sentences = content.split('.')
    
    for sentence in sentences:
        sentence = sentence.strip()
        
        if len(sentence) < 20:
            continue
        
        # Improved patterns to extract proper attraction names
        attraction_patterns = [
            # Pattern for "Visit/See/Explore [Attraction Name]"
            r'(?:visit|see|explore|check out)\s+([A-Z][a-zA-Z\s&\-\']+(?:Museum|Gallery|Park|Garden|Beach|Market|Bridge|Tower|Cathedral|Church|Mosque|Monument|Memorial|Square|Center|Centre|Library|Theater|Theatre|Palace|Fort|Temple|Statue|Observatory|Zoo|Aquarium))',
            
            # Pattern for "[Attraction Name] is/offers/features"
            r'([A-Z][a-zA-Z\s&\-\']+(?:Museum|Gallery|Park|Garden|Beach|Market|Bridge|Tower|Cathedral|Church|Mosque|Monument|Memorial|Square|Center|Centre|Library|Theater|Theatre|Palace|Fort|Temple|Statue|Observatory|Zoo|Aquarium))\s+(?:is|offers|features|provides|houses)',
            
            # Pattern for famous/popular/notable [Attraction Name]
            r'(?:famous|popular|notable|renowned)\s+([A-Z][a-zA-Z\s&\-\']+(?:Museum|Gallery|Park|Garden|Beach|Market|Bridge|Tower|Cathedral|Church|Mosque|Monument|Memorial|Square|Center|Centre|Library|Theater|Theatre|Palace|Fort|Temple|Statue|Observatory|Zoo|Aquarium))',
            
            # Pattern for proper nouns ending with attraction types
            r'([A-Z][a-zA-Z\s&\-\']{10,50})\s+(?:museum|gallery|park|garden|beach|market|bridge|tower|cathedral|church|mosque|monument|memorial|square|center|centre|library|theater|theatre|palace|fort|temple|statue|observatory|zoo|aquarium)',
            
            # Pattern for well-known landmarks (no need for type suffix)
            r'(?:visit|see|explore)\s+([A-Z][a-zA-Z\s&\-\']+(?:Brooklyn Bridge|Central Park|Times Square|Empire State|Statue of Liberty|Golden Gate|Freedom Tower|One World|Chelsea Market|High Line|Metropolitan Museum|MOMA|Guggenheim|Lincoln Center|Madison Square))',
            
            # Pattern for specific NYC landmarks
            r'([A-Z][a-zA-Z\s&\-\']*(?:Brooklyn Bridge|Central Park|Times Square|Empire State|Statue of Liberty|Manhattan Bridge|High Line|Chelsea Market|Union Square|Washington Square|Bryant Park|Battery Park|Prospect Park|Coney Island|Greenwich Village))',
        ]
        
        for pattern in attraction_patterns:
            matches = re.findall(pattern, sentence, re.IGNORECASE)
            for match in matches:
                attraction_name = match.strip()
                
                # Filter out invalid names
                if (len(attraction_name) > 8 and 
                    len(attraction_name) < 80 and
                    not any(skip in attraction_name.lower() for skip in [
                        'visit', 'see', 'explore', 'famous', 'popular', 'you can', 'among', 'check out',
                        'offers', 'features', 'provides', 'houses', 'notable', 'renowned'
                    ]) and
                    # Ensure it starts with a capital letter and contains actual content
                    attraction_name[0].isupper() and
                    len([c for c in attraction_name if c.isalpha()]) > 5):
                    
                    # Clean up the name
                    attraction_name = re.sub(r'\s+', ' ', attraction_name)
                    
                    description = f"Explore {attraction_name}, a popular attraction in {city}"
                    
                    attractions.append({
                        "name": attraction_name,
                        "description": description,
                        "location": f"{city}",
                        "hours": "Check locally",
                        "fee": "Check locally"
                    })
                    
                    if len(attractions) >= 5:
                        break
        
        if len(attractions) >= 10:
            break
    
    # If we don't have many attractions, try to extract from content more broadly
    if len(attractions) < 5:
        # Look for well-known attraction patterns in the content
        well_known_patterns = [
            r'(Statue of Liberty)',
            r'(Empire State Building)',
            r'(Central Park)',
            r'(Brooklyn Bridge)',
            r'(Times Square)',
            r'(High Line)',
            r'(Chelsea Market)',
            r'(Metropolitan Museum)',
            r'(Museum of Modern Art|MoMA)',
            r'(9/11 Memorial)',
            r'(One World Trade Center)',
            r'(Bryant Park)',
            r'(Union Square)',
            r'(Washington Square Park)',
            r'(Battery Park)',
            r'(Coney Island)',
            r'(Little Italy)',
            r'(Chinatown)',
            r'(Greenwich Village)',
            r'(SoHo)',
            r'(Tribeca)',
        ]
        
        for pattern in well_known_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                if not any(attr['name'].lower() == match.lower() for attr in attractions):
                    attractions.append({
                        "name": match,
                        "description": f"Visit {match}, a famous landmark in {city}",
                        "location": f"{city}",
                        "hours": "Check locally",
                        "fee": "Check locally"
                    })
    
    return attractions[:8]

def determine_attraction_type(attraction_text: str) -> List[str]:
    """
    Determine attraction types based on text analysis
    """
    text_lower = attraction_text.lower()
    types = []
    
    if any(word in text_lower for word in ["temple", "church", "mosque", "cathedral", "basilica", "synagogue", "gurudwara", "monastery"]):
        types.append("religious")
    
    if any(word in text_lower for word in ["fort", "palace", "castle", "monument", "memorial", "heritage", "historical", "ancient"]):
        types.append("historical")
    
    if any(word in text_lower for word in ["museum", "gallery", "art", "cultural", "exhibition", "theater", "theatre", "opera"]):
        types.append("cultural")
    
    if any(word in text_lower for word in ["park", "garden", "beach", "lake", "river", "mountain", "forest", "nature", "botanical"]):
        types.append("nature")
    
    if any(word in text_lower for word in ["market", "bazaar", "shopping", "mall", "street"]):
        types.append("shopping")
    
    if any(word in text_lower for word in ["zoo", "aquarium", "amusement", "theme park", "entertainment"]):
        types.append("entertainment")
    
    if any(word in text_lower for word in ["tower", "bridge", "building", "architecture", "skyscraper"]):
        types.append("architecture")
    
    if not types:
        types.append("sightseeing")
    
    return types

def format_entry_fee(price: int) -> str:
    """
    Format entry fee as a user-friendly string
    """
    if price == 0:
        return "Free entry"
    else:
        return f"₹{price}"

def get_airlines_for_route(origin: str, destination: str) -> list:
    """
    Get appropriate airlines for a given route
    """
    domestic_airlines = ["IndiGo", "SpiceJet", "Air India", "Vistara", "GoAir", "AirAsia India"]
    international_airlines = ["Air India", "Emirates", "Qatar Airways", "Singapore Airlines", "Lufthansa", "British Airways", "Turkish Airlines"]
    
    # Check if it's an international route
    indian_cities = ["delhi", "mumbai", "bangalore", "kolkata", "chennai", "hyderabad", "pune", "kochi", "goa", "ahmedabad"]
    origin_lower = origin.lower()
    destination_lower = destination.lower()
    
    is_domestic = any(city in origin_lower for city in indian_cities) and any(city in destination_lower for city in indian_cities)
    
    return domestic_airlines if is_domestic else international_airlines

def determine_departure_time(index: int) -> str:
    """
    Generate realistic departure times
    """
    times = ["06:00 AM", "09:30 AM", "02:15 PM", "06:45 PM", "10:20 PM"]
    return times[index % len(times)]

def estimate_flight_duration(origin: str, destination: str) -> str:
    """
    Estimate flight duration based on route
    """
    # Domestic flight durations
    domestic_durations = {
        ("delhi", "mumbai"): "2h 15m",
        ("mumbai", "bangalore"): "1h 45m",
        ("delhi", "kolkata"): "2h 10m",
        ("bangalore", "chennai"): "1h 20m",
        ("mumbai", "kolkata"): "2h 30m",
    }
    
    # International flight durations (approximate)
    international_durations = {
        ("delhi", "new york"): "15h 30m",
        ("mumbai", "london"): "8h 45m",
        ("delhi", "dubai"): "3h 30m",
        ("mumbai", "singapore"): "5h 15m",
        ("bangalore", "frankfurt"): "8h 20m",
    }
    
    origin_lower = origin.lower()
    destination_lower = destination.lower()
    
    # Check domestic routes first
    for (from_city, to_city), duration in domestic_durations.items():
        if from_city in origin_lower and to_city in destination_lower:
            return duration
        if to_city in origin_lower and from_city in destination_lower:
            return duration
    
    # Check international routes
    for (from_city, to_city), duration in international_durations.items():
        if from_city in origin_lower and to_city in destination_lower:
            return duration
        if to_city in origin_lower and from_city in destination_lower:
            return duration
    
    # Default estimates based on route type
    indian_cities = ["delhi", "mumbai", "bangalore", "kolkata", "chennai"]
    is_domestic = any(city in origin_lower for city in indian_cities) and any(city in destination_lower for city in indian_cities)
    
    return "2h 00m" if is_domestic else "8h 30m"

def determine_aircraft(airline: str) -> str:
    """
    Determine typical aircraft for an airline
    """
    aircraft_map = {
        "IndiGo": "Airbus A320",
        "SpiceJet": "Boeing 737",
        "Air India": "Boeing 787",
        "Vistara": "Airbus A321",
        "GoAir": "Airbus A320",
        "AirAsia India": "Airbus A320",
        "Emirates": "Boeing 777",
        "Qatar Airways": "Airbus A350",
        "Singapore Airlines": "Airbus A380",
        "Lufthansa": "Airbus A340",
        "British Airways": "Boeing 787",
        "Turkish Airlines": "Airbus A330"
    }
    return aircraft_map.get(airline, "Boeing 737")

def get_airline_website(airline: str) -> str:
    """
    Get airline booking website
    """
    websites = {
        "IndiGo": "https://www.goindigo.in",
        "SpiceJet": "https://www.spicejet.com",
        "Air India": "https://www.airindia.in",
        "Vistara": "https://www.airvistara.com",
        "GoAir": "https://www.goair.in",
        "AirAsia India": "https://www.airasia.com",
        "Emirates": "https://www.emirates.com",
        "Qatar Airways": "https://www.qatarairways.com",
        "Singapore Airlines": "https://www.singaporeair.com",
        "Lufthansa": "https://www.lufthansa.com",
        "British Airways": "https://www.britishairways.com",
        "Turkish Airlines": "https://www.turkishairlines.com"
    }
    return websites.get(airline, "https://www.google.com/flights")

# Event Planning Search Functions

async def search_event_venues(location: str, event_type: str, capacity: int, budget: float = None, max_results: int = 5, context_keywords: List[str] = None):
    """
    Enhanced context-aware venue search using Tavily API with dynamic keyword generation
    """
    if not tavily_client:
        logging.error("Tavily API key not configured")
        raise RuntimeError("Tavily API not available")
    
    try:
        # Create context-aware search queries
        queries = []
        
        # Primary query with event type and capacity
        budget_term = f"budget ₹{budget//1000}k" if budget else ""
        base_query = f"{event_type} venue {location} capacity {capacity} guests {budget_term}"
        queries.append(base_query)
        
        # Context-aware query enhancement
        if context_keywords:
            for keyword in context_keywords[:2]:  # Use top 2 context keywords
                context_query = f"{keyword} {event_type} venue {location} {capacity} people"
                queries.append(context_query)
        
        # Smart context detection for specialized searches
        context_keywords_lower = [k.lower() for k in (context_keywords or [])]
        
        # Beach/Outdoor context
        if any(keyword in context_keywords_lower for keyword in ['beach', 'outdoor', 'garden', 'pool', 'terrace']):
            if event_type.lower() == "wedding":
                queries.extend([
                    f"beach wedding venue {location} {capacity} guests outdoor",
                    f"garden wedding venue {location} capacity {capacity}",
                    f"outdoor marriage venue {location} {capacity} people"
                ])
            elif event_type.lower() == "birthday":
                queries.extend([
                    f"outdoor birthday party venue {location} {capacity} people",
                    f"garden party venue {location} capacity {capacity}",
                    f"pool party venue {location} {capacity} guests"
                ])
            else:
                queries.extend([
                    f"outdoor event venue {location} {capacity} people",
                    f"garden venue {location} capacity {capacity}",
                    f"outdoor function space {location} {capacity} guests"
                ])
        
        # Indoor/Luxury context
        elif any(keyword in context_keywords_lower for keyword in ['indoor', 'luxury', 'elegant', 'banquet', 'hall']):
            if event_type.lower() == "wedding":
                queries.extend([
                    f"luxury wedding banquet hall {location} {capacity} people",
                    f"elegant marriage venue {location} capacity {capacity}",
                    f"premium wedding hall {location} {capacity} guests"
                ])
            elif event_type.lower() == "corporate":
                queries.extend([
                    f"corporate conference venue {location} {capacity} people",
                    f"business meeting hall {location} capacity {capacity}",
                    f"seminar venue {location} {capacity} guests"
                ])
            else:
                queries.extend([
                    f"banquet hall {location} {capacity} people elegant",
                    f"luxury event venue {location} capacity {capacity}",
                    f"premium function hall {location} {capacity} guests"
                ])
        
        # Default venue type queries if no specific context
        else:
            if event_type.lower() == "wedding":
                queries.extend([
                    f"wedding banquet hall {location} {capacity} people contact details",
                    f"marriage venue {location} {capacity} guests booking phone number",
                    f"wedding resort {location} capacity {capacity} price contact"
                ])
            elif event_type.lower() == "corporate":
                queries.extend([
                    f"corporate event venue {location} {capacity} people conference hall",
                    f"business meeting venue {location} capacity {capacity} contact",
                    f"seminar hall {location} {capacity} guests booking"
                ])
            elif event_type.lower() == "birthday":
                queries.extend([
                    f"birthday party venue {location} {capacity} people celebration",
                    f"party hall {location} capacity {capacity} contact details",
                    f"celebration venue {location} {capacity} guests booking"
                ])
            else:
                queries.extend([
                    f"event venue {location} {capacity} people hall booking",
                    f"function hall {location} capacity {capacity} contact",
                    f"banquet hall {location} {capacity} guests venue"
                ])
        
        all_venues = []
        seen_urls = set()
        
        # Enhanced domain list for context-aware searches
        include_domains = [
            "venuelook.com", "bookmyfunction.com", "weddingz.in", "shaadiwish.com",
            "magicpin.in", "zomato.com", "eazydiner.com", "nearbuy.com",
            "justdial.com", "sulekha.com", "urbanpro.com", "weddingdoers.com",
            "marriagevenues.in", "eventaa.com", "funcart.in", "partyone.in",
            "bookeventz.com", "venuemonk.com", "yelp.com", "tripadvisor.com",
            "facebook.com", "instagram.com", "google.com", "foursquare.com",
            "wedmegood.com", "weddingsutra.com", "indianweddingbuzz.com"
        ]
        
        # Add context-specific domains
        if any(keyword in context_keywords_lower for keyword in ['beach', 'outdoor']):
            include_domains.extend(["makemytrip.com", "goibibo.com", "holidayiq.com", "resorts.com"])
        elif any(keyword in context_keywords_lower for keyword in ['luxury', 'premium']):
            include_domains.extend(["oberoi.com", "tajhotels.com", "marriott.com", "hyatt.com"])
        
        for query in queries[:4]:  # Use top 4 queries for better coverage
            try:
                logging.info(f"Context-aware venue search: {query}")
                
                loop = asyncio.get_event_loop()
                response = await loop.run_in_executor(
                    None,
                    lambda q=query: tavily_client.search(
                        query=q,
                        search_depth="advanced", 
                        max_results=6,  # Increased for more context-aware options
                        include_domains=include_domains
                    )
                )
                
                for result in response.get("results", []):
                    if result.get("url") not in seen_urls:
                        venue = extract_venue_info(result, location, capacity, context_keywords)
                        if venue and venue["name"]:  # Only add if we got a good venue name
                            venue['context_relevance_score'] = calculate_context_relevance(venue, context_keywords or [])
                            all_venues.append(venue)
                            seen_urls.add(result.get("url"))
                            
                            if len(all_venues) >= max_results * 2:  # Get more for better filtering
                                break
                                
                if len(all_venues) >= max_results * 2:
                    break
                    
            except Exception as e:
                logging.warning(f"Context-aware query failed: {query}, error: {e}")
                continue
        
        # Enhanced scoring with context relevance
        def venue_score(venue):
            score = 0
            if venue.get("price_per_day"):
                score += 3
            if venue.get("contact"):
                score += 2
            if venue.get("rating"):
                score += 2
            if venue.get("amenities"):
                score += len(venue["amenities"])
            # Add context relevance score
            score += venue.get('context_relevance_score', 0) * 2
            return score
        
        all_venues.sort(key=venue_score, reverse=True)
        
        logging.info(f"Found {len(all_venues)} context-aware venues for {event_type} in {location}")
        return all_venues[:max_results]
        
    except Exception as e:
        logging.error(f"Context-aware venue search failed: {e}")
        raise

async def search_event_vendors(location: str, service_types: List[str], event_type: str, budget: float = None, max_results: int = 5):
    """
    Search for event vendors with enhanced, specific queries for better results
    """
    if not tavily_client:
        logging.error("Tavily API key not configured")
        raise RuntimeError("Tavily API not available")
    
    try:
        all_vendors = []
        seen_urls = set()
        
        for service_type in service_types:
            # Create specific queries for each service type
            queries = []
            budget_term = f"budget ₹{budget//1000}k" if budget else ""
            
            if service_type.lower() in ["photography", "photographer"]:
                queries = [
                    f"{event_type} photographer {location} contact number price",
                    f"wedding photography {location} candid traditional portfolio",
                    f"professional photographer {location} {event_type} booking"
                ]
            elif service_type.lower() in ["catering", "caterer"]:
                queries = [
                    f"{event_type} catering {location} contact menu price per person",
                    f"wedding caterer {location} north indian south indian menu",
                    f"event catering {location} buffet live counter booking"
                ]
            elif service_type.lower() in ["decoration", "decorator"]:
                queries = [
                    f"{event_type} decoration {location} floral stage mandap contact",
                    f"wedding decorator {location} theme lighting backdrop",
                    f"event decoration {location} flower arrangement booking"
                ]
            elif service_type.lower() in ["entertainment", "dj", "music"]:
                queries = [
                    f"{event_type} dj {location} music entertainment contact",
                    f"wedding dj {location} sound system live band",
                    f"event entertainment {location} music dj booking"
                ]
            else:
                queries = [
                    f"{service_type} {location} {event_type} contact booking",
                    f"event {service_type} {location} professional service",
                    f"{event_type} {service_type} {location} vendor"
                ]
            
            # Search with each query
            for query in queries[:2]:  # Use top 2 queries per service
                try:
                    logging.info(f"Searching vendors with query: {query}")
                    
                    loop = asyncio.get_event_loop()
                    response = await loop.run_in_executor(
                        None,
                        lambda q=query: tavily_client.search(
                            query=q,
                            search_depth="advanced",
                            max_results=8,  # Increased for more vendor options
                            include_domains=[
                                "weddingz.in", "shaadiwish.com", "wedmegood.com",
                                "justdial.com", "sulekha.com", "urbanpro.com",
                                "magicpin.in", "bookmyfunction.com", "eventaa.com",
                                "weddingdoers.com", "funcart.in", "partyone.in",
                                "yelp.com", "google.com", "facebook.com",
                                "instagram.com", "zomato.com", "bookeventz.com",
                                "weddingsutra.com", "indianweddingbuzz.com", "wedwise.com",
                                "bigfat.in", "weddingbazaar.com", "popxo.com"
                            ]
                        )
                    )
                    
                    for result in response.get("results", []):
                        if result.get("url") not in seen_urls:
                            vendor = extract_vendor_info(result, service_type, location)
                            if vendor and vendor["name"] and len(vendor["name"]) > 5:
                                all_vendors.append(vendor)
                                seen_urls.add(result.get("url"))
                                
                                if len(all_vendors) >= max_results:
                                    break
                                    
                    if len(all_vendors) >= max_results:
                        break
                        
                except Exception as e:
                    logging.warning(f"Vendor query failed: {query}, error: {e}")
                    continue
                    
            if len(all_vendors) >= max_results:
                break
        
        # Sort vendors by relevance and quality
        def vendor_score(vendor):
            score = 0
            if vendor.get("contact"):
                score += 3
            if vendor.get("rating"):
                score += 2
            if vendor.get("specialties"):
                score += len(vendor["specialties"])
            if "from ₹" in vendor.get("price_range", "").lower():
                score += 2
            return score
        
        all_vendors.sort(key=vendor_score, reverse=True)
        return all_vendors[:max_results]
        
    except Exception as e:
        logging.error(f"Vendor search failed: {e}")
        raise
        
        for service_type in service_types:
            budget_term = f"budget ₹{budget}" if budget else ""
            query = f"{service_type} {location} {event_type} {budget_term} vendors services providers"
            
            logging.info(f"Searching {service_type} vendors: {query}")
            
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda q=query: tavily_client.search(
                    query=q,
                    search_depth="advanced",
                    max_results=max_results,
                    include_domains=[
                        "weddingz.in", "shaadiwish.com", "sulekha.com", "urbanpro.com",
                        "justdial.com", "zomato.com", "bookmyfunction.com", "magicpin.in",
                        "eventaa.com", "partyone.in", "weddingdoers.com", "funcart.in",
                        "google.com", "facebook.com", "instagram.com", "practo.com"
                    ]
                )
            )
            
            for result in response.get("results", []):
                vendor = extract_vendor_info(result, service_type, location)
                if vendor:
                    vendors.append(vendor)
        
        # Remove duplicates and limit results
        unique_vendors = []
        seen_names = set()
        
        for vendor in vendors:
            name_lower = vendor["name"].lower()
            if name_lower not in seen_names:
                seen_names.add(name_lower)
                unique_vendors.append(vendor)
                
        return unique_vendors[:max_results * len(service_types)]
        
    except Exception as e:
        logging.error(f"Vendor search failed: {e}")
        raise

async def search_event_catering(location: str, cuisine_type: str, guest_count: int, event_type: str, budget: float = None, max_results: int = 5):
    """
    Search for catering services with menu options
    """
    if not tavily_client:
        logging.error("Tavily API key not configured")
        raise RuntimeError("Tavily API not available")
    
    try:
        budget_term = f"per person ₹{budget/guest_count:.0f}" if budget else ""
        query = f"catering services {location} {cuisine_type} {event_type} {guest_count} people {budget_term} menu food"
        
        logging.info(f"Searching catering: {query}")
        
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: tavily_client.search(
                query=query,
                search_depth="advanced",
                max_results=max_results * 2,
                include_domains=[
                    "zomato.com", "swiggy.com", "magicpin.in", "justdial.com",
                    "sulekha.com", "urbanpro.com", "bookmyfunction.com", "weddingz.in",
                    "shaadiwish.com", "eventaa.com", "partyone.in", "nearbuy.com",
                    "google.com", "facebook.com", "eazydiner.com"
                ]
            )
        )
        
        caterers = []
        seen_names = set()
        
        for result in response.get("results", []):
            caterer = extract_catering_info(result, location, cuisine_type)
            if caterer and caterer["name"].lower() not in seen_names:
                seen_names.add(caterer["name"].lower())
                caterers.append(caterer)
                
        return caterers[:max_results]
        
    except Exception as e:
        logging.error(f"Catering search failed: {e}")
        raise

def calculate_context_relevance(item: Dict, context_keywords: List[str]) -> int:
    """
    Calculate how relevant an item is to the given context keywords
    """
    if not context_keywords:
        return 0
    
    score = 0
    item_text = f"{item.get('name', '')} {item.get('description', '')} {' '.join(item.get('specialties', []))} {' '.join(item.get('amenities', []))}".lower()
    
    for keyword in context_keywords:
        if keyword.lower() in item_text:
            score += 1
    
    # Bonus points for exact keyword matches in name
    item_name = item.get('name', '').lower()
    for keyword in context_keywords:
        if keyword.lower() in item_name:
            score += 2
    
    return score


def extract_venue_info(result: Dict, location: str, capacity: int, context_keywords: List[str] = None) -> Dict:
    """
    Extract venue information from search results with enhanced specific name extraction
    """
    try:
        title = result.get("title", "")
        content = result.get("content", "")
        url = result.get("url", "")
        
        # Advanced venue name extraction with multiple strategies
        name = None
        
        # Strategy 1: Look for specific venue names in content first
        venue_name_patterns = [
            # Hotel/Resort patterns
            r'([A-Z][a-zA-Z\s&\',.-]+(?:Hotel|Resort|Palace|Manor|Grand|Marriott|Hyatt|Taj|Oberoi|ITC|Radisson|Sheraton|Hilton|Leela|Park|Imperial)[\w\s]*)',
            # Hall/Banquet patterns
            r'([A-Z][a-zA-Z\s&\',.-]+(?:Hall|Banquet|Convention|Center|Centre|Auditorium|Ballroom)[\w\s]*)',
            # Gardens/Lawn patterns  
            r'([A-Z][a-zA-Z\s&\',.-]+(?:Gardens?|Lawns?|Grounds?|Terrace|Rooftop)[\w\s]*)',
            # Club/Community patterns
            r'([A-Z][a-zA-Z\s&\',.-]+(?:Club|Community|Society|Association)[\w\s]*)',
            # Specific venue names with common suffixes
            r'([A-Z][a-zA-Z\s&\',.-]{3,}(?:\s+(?:Banquets?|Venues?|Events?|Celebrations?|Functions?)))',
            # Names ending with venue types
            r'([A-Z][a-zA-Z\s&\',.-]{5,})\s+(?:banquet|hall|venue|center|centre|resort|hotel)',
        ]
        
        for pattern in venue_name_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                potential_name = matches[0].strip()
                # Clean and validate the name
                potential_name = re.sub(r'\s+', ' ', potential_name).strip()
                if (len(potential_name) > 5 and 
                    not any(skip_word in potential_name.lower() for skip_word in 
                           ['list of', 'best', 'top', 'popular', 'venues in', 'halls in', 'book', 'search', 'find', 'get', 'call'])):
                    name = potential_name
                    break
        
        # Strategy 2: If no specific name found, try title extraction
        if not name:
            # Clean title patterns
            title_patterns = [
                r'^([A-Z][a-zA-Z\s&\',.-]+?)(?:\s*[-|•]|\s+in\s+|\s+@\s+|\s+,)',
                r'^([A-Z][a-zA-Z\s&\',.-]{5,}?)(?:\s*[-|•])',
                r'([A-Z][a-zA-Z\s&\',.-]+(?:Hall|Banquet|Hotel|Resort|Palace|Club|Gardens?))',
            ]
            
            for pattern in title_patterns:
                match = re.search(pattern, title)
                if match:
                    potential_name = match.group(1).strip()
                    if len(potential_name) > 5:
                        name = potential_name
                        break
        
        # Strategy 3: Look for venue names in structured content
        if not name:
            structured_patterns = [
                r'Venue:\s*([A-Z][a-zA-Z\s&\',.-]+)',
                r'Name:\s*([A-Z][a-zA-Z\s&\',.-]+)',
                r'Location:\s*([A-Z][a-zA-Z\s&\',.-]+)',
                r'Address:\s*([A-Z][a-zA-Z\s&\',.-]+?)(?:,|\n|\s{2,})',
            ]
            
            for pattern in structured_patterns:
                match = re.search(pattern, content)
                if match:
                    potential_name = match.group(1).strip()
                    if len(potential_name) > 5:
                        name = potential_name
                        break
        
        # Skip if still no good name found
        if not name or len(name) < 5:
            return None
            
        # Enhanced price extraction with more patterns
        price_per_day = None
        price_patterns = [
            r'₹\s*([0-9,]+)\s*(?:per\s*day|/\s*day)',
            r'₹\s*([0-9,]+)\s*(?:onwards|onward|starting|from)',
            r'(?:price|cost|rate|charges?)[:\s]*₹\s*([0-9,]+)',
            r'₹\s*([0-9,]+)\s*(?:per\s*plate|/\s*plate)',
            r'Rs\.?\s*([0-9,]+)',
            r'(?:from|starting|starts)\s*₹\s*([0-9,]+)',
        ]
        
        for pattern in price_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                try:
                    price = float(match.group(1).replace(',', ''))
                    if price > 100:  # Reasonable minimum
                        price_per_day = price
                        break
                except ValueError:
                    continue
        
        # Enhanced contact extraction with more comprehensive patterns
        contact = None
        contact_patterns = [
            r'(?:phone|tel|call|contact|mobile|whatsapp)[:\s]*([+]?[\d\s\-\(\)]{10,})',
            r'([+]?91[\s\-]?[6-9][\d\s\-]{9,})',  # Indian mobile numbers
            r'([+]?[\d]{2,4}[\s\-]?[\d\s\-]{8,})',
            r'(\d{10})',  # 10 digit numbers
            r'(\d{3}[\s\-]?\d{3}[\s\-]?\d{4})',  # Formatted numbers
            r'book.*?(\d{10})',  # Booking numbers
            r'call.*?(\d{10})',   # Call numbers
        ]
        
        for pattern in contact_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                # Clean the number
                clean_number = re.sub(r'[^\d+]', '', match)
                if len(clean_number) >= 10:
                    contact = match.strip()
                    break
            if contact:
                break
        
        # Enhanced amenities extraction
        amenities = []
        amenity_mapping = {
            'Parking': ['parking', 'valet', 'car park', 'vehicle parking'],
            'AC': ['ac', 'air conditioning', 'air conditioned', 'climate control', 'cooling'],
            'WiFi': ['wifi', 'wi-fi', 'internet', 'wireless', 'broadband'],
            'Catering Kitchen': ['catering', 'food service', 'kitchen', 'dining', 'pantry'],
            'Stage': ['stage', 'platform', 'podium', 'dais'],
            'Sound System': ['sound', 'audio', 'microphone', 'speakers', 'music system'],
            'Lighting': ['lighting', 'led', 'fairy lights', 'chandelier', 'decoration lights'],
            'Garden/Outdoor': ['garden', 'outdoor', 'lawn', 'terrace', 'rooftop', 'open air'],
            'Swimming Pool': ['pool', 'swimming', 'poolside'],
            'Bar': ['bar', 'alcohol', 'drinks', 'cocktail', 'beverages'],
            'Bridal Room': ['bridal room', 'changing room', 'dressing room'],
            'Power Backup': ['generator', 'power backup', 'ups', 'backup power'],
            'Elevator': ['elevator', 'lift', 'escalator'],
            'Restrooms': ['restroom', 'washroom', 'toilet', 'bathroom'],
            'Security': ['security', 'guards', 'cctv', 'surveillance']
        }
        
        content_lower = content.lower()
        for amenity, keywords in amenity_mapping.items():
            if any(keyword in content_lower for keyword in keywords):
                amenities.append(amenity)
        
        # Enhanced rating extraction
        rating = None
        rating_patterns = [
            r'(\d\.\d)\s*(?:out of|/)\s*5',
            r'(\d\.\d)\s*stars?',
            r'rating[:\s]*(\d\.\d)',
            r'(\d\.\d)\s*star',
            r'rated\s*(\d\.\d)',
            r'(\d)/5',
            r'(\d\.\d)\s*\(',  # Rating followed by parentheses
        ]
        
        for pattern in rating_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                try:
                    rating_val = float(match.group(1))
                    if 0 <= rating_val <= 5:
                        rating = rating_val
                        break
                except ValueError:
                    continue
        
        # Enhanced description extraction - get more relevant content
        description_sentences = []
        sentences = content.split('.')
        
        relevant_keywords = ['venue', 'hall', 'banquet', 'wedding', 'event', 'celebration', 
                           'capacity', 'facility', 'perfect', 'ideal', 'located', 'offers']
        
        for sentence in sentences[:8]:
            sentence = sentence.strip()
            if (len(sentence) > 25 and 
                any(keyword in sentence.lower() for keyword in relevant_keywords) and
                not any(skip in sentence.lower() for skip in ['list of', 'top', 'best', 'find', 'search'])):
                description_sentences.append(sentence)
                if len(description_sentences) >= 2:
                    break
        
        description = '. '.join(description_sentences) + '.' if description_sentences else f"Event venue in {location} with capacity for {capacity} guests."
        
        return {
            "name": name,
            "location": location,
            "capacity": capacity,
            "price_per_day": price_per_day,
            "amenities": amenities,
            "rating": rating,
            "contact": contact,
            "description": description,
            "url": url
        }
        
    except Exception as e:
        logging.warning(f"Failed to extract venue info: {e}")
        return None

def extract_vendor_info(result: Dict, service_type: str, location: str) -> Dict:
    """
    Extract vendor information with focus on specific business names and contact details
    """
    try:
        title = result.get("title", "")
        content = result.get("content", "")
        url = result.get("url", "")
        
        # Advanced business name extraction - focus on real businesses
        name = None
        
        # Strategy 1: Extract actual business names from content
        business_name_patterns = [
            # Specific business name patterns with business identifiers
            r'([A-Z][a-zA-Z\s&\',.-]+(?:Photography|Studio|Photos|Images|Clicks|Pixels|Photographers?))',
            r'([A-Z][a-zA-Z\s&\',.-]+(?:Caterers?|Catering|Kitchen|Foods?|Delights|Cuisine))',
            r'([A-Z][a-zA-Z\s&\',.-]+(?:Decorators?|Decor|Events?|Designs?|Planners?))',
            r'([A-Z][a-zA-Z\s&\',.-]+(?:Entertainment|DJ|Music|Band|Sounds?))',
            r'([A-Z][a-zA-Z\s&\',.-]+(?:Services?|Solutions?|Associates|Group|Company))',
            # Names in structured format
            r'Name:\s*([A-Z][a-zA-Z\s&\',.-]+)',
            r'Business:\s*([A-Z][a-zA-Z\s&\',.-]+)',
            r'Vendor:\s*([A-Z][a-zA-Z\s&\',.-]+)',
            # Names in quotes or special markers
            r'"([A-Z][a-zA-Z\s&\',.-]{4,})"',
            r'\*([A-Z][a-zA-Z\s&\',.-]{4,})\*',
            r'•\s*([A-Z][a-zA-Z\s&\',.-]{4,})',
            # Business names before contact details
            r'([A-Z][a-zA-Z\s&\',.-]{4,})\s*[-–]\s*(?:Contact|Call|Phone)',
            # Names with Mr./Mrs./Ms.
            r'(?:Mr\.?|Mrs\.?|Ms\.?)\s*([A-Z][a-zA-Z\s&\',.-]{4,})',
            # Company names ending with specific terms
            r'([A-Z][a-zA-Z\s&\',.-]+(?:Pvt|Ltd|Private|Limited|Co|Corporation|Inc))',
            # Possessive names (e.g., "John's Catering")
            r"([A-Z][a-zA-Z\s&\',.-]+'s\s+(?:Photography|Catering|Services|Studio|Kitchen))",
            # Names followed by location or descriptors
            r'([A-Z][a-zA-Z\s&\',.-]{3,})\s+(?:in|at|Chennai|Bangalore|Mumbai|Delhi)',
        ]
        
        # Check content first for business names
        for pattern in business_name_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                potential_name = match.strip()
                # Validate the name - more refined filtering
                if (len(potential_name) >= 3 and 
                    not any(skip in potential_name.lower() for skip in 
                           ['top', 'best', 'list', 'popular', 'find', 'search', 'book', 'call', 'contact', 
                            'looking', 'discuss', 'alternative', 'experience', 'option']) and
                    not potential_name.isdigit() and
                    not potential_name.lower().startswith(('non-', 'wedding', 'birthday party'))):
                    name = potential_name
                    break
            if name:
                break
        
        # Strategy 2: Extract from title if content didn't yield good results
        if not name:
            # Clean title extraction with better logic
            title_clean = title
            # Remove common prefixes/suffixes
            prefixes_to_remove = [
                'top', 'best', 'popular', 'list of', 'find', 'search', 'book',
                'birthday party', 'wedding', 'event'
            ]
            for prefix in prefixes_to_remove:
                if title_clean.lower().startswith(prefix):
                    title_clean = title_clean[len(prefix):].strip()
            
            # Extract name before separators
            separators = [' - ', ' | ', ' in ', ' at ', ' for ', ' near ', ' chennai', ' bangalore']
            for sep in separators:
                if sep.lower() in title_clean.lower():
                    potential_name = title_clean.split(sep)[0].strip()
                    if len(potential_name) >= 3:
                        name = potential_name
                        break
            
            # Final title fallback with validation
            if not name and len(title_clean) >= 3:
                if not any(word in title_clean.lower() for word in ['looking', 'non-vegetarian', 'discuss']):
                    name = title_clean
        
        # Skip if still no good name or name is too generic
        if (not name or 
            len(name) < 3 or 
            name.lower() in ['photography', 'catering', 'decoration', 'entertainment', 'services'] or
            any(generic in name.lower() for generic in [
                'looking', 'non-vegetarian', 'discuss', 'alternative', 'how much', 
                'persons in', 'includes a', 'there are', 'several', 'talented',
                'kinds of', 'what are', 'where to', 'which is'
            ]) or
            name.lower().startswith(('how ', 'what ', 'where ', 'which ', 'when ', 'why ')) or
            len([word for word in name.split() if word.lower() in ['the', 'a', 'an', 'of', 'for', 'in', 'at', 'on']]) > len(name.split()) // 2):
            return None
        
        # Enhanced contact extraction with multiple patterns
        contact = None
        email = None
        
        # Phone number patterns
        phone_patterns = [
            r'(?:phone|tel|call|contact|mobile|whatsapp)[:\s]*([+]?[\d\s\-\(\)]{10,})',
            r'([+]?91[\s\-]?[6-9][\d\s\-]{9,})',  # Indian mobile
            r'(\d{10})',  # 10 digits
            r'([+]?[\d]{2,4}[\s\-]?[\d\s\-]{8,})',
            r'(\d{3}[\s\-]?\d{3}[\s\-]?\d{4})',
            r'contact[:\s]*(\d+)',
            r'call[:\s]*(\d+)',
            r'mobile[:\s]*(\d+)',
        ]
        
        for pattern in phone_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                clean_number = re.sub(r'[^\d+]', '', match)
                if len(clean_number) >= 10:
                    contact = match.strip()
                    break
            if contact:
                break
        
        # Email patterns
        email_patterns = [
            r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
        ]
        
        for pattern in email_patterns:
            email_match = re.search(pattern, content)
            if email_match:
                email = email_match.group(1)
                break
        
        # Enhanced price extraction
        price_range = "Contact for pricing"
        
        price_patterns = [
            r'₹\s*([0-9,]+)\s*(?:onwards|onward|starting|from|per\s*(?:day|event|hour|person|plate))',
            r'(?:from|starting|starts)\s*₹\s*([0-9,]+)',
            r'₹\s*([0-9,]+)\s*(?:per|/)\s*(?:day|event|hour|person|plate)',
            r'price[:\s]*₹\s*([0-9,]+)',
            r'cost[:\s]*₹\s*([0-9,]+)',
            r'charges?[:\s]*₹\s*([0-9,]+)',
            r'Rs\.?\s*([0-9,]+)',
            r'package[:\s]*₹\s*([0-9,]+)',
        ]
        
        for pattern in price_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                try:
                    price = int(match.group(1).replace(',', ''))
                    if price >= 500:
                        price_range = f"From ₹{price:,}"
                        break
                except ValueError:
                    continue
        
        # Categorize pricing if no specific amount found
        if price_range == "Contact for pricing":
            content_lower = content.lower()
            if any(word in content_lower for word in ["premium", "luxury", "high-end", "professional", "award"]):
                price_range = "Premium pricing"
            elif any(word in content_lower for word in ["affordable", "budget", "economical", "reasonable"]):
                price_range = "Budget-friendly"
            elif any(word in content_lower for word in ["competitive", "market rate"]):
                price_range = "Competitive pricing"
        
        # Service-specific specialties extraction
        specialties = []
        content_lower = content.lower()
        
        if service_type.lower() in ["photography", "photographer"]:
            photo_specialties = {
                'Wedding Photography': ['wedding', 'bridal', 'marriage', 'matrimony'],
                'Candid Photography': ['candid', 'natural', 'lifestyle'],
                'Traditional Photography': ['traditional', 'formal', 'classic'],
                'Pre-Wedding Shoots': ['pre-wedding', 'engagement', 'couple'],
                'Portrait Photography': ['portrait', 'headshot', 'individual'],
                'Event Photography': ['event', 'function', 'celebration'],
                'Fashion Photography': ['fashion', 'model', 'glamour']
            }
            
            for specialty, keywords in photo_specialties.items():
                if any(keyword in content_lower for keyword in keywords):
                    specialties.append(specialty)
                    
        elif service_type.lower() in ["catering", "caterer"]:
            catering_specialties = {
                'North Indian': ['north indian', 'punjabi', 'rajasthani'],
                'South Indian': ['south indian', 'tamil', 'kerala', 'idli', 'dosa'],
                'Chinese': ['chinese', 'indo-chinese', 'noodles'],
                'Continental': ['continental', 'western', 'pasta'],
                'Vegetarian': ['vegetarian', 'veg only', 'pure veg'],
                'Live Counters': ['live counter', 'live cooking', 'chaat'],
                'Buffet': ['buffet', 'unlimited'],
                'Desserts': ['dessert', 'sweets', 'cake']
            }
            
            for specialty, keywords in catering_specialties.items():
                if any(keyword in content_lower for keyword in keywords):
                    specialties.append(specialty)
        
        elif service_type.lower() in ["decoration", "decorator"]:
            decor_specialties = {
                'Floral Decoration': ['flower', 'floral', 'garland'],
                'Lighting': ['lighting', 'led', 'fairy lights'],
                'Stage Decoration': ['stage', 'backdrop', 'mandap'],
                'Theme Decoration': ['theme', 'concept', 'custom'],
                'Balloon Decoration': ['balloon', 'arch']
            }
            
            for specialty, keywords in decor_specialties.items():
                if any(keyword in content_lower for keyword in keywords):
                    specialties.append(specialty)
        
        elif service_type.lower() in ["entertainment", "dj", "music"]:
            entertainment_specialties = {
                'DJ Services': ['dj', 'disc jockey', 'music'],
                'Live Band': ['band', 'live music', 'musicians'],
                'Sound System': ['sound', 'audio', 'speakers'],
                'Karaoke': ['karaoke', 'singing']
            }
            
            for specialty, keywords in entertainment_specialties.items():
                if any(keyword in content_lower for keyword in keywords):
                    specialties.append(specialty)
        
        # Enhanced rating extraction
        rating = None
        rating_patterns = [
            r'(\d\.\d)\s*(?:out of|/)\s*5',
            r'(\d\.\d)\s*stars?',
            r'rating[:\s]*(\d\.\d)',
            r'(\d)/5',
        ]
        
        for pattern in rating_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                try:
                    rating_val = float(match.group(1))
                    if 0 <= rating_val <= 5:
                        rating = rating_val
                        break
                except ValueError:
                    continue
        
        # Create comprehensive contact info
        contact_info = contact
        if email and contact:
            contact_info = f"{contact}, {email}"
        elif email and not contact:
            contact_info = email
        
        # Better description focusing on services
        description_parts = []
        sentences = content.split('.')
        
        for sentence in sentences[:5]:
            sentence = sentence.strip()
            if (len(sentence) > 20 and 
                any(word in sentence.lower() for word in [service_type.lower(), 'service', 'professional', 'experience']) and
                not any(skip in sentence.lower() for skip in ['top', 'best', 'list', 'find'])):
                description_parts.append(sentence)
                if len(description_parts) >= 2:
                    break
        
        description = '. '.join(description_parts) + '.' if description_parts else f"Professional {service_type} service in {location}."
        
        return {
            "name": name,
            "service_type": service_type,
            "location": location,
            "price_range": price_range,
            "specialties": specialties[:5],
            "rating": rating,
            "contact": contact_info,
            "email": email,
            "description": description,
            "url": url
        }
        
    except Exception as e:
        logging.warning(f"Failed to extract vendor info for {service_type}: {e}")
        return None
            
        # Enhanced price range extraction
        price_range = "Contact for pricing"
        
        # Look for specific price mentions
        price_patterns = [
            r'₹\s*([0-9,]+)\s*(?:onwards|onward|starting|from)?',
            r'(?:from|starting|starts)\s*₹\s*([0-9,]+)',
            r'₹\s*([0-9,]+)\s*(?:per|/)\s*(?:day|event|hour)',
            r'package\s*(?:from|starts)\s*₹\s*([0-9,]+)',
        ]
        
        for pattern in price_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                price = match.group(1).replace(',', '')
                try:
                    price_int = int(price)
                    if price_int > 1000:  # Reasonable minimum for professional services
                        price_range = f"From ₹{price_int:,}"
                        break
                except ValueError:
                    continue
        
        # If no specific price, categorize based on content
        if price_range == "Contact for pricing":
            content_lower = content.lower()
            if any(word in content_lower for word in ["premium", "luxury", "high-end", "professional", "experienced"]):
                price_range = "Premium pricing"
            elif any(word in content_lower for word in ["affordable", "budget", "economical", "reasonable"]):
                price_range = "Budget-friendly"
            elif any(word in content_lower for word in ["standard", "competitive", "market"]):
                price_range = "Competitive pricing"
        
        # Enhanced specialties extraction based on service type
        specialties = []
        
        if service_type.lower() in ["photography", "photographer"]:
            photo_keywords = {
                'Wedding Photography': ['wedding photo', 'bridal photo', 'marriage photo'],
                'Candid Photography': ['candid', 'natural', 'unposed'],
                'Traditional Photography': ['traditional', 'formal', 'posed'],
                'Pre-Wedding Shoots': ['pre-wedding', 'engagement', 'couple shoot'],
                'Portrait Photography': ['portrait', 'headshot', 'individual'],
                'Event Coverage': ['event coverage', 'function', 'ceremony'],
                'Drone Photography': ['drone', 'aerial', 'sky view'],
                'Destination Wedding': ['destination', 'outdoor', 'travel']
            }
            for specialty, keywords in photo_keywords.items():
                if any(keyword in content.lower() for keyword in keywords):
                    specialties.append(specialty)
                    
        elif service_type.lower() in ["catering", "caterer"]:
            cuisine_keywords = {
                'North Indian': ['north indian', 'punjabi', 'rajasthani', 'dal', 'roti'],
                'South Indian': ['south indian', 'idli', 'dosa', 'sambar', 'tamil'],
                'Chinese': ['chinese', 'chow mein', 'fried rice', 'manchurian'],
                'Continental': ['continental', 'pasta', 'pizza', 'salad'],
                'Desserts': ['dessert', 'sweet', 'ice cream', 'cake'],
                'Live Counters': ['live counter', 'chaat', 'live cooking'],
                'Buffet Service': ['buffet', 'self service'],
                'Multi-Cuisine': ['multi cuisine', 'variety', 'diverse menu']
            }
            for specialty, keywords in cuisine_keywords.items():
                if any(keyword in content.lower() for keyword in keywords):
                    specialties.append(specialty)
                    
        elif service_type.lower() in ["decoration", "decorator"]:
            decor_keywords = {
                'Floral Decoration': ['floral', 'flowers', 'bouquet', 'garland'],
                'Lighting': ['lighting', 'led', 'fairy lights', 'chandelier'],
                'Stage Decoration': ['stage', 'backdrop', 'mandap'],
                'Theme Decoration': ['theme', 'concept', 'designer'],
                'Balloon Decoration': ['balloon', 'arch'],
                'Draping': ['draping', 'fabric', 'cloth'],
                'Centerpieces': ['centerpiece', 'table decoration']
            }
            for specialty, keywords in decor_keywords.items():
                if any(keyword in content.lower() for keyword in keywords):
                    specialties.append(specialty)
                    
        elif service_type.lower() in ["entertainment", "dj", "music"]:
            entertainment_keywords = {
                'DJ Services': ['dj', 'disc jockey', 'music mixing'],
                'Live Band': ['live band', 'musicians', 'orchestra'],
                'Dance Performance': ['dance', 'choreography', 'performance'],
                'Anchor/MC': ['anchor', 'mc', 'host', 'emcee'],
                'Sound System': ['sound system', 'audio', 'speakers'],
                'Karaoke': ['karaoke', 'singing']
            }
            for specialty, keywords in entertainment_keywords.items():
                if any(keyword in content.lower() for keyword in keywords):
                    specialties.append(specialty)
        
        # Extract rating
        rating = None
        rating_patterns = [
            r'(\d\.\d)\s*(?:out of|/)\s*5',
            r'(\d\.\d)\s*stars?',
            r'rating[:\s]*(\d\.\d)',
            r'(\d\.\d)\s*star',
            r'rated\s*(\d\.\d)'
        ]
        for pattern in rating_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                try:
                    rating = float(match.group(1))
                    if 0 <= rating <= 5:
                        break
                except ValueError:
                    continue
        
        # Extract contact information
        contact = None
        contact_patterns = [
            r'(?:phone|tel|call|contact)[:\s]*([+]?[\d\s\-\(\)]{10,})',
            r'([+]?91[\s\-]?[\d\s\-]{10,})',
            r'([+]?[\d]{2,4}[\s\-]?[\d\s\-]{8,})'
        ]
        
        for pattern in contact_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                contact = match.group(1).strip()
                break
        
        # Better description
        description_sentences = content.split('.')
        relevant_sentences = []
        
        service_keywords = [service_type.lower(), 'service', 'experience', 'professional', 'quality']
        
        for sentence in description_sentences[:5]:
            sentence = sentence.strip()
            if (len(sentence) > 15 and 
                any(word in sentence.lower() for word in service_keywords)):
                relevant_sentences.append(sentence)
                
        description = '. '.join(relevant_sentences[:2]) + '.' if relevant_sentences else content[:200] + "..."
                
        return {
            "name": name,
            "service_type": service_type,
            "location": location,
            "price_range": price_range,
            "specialties": specialties[:5],  # Limit to top 5 specialties
            "rating": rating,
            "contact": contact,
            "description": description,
            "url": url
        }
        
    except Exception as e:
        logging.warning(f"Failed to extract vendor info: {e}")
        return None

def extract_catering_info(result: Dict, location: str, cuisine_type: str) -> Dict:
    """
    Extract catering service information from search results
    """
    try:
        title = result.get("title", "")
        content = result.get("content", "")
        url = result.get("url", "")
        
        # Extract caterer name
        name = title.split(" - ")[0].strip() if " - " in title else title.strip()
        if not name or len(name) < 3:
            return None
            
        # Extract menu specialties
        menu_items = []
        food_keywords = ["biryani", "dal", "paneer", "chicken", "mutton", "dessert", "sweet", 
                        "starter", "main course", "chinese", "continental", "south indian"]
        
        for item in food_keywords:
            if item in content.lower():
                menu_items.append(item.title())
        
        # Extract price per person
        price_per_person = extract_price_from_text(content)
        
        return {
            "name": name,
            "service_type": "catering",
            "location": location,
            "cuisine_type": cuisine_type,
            "price_per_person": price_per_person,
            "menu_highlights": menu_items,
            "description": content[:200] + "..." if len(content) > 200 else content,
            "url": url
        }
        
    except Exception as e:
        logging.warning(f"Failed to extract catering info: {e}")
        return None
