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
    LoadingColumnConfig,
    DestinationTableConfig,
)


# revision identifiers, used by Alembic.
revision = "02798e54b562"
down_revision = "e2afd102cb2d"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_vectorizer(
        source="pages",
        name="pages_content_embedder",
        destination=DestinationTableConfig(
            destination='pages_embeddings',
        ),
        loading=LoadingColumnConfig(
            column_name='content',
        ),
        embedding=EmbeddingOllamaConfig(
            model=CONFIG.OLLAMA_EMBEDDING_MODEL,
            dimensions=768,
        ),
        chunking=ChunkingCharacterTextSplitterConfig(
            chunk_size=800,
            chunk_overlap=400,
            separator=".",
            is_separator_regex=False,
        ),
        formatting=FormattingPythonTemplateConfig(template="$title - $chunk"),
    )


def downgrade() -> None:
    op.drop_vectorizer(
        name="pages_content_embedder",
        drop_all=True,
    )
