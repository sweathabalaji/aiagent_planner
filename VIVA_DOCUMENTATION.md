# PlanAI — Multi AI Agent Planner
## Complete Project Documentation & Viva Q&A Guide

---

# PART 1: PROJECT OVERVIEW

## 1.1 What is PlanAI?

PlanAI is a **full-stack AI-powered planning platform** built as a final year project. It exposes **five domain-specific intelligent agents**, each capable of receiving a user's high-level request and returning a detailed, structured plan using live web data and a large language model (LLM).

The five agents are:

| Agent | Domain | Endpoint |
|-------|--------|----------|
| Travel Planner | Trip planning with flights, hotels, day-wise itinerary | `POST /api/plan_trip` |
| Event Planner | Corporate/personal event with venues, vendors, timeline | `POST /api/event/plan` |
| Tech Planner | Software project architecture & sprint planning | `POST /api/tech/plan` |
| Learning Planner | Personalised learning roadmap with MCQ & certificate | `POST /api/learning/plan` |
| Business Planner | Full business plan (canvas, funding, GTM, financials) | `POST /api/business/plan` |

---

## 1.2 Problem Statement

> **"Planning a trip, organising an event, scoping a software project, creating a learning path, or drafting a business plan all require significant research, domain knowledge, and time — yet most tools either give generic templates or require expensive consultants."**

PlanAI solves this by deploying domain-specific AI agents that:
1. Accept a simple natural-language-style form input from the user.
2. Perform real-time web research using the **Tavily Search API**.
3. Feed retrieved data into an **LLM (Groq-hosted LLaMA 3.1 / Moonshot)** via **LangChain**.
4. Return a structured, budget-aware, personalised plan — no static templates.

---

## 1.3 Key Differentiators

- **No dummy data**: Every plan is generated from live search results.
- **Budget-aware variants**: Travel and Event agents produce Budget / Standard / Premium options.
- **Agentic architecture**: Tech planner uses LangChain **ReAct** (Reasoning + Acting) loop.
- **Persistence layer**: Learning planner saves paths to SQLite + MongoDB; supports MCQ and certificate generation.
- **Parallel execution**: Travel agent runs flight, hotel, and POI searches concurrently with `asyncio.gather`.

---

# PART 2: SYSTEM ARCHITECTURE

## 2.1 High-Level Architecture Diagram

```
┌──────────────────────────────────────────────────────┐
│                FRONTEND (React + Vite)               │
│  Port 3000 — /api proxy → localhost:8000             │
│  Dashboard → [Travel | Event | Tech | Learn | Biz]   │
└────────────────────┬─────────────────────────────────┘
                     │ HTTP JSON (REST)
                     ▼
┌──────────────────────────────────────────────────────┐
│              BACKEND (FastAPI + Uvicorn)              │
│  Port 8000 — CORS: allow_origins=["*"]               │
│                                                      │
│  app.py ──── router: /api/tech/*                    │
│           ├── router: /api/event/*                   │
│           ├── router: /api/learning/*                │
│           ├── router: /api/business/*                │
│           └── direct: POST /api/plan_trip            │
└────────────────────┬─────────────────────────────────┘
                     │
         ┌───────────┼───────────┐
         ▼           ▼           ▼
  ┌──────────┐ ┌──────────┐ ┌──────────┐
  │  Tavily  │ │   LLM    │ │ Database │
  │ Search   │ │  (Groq   │ │ SQLite + │
  │   API    │ │  /Moonsh)│ │ MongoDB  │
  └──────────┘ └──────────┘ └──────────┘
```

---

## 2.2 Technology Stack

### Backend
| Technology | Version | Purpose |
|-----------|---------|---------|
| Python | 3.10+ | Server-side language |
| FastAPI | ≥0.118 | REST API framework, async support, automatic OpenAPI docs |
| Uvicorn | 0.22 | ASGI server for FastAPI |
| LangChain | ≥0.3.27 | LLM orchestration, ReAct agent, tool calling |
| langchain-openai | ≥0.3.35 | OpenAI-compatible interface for Groq/Moonshot |
| Tavily Python SDK | latest | Web search for real-time data retrieval |
| SQLAlchemy | ≥2.0 | ORM for SQLite (learning paths) |
| Pydantic | ≥2.12 | Request/response validation and schema definition |
| python-dotenv | 1.0 | Environment variable management |

### Frontend
| Technology | Version | Purpose |
|-----------|---------|---------|
| React | 18 | UI component library |
| Vite | 4 | Build tool and dev server (port 3000) |
| Tailwind CSS | 3 | Utility-first styling |
| lucide-react | latest | Icon components |
| react-hot-toast | latest | Notification toasts |
| axios / fetch | built-in | HTTP client |

### External APIs
| API | Purpose | Used By |
|-----|---------|---------|
| **Tavily Search API** | Real-time web search, travel/business/academic domains | All 5 agents |
| **Groq API** (OpenAI-compatible) | LLaMA 3.1 70B LLM inference | All 5 agents |
| **MongoDB Atlas** | Cloud database for learning paths, todos, certificates | Learning planner |
| **SQLite** (`learning_paths.db`) | Local relational storage for learning data | Learning planner |

---

## 2.3 Project Folder Structure

