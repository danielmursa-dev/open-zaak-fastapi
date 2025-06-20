from fastapi import FastAPI
from app.api.main import api_router
from app.core.config import settings

from fastapi_pagination import add_pagination

app = FastAPI(title=settings.PROJECT_NAME)
app.include_router(api_router)

add_pagination(app)
