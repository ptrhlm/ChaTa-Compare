import { mutations } from './mutations';
import { getters } from './getters';
import { actions } from './actions';
import { SurveyState } from './state';

const defaultState: SurveyState = {
  chartsInTask: [],
};

export const surveyModule = {
  state: defaultState,
  mutations,
  actions,
  getters,
};
