from enum import Enum
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


class ChartType(str, Enum):
    AREA_PLOT = 'area_plot'
    BAR_PLOT = 'bar_plot'
    BOX_PLOT = 'box_plot'
    BUBBLE_CHART = 'bubble_chart'
    CHART = 'chart'
    COLUMN_PLOT = 'column_plot'
    DIAGRAM = 'diagram'
    DOT_PLOT = 'dot_plot'
    LINEAR_PLOT = 'linear_plot'
    OTHER_PLOT = 'other_plot'
    PARETO_CHART = 'pareto_chart'
    PIE_CHART = 'pie_chart'
    RADAR_PLOT = 'radar_plot'
    SCATTER_PLOT = 'scatter_plot'


class ChartBase(BaseModel):
    type: List[ChartType]
    title: Optional[str]
    x_axis_title: Optional[str]
    y_axis_title: Optional[str]
    description: Optional[str]


class ChartInDB(ChartBase):
    file_hash: str
    file_ext: str
    created: datetime


class ChartInCreate(ChartBase):
    file_name: str
    file_contents: str
    mimetype: str


class Chart(ChartBase):
    file_path: str
    created: datetime


class SearchParams(BaseModel):
    q: Optional[str] = None
    chart_types: Optional[List[ChartType]] = None
