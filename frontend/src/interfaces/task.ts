import { IChart } from "@/interfaces/chart";
import { ISurvey } from "@/interfaces/survey";

export interface ITask {
    id: number;
    chart1: IChart;
    chart2: IChart;
    survey: ISurvey;
}
