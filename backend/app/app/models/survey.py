from enum import Enum
from typing import List

from pydantic import BaseModel

from app.models.user import User


class SurveyType(str, Enum):
    SINGLE = 'single'
    COMPARISON = 'comparison'


class SurveyStatus(str, Enum):
    OPEN = 'open'
    CLOSED = 'closed'


class SurveyBase(BaseModel):
    name: str
    description: str
    status: SurveyStatus
    type: SurveyType
    researcher: User
    answers_per_task: int
    tasks_per_chart: int
    exp_required: bool = False
    min_answers_quality: float = 0.0


class SurveyBaseInDB(SurveyBase):
    id: int


class Survey(SurveyBaseInDB):
    pass


class SurveySummary(BaseModel):
    pass  # TODO


class SurveyParticipant(BaseModel):
    participant: User
    answers: int
    experience: float = 0.0


class CreateSurvey(BaseModel):
    name: str
    description: str
    type: SurveyType
    answers_per_task: int
    tasks_per_chart: int
    exp_required: bool = False
    min_answers_quality: float = 0.0
