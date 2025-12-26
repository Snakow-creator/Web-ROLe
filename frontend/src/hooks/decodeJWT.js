export default function decodeJWT(token) {
  if (!token) return null;
  try {
    const parts = token.split('.');
    if (parts.length !== 3) return null; // not is JWT

    const payloadBase64 = parts[1];

    // Обработка URL-safe base64 (JWT использует - и _ вместо + и /)
    const normalizedBase64 = payloadBase64
      .replace(/-/g, '+')
      .replace(/_/g, '/');

    // Добавляем padding (JWT иногда обрезает = в конце)
    const paddedBase64 = normalizedBase64 + '==='.slice((normalizedBase64.length % 4));

    const decoded = atob(paddedBase64);
    const payload = JSON.parse(decoded);

    console.log(payload)
    return payload;
  } catch (e) {
    console.error("Invalid token");
    return null;
  }
}
