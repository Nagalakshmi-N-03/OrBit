import api from './axiosConfig';

export const generateApp = async (prompt, mode = 'balanced') => {
  const response = await api.post('/api/generator/generate', {
    prompt,
    mode
  });
  return response.data;
};

export const getHistory = async () => {
  const response = await api.get('/api/generator/history');
  return response.data;
};