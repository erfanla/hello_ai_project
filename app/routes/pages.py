"""Simple pages that need no login."""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.templating import templates

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def hello(request: Request):
    return templates.TemplateResponse(request, "hello.html")
