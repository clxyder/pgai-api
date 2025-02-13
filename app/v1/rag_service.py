from sqlalchemy import func, select
from config import CONFIG

from app.common.models import Page


async def retrieve_embeddings_for_page_query(
    session, query: str, limit: int = 5, similarity_threshold: float = 0.5
):
    embedding_query = func.ai.ollama_embed(CONFIG.OLLAMA_EMBEDDING_MODEL, query)
    similarity_score = Page.content_embeddings.embedding.cosine_distance(
        embedding_query
    )
    stmt = (
        select(Page.content_embeddings)
        .filter(similarity_score < similarity_threshold)
        .order_by(similarity_score)
        .limit(limit)
    )
    results = await session.execute(stmt)
    return results.scalars().all()
