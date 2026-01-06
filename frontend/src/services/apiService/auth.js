import api from './api';
import { getAccessToken } from '../../hooks/getTokens';

// check auth
// if auth=false, user is not auth
// if expire=true, token is expired, refresh it
export async function getAuth() {
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

    // if token is not expired
    if (!res.data.expire) {
      return {
        "message": res.data.message,
        "auth": res.data.auth,
        "expire": res.data.expire
      }
    } else {
      const res = await api.post("/refresh");

      localStorage.removeItem('access_token');
      localStorage.setItem("access_token", res.data.access_token);

      // reload page with new access token
      window.location.reload();
    }

  } catch (err) {
    console.error(err.response?.data || err.message);
  }
};


export const login = async (creds) => {
  try {
    const res = await api.post("/login", creds.formData);

    localStorage.setItem("access_token", res.data.access_token);
    window.location.href = "/";
  } catch (err) {
    console.error(err);
  }
}


export const logout = async (creds) => {
  const res = await api.post("/logout");

  localStorage.removeItem('access_token');
  creds.onFinish();

  return res
}
