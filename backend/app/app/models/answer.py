from typing import Optional
from datetime import datetime

from pydantic import BaseModel

from app.models.criterion import Criterion
from app.models.user import User
from app.models.task import Task


class Answer(BaseModel):
    id: Optional[int]

    # Only one of these is present at time
    decision: Optional[int]
    score: Optional[int]
    created: datetime
