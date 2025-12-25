import api from "../api";

export default async function addTask(formData) {
  try {
    const res = await api.post("/add/task", formData);
    console.log(res)
    return res

  } catch (error) {
    console.error(error);
    return false
  }
};
