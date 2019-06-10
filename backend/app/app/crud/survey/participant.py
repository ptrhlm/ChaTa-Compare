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


def get_participants(db_session, *, survey: Survey, skip=0,
                     limit=100) -> List[Optional[Any]]:
    return survey.participants.offset(skip).limit(limit).all()  # type: ignore


def add_participants(db_session, *, survey: Survey,
                     participant_ids: List[int]) -> None:
    survey_id = survey.id
    db_session.execute(survey_user_association.insert(), [{
        "survey_id": survey_id,
        "user_id": user_id
    } for user_id in participant_ids])
    db_session.commit()


def remove_participants(db_session, *, survey: Survey,
                        participant_ids: List[int]) -> None:
    survey_id = survey.id
    db_session.execute(survey_user_association.delete().where(
        survey_user_association.c.survey_id == survey_id).where(
            survey_user_association.c.user_id.in_(participant_ids)))
    db_session.commit()


def is_participant(db_session, *, survey_id: int, user: User) -> bool:
    result = db_session.query(func.count('*')) \
                       .select_from(survey_user_association) \
                       .filter(survey_user_association.c.survey_id == survey_id) \
                       .filter(survey_user_association.c.user_id == User.id) \
                       .group_by(survey_user_association.c.survey_id).scalar()
    return result or False
