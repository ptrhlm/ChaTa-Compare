import logging
from typing import Any, List, Optional

from app.db_models.answer import Answer
from app.db_models.associations import survey_user_association, chart_survey_association
from app.db_models.chart import Chart
from app.db_models.criterion import Criterion
from app.db_models.survey import Survey
from app.db_models.task import Task
from app.db_models.user import User
from app.models.survey import SurveyInCreate, SurveyStatus
from sqlalchemy import func, case


def get(db_session, *, survey_id: int) -> Optional[Survey]:
    return db_session.query(Survey).filter(Survey.id == survey_id).first()


def get_multi(db_session, *, skip=0, limit=100) -> List[Optional[Survey]]:
    return db_session.query(Survey).offset(skip).limit(limit).all()


def get_current_multi(db_session, *, skip=0, limit=100) -> List[Optional[Survey]]:
    return db_session.query(Survey)\
        .filter(Survey.status == SurveyStatus.OPEN)\
        .offset(skip)\
        .limit(limit)\
        .all()


def create(db_session, *, survey_in: SurveyInCreate,
           researcher: User) -> Survey:
    survey = Survey(name=survey_in.name,
                    description=survey_in.description,
                    status=survey_in.status,
                    type=survey_in.type,
                    researcher=researcher,
                    answers_per_task=survey_in.answers_per_task,
                    tasks_per_chart=survey_in.tasks_per_chart,
                    exp_required=survey_in.exp_required,
                    min_answers_quality=survey_in.min_answers_quality)
    db_session.add(survey)
    db_session.flush()
    db_session.refresh(survey)

    criterion = []
    for criterion_name in survey_in.criteria:
        criterion.append(Criterion(name=criterion_name, survey=survey))
    db_session.add_all(criterion)

    chart_survey_associations = [{
        'chart_id': chart_id,
        'survey_id': survey.id
    } for chart_id in survey_in.charts_ids]
    chart_survey_association_insert = chart_survey_association.insert().values(
        chart_survey_associations)

    db_session.execute(chart_survey_association_insert)
    db_session.commit()
    db_session.refresh(survey)

    survey_id = survey.id
    db_session.execute(
        Task.__table__.insert(),
        [{
            "survey_id": survey_id,
            "chart1_id": chart1_id,
            "chart2_id": chart2_id
        } for chart1_id in survey_in.charts_ids
         for chart2_id in survey_in.charts_ids if chart1_id < chart2_id
         ])  # Yeah, it's quadratic. Choose your data structures better, kids
    db_session.commit()
    db_session.refresh(survey)
    return survey


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
    return db_session.query(Chart)\
        .with_parent(survey)\
        .count()


def close(db_session, *, survey: Survey) -> Survey:
    survey.status = SurveyStatus.CLOSED
    db_session.add(survey)
    db_session.commit()
    db_session.refresh(survey)
    return survey


def get_participants(db_session, *, survey: Survey, skip=0,
                     limit=100) -> List[Optional[Any]]:
    return survey.participants.offset(skip).limit(limit).all()


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
    return result


def get_criterion(db_session, *, criterion_id: int) -> Optional[Criterion]:
    return db_session.query(Criterion)\
        .filter(Criterion.id == criterion_id)\
        .first()


def get_criteria(db_session, *, survey_id: int, skip=0, limit=100) -> List[Criterion]:
    return db_session.query(Criterion)\
        .filter(Criterion.survey_id == survey_id)\
        .offset(skip)\
        .limit(limit)\
        .all()


def get_tasks(db_session, *, survey_id: int, user: User, skip=0,
              limit=100) -> List[Optional[Task]]:
    return db_session.query(Task).where(
        Task.survey_id == survey_id).offset(skip).limit(limit).all()


def get_task(db_session, *, survey_id: int, task_id: int, user: User) -> Task:
    return db_session.query(Task).where(Task.survey_id == survey_id).where(
        Task.id == task_id).first()


def get_next_task(db_session, *, survey_id: int,  criterion_id: int,
                  user: User) -> Task:
    survey = get(db_session, survey_id=survey_id)
    subquery = db_session.query(
        Answer.task_id,
        func.count(Answer.id).label("task_num"),
        func.sum(case([(Answer.user_id == user.id, 1)], else_=0)).label("checked")
    ).select_from(Answer) \
        .filter(Answer.criterion_id == criterion_id)\
        .group_by("task_id")\
        .subquery()
    task = db_session.query(Task) \
        .outerjoin(subquery)\
        .filter(Task.survey_id == survey_id).filter(
        ((subquery.c.task_num < survey.answers_per_task) | (subquery.c.task_num == None)) &
        ((subquery.c.checked == 0) | (subquery.c.checked == None))
    ).first()
    return task


def save_answer(db_session, *, criterion_id: int, task_id: int,
                score: int, user: User) -> None:
    answer = Answer(task_id=task_id,
                    criterion_id=criterion_id,
                    score=score,
                    user_id=user.id)
    db_session.add(answer)
    db_session.commit()


def save_report(db_session, *, survey_id: int, task_id: int,
                user: User) -> None:
    raise NotImplementedError()  # TODO: later
