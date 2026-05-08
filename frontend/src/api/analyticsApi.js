import api from './axiosConfig';

export const getMetrics = async () => {
  const response = await api.get('/api/analytics/metrics');
  return response.data;
};

export const getRecent = async () => {
  const response = await api.get('/api/analytics/recent');
  return response.data;
};

export const getEvaluationResults = async () => {
  const response = await api.get('/api/evaluation/results');
  return response.data;
};

export const runEvaluation = async (mode = 'balanced') => {
  const response = await api.post(`/api/evaluation/run?mode=${mode}`);
  return response.data;
};