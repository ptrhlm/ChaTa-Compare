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

export interface ISurveySummary {
    id: number;
    name: string;
    answers: number;
    finished_tasks: number;
    active_users: number;
    end_date: string;
    status: ESurveyStatus;
}
export interface ICurrentSurvey {
    name: string;
    criterion: string;
    id: number;
}

export interface ISurveyDetails {
    name: string;
    description: string;
	criteria: string[];
    assessment: string;
    dataCharacteristics: string[];
}