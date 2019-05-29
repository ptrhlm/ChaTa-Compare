from pydantic import BaseModel

from app.models.survey import Survey


class Criterion(BaseModel):
    id: int
    name: str
    survey: Survey
