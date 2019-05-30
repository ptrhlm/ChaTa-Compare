import { SurveyState } from './state';
import { getStoreAccessors } from 'typesafe-vuex';
import { State } from '../state';

export const getters = {
    chartsInTask: (state: SurveyState) => state.chartsInTask,
};

const { read } = getStoreAccessors<SurveyState, State>('');

export const readChartsInTask = read(getters.chartsInTask);
