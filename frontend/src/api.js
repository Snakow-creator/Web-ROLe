import axios from "axios";
import { getAccessToken, getCSRFAccessToken } from "./hooks/getTokens";


// create connection with backend
const api = axios.create({
  baseURL: "/api",
  withCredentials: true,
});

api.interceptors.request.use((config) => {
  const accessToken = getAccessToken();

  if (accessToken) {
    // Всегда добавляем Bearer токен
    config.headers.Authorization = `Bearer ${accessToken}`;

    // const CSRFToken = getCSRFAccessToken();
    // if (CSRFToken) {
    //   config.headers['X-CSRF-Token'] = CSRFToken
    // }
  }

  return config;
}, (error) => {
  return Promise.reject(error);
});

export default api;