```
Multi AI agent Planner/
├── .env                         # API keys (MOONSHOT_API_KEY, TAVILY_API_KEY, etc.)
├── .env.example                 # Template for environment variables
├── requirements.txt             # Python dependencies
├── start.sh                     # Convenience startup script
├── README.md                    # Project readme
├── VIVA_DOCUMENTATION.md        # This document
│
├── backend/
│   ├── app.py                   # FastAPI entry point; registers all routers
│   │
│   ├── agents/                  # Domain-specific AI agents
│   │   ├── planner.py           # Travel agent orchestrator
│   │   ├── flights.py           # Flight search wrapper
│   │   ├── hotels.py            # Hotel search wrapper
│   │   ├── poi.py               # Points-of-interest search
│   │   ├── event_planner.py     # Event planner agent (large: ~2900 lines)
│   │   ├── event_venues.py      # Venue search helper
│   │   ├── event_vendors.py     # Vendor search helper
│   │   ├── event_catering.py    # Catering search helper
│   │   ├── learning_planner.py  # Learning path agent
│   │   ├── business_planner.py  # Business plan agent
│   │   └── cost_estimation.py   # Cost utilities shared across agents
│   │
│   ├── utils/
│   │   ├── llm.py               # LLM factory (ChatOpenAI → Groq endpoint)
│   │   ├── tavily_search.py     # All Tavily client calls + parsing helpers
│   │   ├── optimizer.py         # Travel plan variant generator (LLM + fallback)
│   │   └── schemas.py           # Pydantic data models
│   │
│   ├── tech_planner/
│   │   └── routes.py            # /api/tech/* endpoints + ReAct agent
│   ├── event_planner/
│   │   └── routes.py            # /api/event/* endpoints
│   ├── learning_planner/
│   │   └── routes.py            # /api/learning/* endpoints
│   ├── business_planner/
│   │   └── routes.py            # /api/business/* endpoints
│   │
│   └── memory/
│       ├── db.py                # MongoDB connection + CRUD
│       ├── cache.py             # In-memory caching
│       ├── learning_path_db.py  # Learning-specific DB operations
│       ├── models.py            # DB models
│       └── sqlalchemy_db.py     # SQLite via SQLAlchemy
│
└── frontend/
    ├── vite.config.js           # Port 3000; /api proxy to localhost:8000
    ├── package.json             # React 18, Vite, Tailwind, lucide-react
    └── src/
        ├── App.jsx              # Root: renders Dashboard + Toaster
        ├── main.jsx             # ReactDOM.render entry point
        └── components/
            ├── Dashboard.jsx            # Main navigation hub
            ├── Hero.jsx                 # Landing hero section
            ├── Header.jsx              # App header
            ├── TravelPlanner.jsx       # Travel orchestrator component
            ├── TravelForm.jsx          # Travel input form
            ├── TravelResults.jsx       # Rich travel results display
            ├── EventPlanner.jsx        # Event orchestrator
            ├── EventForm.jsx           # Event input form
            ├── EventResults.jsx        # Event results
            ├── EnhancedEventResults.jsx # Enhanced event display
            ├── TechPlanner.jsx         # Tech orchestrator
            ├── LearningPlanner.jsx     # Learning orchestrator
            ├── LearningForm.jsx        # Learning input form
            ├── LearningResults.jsx     # Course/roadmap display
            ├── MCQAssessment.jsx       # Quiz component
            ├── Certificate.jsx         # Certificate generator
            ├── TodoList.jsx            # Learning todo tracker
            ├── PastLearnings.jsx       # History component
            ├── BusinessPlanner.jsx     # Business orchestrator
            ├── BusinessForm.jsx        # Business input form
            ├── BusinessResults.jsx     # Business plan display
            └── LoadingSpinner.jsx      # Loading state UI
```

---

# PART 3: AGENT-BY-AGENT DEEP DIVE

## 3.1 Travel Planning Agent

### Data Flow
```
User Form (TravelForm.jsx)
  → POST /api/plan_trip  {origin, destination, start_date, end_date, budget, travellers, interests}
  → create_plan_agent()  [backend/agents/planner.py]
       │
       ├── asyncio.gather() — PARALLEL
       │     ├── search_flights(origin, destination, dates, travelers)
       │     │     └── tavily_search.search_flights() → Tavily API → parse → dedupe
       │     ├── search_hotels(destination, check_in, check_out)
       │     │     └── tavily_search.search_hotels() → Tavily API → validate names & prices
       │     └── get_pois_near(destination, interests)
       │           └── tavily_search.search_attractions() → Tavily API → extract place names
       │
       └── optimize_travel_plan(flights, hotels, pois, budget, ...)
             │
             ├── _llm_single_variant("Budget Plan",   budget*0.70)  → LLM JSON
             ├── _llm_single_variant("Standard Plan", budget*1.00)  → LLM JSON
             └── _llm_single_variant("Premium Plan",  budget*1.30)  → LLM JSON
                   │
                   Each variant: 3 flights | 3 hotels | N-day itinerary (5 places/day)
                   Budget split: 35% flights | 35% accommodation | 15% activities | 15% meals+transport

  ← TravelResults.jsx displays: flight cards | hotel cards | day-by-day itinerary
```

### Budget Splitting Formula
For a budget of ₹30,000:
- **Budget Plan** = ₹21,000 (70%) → Flights ₹7,350 | Hotel ₹7,350 | Activities ₹3,150 | Meals ₹3,150
- **Standard Plan** = ₹30,000 (100%) → Flights ₹10,500 | Hotel ₹10,500 | Activities ₹4,500 | Meals ₹4,500
- **Premium Plan** = ₹39,000 (130%) → Flights ₹13,650 | Hotel ₹13,650 | Activities ₹5,850 | Meals ₹5,850

### Key Design Decisions
- **Parallel search** with `asyncio.gather` reduces total wait time (3 searches run simultaneously, not sequentially).
- **Separate LLM calls per variant** prevents JSON truncation (each JSON response is ~6,000 tokens instead of ~22,000).
- **Tavily hotel name validation** rejects sentence fragments from search snippets.
- **Per-night price sanity check**: ₹14 for a hotel room is rejected; minimum ₹250/night for Indian destinations.

---

## 3.2 Event Planning Agent

### Capabilities
- Venue search (banquet halls, hotels, resorts, outdoor spaces)
- Vendor discovery (catering, photography, decoration, entertainment)
- Timeline generation (pre-event, D-day, post-event milestones)
- Cost breakdown with budget optimisation
- Comparison of multiple venue options

### Data Flow
```
EventForm.jsx
  → POST /api/event/plan  {event_type, location, guests, budget, date, preferences}
  → create_event_plan_agent(event_data)  [backend/agents/event_planner.py]
       │
       ├── Tavily venue search (location-specific queries on Indian OTAs/directories)
       ├── Tavily vendor search (catering/photography/decor services)
       ├── Tavily catering search
       ├── LLM synthesis → event plan JSON
       └── Cost estimation [cost_estimation.py]
  ← EventResults.jsx / EnhancedEventResults.jsx
```

---

## 3.3 Tech Project Planning Agent

### Key Feature: ReAct Agent Pattern
The Tech planner uses LangChain's **ReAct (Reason + Act)** paradigm — the most advanced agent pattern in the codebase.

