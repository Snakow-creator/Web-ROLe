import axios from "axios";

// create connection with backend
const api = axios.create({
  baseURL: "http://localhost:7878",
  withCredentials: true,
  headers: {
    "Content-Type": "application/json"
  },
});

export default api;
