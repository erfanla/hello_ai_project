"""App entry point: `uv run uvicorn app.main:app --reload`."""

import logging
import sys
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.routes import pages
from app.services.errors import InvalidState, NotAllowed, NotFound, ServiceError
from app.templating import templates

# Logging: stdout, one line per event.
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger("app")

STATIC_DIR = Path(__file__).parent / "static"

app = FastAPI(title="Hello AI project")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
app.include_router(pages.router)


# Each service error maps to one status code and one friendly message.
ERROR_PAGES: dict[type[ServiceError], tuple[int, str, str]] = {
    NotFound: (404, "Not found", "We couldn't find this page."),
    NotAllowed: (403, "Not allowed", "You can't do this."),
    InvalidState: (409, "Can't do that now", "This can't be done right now."),
}


@app.exception_handler(ServiceError)
async def service_error_handler(request: Request, exc: ServiceError):
    """Turn a service error into a page (or a fragment for HTMX requests)."""
    status_code, title, message = 409, "Can't do that now", "This can't be done right now."
    for error_type, page in ERROR_PAGES.items():
        if isinstance(exc, error_type):
            status_code, title, message = page
            break

    logger.info(
        "service_error type=%s status=%s path=%s",
        type(exc).__name__,
        status_code,
        request.url.path,
    )

    return render_error(request, status_code, title, message)


@app.exception_handler(StarletteHTTPException)
async def http_error_handler(request: Request, exc: StarletteHTTPException):
    """Unknown URLs and other HTTP errors get the same friendly page.

    We never show `exc.detail`: it may contain internal information.
    """
    if exc.status_code == 404:
        title, message = "Not found", "We couldn't find this page."
    else:
        title, message = "Something went wrong", "Please try again."
    logger.info("http_error status=%s path=%s", exc.status_code, request.url.path)
    response = render_error(request, exc.status_code, title, message)
    if exc.headers:
        response.headers.update(exc.headers)
    return response


def render_error(request: Request, status_code: int, title: str, message: str):
    """Full error page, or only the fragment for HTMX requests."""
    is_htmx = request.headers.get("HX-Request") == "true"
    template = "fragments/error.html" if is_htmx else "error.html"
    return templates.TemplateResponse(
        request,
        template,
        {"title": title, "message": message},
        status_code=status_code,
    )
