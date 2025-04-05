export default function parseJwt(token) {
    const base64Url = token.split('.')[1];  // Берем payload
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');  // Преобразуем в стандартный Base64
    const jsonPayload = decodeURIComponent(atob(base64).split('').map(function (c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));

    return JSON.parse(jsonPayload);  // Возвращаем данные как объект
}