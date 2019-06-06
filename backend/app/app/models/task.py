from app.models.chart import Chart
from app.models.survey import Survey
from pydantic import BaseModel


class Task(BaseModel):
    id: int
    chart1: Chart
    chart2: Chart
    survey: Survey
    criterion: str
