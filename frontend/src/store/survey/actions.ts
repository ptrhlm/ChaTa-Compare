import { api } from '@/api';
import { ActionContext } from 'vuex';
import { State } from '../state';
import { SurveyState } from './state';
import { getStoreAccessors } from 'typesafe-vuex';
import { commitAddChartInTask, commitClearChartsInTask } from './mutations';
import { dispatchCheckApiError } from '../main/actions';
import { commitAddNotification, commitRemoveNotification } from "@/store/main/mutations";
import { ISurveyCreate } from "@/interfaces/survey";
import { IChartSearchParams } from "@/interfaces/chart";
import { IAnswer } from "@/interfaces/answer";

type MainContext = ActionContext<SurveyState, State>;

export const actions = {
    async actionCreateSurvey(context: MainContext, payload: ISurveyCreate) {
        try {
            const loadingNotification = { content: 'saving', showProgress: true };
            commitAddNotification(context, loadingNotification);
            const response = (await Promise.all([
                api.createSurvey(context.rootState.main.token, payload),
                await new Promise((resolve, reject) => setTimeout(() => resolve(), 500)),
            ]))[0];
            commitRemoveNotification(context, loadingNotification);
            commitAddNotification(context, { content: 'Survey successfully created', color: 'success' });
            return response.data
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }
    },
    async actionGetSurveySummaries(context: MainContext, payload: { userId: number }) {
        try {
            const response = await api.getSurveySummaries(context.rootState.main.token);
            if (response) {
                return response.data
            }
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }
    },
    async actionSearchChartIds(context: MainContext, payload: IChartSearchParams) {
        return await callApi(context, api.searchChartIds, payload);
    },
    async actionGetChart(context: MainContext, payload: { chartId: number }) {
        return await callApi(context, api.getChart, payload.chartId)
    },
    async actionLoadChartsInTask(context: MainContext, payload: { chartIds: number[] }) {
        commitClearChartsInTask(context);
        try {
            for (const chartId of payload.chartIds) {
                const response = await api.getChart(context.rootState.main.token, chartId);
                if (response) {
                    commitAddChartInTask(context, response.data);
                }
            }
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }
    },
    async actionLoadCurrentSurveys(context: MainContext) {
        try {
            const response = await api.getCurrentSurveys(context.rootState.main.token);
            if (response) {
                return response.data;
            }
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }
    },
    async actionGetSurveyDetails(context: MainContext, payload: { surveyId: number}) {
        try {
            const response = await api.getSurveyDetails(context.rootState.main.token, payload.surveyId);
            if (response) {
                return response.data;
            }
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }
    },
    async actionJoinSurvey(context: MainContext, payload: { surveyId: number, userId: number }) {
        return await callApi(context, api.joinSurvey, payload.surveyId, payload.userId)
    },
    async actionGetNextTask(context: MainContext, payload: { surveyId: number}) {
        return await callApi(context, api.getNextTask, payload.surveyId)
    },
    async actionSaveAnswer(context: MainContext,
                           payload: { surveyId: number, taskId: number, data: IAnswer }) {
        await callApi(context, api.saveAnswer, payload.surveyId, payload.taskId, payload.data)
    },
};

async function callApi(context: MainContext, apiFunc, ...args) {
    try {
        const response = await apiFunc(context.rootState.main.token, ...args);
        if (response) {
            return response.data;
        }
    } catch (error) {
        await dispatchCheckApiError(context, error);
    }
}

const { dispatch } = getStoreAccessors<SurveyState, State>('');

export const dispatchCreateSurvey = dispatch(actions.actionCreateSurvey);
export const dispatchGetSurveySummaries = dispatch(actions.actionGetSurveySummaries);
export const dispatchSearchChartIds = dispatch(actions.actionSearchChartIds);
export const dispatchGetChart = dispatch(actions.actionGetChart);
export const dispatchLoadCharts = dispatch(actions.actionLoadChartsInTask);
export const dispatchLoadCurrentSurveys = dispatch(actions.actionLoadCurrentSurveys);
export const dispatchGetSurveyDetails = dispatch(actions.actionGetSurveyDetails);
export const dispatchJoinSurvey = dispatch(actions.actionJoinSurvey);
export const dispatchGetNextTask = dispatch(actions.actionGetNextTask);
export const dispatchSaveAnswer = dispatch(actions.actionSaveAnswer);
