import logging

from fastapi import APIRouter, FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import RedirectResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.common.exception_handlers import (
    custom_http_exception_handler,
    unhandled_exception_handler,
    validation_exception_handler,
)
from app.v1.routes import router as v1_router

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/", include_in_schema=False)
def home():
    return RedirectResponse(url="/docs")


def create_app():
    app = FastAPI()

    app.include_router(router)

    # version routers
    app.include_router(v1_router, prefix="/v1", tags=["v1"])

    # latest router
    app.include_router(v1_router, prefix="/latest", tags=["latest"])

    return app


app = create_app()

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(StarletteHTTPException, custom_http_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)