```
POST /api/tech/plan  {project_type, description, team_size, timeline, tech_preferences}
  → create_react_agent(llm, tools, prompt)  [tech_planner/routes.py]
       │
       Loop:
       ├── THINK: "What do I need to research to plan this?"
       ├── ACT:   call search_tech_research(query) [Tavily, dev domains]
       ├── OBSERVE: read search results
       └── THINK: "Do I have enough info?"  → repeat or FINISH
       │
       └── Final LLM pass → structured JSON (architecture, sprints, team, stack)
  ← Tech plan returned to UI
```

**Tavily domains used for tech research:**
`github.com, stackoverflow.com, medium.com, dev.to, arxiv.org, hackernoon.com, techcrunch.com, reactjs.org, fastapi.tiangolo.com, docker.com, kubernetes.io` (and many more)

---

## 3.4 Learning Path Agent

### Capabilities
- Multi-phase learning roadmap (Beginner → Advanced)
- Resource recommendations per phase (courses, books, tutorials, practice problems, communities, tools)
- Interactive MCQ assessment generation
- Digital certificate creation on completion
- Todo tracking (per-module checklist)
- Persistence: saves to SQLite (`learning_paths.db`) with MongoDB fallback

### Data Flow
```
LearningForm.jsx
  → POST /api/learning/plan  {topic, level, duration_weeks, goals}
  → create_learning_path(request)  [agents/learning_planner.py]
       │
       ├── search_learning_resources(topic, "courses")    → Tavily → Udemy, Coursera, edX
       ├── search_learning_resources(topic, "books")      → Tavily → O'Reilly, Amazon
       ├── search_learning_resources(topic, "tutorials")  → Tavily → Medium, freeCodeCamp
       ├── search_learning_resources(topic, "practice")   → Tavily → LeetCode, HackerRank
       ├── search_learning_resources(topic, "communities")→ Tavily → Reddit, Discord
       ├── search_learning_resources(topic, "tools")      → Tavily → GitHub, npm, PyPI
       └── LLM synthesises phased roadmap
       │
       └── save_learning_path() → SQLite + MongoDB
  ← LearningResults.jsx → TodoList → MCQAssessment → Certificate
```

**Additional API routes:**
| Route | Purpose |
|-------|---------|
| `PATCH /api/learning/update-todo` | Update todo item status |
| `POST /api/learning/generate-assessment` | Generate MCQ from learning topic |
| `POST /api/learning/submit-assessment` | Submit MCQ answers, get score |
| `GET /api/learning/generate-certificate` | Issue completion certificate |
| `GET /api/learning/statistics` | Usage statistics |

---

## 3.5 Business Planner Agent

### Capabilities
Generates a **complete business plan** document covering:

| Section | Content |
|---------|---------|
| Business Model Canvas | Key partners, activities, value propositions, customer segments |
| Market Analysis | TAM/SAM/SOM, competitors, market trends |
| Financial Projections | Revenue model, cost structure, break-even analysis |
| Funding Strategy | Seed/Series A, bootstrap, angel/VC recommendations |
| Go-to-Market Strategy | Launch channels, pricing, marketing plan |
| Competitive Analysis | Direct/indirect competitors, SWOT |
| Team Structure | Roles, hiring plan, advisors |

**LLM approach:** Runs parallel LLM calls for each section, then combines into a final document — faster than a single monolithic prompt.

---

# PART 4: KEY TECHNICAL CONCEPTS

## 4.1 What is a ReAct Agent?

**ReAct = Reasoning + Acting** — an AI agent paradigm introduced by Google Research (2022).

Instead of a single LLM call, the agent enters a **loop**:
```
Thought: I need to find the best framework for this project.
Action: search_tech_research("best Python web frameworks 2024 FastAPI Django performance")
Observation: [Tavily returns search results about FastAPI, Django, Flask...]
Thought: FastAPI is better for async APIs. Now I need to check deployment options.
Action: search_tech_research("FastAPI Docker Kubernetes deployment best practices")
Observation: [More results...]
Thought: I have enough information to generate the plan.
Final Answer: {structured plan JSON}
```

**In PlanAI:** The Tech planner uses `langchain.agents.create_react_agent` + `AgentExecutor` with Tavily-backed tool functions.

---

## 4.2 What is LangChain?

LangChain is a Python framework for building LLM-powered applications. It provides:
- **`ChatOpenAI`**: Unified interface for OpenAI, Groq, Azure, etc.
- **`SystemMessage` / `HumanMessage`**: Structured message roles for chat models.
- **`create_react_agent`**: Pre-built ReAct agent loop.
- **`AgentExecutor`**: Runs the agent loop with tool calling and observation feeding.
- **Tool definition**: Wraps functions as callable tools the agent can invoke.

**In PlanAI**, LangChain wraps the Groq LLaMA 3.1 endpoint using `ChatOpenAI` with a custom `openai_api_base` pointing to Groq's OpenAI-compatible URL.

---

## 4.3 What is Tavily?

Tavily is a **search API purpose-built for AI agents**. Unlike Google Search (HTML pages), Tavily returns:
- **Structured JSON** with title, URL, content snippets
- **`search_depth="advanced"`** for richer results
- **`include_domains`** to restrict to trusted sources (e.g., only booking.com, expedia.com for hotels)

**PlanAI uses Tavily for:**
- Flight search → `makemytrip.com`, `cleartrip.com`, `ixigo.com`, etc.
- Hotel search → `booking.com`, `agoda.com`, `hotels.com`, etc.
- Attractions → `tripadvisor.com`, travel blogs
- Learning resources → `coursera.org`, `udemy.com`, `freecodecamp.org`, etc.
- Tech research → `github.com`, `stackoverflow.com`, `arxiv.org`, etc.
- Business data → Generic web search

---

## 4.4 Async and Parallel Execution

Python's `asyncio` is used for **concurrent I/O** — critical because Tavily API calls are network-bound (slow if sequential).

```python
# Travel agent: 3 searches in parallel — NOT sequential
flights_data, hotels_data, pois_data = await asyncio.gather(
    search_flights(origin, destination, start_date, end_date),
    search_hotels(destination, start_date, end_date),
    get_pois_near(destination, interests=interests)
)
```

**Without `asyncio.gather`:** 3 × 2 seconds = ~6 seconds total.
**With `asyncio.gather`:** max(2, 2, 2) = ~2 seconds total (3× faster).

---

## 4.5 Pydantic Data Validation

