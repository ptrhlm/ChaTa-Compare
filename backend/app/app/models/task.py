from datetime import datetime

from pydantic import BaseModel

from app.models.chart import Chart
from app.models.survey import Survey


class Task(BaseModel):
    id: int
    chart1: Chart
    chart2: Chart
    survey: Survey
    created: datetime
