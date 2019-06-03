import { SurveyState } from './state';
import { getStoreAccessors } from 'typesafe-vuex';
import { State } from '../state';
import { IChart } from "@/interfaces/chart";

export const mutations = {
    clearChartsInTask(state: SurveyState) {
        state.chartsInTask = [];
    },
    addChartInTask(state: SurveyState, payload: IChart) {
        state.chartsInTask.push(payload);
    },
};

const { commit } = getStoreAccessors<SurveyState, State>('');

export const commitAddChartInTask = commit(mutations.addChartInTask);
export const commitClearChartsInTask = commit(mutations.clearChartsInTask);
