import logging

from fastapi import APIRouter, FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException
from pgai import install

from app.common.exception_handlers import (
    custom_http_exception_handler,
    unhandled_exception_handler,
    validation_exception_handler,
)
from app.v1.routes import router as v1_router
from config import CONFIG

logger = logging.getLogger(__name__)

router = APIRouter()

# install pgai into database
install(db_url=CONFIG.PGAI_DATABASE_URL)

# Setup templates
templates = Jinja2Templates(directory="app/templates")


@router.get("/", include_in_schema=False)
def home():
    return RedirectResponse(url="/docs")


@router.get("/pages/create", response_class=HTMLResponse, include_in_schema=False)
async def render_page(request: Request):
    return templates.TemplateResponse("page_form.html", {"request": request})


def create_app():
    app = FastAPI(title="Gen AI LLM API", description="API for Gen AI LLM with Ollama")

    app.include_router(router)

    # version routers
    app.include_router(v1_router, prefix="/v1", tags=["v1"])

    # latest router
    app.include_router(v1_router, prefix="/latest", tags=["latest"])

    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(StarletteHTTPException, custom_http_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)

    # Mount static files
    app.mount("/static", StaticFiles(directory="app/static"), name="static")

    return app


app = create_app()
