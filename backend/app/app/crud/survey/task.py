from typing import Any, List, Optional

import trueskill
from sqlalchemy import aliased, case, func, literal, tuple_

from app.crud.user import is_superuser
from app.db_models.answer import Answer
from app.db_models.associations import (chart_survey_association,
                                        survey_user_association)
from app.db_models.chart import Chart
from app.db_models.survey import Survey
from app.db_models.task import Task
from app.db_models.user import User
from app.models.survey import (SurveyInCreate, SurveyStatus, SurveySummary,
                               SurveyType)

from .survey import get


def get_tasks(db_session, *, survey_id: int, user: User, skip=0, limit=100):
    return db_session.query(Task).filter(
        Task.survey_id == survey_id).offset(skip).limit(limit).all()


def get_task(db_session, *, survey_id: int, task_id: int, user: User):
    return db_session.query(Task).filter(Task.survey_id == survey_id).filter(
        Task.id == task_id).first()


def get_task_count(db_session, *, survey_id: int) -> int:
    task_count = db_session\
        .query(Task) \
        .filter(Task.survey_id == survey_id)\
        .count()
    return task_count or 0


def get_active_task_count(db_session, *, survey: Survey) -> int:
    subquery = db_session\
        .query(
            Answer.task_id,
            func.count(Answer.id).label("task_num"),
        )\
        .group_by("task_id")\
        .subquery()
    task_count = db_session\
        .query(Task) \
        .outerjoin(subquery)\
        .filter(Task.survey_id == survey.id)\
        .filter(func.coalesce(subquery.c.task_num, 0) < survey.answers_per_task)\
        .count()
    return task_count or 0


def get_next_task(db_session, *, survey_id: int, user: User):
    survey = get(db_session, survey_id=survey_id)
    if not survey:
        raise RuntimeError("Survey not found")
    subquery = db_session\
        .query(
            Answer.task_id,
            func.count(Answer.id).label("task_num"),
            func.sum(case([(Answer.user_id == user.id, 1)], else_=0)).label("checked")
        )\
        .group_by("task_id")\
        .subquery()
    task = db_session\
        .query(Task) \
        .outerjoin(subquery)\
        .filter(Task.survey_id == survey_id)\
        .filter(func.coalesce(subquery.c.task_num, 0) < survey.answers_per_task)\
        .filter(func.coalesce(subquery.c.checked, 0) == 0)\
        .order_by("RANDOM()")\
        .first()
    # Chooses random available task. Let's hope this will limit collisions to minimum
    return task


def generate_new_tasks(db_session, *, survey: Survey) -> None:
    if survey.type == SurveyType.COMPARISON:
        active_task_count = get_active_task_count(db_session, survey=survey)
        existing_tasks = get_task_count(db_session, survey_id=survey.id)
        chart_count = db_session\
            .query(chart_survey_association)\
            .filter(chart_survey_association.c.survey_id == survey.id)\
            .count()
        all_tasks = chart_count * survey.tasks_per_chart
        tasks_to_add = min(500, all_tasks - existing_tasks) - active_task_count

        if tasks_to_add < 100:
            return

        sub1 = db_session\
            .query(
                Task.chart1_id.label("chart_id"), func.count('*').label("task1_count")
            )\
            .filter(Task.survey_id == survey.id)\
            .group_by(Task.chart1_id)
        sub2 = db_session\
            .query(
                Task.chart2_id.label("chart_id"), func.count('*').label("task2_count")
            )\
            .filter(Task.survey_id == survey.id)\
            .group_by(Task.chart2_id)
        chart_task_count = db_session\
            .query(
                chart_survey_association.c.chart_id.label("chart_id"),
                (func.coalesce(sub1.task1_count, 0) + func.coalesce(sub1.task2_count, 0)).label("task_count")
            )\
            .filter(chart_survey_association.c.survey_id == survey.id)\
            .outerjoin(sub1, sub1.c.chart_id == chart_survey_association.c.chart_id)\
            .outerjoin(sub2, sub1.c.chart_id == chart_survey_association.c.chart_id)\
            .subquery()
        charts = db_session\
            .query(chart_task_count.c.chart_id.label("chart_id"))\
            .filter(chart_task_count.c.count < survey.tasks_per_chart)\
            .subquery()

        current_tasks = db_session\
            .query(
                Task.chart1_id,
                Task.chart2_id
            )\
            .filter(Task.survey_id == survey.id)\
            .subquery()

        chart1 = aliased(Chart)
        chart2 = aliased(Chart)
        task_candidates = db_session\
            .query(
                charts.c.chart_id.label("chart1_id"),
                chart1.c.sigma.label("sigma1"),
                chart1.c.mu.label("mu1"),
                charts.c.chart_id.label("chart2_id"),
                chart2.c.sigma.label("sigma2"),
                chart2.c.mu.label("mu2"),
            )\
            .filter("chart1_id < chart2_id")\
            .filter(tuple_("chart1_id", "chart2_id").notin_(current_tasks))\
            .join(chart1, charts.c.chart_id == chart1.id)\
            .join(chart2, charts.c.chart_id == chart2.id)\
            .order_by("RANDOM()")\
            .limit(1000)\
            .all()

        task_candidates = [t._asdict() for t in task_candidates]
        task_candidates = [
            (t["chart1_id"], t["chart2_id"],
             trueskill.quality_1vs1(trueskill.Rating(t["sigma1"], t["mu1"]),
                                    trueskill.Rating(t["sigma2"], t["mu2"])))
            for t in task_candidates
        ]

        selected_tasks = list(
            sorted(task_candidates, key=lambda x: x[2],
                   reverse=True))[:tasks_to_add]

        db_session.execute(Task.__table__.insert(), [{
            "survey_id": survey.id,
            "chart1_id": chart1_id,
            "chart2_id": chart2_id
        } for chart1_id, chart2_id, score in selected_tasks])

        db_session.commit()
    elif survey.type == SurveyType.SINGLE:
        charts = db_session\
            .query(chart_survey_association.c.chart_id.label("chart_id"))\
            .filter(chart_survey_association.c.survey_id == survey.id)\
            .subquery()
        tasked_charts = db_session\
            .query(Task.chart1_id)\
            .filter(Task.survey_id == survey.id)\
            .subquery
        untasked_charts = db_session\
            .query(charts.c.chart_id.label("chart1_id"), literal(survey.id).label("survey_id"))\
            .filter(charts.c.chart_id.notin_(tasked_charts))\
            .subquery()

        db_session.execute(Task.__table__.insert().from_select(
            ["chart1_id", "survey_id"], untasked_charts))
        db_session.commit()
    else:
        raise RuntimeError("Type of survey unknown")
