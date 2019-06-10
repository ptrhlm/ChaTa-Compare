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
from app.models.survey import SurveyInCreate, SurveyStatus, SurveySummary, Ranking, SurveyType, RankingEntry

from .survey import get


def get_ranking(db_session, *, survey_id: int) -> Ranking:
    survey = get(db_session, survey_id=survey_id)
    if not survey:
        raise RuntimeError("Survey not found")

    if survey.type == SurveyType.COMPARISON:
        charts = db_session\
            .query(
                Chart,
                (chart_survey_association.c.sigma + 3 * chart_survey_association.c.mu).label("score")
            )\
            .filter(chart_survey_association.c.survey_id == survey.id)\
            .join(Chart, Chart.id == chart_survey_association.c.chart_id)\
            .order_by("score desc")\
            .all()
        return Ranking(
            survey=survey,
            ranking=[
                RankingEntry(
                    chart=Chart(**ch._asdict()),
                    score=ch.score)
                for ch in charts]
        )
    elif survey.type == SurveyType.SINGLE:
        scores = db_session\
            .query(Answer.task_id, func.avg(Answer.score).label("score"))\
            .group_by(Answer.task_id)\
            .subquery()

        charts = db_session\
            .query(Chart, func.coalesce(scores.c.score, 0.0))\
            .select_from(Task)\
            .filter(Task.survey_id == survey.id)\
            .join(Chart, Chart.id == Task.chart1_id)\
            .outerjoin(scores, scores.c.task_id == Task.id)\
            .all()

        return Ranking(
            survey=survey,
            ranking=[
                RankingEntry(
                    chart=Chart(**ch._asdict()),
                    score=ch.score
                ) for ch in charts
            ]
        )
    else:
        raise RuntimeError("Type of survey unknown")
