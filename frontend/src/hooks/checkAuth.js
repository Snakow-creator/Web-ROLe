import api from '../api';
import { getCookie, getCSRFCookie } from './getCookies';

export default async function getAuth() {
  try {
    const TOKEN = getCookie("my_access_token");
    const res = await api.get("/protected", {}, {
      withCredentials: true,
      headers: {
        "Authorization": `Bearer ${TOKEN}`,
      }
    });

    // if token is not expired
    if (!res.data.expire) {
      return {
        "message": res.data.message,
        "auth": res.data.auth,
        "expire": res.data.expire
      }
    } else {
      const csrfResfreshToken = getCSRFCookie();

      await api.post("/refresh", {}, {
        withCredentials: true,
        headers: {
          "Content-Type": "application/json",
          "X-CSRF-TOKEN": csrfResfreshToken,
        },
      });
      // reload page with new access token
      window.location.reload();
    }

  } catch (err) {
    console.error(err.response?.data || err.message);
  }
};
