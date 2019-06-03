from datetime import date
from enum import Enum
from typing import List

from pydantic import BaseModel

from app.models.user import User

from typing import List


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
    researcher_id: int
    answers_per_task: int
    tasks_per_chart: int
    exp_required: bool = False
    min_answers_quality: float = 0.0


class SurveyBaseInDB(SurveyBase):
    id: int


class Survey(SurveyBaseInDB):
    pass


class SurveySummary(BaseModel):
    id: int
    name: str
    answers: int
    finished_tasks: int
    active_users: int
    end_date: date
    status: SurveyStatus


class SurveyParticipant(BaseModel):
    participant: User
    answers: int
    experience: float = 0.0


class SurveyInCreate(BaseModel):
    name: str
    description: str
    status: SurveyStatus
    type: SurveyType
    criteria: List[str]
    charts_ids: List[int]
    answers_per_task: int
    tasks_per_chart: int
    exp_required: bool = False
    min_answers_quality: float = 0.0

class CurrentSurvey(BaseModel):
    name: str
    id: int
    criterion: str
	
class SurveyDetails(BaseModel):
    name: str
    description: str
    criteria: List[str] = []
    assessment: str
    dataCharacteristics: List[str] = []
