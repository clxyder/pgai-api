from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.database import get_session

Session = Annotated[AsyncSession, Depends(get_session)]
