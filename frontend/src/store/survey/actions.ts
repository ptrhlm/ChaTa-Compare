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
};

const { dispatch } = getStoreAccessors<SurveyState, State>('');

export const dispatchLoadCharts = dispatch(actions.actionLoadChartsInTask);
