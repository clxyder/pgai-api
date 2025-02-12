from sqlalchemy import func, select
from config import CONFIG

from app.common.models import Page


async def retrieve_embeddings_for_page_query(session, query: str, limit: int = 5):
    stmt = (
        select(Page.content_embeddings)
        .order_by(
            Page.content_embeddings.embedding.cosine_distance(
                func.ai.ollama_embed(
                    CONFIG.OLLAMA_EMBEDDING_MODEL,
                    query,
                )
            )
        )
        .limit(limit)
    )
    results = await session.execute(stmt)
    return results.scalars().all()
