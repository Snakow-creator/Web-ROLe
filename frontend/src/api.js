import axios from "axios";

// create connection with backend
const api = axios.create({
  baseURL: "/api",
  withCredentials: true,
  headers: {
    "Content-Type": "application/json"
  },
});

export default api;
