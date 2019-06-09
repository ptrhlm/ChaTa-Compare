from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.api.utils.db import get_db
from app.api.utils.security import get_current_active_superuser, get_current_active_user
from app.db_models.user import User
from app.models.survey import SurveyStatistics
from app.models.report import Report

router = APIRouter()


@router.get("/surveys/{id}/statistics", tags=["survey", "report"], response_model=SurveyStatistics)
async def survey_statistics(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Survey summary"""
    raise NotImplementedError()  # TODO: later


@router.get("/surveys/{id}/report", tags=["survey", "report"], response_model=Report)
async def survey_report(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Generate survey report"""
    raise NotImplementedError()  # TODO: later
