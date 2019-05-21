from typing import Optional

from pydantic import BaseModel

from app.enums.chart_type import ChartType


class ChartBase(BaseModel):
    file_name: str
    type: ChartType
    title: Optional[str]
    x_axis_title: Optional[str]
    y_axis_title: Optional[str]
    description: Optional[str]


class ChartInCreate(ChartBase):
    pass
