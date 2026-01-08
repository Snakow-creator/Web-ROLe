import decodeJWT from "../hooks/decodeJWT";


export function getAccessToken() {
  return localStorage.getItem("access_token");
}


export function getCSRFAccessToken() {
  const TOKEN = localStorage.getItem("access_token");
  if (!TOKEN) {
    console.warn("Access token not found");
  }
  try {
    const payload = decodeJWT(TOKEN);

    if (!payload || !payload.csrf) {
      console.warn("CSRF token not found in payload");
      return null
    }

    return payload.csrf
  } catch (e) {
    console.error("Failed to decode JWT or extract CSRF token");
  }
}

