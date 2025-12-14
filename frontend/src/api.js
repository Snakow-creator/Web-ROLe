import axios from "axios";

// create connection with backend
const api = axios.create({
  baseURL: "http://127.0.0.1:7878",
  withCredentials: true,
  headers: {
    "Content-Type": "application/json"
  },
});

export default api;
