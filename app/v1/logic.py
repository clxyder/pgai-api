import logging

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from fastapi.exceptions import RequestValidationError

from app.common.models import User
from app.v1.schema import UserSchema

logger = logging.getLogger(__name__)


async def get_all_users(session):
    user_results = await session.execute(select(User))
    return user_results.scalars().all()


async def get_user(session, user_id):
    query = select(User).where(User.uuid == user_id)

    try:
        user_result = await session.execute(query)
    except SQLAlchemyError as exc:
        if isinstance(exc.orig, ValueError):
            raise RequestValidationError("Invalid UUID provided") from exc
        logger.exception("%s", exc)
        raise

    user = user_result.scalar_one_or_none()

    if user is None:
        raise HTTPException(404, f"User with id '{user_id}' not found")

    return user


async def create_user(session, user_payload: UserSchema):
    user = User(**user_payload.model_dump())
    session.add(user)

    try:
        await session.commit()
        await session.refresh(user)

    except SQLAlchemyError as e:
        logger.exception("%s", e)
        raise

    return user
