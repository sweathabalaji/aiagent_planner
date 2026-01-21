"""Learning Planner Routes"""
from fastapi import HTTPException
from pydantic import BaseModel, Field
from typing import Literal, List, Optional
from . import router
from agents.learning_planner import create_learning_path, LearningPathAgent
from memory.db import get_db
from memory.learning_path_db import (
    save_learning_path,
    get_learning_path,
    update_todo_status,
    save_assessment,
    save_assessment_results,
    save_certificate,
    get_all_learning_paths,
    get_learning_paths_by_topic,
    delete_learning_path,
    get_user_statistics
)
from datetime import datetime


# Store learning sessions in memory for backward compatibility
# New data will be stored in MongoDB
learning_sessions = {}


class LearningRequest(BaseModel):
    """Learning path request model"""
    topic: str = Field(..., description="Subject to learn (e.g., 'Python Programming', 'Machine Learning')")
    skill_level: Literal["Beginner", "Intermediate", "Advanced"] = Field(..., description="Current skill level")
    duration_weeks: int = Field(..., ge=1, le=52, description="Learning duration in weeks (1-52)")
    learning_goals: str = Field(..., description="Specific learning objectives")
    time_per_week: int = Field(..., ge=1, le=168, description="Available study hours per week (1-168)")


class LearningResponse(BaseModel):
    """Learning path response model"""
    success: bool
    learning_path: dict


@router.post("/plan", response_model=LearningResponse)
async def plan_learning(request: LearningRequest):
    """
    Generate a comprehensive learning path with real resources.
    
    Creates a personalized study plan including:
    - Structured learning phases
    - Real course and book recommendations
    - Week-by-week study schedule
    - Progress tracking system
    - Assessment milestones
    """
    try:
        # Generate learning path using AI agent
        learning_path = await create_learning_path(
            topic=request.topic,
            skill_level=request.skill_level,
            duration_weeks=request.duration_weeks,
            learning_goals=request.learning_goals,
            time_per_week=request.time_per_week
        )
        
        # Save to database
        try:
            db_id = await save_learning_path(learning_path)
            learning_path["db_id"] = db_id
            learning_path["session_id"] = db_id  # Use db_id as session_id
        except Exception as db_error:
            # If database save fails, use memory fallback
            print(f"Database save failed, using memory: {db_error}")
            session_id = f"session_{datetime.now().timestamp()}"
            learning_sessions[session_id] = {
                "learning_path": learning_path,
                "created_at": datetime.now().isoformat()
            }
            learning_path["session_id"] = session_id
        
        return LearningResponse(
            success=True,
            learning_path=learning_path
        )
        
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(ve)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate learning path: {str(e)}")


class TodoUpdateRequest(BaseModel):
    """Todo item update request"""
    session_id: str
    todo_id: int
    completed: bool


@router.post("/update-todo")
async def update_todo(request: TodoUpdateRequest):
    """Update a todo item's completion status"""
    try:
        # Try database first
        session_data = None
        try:
            session_data = await get_learning_path(request.session_id)
        except:
            pass
        
        # Fallback to memory
        if not session_data and request.session_id in learning_sessions:
            session = learning_sessions[request.session_id]
            todo_list = session["learning_path"]["todo_list"]
            
            # Find and update the todo item
            updated = False
            for item in todo_list["items"]:
                if item["id"] == request.todo_id:
                    item["completed"] = request.completed
                    updated = True
                    break
            
            if not updated:
                raise HTTPException(status_code=404, detail="Todo item not found")
            
            # Update completed count
            todo_list["completed_count"] = sum(1 for item in todo_list["items"] if item["completed"])
            all_completed = todo_list["completed_count"] == todo_list["total_count"]
            
            return {
                "success": True,
                "completed_count": todo_list["completed_count"],
                "total_count": todo_list["total_count"],
                "all_completed": all_completed
            }
        
        # Use database
        if session_data:
            success = await update_todo_status(request.session_id, request.todo_id, request.completed)
            
            if not success:
                raise HTTPException(status_code=404, detail="Todo item not found")
            
            # Get updated data
            updated_data = await get_learning_path(request.session_id)
            todo_list = updated_data["todo_list"]
            all_completed = todo_list["completed_count"] == todo_list["total_count"]
            
            return {
                "success": True,
                "completed_count": todo_list["completed_count"],
                "total_count": todo_list["total_count"],
                "all_completed": all_completed
            }
        
        raise HTTPException(status_code=404, detail="Session not found")
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update todo: {str(e)}")


