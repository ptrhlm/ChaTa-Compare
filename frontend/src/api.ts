import axios from 'axios';
import { apiUrl } from '@/env';
import { IUserProfile, IUserProfileCreate, IUserProfileUpdate } from './interfaces';
import { ISurvey, ISurveyCreate, ISurveySummary, ICurrentSurvey, ISurveyDetails } from "@/interfaces/survey";
import { IChart, IChartSearchParams } from "@/interfaces/chart";

function authHeaders(token: string) {
  return {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  };
}

export const api = {
  async logInGetToken(username: string, password: string) {
    const params = new URLSearchParams();
    params.append('username', username);
    params.append('password', password);

    return axios.post(`${apiUrl}/api/v1/login/access-token`, params);
  },
  async getMe(token: string) {
    return axios.get<IUserProfile>(`${apiUrl}/api/v1/users/me`, authHeaders(token));
  },
  async updateMe(token: string, data: IUserProfileUpdate) {
    return axios.put<IUserProfile>(`${apiUrl}/api/v1/users/me`, data, authHeaders(token));
  },
  async getUsers(token: string) {
    return axios.get<IUserProfile[]>(`${apiUrl}/api/v1/users/`, authHeaders(token));
  },
  async updateUser(token: string, userId: number, data: IUserProfileUpdate) {
    return axios.put(`${apiUrl}/api/v1/users/${userId}`, data, authHeaders(token));
  },
  async createUser(token: string, data: IUserProfileCreate) {
    return axios.post(`${apiUrl}/api/v1/users/`, data, authHeaders(token));
  },
  async passwordRecovery(email: string) {
    return axios.post(`${apiUrl}/api/v1/password-recovery/${email}`);
  },
  async resetPassword(password: string, token: string) {
    return axios.post(`${apiUrl}/api/v1/reset-password/`, {
      new_password: password,
      token,
    });
  },
  async createSurvey(token: string, data: ISurveyCreate) {
    return axios.post<ISurvey>(`${apiUrl}/api/v1/surveys`, data, authHeaders(token));
  },
  async getSurveySummaries(token: string, userId: number) {
    return axios.get<ISurveySummary[]>(`${apiUrl}/api/v1/surveys/summary?userId=${userId}`, authHeaders(token));
  },
  async searchChart(token: string, data: IChartSearchParams) {
    return axios.post<number[]>(`${apiUrl}/api/v1/charts/search`, data, authHeaders(token));
  },
  async getChart(token: string, chartId: number) {
    return axios.get<IChart>(`${apiUrl}/api/v1/charts/${chartId}`, authHeaders(token));
  },
  async getCurrentSurveys(token: string) {
    return axios.get<ICurrentSurvey[]>(`${apiUrl}/api/v1/surveys/current`, authHeaders(token));
  },
  async getSurveyDetails(token: string, survey_id: number) {
    return axios.get<ISurveyDetails>(`${apiUrl}/api/v1/surveys/${survey_id}/details`, authHeaders(token));
  }
};
