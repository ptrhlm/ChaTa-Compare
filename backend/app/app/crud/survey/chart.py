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


def add_charts(db_session, *, survey: Survey, chart_ids: List[int]) -> None:
    survey_id = survey.id
    db_session.execute(chart_survey_association.insert(), [{
        "survey_id": survey_id,
        "chart_id": chart_id
    } for chart_id in chart_ids])


def remove_charts(db_session, *, survey: Survey, chart_ids: List[int]) -> None:
    survey_id = survey.id
    db_session.execute(chart_survey_association.delete().where(
        chart_survey_association.c.survey_id == survey_id).where(
            chart_survey_association.c.chart_id.in_(chart_ids)))


def get_charts_count(db_session, *, survey: Survey) -> int:
    count = db_session\
        .query(Chart)\
        .with_parent(survey)\
        .count()

    return count or 0
