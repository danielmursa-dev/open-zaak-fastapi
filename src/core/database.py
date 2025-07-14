from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base

from .config import settings

engine = create_async_engine(
    str(settings.SQLALCHEMY_DATABASE_URI), echo=False, future=True
)

Base = declarative_base()
