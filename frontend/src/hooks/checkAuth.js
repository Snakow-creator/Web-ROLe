import api from '../api';
import { getCookie } from './getCookies';

export default async function getAuth(csrfToken) {
  try {
    const res = await api.post("/protected", {}, {
      withCredentials: true,
      headers: {
        "Content-Type": "application/json",
        "X-CSRF-TOKEN": csrfToken,
      }
    });
    // // if token is not expired
    // if (!res.data.expire) {
    //   return {
    //     "message": res.data.message,
    //     "auth": res.data.auth,
    //     "expire": res.data.expire
    //   }
    // } else {
    //   await api.post("/refresh", {
    //     refresh_token: getCookie("my_refresh_token")
    //   }, {
    //     withCredentials: true,
    //     headers: {
    //       "Content-Type": "application/json",
    //       "X-CSRF-TOKEN": csrfToken,
    //       "refresh_token": getCookie("my_refresh_token")
    //     }
    //   });

    return {
      "message": res.data.message,
      "auth": res.data.auth,
      "expire": res.data.expire
    };

  } catch (error) {
    console.error(error);
    return {"message": "error", "auth": false}
  }
};
