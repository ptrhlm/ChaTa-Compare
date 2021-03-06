from datetime import date
from typing import List

from app import crud
from app.api.utils.db import get_db
from app.api.utils.security import (get_current_active_researcher,
                                    get_current_active_user)
from app.db_models.user import User
from app.models.survey import (SurveyInCreate, Survey, SurveyParticipant,
                               SurveyStatus, SurveySummary, CurrentSurvey,
                               SurveyDetails, SurveyParticipantIds)
from fastapi import APIRouter, Depends, HTTPException, Path, Query
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
    if not survey:
        raise HTTPException(
            status_code=404,
            detail="Survey not found"
        )
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
    if not survey:
        raise HTTPException(
            status_code=404,
            detail="Survey not found"
        )
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
async def list_surveys(skip: int = Query(0, ge=0),
                       limit: int = Query(100, gt=0, le=1000),
                       db: Session = Depends(get_db),
                       current_user: User = Depends(get_current_active_user)):
    """List all surveys"""
    surveys = crud.survey.get_multi(db, skip=skip, limit=limit)
    return surveys


@router.get("/surveys/current",
            tags=["survey"],
            response_model=List[CurrentSurvey])
async def list_current_surveys(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, gt=0, le=1000),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)):
    """List all surveys"""
    surveys = crud.survey.get_current_multi(db, skip=skip, limit=limit)
    current_surveys = []
    for survey in surveys:
        if survey:
            current_surveys.append(
                CurrentSurvey(id=survey.id,
                              name=survey.name))

    return current_surveys


@router.get("/surveys/{survey_id}/details",
            tags=["survey"],
            response_model=SurveyDetails)
async def survey_details(
        survey_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)):
    """Get survey details"""
    survey = crud.survey.get(db, survey_id=survey_id)
    if not survey:
        raise HTTPException(
            status_code=404,
            detail="Survey not found"
        )
    charts_count = crud.survey.get_charts_count(db, survey=survey)
    current_user_participant = crud.survey.is_participant(db,
                                                          survey_id=survey_id,
                                                          user=current_user)
    details = SurveyDetails(
        name=survey.name,
        description=survey.description,
        type=survey.type,
        data_characteristics=["Charts count: " + str(charts_count)],
        current_user_participant=current_user_participant)
    return details


@router.get("/surveys/{id}/summary",
            tags=["survey"],
            response_model=SurveySummary)
async def survey_summary(
        id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)):
    surveys = crud.survey.get_summary(db, id=id, user=current_user)
    return surveys


@router.get("/surveys/summary",
            tags=["survey"],
            response_model=List[SurveySummary]
)
async def list_survey_summaries(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, gt=0, le=1000),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)):
    surveys = crud.survey.get_summary_multi(db,
                                            skip=skip,
                                            limit=limit,
                                            user=current_user)
    return surveys


@router.put("/surveys/{id}/close", tags=["survey"], response_model=Survey)
async def close_survey(id: int,
                       db: Session = Depends(get_db),
                       current_user: User = Depends(get_current_active_user)):
    """Close survey"""
    survey = crud.survey.get(db, survey_id=id)
    if not survey:
        raise HTTPException(
            status_code=404,
            detail="Survey not found"
        )
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
    if not survey:
        raise HTTPException(
            status_code=404,
            detail="Survey not found"
        )
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
        *,
        participants: SurveyParticipantIds,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)):
    """Add survey participants"""
    participant_ids = participants.participant_ids
    if len(participant_ids) == 0:
        raise HTTPException(
            status_code=400,
            detail="Received empty list",
        )
    survey = crud.survey.get(db, survey_id=id)
    if not survey:
        raise HTTPException(
            status_code=404,
            detail="Survey not found"
        )
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
        *,
        participants: SurveyParticipantIds,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)):
    """Remove participants from survey"""
    participant_ids = participants.participant_ids
    if len(participant_ids) == 0:
        raise HTTPException(
            status_code=400,
            detail="Received empty list",
        )
    survey = crud.survey.get(db, survey_id=id)
    if not survey:
        raise HTTPException(
            status_code=404,
            detail="Survey not found"
        )
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
