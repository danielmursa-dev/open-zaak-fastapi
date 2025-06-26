import contextvars
from typing import Optional

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

request_contextvar: contextvars.ContextVar[Optional[Request]] = contextvars.ContextVar(
    "request", default=None
)


class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        token = request_contextvar.set(request)
        try:
            response = await call_next(request)
            return response
        finally:
            request_contextvar.reset(token)
