import api from "../api";
import { getCSRFCookie, getCookie } from "../components/GetCookies";

export default function useLogout() {
    const csrfToken = getCSRFCookie();
    const TOKEN = getCookie("my_access_token");
    const res = api.post("/logout", {}, {
      withCredentials: true,
      headers: {
        "Content-Type": "application/json",
        "X-CSRF-TOKEN": csrfToken,
        "Authorization": `Bearer ${TOKEN}`
      }
    });
    return res
}

