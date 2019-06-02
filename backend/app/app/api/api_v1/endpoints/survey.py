from typing import List

from app import crud
from app.api.utils.db import get_db
from app.api.utils.security import (get_current_active_researcher,
                                    get_current_active_user)
from app.db_models.user import User
from app.models.survey import (SurveyInCreate, Survey, SurveyParticipant,
                               SurveyStatus)
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/surveys", tags=["survey"], response_model=Survey)
async def create_survey(
        survey: SurveyInCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_researcher)):
    """Create a survey"""
    survey = crud.survey.create(db, survey_in=survey, researcher=current_user)
    return survey


@router.post("/surveys/{id}/charts", tags=["survey"])
async def add_charts_to_survey(
        id: int,
        chart_ids: List[int],
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_researcher)):
    """Add charts to survey"""
    if len(chart_ids) == 0:
        raise HTTPException(
            status_code=400,
            detail="Received empty list",
        )
    survey = crud.survey.get(db, survey_id=id)
    if survey.researcher != current_user and crud.user.is_superuser(
            current_user):
        raise HTTPException(
            status_code=403,
            detail="User does not have necessary permissions",
        )
    elif survey.status == SurveyStatus.CLOSED:
        raise HTTPException(
            status_code=400,
            detail="Survey is closed - change is prohibited",
        )
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
        raise HTTPException(
            status_code=400,
            detail="Received empty list",
        )
    survey = crud.survey.get(db, survey_id=id)
    if survey.researcher != current_user and crud.user.is_superuser(
            current_user):
        raise HTTPException(
            status_code=403,
            detail="User does not have necessary permissions",
        )
    elif survey.status == SurveyStatus.CLOSED:
        raise HTTPException(
            status_code=400,
            detail="Survey is closed - change is prohibited",
        )
    else:
        # TODO: verify that removed charts weren't used in survey (ie. no answers)
        crud.survey.remove_charts(db, survey=survey, chart_ids=chart_ids)


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
    if survey.researcher != current_user and crud.user.is_superuser(
            current_user):
        raise HTTPException(
            status_code=403,
            detail="User does not have necessary permissions",
        )
    elif survey.status == SurveyStatus.CLOSED:
        raise HTTPException(
            status_code=400,
            detail="Survey is closed - change is prohibited",
        )
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
    if survey.researcher != current_user and crud.user.is_superuser(
            current_user):
        raise HTTPException(
            status_code=403,
            detail="User does not have necessary permissions",
        )
    else:
        return crud.survey.get_participants(db,
                                            survey=survey,
                                            skip=skip,
                                            limit=limit)


@router.post("/surveys/{id}/participants", tags=["survey"])
async def add_participants(
        id: int,
        participant_ids: List[int],
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)):
    """Add survey participants"""
    if len(participant_ids) == 0:
        raise HTTPException(
            status_code=400,
            detail="Received empty list",
        )
    survey = crud.survey.get(db, survey_id=id)
    if survey.researcher != current_user and crud.user.is_superuser(
            current_user):
        raise HTTPException(
            status_code=403,
            detail="User does not have necessary permissions",
        )
    elif survey.status == SurveyStatus.CLOSED:
        raise HTTPException(
            status_code=400,
            detail="Survey is closed - change is prohibited",
        )
    else:
        crud.survey.add_participants(db,
                                     survey=survey,
                                     participant_ids=participant_ids)


@router.delete("/surveys/{id}/participants", tags=["survey"])
async def remove_participants(
        id: int,
        participant_ids: List[SurveyParticipant],
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)):
    """Remove participants from survey"""
    if len(participant_ids) == 0:
        raise HTTPException(
            status_code=400,
            detail="Received empty list",
        )
    survey = crud.survey.get(db, survey_id=id)
    if survey.researcher != current_user and crud.user.is_superuser(
            current_user):
        raise HTTPException(
            status_code=403,
            detail="User does not have necessary permissions",
        )
    elif survey.status == SurveyStatus.CLOSED:
        raise HTTPException(
            status_code=400,
            detail="Survey is closed - change is prohibited",
        )
    else:
        # TODO: verify that participants concerned did not give any answers
        crud.survey.remove_participants(db,
                                        survey=survey,
                                        participant_ids=participant_ids)
