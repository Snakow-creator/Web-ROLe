import api from '../api';
import { getCookie, getCSRFCookie, getCSRFResfreshCookie } from './getCookies';

export default async function getAuth() {
  try {
    const res = await api.get("/protected");

    // if token is not expired
    if (!res.data.expire) {
      return {
        "message": res.data.message,
        "auth": res.data.auth,
        "expire": res.data.expire
      }
    } else {
      const csrfResfreshToken = getCSRFResfreshCookie();

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

  } catch (error) {
    console.error(error);
    return {"message": "error", "auth": false}
  }
};
