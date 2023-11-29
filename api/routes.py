# /api/routes.py
"""
Implementation of the API routes.
"""
from fastapi import APIRouter, HTTPException, Path, status
from app.models.pydantic_execution_info import ExecutionInfo
import api.views as views
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/crawls", status_code=status.HTTP_201_CREATED)
def create_crawl():
    try:
        logger.info("Creating new crawl...")
        crawl = views.create_crawl()
        return crawl
    except Exception as e:
        logger.error(f"Error while creating crawl: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error while creating crawl")

@router.get("/crawls/{execution_id}", response_model=ExecutionInfo)
def read_crawl_status(execution_id: str = Path(..., title="The ID of the crawl execution")):
    return views.read_crawl_status(execution_id)

@router.get("/crawls", response_model=list[ExecutionInfo])
def read_crawl_history():
    return views.read_crawl_history()

# TODO: The client call this endpoints asynchronoulsy. Should be async here as well?