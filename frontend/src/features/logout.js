import api from "../api";

export default function useLogout() {
    const res = api.post("/logout");
    localStorage.removeItem('refresh_token');
    return res
}

