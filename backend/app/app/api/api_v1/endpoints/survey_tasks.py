from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.api.utils.db import get_db
from app.api.utils.security import get_current_active_superuser, get_current_active_user
from app.core import config
from app.db_models.user import User
from app.models.answer import Answer
from app.models.task import Task

router = APIRouter()


@router.get("/surveys/{id}/tasks/next", tags=["survey", "task"], response_model=Task)
async def get_next_task(
        id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    """Get next task for user"""
    raise NotImplementedError()  # TODO


@router.post("/surveys/{id}/tasks/{task_id}/answers", tags=["survey", "task"])
async def save_answer(
        id: int,
        task_id: int,
        answer: Answer,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    """Save user's answer for the task"""
    raise NotImplementedError()  # TODO


@router.post("/surveys/{id}/tasks/{task_id}/report", tags=["survey", "task"])
async def report_task(
        id: int,
        task_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    """Report task"""
    raise NotImplementedError()  # TODO


@router.get("/surveys/{id}/tasks", tags=["survey", "task"], response_model=List[Task])
async def list_tasks(
        id: int,
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    """List tasks for current user"""
    raise NotImplementedError()  # TODO


@router.get("/surveys/{id}/tasks/{task_id}", tags=["survey", "task"], response_model=Task)
async def task_info(
        id: int,
        task_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    """Get task details"""
    raise NotImplementedError()  # TODO
