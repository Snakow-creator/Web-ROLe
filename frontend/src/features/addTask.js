import api from "../api";
import { getCSRFCookie } from "../hooks/getCookies";

export default async function addTask(formData) {
  try {
    const csrfToken = getCSRFCookie();
    const res = await api.post("/add/task", formData, {
      withCredentials: true,
      headers: {
        "Content-Type": "application/json",
        "X-CSRF-TOKEN": csrfToken,
      }
    });
    console.log(res)
    return res

  } catch (error) {
    console.error(error);
    return false
  }
};
