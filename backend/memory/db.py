import os
import logging

logger = logging.getLogger(__name__)

# MongoDB is no longer required - we use SQLAlchemy now
# This file is kept for backward compatibility with other planners
MONGO_URI = os.getenv("MONGODB_URI")

# Don't initialize the client at module level - do it lazily
_client = None
_db = None

def get_db():
    """Get database connection, initializing if needed"""
    global _client, _db
    
    # MongoDB is optional now
    if not MONGO_URI:
        logger.warning("MongoDB not configured - using SQLite instead")
        return None
    
    if _client is None:
        try:
            from motor.motor_asyncio import AsyncIOMotorClient
            _client = AsyncIOMotorClient(MONGO_URI)
            _db = _client.get_default_database()
            logger.info("MongoDB connection initialized")
        except ImportError:
            logger.warning("motor package not installed - MongoDB unavailable")
            return None
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            # Return None to indicate MongoDB is not available
            # The calling functions will handle this gracefully
            return None
    return _db

async def save_plan(doc: dict):
    try:
        db = get_db()
        if db is None:
            raise Exception("MongoDB not available")
        plans_collection = db.get_collection("plans")
        res = await plans_collection.insert_one(doc)
        return str(res.inserted_id)
    except Exception as e:
        logger.error(f"Failed to save plan to MongoDB: {e}. Returning mock ID.")
        # Return a mock ID for testing when MongoDB is not available
        import uuid
        return f"mock_plan_{uuid.uuid4().hex[:8]}"

async def get_plan(plan_id: str):
    try:
        db = get_db()
        if db is None:
            raise Exception("MongoDB not available")
        plans_collection = db.get_collection("plans")
        return await plans_collection.find_one({"_id": plan_id})
    except Exception as e:
        logger.error(f"Failed to get plan from MongoDB: {e}")
        return None