class AssessmentRequest(BaseModel):
    """MCQ Assessment generation request"""
    session_id: str


@router.post("/generate-assessment")
async def generate_assessment(request: AssessmentRequest):
    """Generate MCQ assessment based on completed learning"""
    try:
        # Try database first
        session_data = None
        try:
            session_data = await get_learning_path(request.session_id)
        except:
            pass
        
        # Fallback to memory
        if not session_data and request.session_id in learning_sessions:
            session = learning_sessions[request.session_id]
            learning_path = session["learning_path"]
        elif session_data:
            learning_path = session_data
        else:
            raise HTTPException(status_code=404, detail="Session not found")
        
        # Check if all todos are completed
        todo_list = learning_path["todo_list"]
        incomplete_todos = [item["title"] for item in todo_list["items"] if not item["completed"]]
        
        if todo_list["completed_count"] < todo_list["total_count"]:
            print(f"Incomplete todos found: {incomplete_todos}")
            raise HTTPException(
                status_code=400, 
                detail=f"Please complete all todos first. {todo_list['completed_count']}/{todo_list['total_count']} completed. Incomplete: {', '.join(incomplete_todos[:3])}"
            )
        
        # Generate MCQ assessment
        agent = LearningPathAgent()
        completed_topics = [item["title"] for item in todo_list["items"] if item["completed"]]
        assessment = agent.generate_mcq_assessment(learning_path["learning_plan"], completed_topics)
        
        # Save to database
        try:
            await save_assessment(request.session_id, assessment)
        except:
            # Fallback to memory
            if request.session_id in learning_sessions:
                learning_sessions[request.session_id]["assessment"] = assessment
        
        return {
            "success": True,
            "assessment": assessment
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate assessment: {str(e)}")


class AssessmentSubmission(BaseModel):
    """Assessment submission with user answers"""
    session_id: str
    answers: dict  # question_id -> selected_option_id


@router.post("/submit-assessment")
async def submit_assessment(request: AssessmentSubmission):
    """Score the assessment and determine if user passes"""
    try:
        # Try database first
        session_data = None
        assessment = None
        
        try:
            session_data = await get_learning_path(request.session_id)
            assessment = session_data.get("assessment")
        except:
            pass
        
        # Fallback to memory
        if not session_data and request.session_id in learning_sessions:
            session = learning_sessions[request.session_id]
            if "assessment" not in session:
                raise HTTPException(status_code=400, detail="No assessment found. Generate assessment first")
            assessment = session["assessment"]
        elif not assessment:
            raise HTTPException(status_code=400, detail="No assessment found. Generate assessment first")
        
        questions = assessment["questions"]
        
        # Score the assessment
        correct_count = 0
        total_questions = len(questions)
        results = []
        
        for question in questions:
            q_id = str(question["id"])
            user_answer = request.answers.get(q_id, "")
            correct_answer = question["correct_answer"]
            is_correct = user_answer == correct_answer
            
            if is_correct:
                correct_count += 1
            
            results.append({
                "question_id": question["id"],
                "question": question["question"],
                "user_answer": user_answer,
                "correct_answer": correct_answer,
                "is_correct": is_correct,
                "explanation": question.get("explanation", "")
            })
        
        score = (correct_count / total_questions * 100) if total_questions > 0 else 0
        passing_score = assessment.get("passing_score", 70)
        passed = score >= passing_score
        
        assessment_results = {
            "score": score,
            "correct_count": correct_count,
            "total_questions": total_questions,
            "passed": passed,
            "results": results,
            "submitted_at": datetime.now().isoformat()
        }
        
        # Save to database
        try:
            await save_assessment_results(request.session_id, assessment_results)
        except:
            # Fallback to memory
            if request.session_id in learning_sessions:
                learning_sessions[request.session_id]["assessment_results"] = assessment_results
        
        return {
            "success": True,
            "score": score,
            "correct_count": correct_count,
            "total_questions": total_questions,
            "passed": passed,
            "passing_score": passing_score,
            "results": results
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to submit assessment: {str(e)}")


class CertificateRequest(BaseModel):
    """Certificate generation request"""
    session_id: str
    user_name: str


@router.post("/generate-certificate")
async def generate_certificate(request: CertificateRequest):
    """Generate completion certificate after passing assessment"""
    try:
        # Try database first
        session_data = None
        assessment_results = None
        
        try:
            session_data = await get_learning_path(request.session_id)
            assessment_results = session_data.get("latest_assessment_result")
        except:
            pass
        
        # Fallback to memory
        if not session_data and request.session_id in learning_sessions:
            session = learning_sessions[request.session_id]
            if "assessment_results" not in session:
                raise HTTPException(status_code=400, detail="No assessment results found. Complete assessment first")
            assessment_results = session["assessment_results"]
            learning_path = session["learning_path"]
        elif session_data:
            learning_path = session_data
        else:
            raise HTTPException(status_code=404, detail="Session not found")
        
        if not assessment_results:
            raise HTTPException(status_code=400, detail="No assessment results found. Complete assessment first")
        
        if not assessment_results["passed"]:
            raise HTTPException(
                status_code=400, 
                detail=f"Assessment not passed. Score: {assessment_results['score']}%. Need 70% or higher"
            )
        
        # Generate certificate
        agent = LearningPathAgent()
        certificate = agent.generate_certificate(
            request.user_name,
            learning_path["learning_plan"],
            assessment_results["score"]
        )
        
        # Save to database
        try:
            await save_certificate(request.session_id, certificate)
        except:
            # Fallback to memory
            if request.session_id in learning_sessions:
                learning_sessions[request.session_id]["certificate"] = certificate
        
        return {
            "success": True,
            "certificate": certificate
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate certificate: {str(e)}")


@router.get("/session/{session_id}")
async def get_session(session_id: str):
    """Get learning session data"""
    # Try database first
    try:
        session_data = await get_learning_path(session_id)
        if session_data:
            return {
                "success": True,
                "session": session_data
            }
    except:
        pass
    
    # Fallback to memory
    if session_id in learning_sessions:
        return {
            "success": True,
            "session": learning_sessions[session_id]
        }
    
    raise HTTPException(status_code=404, detail="Session not found")


@router.get("/paths")
async def get_paths(limit: int = 50, skip: int = 0):
    """Get all learning paths with pagination"""
    try:
        paths = await get_all_learning_paths(limit=limit, skip=skip)
        return {
            "success": True,
            "paths": paths,
            "count": len(paths)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve learning paths: {str(e)}")


@router.get("/paths/topic/{topic}")
async def get_paths_by_topic(topic: str, limit: int = 20):
    """Get learning paths by topic"""
    try:
        paths = await get_learning_paths_by_topic(topic, limit=limit)
        return {
            "success": True,
            "paths": paths,
            "count": len(paths),
            "topic": topic
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve learning paths: {str(e)}")


@router.delete("/path/{path_id}")
async def delete_path(path_id: str):
    """Delete (archive) a learning path"""
    try:
        success = await delete_learning_path(path_id)
        if success:
            return {
                "success": True,
                "message": "Learning path archived successfully"
            }
        else:
            raise HTTPException(status_code=404, detail="Learning path not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete learning path: {str(e)}")


@router.get("/statistics")
async def get_statistics():
    """Get learning path statistics"""
    try:
        stats = await get_user_statistics()
        return {
            "success": True,
            "statistics": stats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve statistics: {str(e)}")


@router.post("/sync-todos")
async def sync_todos(request: AssessmentRequest):
    """Force sync all todos to completed status (for fixing stale data)"""
    try:
        session_data = await get_learning_path(request.session_id)
        if not session_data:
            raise HTTPException(status_code=404, detail="Session not found")
        
        # Mark all todos as completed
        todo_list = session_data["todo_list"]
        for item in todo_list["items"]:
            item["completed"] = True
        
        todo_list["completed_count"] = todo_list["total_count"]
        
        # Update in database
        from memory.learning_path_db import get_db_session
        from memory.models import LearningPath
        from sqlalchemy.orm.attributes import flag_modified
        
        db = get_db_session()
        try:
            learning_path = db.query(LearningPath).filter(
                LearningPath.session_id == request.session_id
            ).first()
            
            if learning_path:
                learning_path.todo_list = todo_list
                flag_modified(learning_path, 'todo_list')
                learning_path.updated_at = datetime.now()
                db.commit()
                db.refresh(learning_path)
                
                return {
                    "success": True,
                    "message": "All todos marked as completed",
                    "completed_count": todo_list["completed_count"],
                    "total_count": todo_list["total_count"]
                }
        finally:
            db.close()
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to sync todos: {str(e)}")


@router.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "service": "learning_planner"}
