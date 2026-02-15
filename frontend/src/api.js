import axios from "axios";

const API = "http://localhost:8000";

export const sendMessage = async (message) => {
  const res = await axios.post(`${API}/agent`, { message });
  return res.data;
};

export const rollback = async () => {
  const res = await axios.post(`${API}/rollback`);
  return res.data;
};

export const clearHistory = async () => {
  await axios.post(`${API}/clear`);
};
