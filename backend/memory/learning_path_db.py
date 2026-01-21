"""
Database operations for Learning Path Planner
Stores learning paths, todo progress, assessments, and certificates
Using SQLAlchemy with SQLite
"""

import logging
from datetime import datetime
from typing import Optional, List, Dict
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.attributes import flag_modified
from .sqlalchemy_db import get_db_session, close_db_session
from .models import LearningPath

logger = logging.getLogger(__name__)


async def save_learning_path(learning_path_data: dict) -> str:
    """
    Save a complete learning path to the database
    
    Args:
        learning_path_data: Complete learning path data including plan, resources, schedule, etc.
    
    Returns:
        Session ID of the saved learning path
    """
    db = None
    try:
        db = get_db_session()
        
        # Generate session ID
        session_id = learning_path_data.get("session_id", f"session_{datetime.now().timestamp()}")
        
        # Create new learning path record
        learning_path = LearningPath(
            session_id=session_id,
            learning_plan=learning_path_data.get("learning_plan"),
            resources=learning_path_data.get("resources"),
            schedule=learning_path_data.get("schedule"),
            progress_tracking=learning_path_data.get("progress_tracking"),
            todo_list=learning_path_data.get("todo_list"),
            path_metadata=learning_path_data.get("metadata"),
            status="active",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        db.add(learning_path)
        db.commit()
        db.refresh(learning_path)
        
        logger.info(f"Saved learning path with session ID: {session_id}")
        return session_id
        
    except SQLAlchemyError as e:
        if db:
            db.rollback()
        logger.error(f"Failed to save learning path: {e}")
        raise
    finally:
        if db:
            close_db_session(db)


async def get_learning_path(path_id: str) -> Optional[dict]:
    """
    Retrieve a learning path by session ID
    
    Args:
        path_id: Session ID of the learning path
    
    Returns:
        Learning path data or None if not found
    """
    db = None
    try:
        db = get_db_session()
        
        learning_path = db.query(LearningPath).filter(
            LearningPath.session_id == path_id
        ).first()
        
        if learning_path:
            logger.info(f"Retrieved learning path: {path_id}")
            return learning_path.to_dict()
        
        return None
        
    except SQLAlchemyError as e:
        logger.error(f"Failed to retrieve learning path {path_id}: {e}")
        return None
    finally:
        if db:
            close_db_session(db)


async def update_todo_status(path_id: str, todo_id: int, completed: bool) -> bool:
    """
    Update the completion status of a todo item
    
    Args:
        path_id: Session ID of the learning path
        todo_id: ID of the todo item
        completed: New completion status
    
    Returns:
        True if successful, False otherwise
    """
    db = None
    try:
        db = get_db_session()
        
        learning_path = db.query(LearningPath).filter(
            LearningPath.session_id == path_id
        ).first()
        
        if not learning_path:
            return False
        
        # Update the specific todo item
        todo_list = learning_path.todo_list
        if not todo_list or 'items' not in todo_list:
            return False
        
        updated = False
        for item in todo_list['items']:
            if item['id'] == todo_id:
                item['completed'] = completed
                updated = True
                break
        
        if updated:
            # Recalculate completed count
            completed_count = sum(1 for item in todo_list['items'] if item.get('completed', False))
            todo_list['completed_count'] = completed_count
            
            learning_path.todo_list = todo_list
            # Mark the JSON column as modified so SQLAlchemy detects the change
            flag_modified(learning_path, 'todo_list')
            learning_path.updated_at = datetime.now()
            
            db.commit()
            db.refresh(learning_path)
            logger.info(f"Updated todo {todo_id} in learning path {path_id} - {completed_count}/{todo_list['total_count']} completed")
            return True
        
        return False
        
    except SQLAlchemyError as e:
        if db:
            db.rollback()
        logger.error(f"Failed to update todo status: {e}")
        return False
    finally:
        if db:
            close_db_session(db)


async def save_assessment(path_id: str, assessment_data: dict) -> bool:
    """
    Save assessment data to the learning path
    
    Args:
        path_id: Session ID of the learning path
        assessment_data: Assessment questions and metadata
    
    Returns:
        True if successful, False otherwise
    """
    db = None
    try:
        db = get_db_session()
        
        learning_path = db.query(LearningPath).filter(
            LearningPath.session_id == path_id
        ).first()
        
        if not learning_path:
            return False
        
        learning_path.assessment = assessment_data
        learning_path.assessment_generated_at = datetime.now()
        learning_path.updated_at = datetime.now()
        
        db.commit()
        logger.info(f"Saved assessment for learning path {path_id}")
        return True
        
    except SQLAlchemyError as e:
        if db:
            db.rollback()
        logger.error(f"Failed to save assessment: {e}")
        return False
    finally:
        if db:
            close_db_session(db)


async def save_assessment_results(path_id: str, results: dict) -> bool:
    """
    Save assessment results to the learning path
    
    Args:
        path_id: Session ID of the learning path
        results: Assessment results including score and answers
    
    Returns:
        True if successful, False otherwise
    """
    db = None
    try:
        db = get_db_session()
        
        learning_path = db.query(LearningPath).filter(
            LearningPath.session_id == path_id
        ).first()
        
        if not learning_path:
            return False
        
        # Add to assessment attempts array
        attempts = learning_path.assessment_attempts or []
        attempt_with_timestamp = {
            **results,
            "attempted_at": datetime.now().isoformat()
        }
        attempts.append(attempt_with_timestamp)
        
        learning_path.assessment_attempts = attempts
        learning_path.latest_assessment_result = results
        learning_path.updated_at = datetime.now()
        
        # Update status if passed
        if results.get("passed"):
            learning_path.status = "assessment_passed"
        
        db.commit()
        logger.info(f"Saved assessment results for learning path {path_id}")
        return True
        
    except SQLAlchemyError as e:
        if db:
            db.rollback()
        logger.error(f"Failed to save assessment results: {e}")
        return False
    finally:
        if db:
            close_db_session(db)


async def save_certificate(path_id: str, certificate_data: dict) -> bool:
    """
    Save certificate data to the learning path
    
    Args:
        path_id: Session ID of the learning path
        certificate_data: Certificate details
    
    Returns:
        True if successful, False otherwise
    """
    db = None
    try:
        db = get_db_session()
        
        learning_path = db.query(LearningPath).filter(
            LearningPath.session_id == path_id
        ).first()
        
        if not learning_path:
            return False
        
        learning_path.certificate = certificate_data
        learning_path.certificate_generated_at = datetime.now()
        learning_path.status = "completed"
        learning_path.updated_at = datetime.now()
        
        db.commit()
        logger.info(f"Saved certificate for learning path {path_id}")
        return True
        
    except SQLAlchemyError as e:
        if db:
            db.rollback()
        logger.error(f"Failed to save certificate: {e}")
        return False
    finally:
        if db:
            close_db_session(db)


async def get_all_learning_paths(limit: int = 50, skip: int = 0) -> List[dict]:
    """
    Retrieve all learning paths with pagination
    
    Args:
        limit: Maximum number of results to return
        skip: Number of results to skip
    
    Returns:
        List of learning paths
    """
    db = None
    try:
        db = get_db_session()
        
        learning_paths = db.query(LearningPath).order_by(
            LearningPath.created_at.desc()
        ).offset(skip).limit(limit).all()
        
        result = [path.to_dict() for path in learning_paths]
        logger.info(f"Retrieved {len(result)} learning paths")
        return result
        
    except SQLAlchemyError as e:
        logger.error(f"Failed to retrieve learning paths: {e}")
        return []
    finally:
        if db:
            close_db_session(db)


async def get_learning_paths_by_topic(topic: str, limit: int = 20) -> List[dict]:
    """
    Retrieve learning paths by topic
    
    Args:
        topic: Topic to search for
        limit: Maximum number of results
    
    Returns:
        List of matching learning paths
    """
    db = None
    try:
        db = get_db_session()
        
        # Search in path_metadata JSON field
        learning_paths = db.query(LearningPath).filter(
            LearningPath.path_metadata.op('->>')('topic').ilike(f'%{topic}%')
        ).order_by(LearningPath.created_at.desc()).limit(limit).all()
        
        result = [path.to_dict() for path in learning_paths]
        logger.info(f"Retrieved {len(result)} learning paths for topic: {topic}")
        return result
        
    except SQLAlchemyError as e:
        logger.error(f"Failed to retrieve learning paths by topic: {e}")
        return []
    finally:
        if db:
            close_db_session(db)


async def delete_learning_path(path_id: str) -> bool:
    """
    Delete a learning path (soft delete by marking as archived)
    
    Args:
        path_id: Session ID of the learning path
    
    Returns:
        True if successful, False otherwise
    """
    db = None
    try:
        db = get_db_session()
        
        learning_path = db.query(LearningPath).filter(
            LearningPath.session_id == path_id
        ).first()
        
        if not learning_path:
            return False
        
        learning_path.status = "archived"
        learning_path.archived_at = datetime.now()
        learning_path.updated_at = datetime.now()
        
        db.commit()
        logger.info(f"Archived learning path {path_id}")
        return True
        
    except SQLAlchemyError as e:
        if db:
            db.rollback()
        logger.error(f"Failed to archive learning path: {e}")
        return False
    finally:
        if db:
            close_db_session(db)


async def get_user_statistics(user_identifier: Optional[str] = None) -> dict:
    """
    Get statistics about learning paths
    
    Args:
        user_identifier: Optional user identifier to filter statistics
    
    Returns:
        Dictionary with statistics
    """
    db = None
    try:
        db = get_db_session()
        
        total_count = db.query(LearningPath).count()
        completed_count = db.query(LearningPath).filter(
            LearningPath.status == "completed"
        ).count()
        active_count = db.query(LearningPath).filter(
            LearningPath.status == "active"
        ).count()
        archived_count = db.query(LearningPath).filter(
            LearningPath.status == "archived"
        ).count()
        
        return {
            "total_learning_paths": total_count,
            "completed": completed_count,
            "active": active_count,
            "archived": archived_count
        }
        
    except SQLAlchemyError as e:
        logger.error(f"Failed to get statistics: {e}")
        return {
            "total_learning_paths": 0,
            "completed": 0,
            "active": 0,
            "archived": 0
        }
    finally:
        if db:
            close_db_session(db)
