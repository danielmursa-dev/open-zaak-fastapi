from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from src.core.database import engine


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]
