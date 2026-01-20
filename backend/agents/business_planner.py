"""
Business Startup Planner Agent
Creates comprehensive business plans, funding strategies, and market analysis using Moonshot AI.
"""

from langchain_core.messages import HumanMessage, SystemMessage
from utils.llm import get_chat_llm
from utils.tavily_search import tavily_search
import json
from typing import Dict, List
import asyncio


class BusinessPlannerAgent:
    """Agent for creating comprehensive business startup plans."""
    
    def __init__(self):
        self.llm = get_chat_llm()
        
    async def create_business_plan(
        self, 
        business_idea: str,
        industry: str,
        target_market: str,
        business_model: str,
        funding_needed: str,
        location: str
    ) -> dict:
        """
        Create a comprehensive business startup plan.
        
        Args:
            business_idea: Core business concept
            industry: Industry sector
            target_market: Target customer segment
            business_model: Revenue model (B2B, B2C, SaaS, etc.)
            funding_needed: Estimated funding requirement
            location: Business location
        """
        
        # Run all analyses in parallel
        results = await asyncio.gather(
            self._generate_business_model_canvas(business_idea, industry, target_market, business_model),
            self._generate_funding_strategy(business_idea, funding_needed, industry),
            self._generate_market_analysis(industry, target_market, location, business_idea),
            self._generate_competitive_analysis(business_idea, industry, location),
            self._generate_financial_projections(business_idea, business_model, funding_needed),
            self._generate_go_to_market_strategy(business_idea, target_market, business_model),
            return_exceptions=True
        )
        
        # Unpack results
        business_model_canvas = results[0] if not isinstance(results[0], Exception) else self._fallback_business_model_canvas()
        funding_strategy = results[1] if not isinstance(results[1], Exception) else self._fallback_funding_strategy()
        market_analysis = results[2] if not isinstance(results[2], Exception) else self._fallback_market_analysis()
        competitive_analysis = results[3] if not isinstance(results[3], Exception) else self._fallback_competitive_analysis()
        financial_projections = results[4] if not isinstance(results[4], Exception) else self._fallback_financial_projections()
        go_to_market = results[5] if not isinstance(results[5], Exception) else self._fallback_go_to_market()
        
        return {
            "business_overview": {
                "business_name": self._generate_business_name(business_idea),
                "tagline": self._generate_tagline(business_idea, target_market),
                "industry": industry,
                "business_model": business_model,
                "location": location
            },
            "business_model_canvas": business_model_canvas,
            "funding_strategy": funding_strategy,
            "market_analysis": market_analysis,
            "competitive_analysis": competitive_analysis,
            "financial_projections": financial_projections,
            "go_to_market_strategy": go_to_market,
            "next_steps": self._generate_next_steps(business_idea, funding_needed)
        }
    
    def _generate_business_name(self, business_idea: str) -> str:
        """Generate a creative business name."""
        prompt = f"""Generate 1 creative, memorable business name for this idea:

Business Idea: {business_idea}

Requirements:
- Short and memorable (1-3 words)
- Easy to spell and pronounce
- Professional and modern
- Available as a domain name likely

Return ONLY the business name, nothing else."""

        response = self.llm.invoke([
            SystemMessage(content="You are a creative branding expert."),
            HumanMessage(content=prompt)
        ])
        
        return response.content.strip().strip('"')
    
    def _generate_tagline(self, business_idea: str, target_market: str) -> str:
        """Generate a compelling tagline."""
        prompt = f"""Create a compelling tagline for this business:

Business Idea: {business_idea}
Target Market: {target_market}

Requirements:
- 5-8 words maximum
- Clear value proposition
- Memorable and catchy
- Professional tone

Return ONLY the tagline, nothing else."""

        response = self.llm.invoke([
            SystemMessage(content="You are a creative marketing expert."),
            HumanMessage(content=prompt)
        ])
        
        return response.content.strip().strip('"')
    
    async def _generate_business_model_canvas(
        self, 
        business_idea: str, 
        industry: str, 
        target_market: str,
        business_model: str
    ) -> dict:
        """Generate Business Model Canvas."""
        
        prompt = f"""Create a detailed Business Model Canvas for this startup:

Business Idea: {business_idea}
Industry: {industry}
Target Market: {target_market}
Business Model: {business_model}

Return ONLY a valid JSON object with this exact structure:
{{
    "value_propositions": [
        {{
            "title": "Main value proposition title",
            "description": "Detailed explanation",
            "benefits": ["benefit1", "benefit2", "benefit3"]
        }}
    ],
    "customer_segments": [
        {{
            "segment": "Segment name",
            "description": "Who they are",
            "size": "Market size estimate",
            "characteristics": ["char1", "char2"]
        }}
    ],
    "channels": [
        {{
            "channel": "Distribution channel",
            "type": "Direct/Indirect",
            "purpose": "Purpose and reach",
            "cost": "Relative cost (Low/Medium/High)"
        }}
    ],
    "customer_relationships": [
        {{
            "type": "Relationship type",
            "description": "How you interact with customers",
            "examples": ["example1", "example2"]
        }}
    ],
    "revenue_streams": [
        {{
            "stream": "Revenue source",
            "type": "One-time/Recurring",
            "pricing_model": "How you charge",
            "potential": "Revenue potential"
        }}
    ],
    "key_resources": [
        {{
            "category": "Resource category",
            "resources": ["resource1", "resource2"],
            "importance": "Why critical"
        }}
    ],
    "key_activities": [
        {{
            "activity": "Core activity",
            "description": "What it involves",
            "frequency": "How often"
        }}
    ],
    "key_partnerships": [
        {{
            "partner_type": "Type of partner",
            "examples": ["partner1", "partner2"],
            "value": "Why needed"
        }}
    ],
    "cost_structure": [
        {{
            "category": "Cost category",
            "items": ["cost1", "cost2"],
            "type": "Fixed/Variable",
            "priority": "High/Medium/Low"
        }}
    ]
}}"""

        response = self.llm.invoke([
            SystemMessage(content="You are a business strategy expert. Always respond with valid JSON only."),
            HumanMessage(content=prompt)
        ])
        
        return self._parse_json_response(response.content, self._fallback_business_model_canvas())
    
    async def _generate_funding_strategy(
        self, 
        business_idea: str, 
        funding_needed: str,
        industry: str
    ) -> dict:
        """Generate comprehensive funding strategy."""
        
        prompt = f"""Create a detailed funding strategy for this startup:

Business Idea: {business_idea}
Industry: {industry}
Funding Needed: {funding_needed}

Return ONLY a valid JSON object with this exact structure:
{{
    "funding_stages": [
        {{
            "stage": "Stage name (e.g., Pre-seed, Seed, Series A)",
            "timing": "When to raise",
            "amount": "Funding amount",
            "purpose": "Use of funds",
            "milestones": ["milestone1", "milestone2"],
            "valuation_range": "Expected valuation"
        }}
    ],
    "funding_sources": [
        {{
            "source": "Funding source type",
            "description": "What it is",
            "pros": ["pro1", "pro2"],
            "cons": ["con1", "con2"],
            "best_for": "When to use this source",
            "typical_amount": "Typical funding range"
        }}
    ],
    "pitch_deck_outline": [
        {{
            "slide": "Slide name",
            "content": "Key points to cover",
            "tips": ["tip1", "tip2"]
        }}
    ],
    "investor_targeting": {{
        "ideal_investor_profile": ["characteristic1", "characteristic2"],
        "investor_types": ["Angel investors", "VCs", "etc"],
        "networking_strategies": ["strategy1", "strategy2"],
        "key_metrics_to_show": ["metric1", "metric2"]
    }},
    "funding_timeline": [
        {{
            "phase": "Phase name",
            "duration": "Time period",
            "activities": ["activity1", "activity2"],
            "outcomes": "Expected results"
        }}
    ],
    "alternative_funding": [
        {{
            "option": "Alternative option",
            "description": "How it works",
            "suitability": "When to consider"
        }}
    ]
}}"""

        response = self.llm.invoke([
            SystemMessage(content="You are a startup funding expert. Always respond with valid JSON only."),
            HumanMessage(content=prompt)
        ])
        
        return self._parse_json_response(response.content, self._fallback_funding_strategy())
    
    async def _generate_market_analysis(
        self, 
        industry: str, 
        target_market: str,
        location: str,
        business_idea: str
    ) -> dict:
        """Generate comprehensive market analysis with real data."""
        
        # Search for real market data
        search_queries = [
            f"{industry} market size and growth trends {location}",
            f"{target_market} consumer behavior and preferences",
            f"{industry} market opportunities and challenges"
        ]
        
        search_results = []
        for query in search_queries[:2]:  # Limit searches
            try:
                results = await tavily_search(query, max_results=3)
                search_results.extend(results)
            except Exception as e:
                print(f"Search failed for {query}: {e}")
        
        # Create market insights context from search results
        market_insights = "\n".join([
            f"- {r.get('title', '')}: {r.get('content', '')[:200]}"
            for r in search_results[:5]
        ])
        
        prompt = f"""Create a detailed market analysis for this business:

Business Idea: {business_idea}
Industry: {industry}
Target Market: {target_market}
Location: {location}

Market Research Insights:
{market_insights if market_insights else "No specific data available - use industry knowledge"}

Return ONLY a valid JSON object with this exact structure:
{{
    "market_size": {{
        "total_addressable_market": "TAM estimate with currency",
        "serviceable_addressable_market": "SAM estimate",
        "serviceable_obtainable_market": "SOM estimate",
        "growth_rate": "Annual growth rate",
        "market_maturity": "Emerging/Growing/Mature"
    }},
    "market_trends": [
        {{
            "trend": "Trend name",
            "description": "What's happening",
            "impact": "Impact on your business",
            "opportunity_level": "High/Medium/Low"
        }}
    ],
    "customer_insights": {{
        "demographics": ["demographic1", "demographic2"],
        "psychographics": ["psychographic1", "psychographic2"],
        "pain_points": ["pain1", "pain2"],
        "buying_behavior": ["behavior1", "behavior2"],
        "spending_capacity": "Estimate with reasoning"
    }},
    "market_entry_barriers": [
        {{
            "barrier": "Barrier type",
            "severity": "High/Medium/Low",
            "mitigation": "How to overcome"
        }}
    ],
    "regulatory_considerations": [
        {{
            "area": "Regulatory area",
            "requirements": ["req1", "req2"],
            "compliance_cost": "Estimated cost",
            "timeline": "Time to comply"
        }}
    ],
    "market_opportunities": [
        {{
            "opportunity": "Opportunity description",
            "potential": "High/Medium/Low",
            "timeframe": "Short/Medium/Long term",
            "action_required": "What to do"
        }}
    ]
}}"""

        response = self.llm.invoke([
            SystemMessage(content="You are a market research expert. Always respond with valid JSON only."),
            HumanMessage(content=prompt)
        ])
        
        return self._parse_json_response(response.content, self._fallback_market_analysis())
    
    async def _generate_competitive_analysis(
        self, 
        business_idea: str, 
        industry: str,
        location: str
    ) -> dict:
        """Generate competitive landscape analysis."""
        
        prompt = f"""Create a detailed competitive analysis for this startup:

Business Idea: {business_idea}
Industry: {industry}
Location: {location}

Return ONLY a valid JSON object with this exact structure:
{{
    "competitive_landscape": {{
        "market_position": "Where you fit in the market",
        "competition_level": "High/Medium/Low",
        "market_saturation": "Saturated/Moderate/Unsaturated",
        "differentiation_opportunities": ["opportunity1", "opportunity2"]
    }},
    "competitor_categories": [
        {{
            "category": "Direct/Indirect/Substitute",
            "description": "Type of competition",
            "threat_level": "High/Medium/Low",
            "examples": ["competitor1", "competitor2"]
        }}
    ],
    "competitive_advantages": [
        {{
            "advantage": "Your unique strength",
            "description": "Why it matters",
            "sustainability": "How long can you maintain it",
            "impact": "High/Medium/Low"
        }}
    ],
    "competitive_disadvantages": [
        {{
            "disadvantage": "Your weakness",
            "impact": "How it affects you",
            "mitigation_strategy": "How to address it"
        }}
    ],
    "swot_analysis": {{
        "strengths": ["strength1", "strength2", "strength3"],
        "weaknesses": ["weakness1", "weakness2", "weakness3"],
        "opportunities": ["opportunity1", "opportunity2", "opportunity3"],
        "threats": ["threat1", "threat2", "threat3"]
    }},
    "competitive_strategy": {{
        "positioning": "How to position in market",
        "differentiation": "Key differentiators",
        "pricing_strategy": "Pricing approach vs competitors",
        "marketing_angle": "Unique marketing message"
    }}
}}"""

        response = self.llm.invoke([
            SystemMessage(content="You are a competitive strategy expert. Always respond with valid JSON only."),
            HumanMessage(content=prompt)
        ])
        
        return self._parse_json_response(response.content, self._fallback_competitive_analysis())
    
    async def _generate_financial_projections(
        self, 
        business_idea: str, 
        business_model: str,
        funding_needed: str
    ) -> dict:
        """Generate financial projections."""
        
        prompt = f"""Create detailed financial projections for this startup:

Business Idea: {business_idea}
Business Model: {business_model}
Initial Funding: {funding_needed}

Return ONLY a valid JSON object with this exact structure:
{{
    "startup_costs": [
        {{
            "category": "Cost category",
            "items": ["item1", "item2"],
            "estimated_cost": "Amount",
            "timing": "When needed"
        }}
    ],
    "monthly_operating_costs": [
        {{
            "category": "Category name",
            "cost": "Monthly amount",
            "type": "Fixed/Variable",
            "notes": "Additional details"
        }}
    ],
    "revenue_projections": [
        {{
            "year": 1,
            "revenue": "Amount",
            "customers": "Number",
            "avg_customer_value": "Amount",
            "growth_rate": "Percentage",
            "assumptions": ["assumption1", "assumption2"]
        }},
        {{
            "year": 2,
            "revenue": "Amount",
            "customers": "Number",
            "avg_customer_value": "Amount",
            "growth_rate": "Percentage",
            "assumptions": ["assumption1", "assumption2"]
        }},
        {{
            "year": 3,
            "revenue": "Amount",
            "customers": "Number",
            "avg_customer_value": "Amount",
            "growth_rate": "Percentage",
            "assumptions": ["assumption1", "assumption2"]
        }}
    ],
    "profitability_timeline": {{
        "break_even_point": "When to reach break-even",
        "path_to_profitability": "Steps to profitability",
        "key_milestones": ["milestone1", "milestone2"],
        "risk_factors": ["risk1", "risk2"]
    }},
    "key_metrics": [
        {{
            "metric": "Metric name (CAC, LTV, etc)",
            "description": "What it measures",
            "target": "Target value",
            "importance": "Why it matters"
        }}
    ],
    "funding_utilization": [
        {{
            "category": "Use of funds",
            "percentage": "% of funding",
            "amount": "Dollar amount",
            "impact": "Expected outcome"
        }}
    ]
}}"""

        response = self.llm.invoke([
            SystemMessage(content="You are a financial planning expert. Always respond with valid JSON only."),
            HumanMessage(content=prompt)
        ])
        
        return self._parse_json_response(response.content, self._fallback_financial_projections())
    
    async def _generate_go_to_market_strategy(
        self, 
        business_idea: str, 
        target_market: str,
        business_model: str
    ) -> dict:
        """Generate go-to-market strategy."""
        
        prompt = f"""Create a comprehensive go-to-market strategy for this startup:

Business Idea: {business_idea}
Target Market: {target_market}
Business Model: {business_model}

Return ONLY a valid JSON object with this exact structure:
{{
    "launch_strategy": {{
        "launch_approach": "Type of launch (Soft/Beta/Full)",
        "timeline": "Launch timeline",
        "initial_markets": ["market1", "market2"],
        "success_criteria": ["criteria1", "criteria2"]
    }},
    "marketing_channels": [
        {{
            "channel": "Marketing channel",
            "priority": "High/Medium/Low",
            "tactics": ["tactic1", "tactic2"],
            "expected_roi": "Estimated return",
            "budget_allocation": "% of marketing budget"
        }}
    ],
    "sales_strategy": {{
        "sales_model": "Direct/Channel/Hybrid",
        "sales_process": ["step1", "step2"],
        "team_structure": "Sales team composition",
        "tools_needed": ["tool1", "tool2"],
        "targets": "Sales targets and quotas"
    }},
    "customer_acquisition": [
        {{
            "phase": "Acquisition phase",
            "strategy": "How to acquire customers",
            "tactics": ["tactic1", "tactic2"],
            "expected_cac": "Customer acquisition cost",
            "timeline": "Duration"
        }}
    ],
    "brand_positioning": {{
        "brand_promise": "What brand stands for",
        "messaging": "Core marketing message",
        "visual_identity": "Brand look and feel",
        "tone_of_voice": "Communication style"
    }},
    "growth_tactics": [
        {{
            "tactic": "Growth tactic",
            "description": "How it works",
            "implementation": "Steps to implement",
            "expected_impact": "Projected results"
        }}
    ],
    "partnerships": [
        {{
            "partner_type": "Type of partner",
            "value": "What they bring",
            "approach": "How to engage them",
            "timeline": "When to establish"
        }}
    ]
}}"""

        response = self.llm.invoke([
            SystemMessage(content="You are a go-to-market strategy expert. Always respond with valid JSON only."),
            HumanMessage(content=prompt)
        ])
        
        return self._parse_json_response(response.content, self._fallback_go_to_market())
    
    def _generate_next_steps(self, business_idea: str, funding_needed: str) -> list:
        """Generate actionable next steps."""
        
        return [
            {
                "step": 1,
                "action": "Validate Business Idea",
                "tasks": [
                    "Conduct customer interviews (20-30 potential customers)",
                    "Create and test MVP or prototype",
                    "Gather feedback and iterate on value proposition",
                    "Validate pricing and willingness to pay"
                ],
                "timeline": "4-6 weeks",
                "priority": "Critical"
            },
            {
                "step": 2,
                "action": "Legal and Administrative Setup",
                "tasks": [
                    "Choose business structure (LLC, C-Corp, etc)",
                    "Register business and get EIN",
                    "Open business bank account",
                    "Set up accounting system",
                    "Draft founder agreements if applicable"
                ],
                "timeline": "2-3 weeks",
                "priority": "High"
            },
            {
                "step": 3,
                "action": "Build Minimum Viable Product",
                "tasks": [
                    "Define core features for MVP",
                    "Hire or partner with technical team if needed",
                    "Develop and test MVP",
                    "Set up analytics and tracking"
                ],
                "timeline": "8-12 weeks",
                "priority": "Critical"
            },
            {
                "step": 4,
                "action": "Develop Brand and Marketing Assets",
                "tasks": [
                    "Create brand identity (logo, colors, guidelines)",
                    "Build website and social media presence",
                    "Develop marketing materials",
                    "Create content strategy and initial content"
                ],
                "timeline": "4-6 weeks",
                "priority": "High"
            },
            {
                "step": 5,
                "action": "Launch and Acquire First Customers",
                "tasks": [
                    "Execute soft launch with beta users",
                    "Implement customer feedback",
                    "Start paid marketing campaigns",
                    "Track key metrics (CAC, retention, satisfaction)"
                ],
                "timeline": "6-8 weeks",
                "priority": "Critical"
            },
            {
                "step": 6,
                "action": "Secure Funding (if needed)",
                "tasks": [
                    "Prepare pitch deck and financial model",
                    "Build investor list and start networking",
                    "Conduct investor meetings",
                    "Negotiate and close funding round"
                ],
                "timeline": "12-16 weeks",
                "priority": "High" if funding_needed.lower() not in ["none", "self-funded", "bootstrapped"] else "Medium"
            }
        ]
    
    def _parse_json_response(self, content: str, fallback: dict) -> dict:
        """Parse JSON response with fallback."""
        try:
            content = content.strip()
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
                content = content.strip()
            return json.loads(content)
        except Exception as e:
            print(f"Failed to parse JSON: {e}")
            return fallback
    
    # Fallback methods for each component
    def _fallback_business_model_canvas(self) -> dict:
        return {
            "value_propositions": [{"title": "Core Value", "description": "Main value proposition", "benefits": ["Benefit 1", "Benefit 2"]}],
            "customer_segments": [{"segment": "Primary Segment", "description": "Target customers", "size": "To be determined", "characteristics": ["Characteristic 1"]}],
            "channels": [{"channel": "Direct", "type": "Direct", "purpose": "Customer acquisition", "cost": "Medium"}],
            "customer_relationships": [{"type": "Personal", "description": "Direct support", "examples": ["Email", "Phone"]}],
            "revenue_streams": [{"stream": "Primary Revenue", "type": "Recurring", "pricing_model": "Subscription", "potential": "High"}],
            "key_resources": [{"category": "Human", "resources": ["Team"], "importance": "Critical"}],
            "key_activities": [{"activity": "Product Development", "description": "Build and improve product", "frequency": "Daily"}],
            "key_partnerships": [{"partner_type": "Technology", "examples": ["Vendors"], "value": "Cost reduction"}],
            "cost_structure": [{"category": "Operations", "items": ["Labor", "Infrastructure"], "type": "Fixed", "priority": "High"}]
        }
    
    def _fallback_funding_strategy(self) -> dict:
        return {
            "funding_stages": [{"stage": "Seed", "timing": "Year 1", "amount": "$500K", "purpose": "MVP Development", "milestones": ["Launch MVP"], "valuation_range": "$2-5M"}],
            "funding_sources": [{"source": "Angel Investors", "description": "Individual investors", "pros": ["Quick decisions"], "cons": ["Smaller amounts"], "best_for": "Early stage", "typical_amount": "$25K-$100K"}],
            "pitch_deck_outline": [{"slide": "Problem", "content": "Problem being solved", "tips": ["Be specific"]}],
            "investor_targeting": {"ideal_investor_profile": ["Industry experience"], "investor_types": ["Angels"], "networking_strategies": ["Events"], "key_metrics_to_show": ["Growth"]},
            "funding_timeline": [{"phase": "Preparation", "duration": "4 weeks", "activities": ["Build deck"], "outcomes": "Ready to pitch"}],
            "alternative_funding": [{"option": "Bootstrapping", "description": "Self-funding", "suitability": "If profitable early"}]
        }
    
    def _fallback_market_analysis(self) -> dict:
        return {
            "market_size": {"total_addressable_market": "To be determined", "serviceable_addressable_market": "To be determined", "serviceable_obtainable_market": "To be determined", "growth_rate": "To be determined", "market_maturity": "Growing"},
            "market_trends": [{"trend": "Digital Transformation", "description": "Industry digitization", "impact": "Positive", "opportunity_level": "High"}],
            "customer_insights": {"demographics": ["To be determined"], "psychographics": ["To be determined"], "pain_points": ["To be determined"], "buying_behavior": ["To be determined"], "spending_capacity": "To be determined"},
            "market_entry_barriers": [{"barrier": "Competition", "severity": "Medium", "mitigation": "Differentiation"}],
            "regulatory_considerations": [{"area": "General", "requirements": ["Business license"], "compliance_cost": "Low", "timeline": "2-4 weeks"}],
            "market_opportunities": [{"opportunity": "Market gap", "potential": "High", "timeframe": "Medium term", "action_required": "Market research"}]
        }
    
    def _fallback_competitive_analysis(self) -> dict:
        return {
            "competitive_landscape": {"market_position": "New entrant", "competition_level": "Medium", "market_saturation": "Moderate", "differentiation_opportunities": ["Innovation"]},
            "competitor_categories": [{"category": "Direct", "description": "Direct competitors", "threat_level": "Medium", "examples": ["Competitor 1"]}],
            "competitive_advantages": [{"advantage": "Innovation", "description": "Unique approach", "sustainability": "Medium term", "impact": "High"}],
            "competitive_disadvantages": [{"disadvantage": "Brand recognition", "impact": "Medium", "mitigation_strategy": "Marketing"}],
            "swot_analysis": {"strengths": ["Innovation"], "weaknesses": ["Resources"], "opportunities": ["Market growth"], "threats": ["Competition"]},
            "competitive_strategy": {"positioning": "Premium", "differentiation": "Quality", "pricing_strategy": "Value-based", "marketing_angle": "Innovation"}
        }
    
    def _fallback_financial_projections(self) -> dict:
        return {
            "startup_costs": [{"category": "Setup", "items": ["Legal", "Branding"], "estimated_cost": "$10,000", "timing": "Month 1"}],
            "monthly_operating_costs": [{"category": "Operations", "cost": "$5,000", "type": "Fixed", "notes": "Basic operations"}],
            "revenue_projections": [
                {"year": 1, "revenue": "$100,000", "customers": "100", "avg_customer_value": "$1,000", "growth_rate": "N/A", "assumptions": ["Conservative estimate"]},
                {"year": 2, "revenue": "$300,000", "customers": "250", "avg_customer_value": "$1,200", "growth_rate": "200%", "assumptions": ["Market expansion"]},
                {"year": 3, "revenue": "$750,000", "customers": "500", "avg_customer_value": "$1,500", "growth_rate": "150%", "assumptions": ["Established brand"]}
            ],
            "profitability_timeline": {"break_even_point": "Month 18", "path_to_profitability": "Scale operations", "key_milestones": ["100 customers"], "risk_factors": ["Market adoption"]},
            "key_metrics": [{"metric": "CAC", "description": "Customer Acquisition Cost", "target": "$500", "importance": "Measure efficiency"}],
            "funding_utilization": [{"category": "Product", "percentage": "40%", "amount": "To be determined", "impact": "MVP launch"}]
        }
    
    def _fallback_go_to_market(self) -> dict:
        return {
            "launch_strategy": {"launch_approach": "Beta Launch", "timeline": "3 months", "initial_markets": ["Primary market"], "success_criteria": ["50 users"]},
            "marketing_channels": [{"channel": "Digital Marketing", "priority": "High", "tactics": ["Social media", "SEO"], "expected_roi": "200%", "budget_allocation": "40%"}],
            "sales_strategy": {"sales_model": "Direct", "sales_process": ["Lead gen", "Demo", "Close"], "team_structure": "Founder-led", "tools_needed": ["CRM"], "targets": "10 customers/month"},
            "customer_acquisition": [{"phase": "Early Adopters", "strategy": "Direct outreach", "tactics": ["Email", "LinkedIn"], "expected_cac": "$500", "timeline": "3 months"}],
            "brand_positioning": {"brand_promise": "Quality and innovation", "messaging": "Transform your business", "visual_identity": "Modern and professional", "tone_of_voice": "Confident and helpful"},
            "growth_tactics": [{"tactic": "Content Marketing", "description": "Educational content", "implementation": "Blog and social", "expected_impact": "30% traffic growth"}],
            "partnerships": [{"partner_type": "Strategic", "value": "Market access", "approach": "Direct outreach", "timeline": "Month 2-3"}]
        }


# Main function to create business plan
async def create_business_plan(
    business_idea: str,
    industry: str,
    target_market: str,
    business_model: str,
    funding_needed: str,
    location: str
) -> dict:
    """Main function to create a comprehensive business plan."""
    agent = BusinessPlannerAgent()
    return await agent.create_business_plan(
        business_idea=business_idea,
        industry=industry,
        target_market=target_market,
        business_model=business_model,
        funding_needed=funding_needed,
        location=location
    )
