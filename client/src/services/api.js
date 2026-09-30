import axios from 'axios';

// When accessed from a phone on LAN, the proxy won't work (proxy only works on localhost).
// So we need to detect if we're on localhost or a LAN IP and set the base URL accordingly.
const getBaseURL = () => {
  // Always use '/api' so Vite proxy seamlessly routes to backend on both desktop and mobile
  return '/api';
};

const getSocketURL = () => {
  // Use same origin so Socket.IO connects through Vite proxy on port 5173
  if (typeof window !== 'undefined') {
    return window.location.origin;
  }
  return 'http://localhost:5000';
};

export const SOCKET_URL = getSocketURL();

const api = axios.create({
  baseURL: getBaseURL(),
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor - add auth token if available
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('qflow_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor - handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('qflow_token');
      localStorage.removeItem('qflow_user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// ========== Auth API ==========
export const authAPI = {
  login: (credentials) => api.post('/auth/login', credentials),
  verify: () => api.get('/auth/verify'),
};

// ========== Tokens API ==========
export const tokenAPI = {
  create: (data) => api.post('/tokens', data),
  getAll: (params) => api.get('/tokens', { params }),
  getById: (id) => api.get(`/tokens/${id}`),
  call: (id, data) => api.post(`/tokens/${id}/call`, data),
  start: (id, data) => api.post(`/tokens/${id}/start`, data),
  complete: (id, data) => api.post(`/tokens/${id}/complete`, data),
  skip: (id, data) => api.post(`/tokens/${id}/skip`, data),
  transfer: (id, data) => api.post(`/tokens/${id}/transfer`, data),
};

// ========== Counters API ==========
export const counterAPI = {
  getAll: () => api.get('/counters'),
  create: (data) => api.post('/counters', data),
  update: (id, data) => api.put(`/counters/${id}`, data),
  delete: (id) => api.delete(`/counters/${id}`),
  callNext: (counterId) => api.post(`/counters/${counterId}/call-next`),
};

// ========== Services API ==========
export const serviceAPI = {
  getAll: (params) => api.get('/services', { params }),
  create: (data) => api.post('/services', data),
  update: (id, data) => api.put(`/services/${id}`, data),
  delete: (id) => api.delete(`/services/${id}`),
};

// ========== Queue API ==========
export const queueAPI = {
  getCurrent: () => api.get('/queue'),
};

// ========== Analytics API ==========
export const analyticsAPI = {
  get: () => api.get('/analytics'),
};

// ========== Prediction API ==========
export const predictionAPI = {
  predict: (data) => api.post('/prediction', data),
};

// ========== Health API ==========
export const healthAPI = {
  check: () => api.get('/health'),
};

export default api;
