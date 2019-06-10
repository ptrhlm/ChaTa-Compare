from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session

from app import crud
from app.api.api_v1.endpoints.chart import db_chart_to_model_chart
from app.api.utils.db import get_db
from app.api.utils.security import get_current_active_user
from app.db_models.user import User
from app.models.answer import Answer
from app.models.task import Task
from app.models.survey import Survey

router = APIRouter()


@router.get("/surveys/{survey_id}/tasks/next",
            tags=["survey", "task"],
            response_model=Task)
async def get_next_task(survey_id: int,
                        db: Session = Depends(get_db),
                        current_user: User = Depends(get_current_active_user)):
    """Get next task for user"""
    if crud.survey.is_participant(db, survey_id=survey_id, user=current_user):
        task = crud.survey.get_next_task(db,
                                         survey_id=survey_id,
                                         user=current_user)
        return Task(id=task.id,
                    chart1=db_chart_to_model_chart(task.chart1),
                    chart2=db_chart_to_model_chart(task.chart2),
                    survey=Survey(**task.survey.__dict__))
    else:
        raise HTTPException(
            status_code=403,
            detail="User does not have necessary permissions",
        )


@router.post("/surveys/{survey_id}//tasks/{task_id}/answers", tags=["survey", "task"])
async def save_answer(survey_id: int,
                      task_id: int,
                      answer: Answer,
                      db: Session = Depends(get_db),
                      current_user: User = Depends(get_current_active_user)):
    """Save user's answer for the task"""
    if crud.survey.is_participant(db, survey_id=survey_id, user=current_user):
        crud.survey.save_answer(db,
                                task_id=task_id,
                                score=answer.score,
                                chosen_chart=answer.chosen_chart,
                                user=current_user)
    else:
        raise HTTPException(
            status_code=403,
            detail="User does not have necessary permissions",
        )


@router.post("/surveys/{id}/tasks/{task_id}/report", tags=["survey", "task"])
async def report_task(id: int,
                      task_id: int,
                      db: Session = Depends(get_db),
                      current_user: User = Depends(get_current_active_user)):
    """Report task"""
    if crud.survey.is_participant(db, survey_id=id, user=current_user):
        crud.survey.save_report(db,
                                survey_id=id,
                                task_id=task_id,
                                user=current_user)
    else:
        raise HTTPException(
            status_code=403,
            detail="User does not have necessary permissions",
        )


@router.get("/surveys/{id}/tasks",
            tags=["survey", "task"],
            response_model=List[Task])
async def list_tasks(id: int,
                     skip: int = Path(0, ge=0),
                     limit: int = Path(100, gt=0, le=1000),
                     db: Session = Depends(get_db),
                     current_user: User = Depends(get_current_active_user)):
    """List tasks for current user"""
    if crud.survey.is_participant(db, survey_id=id, user=current_user):
        tasks = crud.survey.get_tasks(db,
                                      survey_id=id,
                                      skip=skip,
                                      limit=limit,
                                      user=current_user)
        return tasks
    else:
        raise HTTPException(
            status_code=403,
            detail="User does not have necessary permissions",
        )


@router.get("/surveys/{id}/tasks/{task_id}",
            tags=["survey", "task"],
            response_model=Task)
async def task_info(id: int,
                    task_id: int,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_active_user)):
    """Get task details"""
    if crud.survey.is_participant(db, survey_id=id, user=current_user):
        task = crud.survey.get_task(db,
                                    survey_id=id,
                                    task_id=task_id,
                                    user=current_user)
        return task
    else:
        raise HTTPException(
            status_code=403,
            detail="User does not have necessary permissions",
        )
