export enum ESurveyStatus {
    Open = 'open',
    Closed = 'closed',
}

export enum ESurveyType {
    Single = 'single',
    Comparison = 'comparison',
}

export interface ISurveyCreate {
    name: string;
    description: string;
    status: ESurveyStatus;
    type: ESurveyType;
    criteria: string[];
    charts_ids: number[];
    answers_per_task: number;
    tasks_per_chart: number;
    exp_required: boolean;
    min_answers_quality: number;
}

export interface ISurvey {
    id: number;
    name: string;
    description: string;
    status: ESurveyStatus;
    type: ESurveyType;
    researcher_id: number;
    answers_per_task: number;
    tasks_per_chart: number;
    exp_required: boolean;
    min_answers_quality: number;
}
