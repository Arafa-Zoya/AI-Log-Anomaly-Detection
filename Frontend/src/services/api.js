import axios from 'axios';

const API_BASE_URL = 'https://ai-log-anomaly-detection-rf9i.onrender.com';

const api = axios.create({
  baseURL: API_BASE_URL,
});

export const analyzeLogs = async (file) => {
  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await api.post('/analyze', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    console.error('Error analyzing logs:', error);
    throw error;
  }
};

export default api;
