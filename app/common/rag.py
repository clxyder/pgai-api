from jinja2 import Environment, FileSystemLoader
from sqlalchemy import func, select

from app.common.models import Page
from config import CONFIG, PROMPT_TEMPLATES_DIR

_env_cache = Environment(
    loader=FileSystemLoader(str(PROMPT_TEMPLATES_DIR)), autoescape=True
)


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


def render_from_template(template_file: str, context) -> str:
    template_path = PROMPT_TEMPLATES_DIR / template_file
    if not template_path.exists():
        raise ValueError(f"Template not found: {template_path}")
    template = _env_cache.get_template(template_file)
    return template.render(context)
