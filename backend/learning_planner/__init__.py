"""Learning Planner Routes Module"""
from fastapi import APIRouter

router = APIRouter(prefix="/api/learning", tags=["learning"])

from . import routes
