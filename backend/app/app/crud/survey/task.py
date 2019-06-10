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

from .survey import get


def get_tasks(db_session, *, survey_id: int, user: User, skip=0,
              limit=100):
    return db_session.query(Task).filter(
        Task.survey_id == survey_id).offset(skip).limit(limit).all()


def get_task(db_session, *, survey_id: int, task_id: int, user: User):
    return db_session.query(Task).filter(Task.survey_id == survey_id).filter(
        Task.id == task_id).first()


def get_next_task(db_session, *, survey_id: int,
                  user: User):
    survey = get(db_session, survey_id=survey_id)
    if not survey:
        raise RuntimeError("Survey not found")
    subquery = db_session.query(
        Answer.task_id,
        func.count(Answer.id).label("task_num"),
        func.sum(case([(Answer.user_id == user.id, 1)], else_=0)).label("checked")
    ).select_from(Answer) \
        .group_by("task_id")\
        .subquery()
    task = db_session.query(Task) \
        .outerjoin(subquery)\
        .filter(Task.survey_id == survey_id).filter(
        ((subquery.c.task_num < survey.answers_per_task) | (subquery.c.task_num == None)) &
        ((subquery.c.checked == 0) | (subquery.c.checked == None))
    ).first()
    return task


def generate_new_tasks():
    pass  # TODO
