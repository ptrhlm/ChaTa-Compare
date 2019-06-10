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


def save_answer(db_session, *, task_id: int, score: Optional[int],
                chosen_chart: Optional[int], user: User) -> None:
    answer = Answer(task_id=task_id,
                    score=score,
                    chosen_chart=chosen_chart,
                    user_id=user.id)
    db_session.add(answer)
    db_session.commit()
