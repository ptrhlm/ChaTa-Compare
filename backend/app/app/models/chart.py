from enum import Enum
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
    type: ChartType
    title: Optional[str]
    x_axis_title: Optional[str]
    y_axis_title: Optional[str]
    description: Optional[str]


class ChartInDB(ChartBase):
    file_hash: str
    file_ext: str


class ChartInCreate(ChartBase):
    file_name: str
    file_contents: str
    mimetype: str


class Chart(ChartBase):
    file_path: str
    file_contents: Optional[str]


class SearchParams(BaseModel):
    q: str = None
    chart_types: Optional[List[ChartType]] = None
