import api from '../api';

export default async function getAuth() {
  try {
    const res = await api.get("/protected");
    if (res.data.auth === true) {
      return true
    } else {
      return false
    }
  } catch {
    return false
  }
};
