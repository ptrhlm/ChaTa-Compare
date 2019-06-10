from datetime import datetime
from enum import Enum
from typing import List, Optional

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
    researcher_id: int
    answers_per_task: int
    tasks_per_chart: int
    exp_required: bool = False
    min_answers_quality: float = 0.0
    created: datetime
    deadline: Optional[datetime]


class SurveyBaseInDB(SurveyBase):
    id: int


class Survey(SurveyBaseInDB):
    pass


class Ranking(BaseModel):
    pass  # TODO


class SurveySummary(BaseModel):
    id: int
    name: str
    answers: int
    finished_tasks: int
    active_users: int
    end_date: datetime
    status: SurveyStatus


class SurveyStatistics(BaseModel):
    survey: Survey
    ranking: Ranking


class SurveyParticipant(BaseModel):
    participant: User
    answers: int
    experience: float = 0.0


class SurveyParticipantIds(BaseModel):
    participant_ids: List[int]


class SurveyInCreate(BaseModel):
    name: str
    description: str
    status: SurveyStatus
    type: SurveyType
    charts_ids: List[int]
    answers_per_task: int
    tasks_per_chart: int
    exp_required: bool = False
    min_answers_quality: float = 0.0
    deadline: Optional[datetime]


class CurrentSurvey(BaseModel):
    id: int
    name: str


class SurveyDetails(BaseModel):
    name: str
    description: str
    type: SurveyType
    data_characteristics: List[str]
    current_user_participant: bool