Every API request and response is defined as a **Pydantic model** (in `utils/schemas.py`). FastAPI automatically validates incoming JSON against these schemas.

```python
class TravelRequest(BaseModel):
    user_id: Optional[str] = None
    origin: str                     # Required — city or IATA code
    destination: str                # Required
    start_date: str                 # Format: "2025-09-01"
    end_date: str
    budget: float                   # Total in INR
    travellers: int = Field(1, ge=1) # Minimum 1
    interests: Optional[List[str]] = []
```

If a required field is missing or has the wrong type, FastAPI returns a **422 Unprocessable Entity** with details — no custom error handling needed.

---

## 4.6 Database Design (Learning Planner)

The Learning Planner uses a **dual-database approach**:

**SQLite (primary, local):**
- Table: `learning_paths` — stores path JSON, user ID, topic, timestamp
- Managed via **SQLAlchemy ORM** (async-safe)
- File: `backend/learning_paths.db`

**MongoDB Atlas (cloud, optional):**
- Collection: `learning_paths` in the configured database
- Stores same data with document-oriented flexibility
- Falls back to SQLite if Mongo URI is not set

---

# PART 5: ENVIRONMENT CONFIGURATION

## 5.1 Required Environment Variables

```env
# AI Language Model (Groq OpenAI-compatible)
MOONSHOT_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxx      # Your Groq API key
MOONSHOT_BASE_URL=https://api.groq.com/openai/v1
MOONSHOT_MODEL=llama-3.1-70b-versatile         # or llama3-8b-8192

# Search API
TAVILY_API_KEY=tvly-xxxxxxxxxxxxxxxxxxxx

# Database
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/planai
DATABASE_PATH=./learning_paths.db              # SQLite path (optional, default)

# Server
PORT=8000
DEFAULT_CURRENCY=INR
```

## 5.2 How `llm.py` Works

```python
def get_chat_llm(model_name=None, temperature=0.0):
    key = os.getenv("MOONSHOT_API_KEY")      # Groq key
    base = os.getenv("MOONSHOT_BASE_URL")    # Groq base URL
    model = model_name or os.getenv("MOONSHOT_MODEL") or "llama-3.1-70b-versatile"
    
    return ChatOpenAI(
        model=model,
        temperature=temperature,
        openai_api_key=key,
        openai_api_base=base     # Points to Groq instead of OpenAI
    )
```

This means **any OpenAI-compatible LLM provider can be swapped in** — just change the base URL and key.

---

# PART 6: FRONTEND ARCHITECTURE

## 6.1 Component Tree

```
App.jsx
└── Dashboard.jsx
    ├── Hero.jsx                   (landing section)
    ├── Header.jsx                 (navigation bar)
    │
    ├── [Travel selected]
    │   └── TravelPlanner.jsx
    │       ├── TravelForm.jsx     (origin, destination, dates, budget, travellers, interests)
    │       ├── LoadingSpinner.jsx (while API call is in progress)
    │       └── TravelResults.jsx  (variants, flights, hotels, itinerary, recommendations)
    │
    ├── [Event selected]
    │   └── EventPlanner.jsx
    │       ├── EventForm.jsx
    │       └── EventResults.jsx / EnhancedEventResults.jsx
    │
    ├── [Tech selected]
    │   └── TechPlanner.jsx → /api/tech/plan
    │
    ├── [Learning selected]
    │   └── LearningPlanner.jsx
    │       ├── LearningForm.jsx
    │       ├── LearningResults.jsx
    │       │   └── TodoList.jsx
    │       ├── MCQAssessment.jsx
    │       └── Certificate.jsx
    │
    └── [Business selected]
        └── BusinessPlanner.jsx
            ├── BusinessForm.jsx
            └── BusinessResults.jsx
```

## 6.2 API Communication Pattern

```javascript
// TravelPlanner.jsx — typical pattern
const handlePlanTrip = async (formData) => {
    setLoading(true);
    const response = await fetch('/api/plan_trip', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
    });
    const data = await response.json();
    setResults(data);
    setLoading(false);
};
```

- `/api` requests are **proxied by Vite** to `http://localhost:8000` (configured in `vite.config.js`).
- No CORS issues in development.
- Learning/Business routes use `http://localhost:8000/api/...` directly (also works since CORS is `allow_origins=["*"]`).

---

# PART 7: HOW TO RUN THE PROJECT

## 7.1 Start Backend

```bash
cd "Multi AI agent Planner"
source venv/bin/activate
cd backend
uvicorn app:app --reload --port 8000
```

## 7.2 Start Frontend

```bash
cd "Multi AI agent Planner/frontend"
npm run dev
# → http://localhost:3000
```

## 7.3 Verify Everything Works

```
GET http://localhost:8000/         → JSON with all endpoint listing
GET http://localhost:8000/health   → {"status": "healthy"}
GET http://localhost:8000/docs     → Swagger UI (interactive API tester)
```

---

# PART 8: VIVA QUESTIONS & ANSWERS

---

## 8.1 CONCEPTUAL / ARCHITECTURE QUESTIONS

---

**Q1. What is the main idea of your project?**

A: PlanAI is a multi-domain AI planning platform where each domain (travel, event, tech, learning, business) has a dedicated intelligent agent. Each agent combines real-time web search (Tavily API) with a large language model (LLaMA 3.1 via Groq) to produce detailed, personalised plans from simple user inputs — with no hardcoded templates or dummy data.

---

**Q2. Why did you call it a "multi-agent" system? How many agents are there?**

A: There are **five domain-specific agents**. Each operates independently with its own:
- Search strategy (different Tavily domain whitelists)
- LLM prompt design
- Output schema
- Persistence requirements

The agents do not communicate with each other — they are "multi-agent" in the sense of multiple specialist systems rather than a collaborative swarm. The Travel agent, for example, uses parallel sub-agents for flights, hotels, and POIs before an orchestrator combines their results.

---

**Q3. Explain the ReAct agent pattern used in the Tech planner.**

A: ReAct stands for **Reasoning + Acting**. It is an iterative loop:
1. The LLM **thinks** about what information it needs.
2. It **acts** by calling a tool (a Tavily search function).
3. It **observes** the results.
4. It thinks again — repeating until it has enough information.
5. It produces a **final answer**.

