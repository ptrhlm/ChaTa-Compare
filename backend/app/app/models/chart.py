from enum import Enum
from typing import Optional

from pydantic import BaseModel


class ChartType(str, Enum):
    AREA_GRAPH = 'area_graph'
    BAR_GRAPH = 'bar_graph'
    BOX_PLOT = 'box_plot'
    BUBBLE_CHART = 'bubble_chart'
    COLUMN_GRAPH = 'column_graph'
    LINE_GRAPH = 'line_graph'
    PARETO_CHART = 'pareto_chart'
    PIE_CHART = 'pie_chart'
    RADAR_PLOT = 'radar_plot'
    SCATTER_GRAPH = 'scatter_graph'


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


class Chart(ChartBase):
    file_path: str
