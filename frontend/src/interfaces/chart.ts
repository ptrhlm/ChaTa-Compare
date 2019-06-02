export enum EChartType {
    AREA_PLOT = 'area_plot',
    BAR_PLOT = 'bar_plot',
    BOX_PLOT = 'box_plot',
    BUBBLE_CHART = 'bubble_chart',
    CHART = 'chart',
    COLUMN_PLOT = 'column_plot',
    DIAGRAM = 'diagram',
    DOT_PLOT = 'dot_plot',
    LINEAR_PLOT = 'linear_plot',
    OTHER_PLOT = 'other_plot',
    PARETO_CHART = 'pareto_chart',
    PIE_CHART = 'pie_chart',
    RADAR_PLOT = 'radar_plot',
    SCATTER_PLOT = 'scatter_plot',
}

export interface IChart {
    type: EChartType;
    title: string;
    x_axis_title: string;
    y_axis_title: string;
    description: string;
    file_path: string;
    file_contents: string;
}
