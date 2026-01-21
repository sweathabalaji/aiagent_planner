"""
SQLAlchemy database setup and connection
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import StaticPool
import logging

from .models import Base

logger = logging.getLogger(__name__)

# Get database path from environment or use default
DATABASE_PATH = os.getenv("DATABASE_PATH", "learning_paths.db")
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# Create engine with proper settings for SQLite
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    echo=False  # Set to True for SQL debugging
)

# Create session factory
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

def init_db():
    """Initialize database - create all tables"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info(f"Database initialized at {DATABASE_PATH}")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise

def get_db_session():
    """Get database session"""
    db = SessionLocal()
    try:
        return db
    except Exception as e:
        logger.error(f"Failed to get database session: {e}")
        db.close()
        raise

def close_db_session(db):
    """Close database session"""
    try:
        db.close()
    except Exception as e:
        logger.error(f"Error closing database session: {e}")

# Initialize database on module import
try:
    init_db()
except Exception as e:
    logger.warning(f"Database initialization warning: {e}")
