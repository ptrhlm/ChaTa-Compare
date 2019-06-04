from typing import Optional

from pydantic import BaseModel

from app.models.criterion import Criterion
from app.models.user import User
from app.models.task import Task


class Answer(BaseModel):
    id: int
    task: Task
    # criterion: Criterion

    # Only one of these is present at time
    answer: Optional[int]
    score: Optional[int]

    user: User
