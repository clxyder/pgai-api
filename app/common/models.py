from pgai.sqlalchemy import vectorizer_relationship
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.common.database import BaseDbModel


class User(BaseDbModel):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String(50))


class Page(BaseDbModel):
    __tablename__ = "pages"

    title: Mapped[str]
    content: Mapped[str]

    # Add vector embeddings for the content field
    content_embeddings = vectorizer_relationship(
        dimensions=768, target_table="pages_embeddings"
    )
