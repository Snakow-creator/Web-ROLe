import api from '../api';
import { getAccessToken } from '../hooks/getTokens';

export default async function getAuth() {
  try {
    const accessToken = getAccessToken();

    if (!accessToken) {
      return {
        "message": "Access token not found",
        "auth": false,
        "expire": false
      }
    }

    const res = await api.get(`/protected`);
    console.warn(res)

    // if token is not expired
    if (!res.data.expire) {
      return {
        "message": res.data.message,
        "auth": res.data.auth,
        "expire": res.data.expire
      }
    } else {

      const res = await api.post("/refresh");

      console.warn(res)

      localStorage.removeItem('access_token');
      localStorage.setItem("access_token", res.data.access_token);

      console.log("refresh access_token")

      // reload page with new access token
      window.location.reload();
    }

  } catch (err) {
    console.error(err.response?.data || err.message);
  }
};
