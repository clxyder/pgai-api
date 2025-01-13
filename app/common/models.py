from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy_utils import UUIDType

from app.common.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    uuid = Column(UUIDType(), unique=True, index=True, nullable=False, default=uuid4)
    name = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
