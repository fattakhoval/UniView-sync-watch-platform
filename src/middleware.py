from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import jwt

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

class JWTAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        open_routes = {"/auth/login", "/auth/register"}
        if request.url.path in open_routes:
            return await call_next(request)

        token = request.cookies.get("access_token")
        if not token:
            return JSONResponse(status_code=401, content="Missing or invalid JWT token")

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            request.state.user_id = payload.get("user_id")
        except jwt.PyJWTError:
            return JSONResponse(status_code=401, content="Invalid token")
        except jwt.ExpiredSignatureError:
            return JSONResponse(status_code=401, content="Token expired")

        return await call_next(request)
