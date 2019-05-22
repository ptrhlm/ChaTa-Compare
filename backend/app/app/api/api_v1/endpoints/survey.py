from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException, Path
from sqlalchemy.orm import Session

from app import crud
from app.api.utils.db import get_db
from app.api.utils.security import (get_current_active_researcher,
                                    get_current_active_user)
from app.core import config
from app.db_models.user import User
from app.models.survey import (CreateSurvey, Survey, SurveyParticipant,
                               SurveyStatus)

router = APIRouter()


@router.post("/surveys", tags=["survey"], response_model=Survey)
async def create_survey(
        survey: CreateSurvey,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_researcher)):
    """Create a survey"""
    survey = crud.survey.create(db, survey=survey, researcher=current_user)
    return survey


@router.post("/surveys/{id}/charts", tags=["survey"])
async def add_charts_to_survey(
        id: int,
        chart_ids: List[int],
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_researcher)):
    """Add charts to survey"""
    if len(chart_ids) == 0:
        pass  # TODO: do the screaming
    survey = crud.survey.get(db, survey_id=id)
    if survey.researcher != current_user:
        pass  # TODO: do the screaming
    elif survey.status == SurveyStatus.CLOSED:
        pass  # TODO: do the screaming
    else:
        crud.survey.add_charts(db, survey=survey, chart_ids=chart_ids)


@router.delete("/surveys/{id}/charts", tags=["survey"], response_model=Survey)
async def remove_charts_from_survey(
        id: int,
        chart_ids: List[int],
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_researcher)):
    """Remove charts from survey"""
    if len(chart_ids) == 0:
        pass  # TODO: do the screaming
    survey = crud.survey.get(db, survey_id=id)
    if survey.researcher != current_user:
        pass  # TODO: do the screaming
    elif survey.status == SurveyStatus.CLOSED:
        pass  # TODO: do the screaming
    else:
        crud.survey.remove_charts(
            db, survey=survey, chart_ids=chart_ids
        )  # TODO: verify that removed charts weren't used in survey (ie. no answers)


@router.get("/surveys", tags=["survey"], response_model=List[Survey])
async def list_surveys(skip: int = Path(0, ge=0),
                       limit: int = Path(100, gt=0, le=1000),
                       db: Session = Depends(get_db),
                       current_user: User = Depends(get_current_active_user)):
    """List all surveys"""
    surveys = crud.survey.get_multi(db, skip=skip, limit=limit)
    return surveys


@router.put("/surveys/{id}/close", tags=["survey"], response_model=Survey)
async def close_survey(id: int,
                       db: Session = Depends(get_db),
                       current_user: User = Depends(get_current_active_user)):
    """Close survey"""
    survey = crud.survey.get(db, survey_id=id)
    if survey.researcher != current_user:
        pass  # TODO: do the screaming
    elif survey.status == SurveyStatus.CLOSED:
        pass  # TODO: do the screaming
    else:
        return crud.survey.close(db, survey=survey)


@router.get("/surveys/{id}/participants",
            tags=["survey"],
            response_model=List[SurveyParticipant])
def list_participants(id: int,
                      skip: int = Path(0, ge=0),
                      limit: int = Path(100, gt=0, le=1000),
                      db: Session = Depends(get_db),
                      current_user: User = Depends(get_current_active_user)):
    """List all participants"""
    survey = crud.survey.get(db, survey_id=id)
    if survey.researcher != current_user:
        pass  # TODO: do the screaming
    else:
        return crud.survey.get_participants(db, survey=survey, skip=skip, limit=limit)


@router.post("/surveys/{id}/participants", tags=["survey"])
async def add_participants(
        id: int,
        participant_ids: List[int],
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)):
    """Add survey participants"""
    survey = crud.survey.get(db, survey_id=id)
    if survey.researcher != current_user:
        pass  # TODO: do the screaming
    elif survey.status == SurveyStatus.CLOSED:
        pass  # TODO: do the screaming
    else:
        crud.survey.add_participants(db, survey=survey, participant_ids=participant_ids)


@router.delete("/surveys/{id}/participants", tags=["survey"])
async def remove_participants(
        id: int,
        participant_ids: List[SurveyParticipant],
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)):
    """Remove participants from survey"""
    survey = crud.survey.get(db, survey_id=id)
    if survey.researcher != current_user:
        pass  # TODO: do the screaming
    elif survey.status == SurveyStatus.CLOSED:
        pass  # TODO: do the screaming
    else:
        crud.survey.remove_participants(db, survey=survey, participant_ids=participant_ids)  # TODO: verify that participants concerned did not give any answers