This is implemented via LangChain's `create_react_agent` + `AgentExecutor`. The advantage over a single LLM call is that the agent can **dynamically decide** what to search for rather than relying on a pre-written prompt with all context.

---

**Q4. What is LangChain and why did you use it?**

A: LangChain is an open-source Python framework for building LLM applications. We used it because:
1. It provides a **unified `ChatOpenAI` interface** that works with OpenAI, Groq, Azure, and Moonshot by just changing the base URL — making the LLM provider swappable.
2. It has pre-built **ReAct agent** infrastructure (`create_react_agent`, `AgentExecutor`) that we used for the Tech planner.
3. It handles **message formatting** (`SystemMessage`, `HumanMessage`) cleanly.
4. It supports **async invocation** (`llm.ainvoke()`) compatible with FastAPI.

---

**Q5. Why did you choose FastAPI over Flask or Django?**

A: Three main reasons:
1. **Async support**: FastAPI is built on Starlette and supports `async/await` natively — critical for our use of `asyncio.gather` to run parallel searches.
2. **Automatic validation**: Pydantic models are integrated directly — invalid requests are rejected with clear error messages automatically.
3. **Auto-documentation**: FastAPI generates Swagger UI at `/docs` with zero extra code — very useful during development and demonstration.

Flask does not have built-in async support or automatic validation. Django is heavier and better suited for full-stack traditional web apps, not REST API backends.

---

**Q6. What is Tavily and why not use Google Search or SerpAPI?**

A: Tavily is a **search API purpose-built for AI agents**. Unlike scraping Google:
1. It returns **structured JSON** (title, URL, clean content snippet) — no HTML parsing required.
2. It supports **domain whitelisting** (`include_domains`) so we can restrict results to trusted booking sites like `booking.com` or academic sites like `arxiv.org`.
3. It has a **`search_depth="advanced"` mode** for richer content extraction.
4. It does not require browser automation or violate terms of service.
5. It has a **generous free tier** suitable for a final year project.

---

**Q7. How does the Travel agent handle the case when Tavily returns no valid hotels?**

A: We have a multi-level strategy:
1. **Strict name validation**: Rejects sentence fragments (e.g., "this hotel offers exceptional value") — only real property names like "The Taj Mahal Palace Hotel" pass.
2. **Price sanity check**: Prices below ₹250/night (Indian destinations) are rejected as parsing noise.
3. **LLM fallback**: The LLM is instructed to use real hotel names from search data OR generate realistic named options if data is insufficient.
4. **Deterministic fallback**: If the LLM call fails entirely, a deterministic function generates named placeholder hotels (e.g., "Lemon Tree Hotel Mumbai") with budget-appropriate pricing.

---

**Q8. How does `asyncio.gather` work and why is it used?**

A: `asyncio.gather` runs multiple coroutines **concurrently** in a single-threaded async event loop. For the Travel agent:

```python
flights, hotels, pois = await asyncio.gather(
    search_flights(...),   # ~2s Tavily call
    search_hotels(...),    # ~2s Tavily call
    get_pois_near(...)     # ~2s Tavily call
)
```

Without `gather`, these would run sequentially: 2 + 2 + 2 = **~6 seconds**. With `gather`, they run in parallel: max(2, 2, 2) = **~2 seconds**. This 3× speed improvement is critical for user experience since these are all I/O-bound operations (network calls).

---

**Q9. What is Pydantic and how does it help?**

A: Pydantic is a Python data validation library. In FastAPI, every endpoint's request body is a Pydantic `BaseModel`. When a request arrives:
1. FastAPI deserialises the JSON body.
2. Pydantic checks every field's type, required/optional status, and any constraints (like `ge=1` for minimum travellers).
3. If validation fails, FastAPI returns a **422 response** with field-level error details automatically — without any custom error handling code.

This guarantees that `budget` is always a `float`, `travellers` is always an `int ≥ 1`, etc., before any agent logic runs.

---

**Q10. Why do you call the LLM three times for Travel (one per variant) instead of once?**

A: The original design called the LLM once with all three variants in a single JSON prompt. The problem:
- Three full itineraries (5 places × N days × 3 variants) can exceed **22,000 tokens** in the response.
- The LLM truncated the output mid-JSON, causing a **parse failure**.
- The system fell back to deterministic generation, losing the LLM's quality.

Splitting into **three separate calls** keeps each response under ~6,000 tokens, which:
1. Always parses successfully.
2. Allows each variant to be individually retried if it fails.
3. The latency increase is acceptable since we still get 3 good results.

---

## 8.2 SYSTEM DESIGN QUESTIONS

---

**Q11. How does the frontend communicate with the backend?**

A: The frontend (React, port 3000) sends **REST API** calls to the backend (FastAPI, port 8000). In development, Vite proxies all `/api/*` requests to `http://localhost:8000` — configured in `vite.config.js`. This means:
- The browser sends `POST /api/plan_trip` (to port 3000).
- Vite intercepts, forwards to `http://localhost:8000/api/plan_trip`.
- The backend processes and returns JSON.
- Vite relays the response back to React.

This proxy avoids **CORS issues** in development. In production, FastAPI has `allow_origins=["*"]` as a blanket CORS policy.

---

**Q12. What happens if an API call fails midway?**

A: At each layer:
1. **Tavily failures**: Wrapped in `try/except` with `logging.warning`. The affected data list returns empty (`[]`), and the system continues with whatever data was retrieved.
2. **LLM failures**: Each variant LLM call is individually caught. Successful variants are kept; failed ones fall back to the deterministic generator.
3. **`asyncio.gather` with `return_exceptions=True`**: If one of the parallel tasks throws, it returns the exception as a value rather than crashing all three — allowing graceful degradation.
4. **Top-level exceptions**: `optimize_travel_plan` catches everything and returns `{"status": "error", "variants": []}` to the frontend, which shows a user-friendly error toast.

---

**Q13. How is the Learning planner different from the others?**

A: The Learning planner is the most feature-rich in terms of **persistence and user journey**:
1. It is the only planner with **database storage** (SQLite + MongoDB).
2. It has **interactive follow-up features**: after generating a roadmap, users can track todos, take an **MCQ quiz** generated by the LLM, and receive a **digital certificate**.
3. It has the most routes (11 endpoints vs 1–2 for Travel/Business).
4. It categorises resources into 6 types: courses, books, tutorials, practice, communities, tools — each searched with domain-specific Tavily queries.

