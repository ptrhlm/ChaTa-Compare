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


def get_summary(db_session, *, id, user):
    # TODO: access control
    survey = get(db_session, survey_id=id)

    answers = db_session.query(
        func.count('*').label("answer_count")).select_from(Answer).join(
            Task).filter(Task.survey_id == id).scalar()

    tasks = db_session.query(
        Task.id,
        func.count('*').label("answers")).select_from(Answer).join(
            Task).filter(Task.survey_id == id).group_by(Task.id).subquery()
    finished_tasks = db_session.query(
        func.count('*')).select_from(tasks).filter(
            tasks.c.answers >= survey.answers_per_task).scalar()

    active_users = db_session.query(Answer.user_id).join(Task).filter(
        Task.survey_id == id).distinct(Answer.user_id).count()

    return SurveySummary(id=survey.id,
                         name=survey.name,
                         answers=answers,
                         finished_tasks=finished_tasks,
                         active_users=active_users,
                         end_date=survey.deadline,
                         status=survey.status)


def get_summary_multi(db_session, *, user, skip=0, limit=100):
    surveys_of_user = db_session.query(
        Survey.id).filter((Survey.researcher_id == user.id)
                          | (Survey.participants.any(id=user.id))).subquery()

    answers = db_session.query(
        Task.survey_id,
        func.count(Answer.id).label("answer_count")
    ).join(Task)\
     .group_by(Task.survey_id)\
     .subquery()

    tasks = db_session.query(
        Task.id,
        func.count(Answer.id).label("answers")
    ).join(Task)\
     .group_by(Task.id)\
     .subquery()
    answers_per_task = db_session.query(Survey.id,
                                        Survey.answers_per_task).subquery()
    finished_tasks = db_session.query(
        Task.survey_id,
        func.count(tasks.c.id).label("finished_tasks"))\
        .join(Task, tasks.c.id == Task.id)\
        .join(answers_per_task, answers_per_task.c.id == Task.survey_id)\
        .filter(tasks.c.answers >= Survey.answers_per_task)\
        .group_by(Task.survey_id)\
        .subquery()

    survey_users = db_session.query(
        Task.survey_id,
        Answer.user_id
    ).join(Task)\
     .distinct(Answer.user_id, Task.survey_id)\
     .subquery()
    active_users = db_session.query(
        survey_users.c.survey_id,
        func.count(survey_users.c.user_id).label("active_users")
    ).group_by(survey_users.c.survey_id)\
     .subquery()

    surveys = db_session.query(
        Survey.id,
        Survey.name,
        func.coalesce(answers.c.answer_count, 0).label("answers"),
        func.coalesce(finished_tasks.c.finished_tasks, 0).label("finished_tasks"),
        func.coalesce(active_users.c.active_users, 0).label("active_users"),
        Survey.deadline.label("end_date"),
        Survey.status
    )\
        .filter(Survey.status == SurveyStatus.OPEN)\
        .outerjoin(answers)\
        .outerjoin(finished_tasks)\
        .outerjoin(active_users)\
        .filter(Survey.id.in_(surveys_of_user))\
        .offset(skip)\
        .limit(limit)\
        .all()
    return [s._asdict() for s in surveys]
