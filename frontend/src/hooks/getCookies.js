export function getCookie(cname) {
      const name = cname + "=";
      const decodedCookie = decodeURIComponent(document.cookie);
      const cookieArray = decodedCookie.split(';');

      for (let i = 0; i < cookieArray.length; i++) {
            let cookie = cookieArray[i];
            while (cookie.charAt(0) === ' ') {
                  cookie = cookie.substring(1);
            }
            if (cookie.indexOf(name) === 0) {
                  return cookie.substring(name.length, cookie.length);
            }
      }
      return "";
}

// Function to get CSRF token from cookie
export function getCSRFCookie() {
return getCookie("csrf_access_token");
}

// Function to get CSRF refresh token from cookie
export function getCSRFResfreshCookie() {
return getCookie("csrf_refresh_token");
}


