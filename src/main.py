from fastapi import FastAPI
from src.api.router import api_router
from src.core.middleware import RequestContextMiddleware
from src.core.config import settings

from fastapi_pagination import add_pagination

app = FastAPI(title=settings.PROJECT_NAME)
app.include_router(api_router)

add_pagination(app)

app.add_middleware(RequestContextMiddleware)
