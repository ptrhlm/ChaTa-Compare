from typing import Optional
from datetime import datetime

from pydantic import BaseModel

from app.models.user import User
from app.models.task import Task


class Answer(BaseModel):
    id: Optional[int]
    task: Task
    chosen_chart: Optional[int]
    score: Optional[int]
    user: User
    created: datetime
