# 🤖 PlanAI — Multi AI Agent Planner

An AI-powered platform that uses **multiple intelligent agents** to generate smart, real-time plans for different domains using live data and LLM reasoning.

---

## 🚀 Features

- ⚡ Real-time planning using Tavily API  
- 🤖 Multi-agent architecture (5 specialized agents)  
- 🧠 Powered by **LLaMA 3.3 70B (Groq)**  
- 📊 Structured, personalized outputs (no templates)  

---

## 🧩 AI Agents

| Agent | Description | Endpoint |
|------|------------|---------|
| ✈️ **Travel Planner** | Flights, hotels, itinerary planning | `/api/plan_trip` |
| 🎉 **Event Planner** | Venues, vendors, budget, timeline | `/api/event/plan` |
| 💻 **Tech Planner** | Architecture, stack, sprint planning (ReAct) | `/api/tech/plan` |
| 📚 **Learning Planner** | Roadmaps, MCQs, certificates | `/api/learning/plan` |
| 💼 **Business Planner** | Full business plan & strategy | `/api/business/plan` |

---

## 🏗️ Tech Stack

**Backend**
- FastAPI  
- LangChain  
- Groq API (LLaMA 3.3)  
- Tavily Search API  

**Frontend**
- React + Vite  
- Tailwind CSS  

**Database**
- SQLite + MongoDB  

---