---

**Q14. What is the role of `memory/db.py` and `memory/sqlalchemy_db.py`?**

A: The `memory/` module handles all persistence for the Learning planner:
- **`db.py`**: MongoDB client; functions like `save_learning_path(doc)`, `get_learning_paths(user_id)`, `delete_learning_path(path_id)`.
- **`sqlalchemy_db.py`**: SQLite via SQLAlchemy ORM; used as the local/primary store when MongoDB is unavailable.
- **`cache.py`**: In-memory Python dict cache for session data — avoids redundant DB reads during a single session.
- **`learning_path_db.py`**: Higher-level functions (combining cache + DB) used by `routes.py`.

The pattern is: **cache first → SQLite → MongoDB** (with fallback at each level).

---

**Q15. How does the MCQ assessment work?**

A:
1. After a learning path is generated, the user clicks "Take Assessment".
2. `POST /api/learning/generate-assessment` sends the topic and learning phases to the LLM.
3. The LLM generates 10–15 multiple-choice questions in JSON format with correct answers.
4. `MCQAssessment.jsx` renders the quiz interactively.
5. On submit, `POST /api/learning/submit-assessment` evaluates answers, calculates score, and determines pass/fail.
6. If passed, `GET /api/learning/generate-certificate` returns a certificate with name, topic, score, and date — rendered by `Certificate.jsx`.

---

## 8.3 DESIGN PATTERN QUESTIONS

---

**Q16. What design patterns did you use?**

A:
1. **Facade Pattern**: Each domain's `routes.py` acts as a facade — hiding the complexity of the agent, Tavily calls, and LLM interactions behind a single clean endpoint.
2. **Strategy Pattern**: `optimize_travel_plan` chooses between LLM strategy and deterministic fallback strategy based on runtime success.
3. **Factory Pattern**: `get_chat_llm()` in `llm.py` is a factory function that creates `ChatOpenAI` instances — callers don't know whether the backend is Groq or OpenAI.
4. **Repository Pattern**: `memory/learning_path_db.py` abstracts database operations — routes don't interact with SQLite or MongoDB directly.
5. **Decorator / Middleware Pattern**: FastAPI middleware handles CORS — applied globally without touching individual route handlers.

---

**Q17. How would you scale this system for production?**

A:
1. **Horizontal scaling**: Run multiple FastAPI instances behind an **Nginx / load balancer** using Gunicorn + Uvicorn workers.
2. **Caching**: Add **Redis** to cache Tavily search results for popular routes (e.g., Mumbai → Goa flights) with a 30-minute TTL.
3. **Message queue**: Add **Celery + RabbitMQ** to process planning requests asynchronously — user gets a job ID, polls for completion.
4. **Database**: Migrate all planners to PostgreSQL or MongoDB Atlas for reliability.
5. **Rate limiting**: Add API rate limits per user (FastAPI + Redis counter).
6. **Secrets management**: Move API keys to AWS Secrets Manager or HashiCorp Vault instead of `.env` files.
7. **CDN**: Serve the React build via Cloudflare CDN.

---

**Q18. What are the limitations of the current system?**

A:
1. **Tavily rate limits**: Free tier limits requests per month — heavy usage could hit the cap.
2. **LLM non-determinism**: The LLM may give different answers for the same input — hard to unit test.
3. **No authentication**: The API has no user login, no JWT tokens — anyone can call any endpoint.
4. **No caching**: Every request hits Tavily and the LLM — slow and expensive for repeated queries.
5. **Synchronous LLM SDK**: LangChain's `ChatOpenAI.ainvoke` is async at the Python level, but the underlying Groq HTTP call is synchronous under the hood — can block the event loop under heavy load.
6. **SQLite for learning**: Not suitable for multi-user production; needs PostgreSQL.

---

**Q19. How did you handle CORS?**

