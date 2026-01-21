"""
SQLAlchemy models for Learning Path Planner
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()


class LearningPath(Base):
    """Model for storing complete learning paths"""
    __tablename__ = 'learning_paths'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(100), unique=True, index=True, nullable=False)
    
    # Learning plan data (stored as JSON)
    learning_plan = Column(JSON, nullable=False)
    resources = Column(JSON)
    schedule = Column(JSON)
    progress_tracking = Column(JSON)
    todo_list = Column(JSON)
    path_metadata = Column(JSON)  # Renamed from 'metadata' (reserved word in SQLAlchemy)
    
    # Assessment data
    assessment = Column(JSON)
    assessment_attempts = Column(JSON)  # List of all attempts
    latest_assessment_result = Column(JSON)
    
    # Certificate data
    certificate = Column(JSON)
    
    # Status tracking
    status = Column(String(50), default='active')  # active, assessment_passed, completed, archived
    
    # Timestamps
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    assessment_generated_at = Column(DateTime)
    certificate_generated_at = Column(DateTime)
    archived_at = Column(DateTime)
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'session_id': self.session_id,
            'learning_plan': self.learning_plan,
            'resources': self.resources,
            'schedule': self.schedule,
            'progress_tracking': self.progress_tracking,
            'todo_list': self.todo_list,
            'metadata': self.path_metadata,  # Expose as 'metadata' for backward compatibility
            'assessment': self.assessment,
            'assessment_attempts': self.assessment_attempts or [],
            'latest_assessment_result': self.latest_assessment_result,
            'certificate': self.certificate,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'assessment_generated_at': self.assessment_generated_at.isoformat() if self.assessment_generated_at else None,
            'certificate_generated_at': self.certificate_generated_at.isoformat() if self.certificate_generated_at else None,
        }
