import { SurveyState } from './state';
import { getStoreAccessors } from 'typesafe-vuex';
import { State } from '../state';

export const mutations = {
    clearChartsInTask(state: SurveyState) {
        state.chartsInTask = [];
    },
    addChartInTask(state: SurveyState, payload: Blob) {
        state.chartsInTask.push(payload);
    },
};

const { commit } = getStoreAccessors<SurveyState, State>('');

export const commitAddChartInTask = commit(mutations.addChartInTask);
export const commitClearChartsInTask = commit(mutations.clearChartsInTask);
