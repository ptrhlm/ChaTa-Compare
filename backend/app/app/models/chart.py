from enum import Enum

from pydantic import BaseModel


class ChartType(str, Enum):
    AREA_GRAPH = 'area_graph'
    BAR_GRAPH = 'bar_graph'
    BOX_PLOT = 'box_plot'
    BUBBLE_CHART = 'bubble_chart'
    COLUMN_GRAPH = 'column_graph'
    LINE_GRAPH = 'line_graph'
    PARETO_CHART = 'pareto_graph'
    PIE_CHART = 'pie_chart'
    RADAR_PLOT = 'radar_plot'
    SCATTER_GRAPH = 'scatter_graph'


class Chart(BaseModel):
    pass  # TODO
