import axios from "axios";

const BASE_URL = import.meta.env.VITE_API_URL || "/api";

const client = axios.create({ baseURL: BASE_URL, timeout: 8000 });

client.interceptors.request.use((config) => {
  const token = localStorage.getItem("freezer_token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

client.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err.response?.status === 401) {
      localStorage.removeItem("freezer_token");
      window.location.href = "/login";
    }
    return Promise.reject(err);
  }
);

export default client;
