"""empty message

Revision ID: 02798e54b562
Revises: e2afd102cb2d
Create Date: 2025-02-10 21:36:25.572736

"""

from alembic import op
from config import CONFIG
from pgai.vectorizer.configuration import (
    EmbeddingOllamaConfig,
    ChunkingCharacterTextSplitterConfig,
    FormattingPythonTemplateConfig,
)


# revision identifiers, used by Alembic.
revision = "02798e54b562"
down_revision = "e2afd102cb2d"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_vectorizer(
        source="pages",
        target_table="pages_embeddings",
        embedding=EmbeddingOllamaConfig(
            model=CONFIG.OLLAMA_EMBEDDING_MODEL, dimensions=768
        ),
        chunking=ChunkingCharacterTextSplitterConfig(
            chunk_column="content",
            chunk_size=800,
            chunk_overlap=400,
            separator=".",
            is_separator_regex=False,
        ),
        formatting=FormattingPythonTemplateConfig(template="$title - $chunk"),
    )


def downgrade() -> None:
    op.drop_vectorizer(target_table="pages_embeddings", drop_all=True)
