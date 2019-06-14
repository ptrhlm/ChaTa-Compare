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
from app.models.survey import SurveyInCreate, SurveyStatus, SurveySummary, SurveyType


def save_answer(db_session, *, task_id: int, score: Optional[int],
                chosen_chart: Optional[int], user: User) -> None:
    task = db_session\
        .query(Task)\
        .filter(Task.id == task_id)\
        .first()
    if not task:
        raise RuntimeError("No such task")
    survey = task.survey
    if survey.type == SurveyType.COMPARISON:
        answer = Answer(task_id=task_id,
                        chosen_chart_id=chosen_chart,
                        user_id=user.id)
        db_session.add(answer)

        answer_count = db_session\
            .query(Answer)\
            .filter(Answer.task_id == task.id)\
            .count()
        if answer_count >= survey.answers_per_task:
            answers = db_session\
                .query(
                    Answer.chosen_chart_id,
                    func.count(Answer.id).label("win_count")
                )\
                .filter(Answer.task_id == task_id)\
                .group_by(Answer.chosen_chart_id)\
                .order_by("win_count desc")\
                .all()
            if len(answers) != 2:
                pass  # TODO: warn
            answers = [a._asdict() for a in answers]
            draw = False
            if answers[0]['win_count']:
              pass  # TODO
        db_session.commit()
    elif survey.type == SurveyType.SINGLE:
        answer = Answer(task_id=task_id,
                        score=score,
                        user_id=user.id)
        db_session.add(answer)
        db_session.commit()
    else:
        raise RuntimeError("Type of survey unknown")
