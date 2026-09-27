import axios from 'axios';

// Get base URL from environment or default to relative '/api' path
let rawBaseURL = import.meta.env.VITE_API_URL || '/api';

// Normalize base URL so it cleanly ends with '/api' without double or missing slashes
rawBaseURL = rawBaseURL.replace(/\/+$/, '');
if (!rawBaseURL.endsWith('/api')) {
  rawBaseURL += '/api';
}

const API = axios.create({
  baseURL: rawBaseURL
});

// Interceptor to attach JWT token to headers if present in localStorage
API.interceptors.request.use((config) => {
  const token = localStorage.getItem('gyaansetu_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, (error) => {
  return Promise.reject(error);
});

export default API;
