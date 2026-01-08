import api from "./api";

export const profile = async (setCurrentData) => {
  try {
    const res = await api.get("/profile");
    setCurrentData(res.data);
  } catch (error) {
    console.log(error);
  }
};
