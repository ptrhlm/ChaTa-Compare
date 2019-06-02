import { api } from '@/api';
import { ActionContext } from 'vuex';
import { State } from '../state';
import { SurveyState } from './state';
import { getStoreAccessors } from 'typesafe-vuex';
import { commitAddChartInTask, commitClearChartsInTask } from './mutations';
import { dispatchCheckApiError } from '../main/actions';

type MainContext = ActionContext<SurveyState, State>;

export const actions = {
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
            console.log(error);
            await dispatchCheckApiError(context, error);
        }
    }
};

const { dispatch } = getStoreAccessors<SurveyState, State>('');

export const dispatchLoadCharts = dispatch(actions.actionLoadChartsInTask);
export const dispatchLoadCurrentSurveys = dispatch(actions.actionLoadCurrentSurveys);

