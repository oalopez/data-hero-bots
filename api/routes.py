# /api/routes.py
"""
Implementation of the API routes.
"""
from fastapi import APIRouter, HTTPException, Path, status
from app.models.pydantic_execution_info import ExecutionInfo
import api.views as views

router = APIRouter()

@router.post("/crawls", response_model=ExecutionInfo, status_code=status.HTTP_201_CREATED)
def create_crawl():
    return views.create_crawl()

@router.get("/crawls/{execution_id}", response_model=ExecutionInfo)
def read_crawl_status(execution_id: str = Path(..., title="The ID of the crawl execution")):
    return views.read_crawl_status(execution_id)

@router.get("/crawls", response_model=list[ExecutionInfo])
def read_crawl_history():
    return views.read_crawl_history()