A: FastAPI's `CORSMiddleware` is added with `allow_origins=["*"]` — this allows any origin to call the API. This is acceptable for a development/demo project. In production, we would restrict to specific origins:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://planai.yourdomain.com"],
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)
```

---

**Q20. Why does Vite proxy `/api` to port 8000?**

A: During development, the React app runs on port 3000 and the FastAPI backend on port 8000. Browsers block cross-origin requests (different ports = different origins = CORS). Instead of configuring CORS for local dev, Vite acts as a **reverse proxy** — it intercepts all `/api/*` requests from the browser, forwards them to `localhost:8000`, and returns the response. To the browser, it looks like a same-origin request (same port 3000).

---

## 8.4 AI / ML QUESTIONS

---

**Q21. What LLM model do you use and why?**

A: The project uses **LLaMA 3.1 70B** (Meta's open-source model) hosted on **Groq Cloud** via an OpenAI-compatible API. Reasons:
1. **Speed**: Groq uses custom LPU (Language Processing Unit) hardware — significantly faster inference than OpenAI or Anthropic.
2. **Cost**: Groq offers a generous free tier — suitable for a student project.
3. **OpenAI compatibility**: LangChain's `ChatOpenAI` class works without modification — just point `openai_api_base` to Groq.
4. **Model quality**: LLaMA 3.1 70B produces high-quality structured JSON output — critical for our use case.

---

**Q22. How do you get the LLM to output valid JSON?**

A: Three-layer approach:
1. **System prompt**: We instruct the LLM: *"Output valid JSON only. No markdown fences. Escape quotes inside strings."*
2. **JSON schema in prompt**: We include the exact shape of the expected JSON object with field names, data types, and example values in the user message — the LLM fills in the values.
3. **Post-processing**: `_extract_json_from_response()` strips markdown code fences (` ```json ... ``` `), then `json.loads()` parses the result. If that fails, we try extracting the substring between the first `{` and last `}`.

---

**Q23. What is `temperature=0.0` in the LLM and why do you use it?**

A: Temperature controls the **randomness** of LLM output:
- `temperature=0.0` → **Deterministic/greedy** — always picks the most probable token. Best for structured outputs (JSON) where we need consistency.
- `temperature=1.0` → High randomness — creative but unpredictable.
- `temperature=0.7` → Middle ground — used for creative writing.

For our use case (structured JSON plans), `temperature=0.0` or `0.3` ensures the LLM reliably produces well-formed JSON rather than varying between runs.

---

**Q24. What prompt engineering techniques did you use?**

A:
1. **System / User role separation**: System message sets the LLM's persona ("You are an expert travel agent..."); user message contains the actual task.
2. **Few-shot examples in schema**: The JSON template in the prompt shows the exact structure expected — the LLM uses it as a template to fill.
3. **Explicit constraints**: "Return ONLY the JSON object", "Each day MUST have EXACTLY 5 activities", "Numbers only for prices".
4. **Context injection**: Real search results (flights, hotels, places) from Tavily are injected into the prompt so the LLM generates plans grounded in real data.
5. **Role prompting**: "You are an expert travel agent with deep knowledge of destinations worldwide."

---

**Q25. How is the system different from ChatGPT for travel planning?**

A:
1. **Structured output**: PlanAI always returns machine-readable JSON that the UI renders as cards, charts, and itineraries. ChatGPT returns free text.
2. **Real-time data**: PlanAI queries Tavily for current hotel prices and flights. ChatGPT's knowledge has a cutoff date.
3. **Budget integration**: PlanAI splits the user's exact budget into components. ChatGPT gives generic advice.
4. **Multi-domain**: PlanAI has 5 specialised agents. ChatGPT is general-purpose.
5. **Persistence**: PlanAI saves learning paths, todos, and certificates. ChatGPT has no persistent state (outside paid memory features).

---

## 8.5 DATABASE QUESTIONS

---

**Q26. Why two databases (SQLite + MongoDB)?**

A: 
- **SQLite** is used as the **primary local store** — zero setup, no server needed, great for development and single-server deployment.
- **MongoDB** is used as the **cloud store** — better for multi-user, multi-server deployments; schema-flexible (documents can have varying structures as features evolve).
- The system checks MongoDB first; if unavailable, falls back to SQLite. This ensures the app works even without a MongoDB connection.

---

**Q27. What is SQLAlchemy and why use an ORM?**

A: SQLAlchemy is a Python SQL toolkit and ORM (Object-Relational Mapper). Instead of writing raw SQL:

```python
# Without ORM
cursor.execute("INSERT INTO learning_paths VALUES (?, ?, ?)", (id, topic, data))

# With SQLAlchemy ORM
session.add(LearningPath(id=id, topic=topic, data=data))
session.commit()
```

Benefits:
1. **Database agnostic**: Switch from SQLite to PostgreSQL with one config change.
2. **Pythonic API**: Work with Python objects, not SQL strings.
3. **SQL injection protection**: Parameterised queries by default.
4. **Migration support**: Can integrate Alembic for schema migrations.

---

## 8.6 FRONTEND QUESTIONS

---

**Q28. Why React and not plain HTML/JavaScript?**

A:
1. **Component reuse**: `FlightCard`, `HotelCard`, `DayCard`, `ActivityCard` are reusable components — written once, used multiple times.
2. **State management**: React's `useState` and `useEffect` manage UI state (loading spinner, selected variant tab, expanded sections) without complex DOM manipulation.
3. **Virtual DOM**: React updates only changed parts of the UI — better performance than re-rendering the whole page.
4. **Ecosystem**: Tailwind CSS, lucide-react icons, react-hot-toast all integrate cleanly with React.

---

**Q29. Why Vite instead of Create React App (CRA)?**

A:
1. **Speed**: Vite uses native ES modules and **esbuild** for bundling — dev server starts in milliseconds vs. 30+ seconds for CRA (Webpack-based).
2. **Hot Module Replacement (HMR)**: Vite's HMR is near-instant — edit a component and see the change in < 50ms.
3. **Smaller config**: Less boilerplate than CRA.
4. **Built-in proxy**: The `/api` proxy is configured in a single `vite.config.js` option.

---

**Q30. How does TravelResults.jsx handle missing data gracefully?**

A: Every field access uses **optional chaining** and **fallback values**:

```javascript
// Hotel name — falls back to generic if null
hotel.name || 'Hotel'

// Flight price — formats as 0 if undefined
fmt(flight.price || 0)

// Activities array — defaults to empty array if missing
(day.activities || []).map(...)

// Rating — clamps between 0 and 5
Math.min(5, Math.max(0, Number(activity.rating) || 0))
```

This ensures the UI never crashes with `TypeError: Cannot read property of null`.

---

## 8.7 TESTING & QUALITY QUESTIONS

---

**Q31. How did you test the system?**

A:
1. **FastAPI Swagger UI** (`/docs`): Used to test every endpoint interactively with different inputs.
2. **`uvicorn --reload`**: Hot-reload on file save made backend iteration fast.
3. **Browser DevTools Network tab**: Inspected actual request/response JSON for every API call.
4. **Logging**: All agents use Python's `logging` module (`logging.info`, `logging.warning`, `logging.error`) — errors visible in terminal.
5. **Manual validation**: Entered real trip details (Mumbai → Goa, ₹20,000 budget) and verified results matched expectations.

---

**Q32. What would you add if you had more time?**

A:
1. **User authentication**: JWT-based login with persistent user profiles.
2. **Redis caching**: Cache popular route results to reduce Tavily API calls.
3. **Unit tests**: pytest test suite for each agent function.
4. **Booking integration**: Deep-link to actual booking pages on MakeMyTrip/Booking.com with query parameters pre-filled.
5. **Real-time pricing**: WebSocket connection to update prices live.
6. **Mobile app**: React Native version of the frontend.
7. **Comparison mode**: Side-by-side comparison of variants on one screen.
8. **Export**: PDF/WhatsApp share of the generated plan.

---

## 8.8 SCENARIO / DEMO QUESTIONS

---

**Q33. Walk me through exactly what happens when a user submits "Mumbai to Goa, 3 days, ₹15,000".**

A:
1. User fills `TravelForm.jsx`: origin=Mumbai, destination=Goa, dates=May 1–4, budget=15000, travellers=1.
2. React's `handlePlanTrip` sends `POST /api/plan_trip` with this JSON.
3. FastAPI's `plan_trip` handler validates via `TravelRequest` Pydantic model, calls `create_plan_agent(req.dict())`.
4. `planner.py` extracts fields and launches `asyncio.gather`:
   - Tavily searches for "flights Mumbai to Goa 2025-05-01 booking prices"
   - Tavily searches for "hotels Goa booking accommodation 2025-05-01 Booking.com Agoda"
   - Tavily searches for "top tourist attractions Goa must visit landmarks"
5. Results are collected (3 flights, some hotels, ~15 attractions).
6. Hotels are validated: names checked against blacklist, prices checked (must be ≥ ₹250/night).
7. `optimize_travel_plan` makes 3 LLM calls:
   - "Budget Plan" (₹10,500): LLM picks economy flights, budget hotels, 3 days × 5 Goa places.
   - "Standard Plan" (₹15,000): LLM picks mid-range options.
   - "Premium Plan" (₹19,500): LLM picks premium flights, beach resorts.
8. Each LLM response is parsed, validated, and cleaned.
9. `generate_recommendations` creates the AI tips section.
10. Full JSON response sent back to React.
11. `TravelResults.jsx` renders 3 variant tabs, flight cards, hotel cards, and day-by-day itinerary with expandable tips.

---

**Q34. What if Tavily returns no results for a route?**

A: The system handles this at every level:
1. Tavily returns `[]` → agent logs a warning, passes empty list to optimizer.
2. LLM prompt says: "if insufficient, use realistic named options for this route" — LLM generates plausible flights (IndiGo, SpiceJet) with route-appropriate pricing from the hardcoded `get_realistic_flight_price()` heuristic.
3. If LLM JSON is also invalid → `_create_deterministic_variants()` runs with named default airlines and `_create_default_hotels()` with destination-appropriate hotel brands.
4. The user always receives a complete plan — the quality degrades gracefully, but the app never crashes.

---

**Q35. How does the system know IndiGo is a budget airline and Emirates is premium?**

A: `tavily_search.py` has hardcoded airline classifications in `get_airline_premium_multiplier()` and `get_international_airline_multiplier()`:

```python
premium_airlines = ["Vistara", "Air India"]         # 1.15× price multiplier
budget_airlines  = ["SpiceJet", "GoAir", "AirAsia"] # 0.9× price multiplier

premium_international = ["Emirates", "Singapore Airlines", "Qatar Airways"]  # 1.3× 
budget_international  = ["IndiGo", "SpiceJet", "AirAsia", "Scoot"]          # 0.85×
```

The LLM also picks up airline tiers from its training data — it knows Emirates is premium from real-world knowledge.

---

# PART 9: QUICK REFERENCE CHEAT SHEET

## Key Numbers
| Item | Value |
|------|-------|
| Backend port | 8000 |
| Frontend port | 3000 |
| LLM model | llama-3.1-70b-versatile (Groq) |
| Travel parallel searches | 3 (flights, hotels, POIs) |
| Activities per day | 5 |
| Variants per travel plan | 3 (Budget 70%, Standard 100%, Premium 130%) |
| Budget split | 35% flights + 35% hotel + 15% activities + 15% meals |
| Min hotel price (India) | ₹250/night (filter threshold) |
| Python version | 3.10+ |
| Node.js version | 16+ |

## API Endpoints Summary
| Method | URL | Agent | Returns |
|--------|-----|-------|---------|
| POST | `/api/plan_trip` | Travel | 3 variants with flights, hotels, N-day itinerary |
| POST | `/api/event/plan` | Event | Venues, vendors, timeline, cost breakdown |
| GET | `/api/event/venues/{location}` | Event | Venue list for location |
| GET | `/api/event/vendors/{location}` | Event | Vendor list for location |
| POST | `/api/tech/plan` | Tech (ReAct) | Architecture, sprint plan, team structure |
| GET | `/api/tech/templates` | Tech | Project template list |
| POST | `/api/learning/plan` | Learning | Learning roadmap with resources by type |
| PATCH | `/api/learning/update-todo` | Learning | Updated todo status |
| POST | `/api/learning/generate-assessment` | Learning | MCQ questions |
| POST | `/api/learning/submit-assessment` | Learning | Score and pass/fail |
| GET | `/api/learning/generate-certificate` | Learning | Certificate data |
| POST | `/api/business/plan` | Business | Full business plan document |
| GET | `/health` | — | `{"status": "healthy"}` |
| GET | `/docs` | — | Swagger UI |

## Environment Variables (required)
```
MOONSHOT_API_KEY      → Groq API key (format: gsk_...)
MOONSHOT_BASE_URL     → https://api.groq.com/openai/v1
MOONSHOT_MODEL        → llama-3.1-70b-versatile
TAVILY_API_KEY        → tvly-...
MONGODB_URI           → mongodb+srv://... (optional, for learning planner)
```

---

# PART 10: GLOSSARY

| Term | Definition |
|------|-----------|
| **Agent** | An AI system that perceives input, reasons about it, and takes actions (like calling APIs) to achieve a goal |
| **ReAct** | Reasoning + Acting — an agent that loops between thinking and calling tools |
| **LLM** | Large Language Model — a neural network trained on text (e.g., LLaMA, GPT-4) |
| **LangChain** | Python framework for building LLM applications with tools, agents, and chains |
| **Tavily** | Search API optimised for AI agents, returns structured JSON from web search |
| **FastAPI** | Python web framework with async support, Pydantic validation, and auto Swagger docs |
| **Pydantic** | Python data validation library using type annotations |
| **asyncio.gather** | Runs multiple async functions concurrently (parallel, not sequential) |
| **CORS** | Cross-Origin Resource Sharing — browser security policy for cross-domain requests |
| **Vite** | Frontend build tool and dev server; much faster than Webpack |
| **SQLAlchemy** | Python ORM for SQL databases (works with SQLite, PostgreSQL, MySQL) |
| **Groq** | AI infrastructure company; hosts LLaMA 3 with very fast inference via custom LPU chips |
| **Hot Module Replacement** | Dev feature: browser updates instantly when you save a file, without full refresh |
| **Pydantic BaseModel** | Base class for all request/response schemas in FastAPI |
| **System Message** | LangChain's message type that sets the LLM's persona/instructions |
| **Temperature** | LLM parameter controlling output randomness (0=deterministic, 1=creative) |
| **JWT** | JSON Web Token — a standard for stateless authentication (not implemented yet) |
| **ORM** | Object-Relational Mapper — lets you work with databases using Python objects |

---

*Document prepared for Final Year Project Viva Review — PlanAI Multi AI Agent Planner*
*All five agents are live and running. Backend: http://localhost:8000 | Frontend: http://localhost:3000*
