from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.api.utils.db import get_db
from app.api.utils.security import get_current_active_superuser, get_current_active_user
from app.core import config
from app.db_models.user import User
from app.models.survey import Survey, SurveyParticipant

router = APIRouter()


@router.post("/surveys", tags=["survey"])
async def create_survey(
        survey: Survey,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    """Create a survey"""
    raise NotImplementedError()  # TODO


@router.put("/surveys/{id}/charts/{chart_id}", tags=["survey"])
async def add_chart_to_survey(
        id: int,
        chart_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    """Add chart to survey"""
    raise NotImplementedError()  # TODO


@router.delete("/surveys/{id}/charts/{chart_id}", tags=["survey"])
async def remove_chart_from_survey(
        id: int,
        chart_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    """Remove chart from survey"""
    raise NotImplementedError()  # TODO


@router.get("/surveys", tags=["survey"], response_model=List[Survey])
async def list_surveys(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    """List all surveys"""
    raise NotImplementedError()  # TODO


@router.put("/surveys/{id}/close", tags=["survey"])
async def close_survey(
        id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    """Close survey"""
    raise NotImplementedError()  # TODO


@router.post("/surveys/{id}/participants", tags=["survey"])
async def add_participants(
        participants: List[SurveyParticipant],
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    """Add survey participants"""
    raise NotImplementedError()  # TODO
