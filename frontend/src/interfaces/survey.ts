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