import logging

import ollama
from fastapi import APIRouter, Depends

from app.common.dependencies import is_valid
from app.common.rag import render_from_template, retrieve_embeddings_for_page_query
from app.common.types import Session
from app.v1.logic import create_page_content, get_all_pages, get_page
from app.v1.schema import MessageSchema, PageSchema, Response
from config import CONFIG

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/pages",
    summary="Create page endpoint",
    description="Create page endpoint description",
    responses={"200": {"model": Response}},
)
async def create_page_handler(page_payload: PageSchema, session: Session):
    logger.info("creating page content...")
    page = await create_page_content(session, page_payload)
    return {"page": page.uuid}


@router.get(
    "/pages",
    summary="pages endpoint",
    description="pages endpoint description",
    responses={"200": {"model": Response}},
    dependencies=[Depends(is_valid)],
)
async def get_all_pages_handler(session: Session):
    logger.info("getting all pages...")
    pages = await get_all_pages(session)
    return {"pages": pages}


@router.get(
    "/pages/{page_id}",
    summary="page endpoint",
    description="page endpoint description",
    responses={"200": {"model": Response}},
    dependencies=[Depends(is_valid)],
)
async def get_page_handler(page_id, session: Session):
    logger.info("getting page...")
    return await get_page(session, page_id)


@router.post("/chat")
async def make_chat(payload: MessageSchema, session: Session):
    logger.info("calling model: %s", CONFIG.OLLAMA_GENERATION_MODEL)

    similar_posts = await retrieve_embeddings_for_page_query(session, payload.message)
    logger.info("similar posts: %s", similar_posts)

    retrieved_text = "\n".join([post.chunk for post in similar_posts])

    ctx = {"question": payload.message, "retrieved_text": retrieved_text}

    chat_response: ollama.ChatResponse = ollama.chat(
        model=CONFIG.OLLAMA_GENERATION_MODEL,
        messages=[
            ollama.Message(
                role="user",
                content=render_from_template("page_prompt.j2", ctx),
            ),
        ],
    )

    return {"response": chat_response.message.content}
