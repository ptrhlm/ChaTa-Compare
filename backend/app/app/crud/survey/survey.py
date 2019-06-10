from typing import Any, List, Optional

from sqlalchemy import case, func

from app.crud.user import is_superuser
from app.db_models.answer import Answer
from app.db_models.associations import (chart_survey_association,
                                        survey_user_association)
from app.db_models.chart import Chart
from app.db_models.survey import Survey
from app.db_models.task import Task
from app.db_models.user import User
from app.models.survey import SurveyInCreate, SurveyStatus, SurveySummary


def get(db_session, *, survey_id: int) -> Optional[Survey]:
    # TODO: access control
    return db_session.query(Survey).filter(Survey.id == survey_id).first()  # type: ignore


def get_multi(db_session, *, skip=0, limit=100) -> List[Optional[Survey]]:
    # TODO: access control
    return db_session.query(Survey).offset(skip).limit(limit).all()  # type: ignore


def get_current_multi(db_session, *, skip=0,
                      limit=100) -> List[Optional[Survey]]:
    # TODO: access control
    surveys = db_session.query(Survey)\
        .filter(Survey.status == SurveyStatus.OPEN)\
        .offset(skip)\
        .limit(limit)\
        .all()

    return surveys  # type: ignore


def create(db_session, *, survey_in: SurveyInCreate,
           researcher: User) -> Survey:
    survey = Survey(name=survey_in.name,
                    description=survey_in.description,
                    status=survey_in.status,
                    type=survey_in.type,
                    researcher=researcher,
                    answers_per_task=survey_in.answers_per_task,
                    tasks_per_chart=survey_in.tasks_per_chart,
                    exp_required=survey_in.exp_required,
                    min_answers_quality=survey_in.min_answers_quality)
    db_session.add(survey)
    db_session.flush()
    db_session.refresh(survey)

    chart_survey_associations = [{
        'chart_id': chart_id,
        'survey_id': survey.id
    } for chart_id in survey_in.charts_ids]
    chart_survey_association_insert = chart_survey_association.insert().values(
        chart_survey_associations)

    db_session.execute(chart_survey_association_insert)
    db_session.commit()
    db_session.refresh(survey)

    return survey


def close(db_session, *, survey: Survey) -> Survey:
    survey.status = SurveyStatus.CLOSED
    db_session.add(survey)
    db_session.commit()
    db_session.refresh(survey)
    return survey


def save_report(db_session, *, survey_id: int, task_id: int,
                user: User) -> None:
    "Intended for reporting bad charts."
    raise NotImplementedError()  # TODO: later
