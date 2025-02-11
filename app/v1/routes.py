import logging

import ollama
from fastapi import APIRouter, Depends

from app.common.database import get_session
from app.common.dependencies import is_valid
from app.v1.logic import create_page_content, create_user, get_all_users, get_user
from app.v1.schema import MessageSchema, PageSchema, Response, UserSchema
from config import CONFIG

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get(
    "/users",
    summary="Users endpoint",
    description="Users endpoint description",
    responses={"200": {"model": Response}},
    dependencies=[Depends(is_valid)],
)
async def get_all_users_handler(session=Depends(get_session)):
    logger.info("getting all users...")
    users = await get_all_users(session)
    return {"users": users}


@router.get(
    "/user/{user_id}",
    summary="User endpoint",
    description="User endpoint description",
    responses={"200": {"model": Response}},
    dependencies=[Depends(is_valid)],
)
async def get_user_handler(user_id, session=Depends(get_session)):
    logger.info("getting user...")
    user = await get_user(session, user_id)
    return {"user": user}


@router.post(
    "/users",
    summary="Create user endpoint",
    description="Create user endpoint description",
    responses={"200": {"model": Response}},
    dependencies=[Depends(is_valid)],
)
async def create_user_handler(user_payload: UserSchema, session=Depends(get_session)):
    logger.info("creating user...")
    user = await create_user(session, user_payload)
    return {"user": user.uuid}


@router.post(
    "/pages",
    summary="Create page endpoint",
    description="Create page endpoint description",
    responses={"200": {"model": Response}},
)
async def create_page_handler(page_payload: PageSchema, session=Depends(get_session)):
    logger.info("creating page content...")
    page = await create_page_content(session, page_payload)
    return {"page": page.uuid}


@router.post("/chat")
async def make_chat(payload: MessageSchema):
    logger.info("calling model: %s", CONFIG.OLLAMA_GENERATION_MODEL)

    chat_response: ollama.ChatResponse = ollama.chat(
        model=CONFIG.OLLAMA_GENERATION_MODEL,
        messages=[ollama.Message(role="user", content=payload.message)],
    )

    return {"response": chat_response.message.content}
