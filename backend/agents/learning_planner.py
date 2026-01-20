"""
Learning Path Planner Agent
Creates personalized study plans with real resource recommendations using Moonshot AI and Tavily search.
"""

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import Tool
from langchain_core.prompts import PromptTemplate
from utils.llm import get_chat_llm
from utils.tavily_search import search_learning_resources
import json
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List


class LearningPathAgent:
    """Agent for creating comprehensive learning paths with real resources."""
    
    def __init__(self):
        self.llm = get_chat_llm()
        
    async def create_learning_plan(self, topic: str, skill_level: str, duration_weeks: int, 
                            learning_goals: str, time_per_week: int) -> dict:
        """
        Create a comprehensive learning plan with real resources.
        
        Args:
            topic: Subject to learn (e.g., "Python Programming", "Machine Learning")
            skill_level: Current level (Beginner, Intermediate, Advanced)
            duration_weeks: How many weeks to complete
            learning_goals: Specific goals (e.g., "Build web applications")
            time_per_week: Available hours per week
        """
        
        # Step 1: Generate structured learning plan
        plan_prompt = f"""You are an expert learning path designer. Create a detailed, structured learning plan.

Topic: {topic}
Current Level: {skill_level}
Duration: {duration_weeks} weeks
Time Available: {time_per_week} hours/week
Learning Goals: {learning_goals}

Create a comprehensive learning plan with:
1. Learning phases (break duration into logical phases)
2. Key concepts to master in each phase
3. Practical projects to build
4. Skills assessment milestones
5. Prerequisites and foundational concepts

Return ONLY a valid JSON object with this structure:
{{
    "overview": {{
        "title": "Learning path title",
        "description": "Brief overview",
        "total_hours": estimated total hours,
        "difficulty_progression": "How difficulty increases"
    }},
    "phases": [
        {{
            "phase_number": 1,
            "phase_name": "Phase name",
            "duration_weeks": weeks for this phase,
            "concepts": ["concept1", "concept2"],
            "skills": ["skill1", "skill2"],
            "project": "Practical project description",
            "assessment": "How to evaluate progress"
        }}
    ],
    "prerequisites": ["prereq1", "prereq2"],
    "final_project": "Capstone project description",
    "success_criteria": ["criteria1", "criteria2"]
}}"""

        plan_response = self.llm.invoke([
            SystemMessage(content="You are a learning path expert. Always respond with valid JSON only."),
            HumanMessage(content=plan_prompt)
        ])
        
        try:
            # Try to parse JSON response
            content = plan_response.content.strip()
            # Remove markdown code blocks if present
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
                content = content.strip()
            learning_plan = json.loads(content)
        except Exception as e:
            print(f"Failed to parse learning plan JSON: {e}")
            # Fallback structure if JSON parsing fails - create proper phases
            weeks_per_phase = max(2, duration_weeks // 3)
            phases = []
            
            if skill_level == "Beginner":
                phases = [
                    {
                        "phase_number": 1,
                        "phase_name": "Fundamentals & Basics",
                        "duration_weeks": weeks_per_phase,
                        "concepts": [f"Basic {topic} syntax", "Core concepts", "Development environment"],
                        "skills": ["Write simple programs", "Debug basic errors", "Use documentation"],
                        "project": f"Build a simple {topic} application",
                        "assessment": "Can write and debug basic code independently"
                    },
                    {
                        "phase_number": 2,
                        "phase_name": "Intermediate Concepts",
                        "duration_weeks": weeks_per_phase,
                        "concepts": ["Data structures", "Algorithms", "Best practices"],
                        "skills": ["Design solutions", "Optimize code", "Write tests"],
                        "project": f"Create a functional {topic} project",
                        "assessment": "Can build complete features independently"
                    },
                    {
                        "phase_number": 3,
                        "phase_name": "Advanced Application",
                        "duration_weeks": duration_weeks - (2 * weeks_per_phase),
                        "concepts": ["Advanced patterns", "Real-world practices", "Production code"],
                        "skills": ["Build scalable solutions", "Handle complex problems", "Deploy applications"],
                        "project": f"Complete production-ready {topic} application",
                        "assessment": "Can independently build and deploy projects"
                    }
                ]
            else:
                phases = [
                    {
                        "phase_number": 1,
                        "phase_name": f"Advanced {topic}",
                        "duration_weeks": duration_weeks,
                        "concepts": ["Advanced techniques", "Best practices", "Industry standards"],
                        "skills": ["Expert-level implementation", "Architecture design", "Performance optimization"],
                        "project": f"Build advanced {topic} solution",
                        "assessment": "Master-level competency"
                    }
                ]
            
            learning_plan = {
                "overview": {
                    "title": f"{topic} Learning Path ({skill_level})",
                    "description": f"Comprehensive {duration_weeks}-week learning plan to {learning_goals}",
                    "total_hours": duration_weeks * time_per_week,
                    "difficulty_progression": f"{skill_level} to Advanced with hands-on projects"
                },
                "phases": phases,
                "prerequisites": ["Basic computer skills", "Problem-solving mindset"],
                "final_project": f"Complete {learning_goals} using {topic}",
                "success_criteria": ["Complete all phases", "Build portfolio projects", "Master core concepts"]
            }
        
        # Step 2: Search for real learning resources
        resources = await self._find_learning_resources_async(topic, skill_level, learning_plan)
        
        # Step 3: Create study schedule
        schedule = self._create_study_schedule(learning_plan, duration_weeks, time_per_week)
        
        # Step 4: Generate progress tracking plan
        tracking = self._create_progress_tracking(learning_plan, duration_weeks)
        
        return {
            "learning_plan": learning_plan,
            "resources": resources,
            "schedule": schedule,
            "progress_tracking": tracking,
            "metadata": {
                "created_at": datetime.now().isoformat(),
                "topic": topic,
                "level": skill_level,
                "duration_weeks": duration_weeks
            }
        }
    
    async def _find_learning_resources_async(self, topic: str, level: str, plan: dict) -> dict:
        """Find real learning resources using Tavily search asynchronously."""
        
        resources = {
            "courses": [],
            "books": [],
            "tutorials": [],
            "practice_platforms": [],
            "communities": [],
            "tools": []
        }
        
        # Search for online courses
        course_query = f"best online courses for {topic} {level} level"
        course_results = await search_learning_resources(course_query, resource_type="courses", max_results=5)
        for result in course_results:
            resources["courses"].append({
                "title": result.get("title", ""),
                "url": result.get("url", ""),
                "description": result.get("content", "")[:200],
                "type": "Online Course"
            })
        
        # Search for books and reading materials
        book_query = f"best books for learning {topic} {level}"
        book_results = await search_learning_resources(book_query, resource_type="books", max_results=4)
        for result in book_results:
            resources["books"].append({
                "title": result.get("title", ""),
                "url": result.get("url", ""),
                "description": result.get("content", "")[:200],
                "type": "Book/Guide"
            })
        
        # Search for tutorials and hands-on content
        tutorial_query = f"{topic} {level} tutorials hands-on projects"
        tutorial_results = await search_learning_resources(tutorial_query, resource_type="tutorials", max_results=5)
        for result in tutorial_results:
            resources["tutorials"].append({
                "title": result.get("title", ""),
                "url": result.get("url", ""),
                "description": result.get("content", "")[:200],
                "type": "Tutorial"
            })
        
        # Search for practice platforms
        practice_query = f"{topic} practice exercises coding challenges"
        practice_results = await search_learning_resources(practice_query, resource_type="practice", max_results=4)
        for result in practice_results:
            resources["practice_platforms"].append({
                "title": result.get("title", ""),
                "url": result.get("url", ""),
                "description": result.get("content", "")[:200],
                "type": "Practice Platform"
            })
        
        # Search for communities and forums
        community_query = f"{topic} community forum discussion group"
        community_results = await search_learning_resources(community_query, resource_type="communities", max_results=3)
        for result in community_results:
            resources["communities"].append({
                "title": result.get("title", ""),
                "url": result.get("url", ""),
                "description": result.get("content", "")[:200],
                "type": "Community"
            })
        
        # Search for tools and software
        tools_query = f"best tools software for {topic}"
        tools_results = await search_learning_resources(tools_query, resource_type="tools", max_results=4)
        for result in tools_results:
            resources["tools"].append({
                "title": result.get("title", ""),
                "url": result.get("url", ""),
                "description": result.get("content", "")[:200],
                "type": "Tool/Software"
            })
        
        # Use AI to analyze and recommend best resources
        resource_analysis = self._analyze_resources(resources, topic, level, plan)
        
        return {
            "all_resources": resources,
            "recommended": resource_analysis
        }
    
    def _analyze_resources(self, resources: dict, topic: str, level: str, plan: dict) -> dict:
        """Use AI to analyze and recommend the best resources."""
        
        analysis_prompt = f"""Analyze these learning resources for {topic} at {level} level.

Available Resources:
{json.dumps(resources, indent=2)[:3000]}

Learning Plan Overview:
{json.dumps(plan.get('overview', {}), indent=2)}

Recommend the top 3 resources from each category that best fit the learning plan.
Consider: relevance, quality indicators in descriptions, and alignment with learning goals.

Return ONLY valid JSON:
{{
    "top_courses": [
        {{"title": "", "url": "", "reason": "Why this is recommended"}}
    ],
    "top_books": [...],
    "top_tutorials": [...],
    "top_practice": [...],
    "study_strategy": "Overall strategy for using these resources"
}}"""

        analysis_response = self.llm.invoke([
            SystemMessage(content="You are a learning resource analyst. Return only valid JSON."),
            HumanMessage(content=analysis_prompt)
        ])
        
        try:
            return json.loads(analysis_response.content)
        except:
            return {
                "top_courses": resources["courses"][:3],
                "top_books": resources["books"][:3],
                "top_tutorials": resources["tutorials"][:3],
                "top_practice": resources["practice_platforms"][:3],
                "study_strategy": f"Combine courses, books, and hands-on practice for comprehensive {topic} mastery."
            }
    
    def _create_study_schedule(self, plan: dict, weeks: int, hours_per_week: int) -> dict:
        """Create a detailed week-by-week study schedule using LangChain agent."""
        
        phases = plan.get("phases", [])
        schedule_prompt = f"""Create a detailed week-by-week study schedule for {weeks} weeks.

Learning Phases:
{json.dumps(phases, indent=2)}

Time Available: {hours_per_week} hours/week

For each week, provide:
- Main focus area from the learning phases
- Specific topics to study
- Time breakdown for activities (reading, practice, projects)
- Milestone to achieve
- Resources to use (courses, documentation, practice)

Return ONLY valid JSON:
{{
    "weekly_schedule": [
        {{
            "week": 1,
            "focus": "Main focus based on phase",
            "topics": ["Specific topic 1", "Specific topic 2"],
            "activities": [
                {{"activity": "Study fundamentals", "hours": 3}},
                {{"activity": "Practice coding", "hours": 4}},
                {{"activity": "Build mini-project", "hours": 3}}
            ],
            "milestone": "Concrete achievement goal",
            "resources_to_use": ["Online course videos", "Practice exercises", "Documentation"]
        }}
    ],
    "daily_routine": {{
        "recommended_pattern": "Best daily study approach",
        "break_strategy": "How to take effective breaks",
        "review_frequency": "How often to review material"
    }}
}}"""

        schedule_response = self.llm.invoke([
            SystemMessage(content="You are a study schedule expert. Return only valid JSON."),
            HumanMessage(content=schedule_prompt)
        ])
        
        try:
            content = schedule_response.content.strip()
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
                content = content.strip()
            schedule = json.loads(content)
        except Exception as e:
            print(f"Failed to parse schedule JSON: {e}")
            # Create intelligent schedule based on phases
            weekly_schedule = []
            week_num = 1
            
            for phase in phases:
                phase_weeks = phase.get("duration_weeks", 2)
                phase_name = phase.get("phase_name", f"Phase {phase.get('phase_number', 1)}")
                concepts = phase.get("concepts", [])
                
                for week_in_phase in range(phase_weeks):
                    # Distribute activities intelligently
                    study_hours = int(hours_per_week * 0.4)
                    practice_hours = int(hours_per_week * 0.4)
                    project_hours = hours_per_week - study_hours - practice_hours
                    
                    weekly_schedule.append({
                        "week": week_num,
                        "focus": f"{phase_name} - Week {week_in_phase + 1}",
                        "topics": concepts[:3] if concepts else [f"Week {week_num} objectives"],
                        "activities": [
                            {"activity": "Learn new concepts", "hours": study_hours},
                            {"activity": "Practice with exercises", "hours": practice_hours},
                            {"activity": "Work on project", "hours": project_hours}
                        ],
                        "milestone": f"Complete {phase_name} fundamentals" if week_in_phase == 0 else f"Master {phase_name} skills",
                        "resources_to_use": ["Online courses", "Tutorial videos", "Practice platforms"]
                    })
                    week_num += 1
                    
                    if week_num > weeks:
                        break
                
                if week_num > weeks:
                    break
            
            schedule = {
                "weekly_schedule": weekly_schedule,
                "daily_routine": {
                    "recommended_pattern": "Study in focused 50-minute blocks with 10-minute breaks (Pomodoro technique)",
                    "break_strategy": "Take short breaks every hour. Walk around, stretch, or do light exercise",
                    "review_frequency": "Review previous week's material every Sunday. Do quick quizzes daily"
                }
            }
        
        # Add calendar dates
        start_date = datetime.now()
        for week_data in schedule["weekly_schedule"]:
            week_num = week_data["week"]
            week_start = start_date + timedelta(weeks=week_num - 1)
            week_end = week_start + timedelta(days=6)
            week_data["date_range"] = f"{week_start.strftime('%b %d')} - {week_end.strftime('%b %d, %Y')}"
        
        return schedule
    
    def _create_progress_tracking(self, plan: dict, weeks: int) -> dict:
        """Create a progress tracking and assessment plan."""
        
        tracking_prompt = f"""Create a progress tracking system for this learning plan.

Plan Overview:
{json.dumps(plan, indent=2)[:2000]}

Duration: {weeks} weeks

Design a system that includes:
1. Skills assessment checklist
2. Knowledge check questions
3. Project milestones
4. Self-evaluation criteria
5. Signs of mastery

Return ONLY valid JSON:
{{
    "skills_checklist": [
        {{"skill": "Skill name", "level": "beginner/intermediate/advanced", "how_to_verify": ""}}
    ],
    "knowledge_checks": [
        {{"phase": 1, "questions": ["Q1", "Q2"], "expected_answers": ["A1", "A2"]}}
    ],
    "project_milestones": [
        {{"milestone": "", "criteria": [""], "estimated_completion": ""}}
    ],
    "self_evaluation": {{
        "weekly_questions": ["Q1", "Q2"],
        "mastery_indicators": ["indicator1", "indicator2"],
        "when_to_slow_down": ["sign1", "sign2"],
        "when_to_accelerate": ["sign1", "sign2"]
    }}
}}"""

        tracking_response = self.llm.invoke([
            SystemMessage(content="You are a learning assessment expert. Return only valid JSON."),
            HumanMessage(content=tracking_prompt)
        ])
        
        try:
            return json.loads(tracking_response.content)
        except:
            return {
                "skills_checklist": [],
                "knowledge_checks": [],
                "project_milestones": [],
                "self_evaluation": {
                    "weekly_questions": [
                        "What did I learn this week?",
                        "What challenges did I face?",
                        "How can I improve next week?"
                    ],
                    "mastery_indicators": [
                        "Can explain concepts to others",
                        "Can build projects independently"
                    ]
                }
            }


async def create_learning_path(topic: str, skill_level: str, duration_weeks: int, 
                        learning_goals: str, time_per_week: int) -> dict:
    """
    Main function to create a learning path.
    
    Args:
        topic: Subject to learn
        skill_level: Current skill level
        duration_weeks: Learning duration in weeks
        learning_goals: Specific learning objectives
        time_per_week: Available study hours per week
    
    Returns:
        Complete learning path with resources and schedule
    """
    agent = LearningPathAgent()
    return await agent.create_learning_plan(topic, skill_level, duration_weeks, learning_goals, time_per_week)
