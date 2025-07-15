import contextvars
import inspect
from functools import wraps
from typing import Optional

from fastapi import Request
from pyinstrument import Profiler
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


def profile_html(filename_prefix="profile"):
    def decorator(func):
        if inspect.iscoroutinefunction(func):

            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                profiler = Profiler()
                profiler.start()

                result = await func(*args, **kwargs)

                profiler.stop()
                _save_profile(profiler, filename_prefix, func.__name__)
                return result

            return async_wrapper
        else:

            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                profiler = Profiler()
                profiler.start()

                result = func(*args, **kwargs)

                profiler.stop()
                _save_profile(profiler, filename_prefix, func.__name__)
                return result

            return sync_wrapper

    return decorator


def _save_profile(profiler: Profiler, prefix: str, func_name: str):
    filename = f"{prefix}_{func_name}.html"
    with open(filename, "w") as f:
        f.write(profiler.output_html())
