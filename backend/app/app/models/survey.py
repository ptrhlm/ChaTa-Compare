from enum import Enum

from pydantic import BaseModel


class SurveyType(str, Enum):
    SINGLE = 'single'
    COMPARISON = 'comparison'


class SurveyStatus(str, Enum):
    OPEN = 'open'
    CLOSED = 'closed'


class Survey(BaseModel):
    pass  # TODO


class SurveySummary(BaseModel):
    pass  # TODO


class SurveyParticipant(BaseModel):
    pass  # TODO
