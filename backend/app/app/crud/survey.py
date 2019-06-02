from typing import Any, List, Optional

from sqlalchemy import func

from app.db_models.criterion import Criterion
from app.db_models.survey import Survey
from app.db_models.task import Task
from app.db_models.user import User
from app.db_models.chart_survey_association import chart_survey_association
from app.db_models.survey_user_association import survey_user_association
from app.models.survey import CreateSurvey, SurveyStatus

def get(db_session, *, survey_id: int) -> Optional[Survey]:
    return db_session.query(Survey).filter(Survey.id == survey_id).first()


def get_multi(db_session, *, skip=0, limit=100) -> List[Optional[Survey]]:
    return db_session.query(Survey).offset(skip).limit(limit).all()

	
def getCurrent_multi(db_session, *, skip=0, limit=100) -> List[Optional[Survey]]:
    return db_session.query(Survey).filter(Survey.status == SurveyStatus.OPEN).offset(skip).limit(limit).all()	


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
    survey_id = survey.id
    db_session.execute(
        chart_survey_association.insert(), [
            {"survey_id": survey_id, "chart_id": chart_id} for chart_id in chart_ids
        ])


def remove_charts(db_session, *, survey: Survey, chart_ids: List[int]) -> None:
    survey_id = survey.id
    db_session.execute(
        chart_survey_association.delete().
        where(chart_survey_association.c.survey_id == survey_id).
        where(chart_survey_association.c.chart_id.in_(chart_ids))
    )


def close(db_session, *, survey: Survey) -> Survey:
    survey.status = SurveyStatus.CLOSED
    db_session.add(survey)
    db_session.commit()
    db_session.refress(survey)
    return survey


def get_participants(db_session, *, survey: Survey, skip=0,
                     limit=100) -> List[Optional[Any]]:
    return survey.participants.offset(skip).limit(limit).all()


def add_participants(db_session, *, survey: Survey,
                     participant_ids: List[int]) -> None:
    survey_id = survey.id
    db_session.execute(
        survey_user_association.insert(), [
            {"survey_id": survey_id, "user_id": user_id} for user_id in participant_ids
        ])


def remove_participants(db_session, *, survey: Survey,
                        participant_ids: List[int]) -> None:
    survey_id = survey.id
    db_session.execute(
        survey_user_association.delete().
        where(survey_user_association.c.survey_id == survey_id).
        where(survey_user_association.c.user_id.in_(participant_ids))
    )


def is_participant(db_session, *, survey_id: int, user: User) -> bool:
    result = db_session.query(survey_user_association) \
                       .select(func.count(survey_user_association.c.user_id) > 0) \
                       .where(survey_user_association.c.survey_id == survey_id) \
                       .where(survey_user_association.c.user_id == User.id).fetchone()
    return result

def get_criterions(db_session, *, survey_id: int, skip=0,
                     limit=100) -> List[str]:
    return db_session.query(Criterion).filter(Criterion.survey_id == survey_id).offset(skip).limit(limit).all()	

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
