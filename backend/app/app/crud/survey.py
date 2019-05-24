from typing import Any, List, Optional

from app.db_models.survey import Survey
from app.db_models.task import Task
from app.db_models.user import User
from app.models.survey import CreateSurvey


def get(db_session, *, survey_id: int) -> Optional[Survey]:
    return db_session.query(Survey).filter(Survey.id == survey_id).first()


def get_multi(db_session, *, skip=0, limit=100) -> List[Optional[Survey]]:
    return db_session.query(Survey).offset(skip).limit(limit).all()


def create(db_session, *, survey: CreateSurvey, researcher: User) -> Survey:
    survey = Survey(name=survey.name,
                    description=survey.description,
                    type=survey.type,
                    researcher=researcher,
                    answers_per_task=survey.answers_per_task,
                    tasks_per_chart=survey.tasks_per_chart,
                    exp_required=survey.exp_required,
                    min_answers_quality=survey.min_answers_quality)
    db_session.add(survey)
    db_session.commit()
    db_session.refresh(survey)
    return survey


def add_charts(db_session, *, survey: Survey, chart_ids: List[int]) -> None:
    raise NotImplementedError()  # TODO


def remove_charts(db_session, *, survey: Survey, chart_ids: List[int]) -> None:
    raise NotImplementedError()  # TODO


def close(db_session, *, survey: Survey) -> Survey:
    raise NotImplementedError()  # TODO


def get_participants(db_session, *, survey: Survey, skip=0,
                     limit=100) -> List[Optional[Any]]:
    raise NotImplementedError()  # TODO


def add_participants(db_session, *, survey: Survey,
                     participant_ids: List[int]) -> List[Optional[Any]]:
    raise NotImplementedError()  # TODO


def remove_participants(db_session, *, survey: Survey,
                        participant_ids: List[int]) -> List[Optional[Any]]:
    raise NotImplementedError()  # TODO


def is_participant(db_session, *, survey_id: int, user: User) -> bool:
    raise NotImplementedError()  # TODO


def get_tasks(db_session, *, survey_id: int, user: User, skip=0,
              limit=100) -> List[Optional[Task]]:
    raise NotImplementedError()  # TODO


def get_task(db_session, *, survey_id: int, task_id: int, user: User) -> Task:
    raise NotImplementedError()  # TODO


def get_next_task(db_session, *, survey_id: int, user: User) -> Task:
    raise NotImplementedError()  # TODO


def save_answer(db_session, *, survey_id: int, task_id: int, user: User,
                answer) -> None:
    raise NotImplementedError()  # TODO


def save_report(db_session, *, survey_id: int, task_id: int,
                user: User) -> None:
    raise NotImplementedError()  # TODO: later
