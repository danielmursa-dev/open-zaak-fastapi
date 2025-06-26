from fastapi import FastAPI
from fastapi_pagination import add_pagination

from src.api.router import api_router
from src.core.config import settings
from src.core.middleware import RequestContextMiddleware

app = FastAPI(title=settings.PROJECT_NAME)
app.include_router(api_router)

add_pagination(app)

app.add_middleware(RequestContextMiddleware)
