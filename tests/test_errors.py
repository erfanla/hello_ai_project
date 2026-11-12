"""The error handlers turn service errors and unknown URLs into friendly pages."""

import pytest
from fastapi import APIRouter

from app.main import app
from app.services.errors import InvalidState, NotAllowed, NotFound, ServiceError

CASES = [
    ("not-found", NotFound, 404, "Not found"),
    ("not-allowed", NotAllowed, 403, "Not allowed"),
    ("invalid-state", InvalidState, 409, "Can&#39;t do that now"),
    ("service-error", ServiceError, 409, "Can&#39;t do that now"),  # fallback for the base class
]


@pytest.fixture(scope="module", autouse=True)
def throwaway_routes():
    """Add test-only routes that raise each error, then remove them."""
    router = APIRouter()
    for name, error_class, _, _ in CASES:

        def raise_error(error_class=error_class):
            raise error_class("secret internal detail")

        router.add_api_route(f"/_test/{name}", raise_error)

    routes_before = list(app.router.routes)
    app.include_router(router)
    yield
    app.router.routes[:] = routes_before


@pytest.mark.parametrize("name, error_class, status_code, title", CASES)
def test_full_page(client, name, error_class, status_code, title):
    response = client.get(f"/_test/{name}")

    assert response.status_code == status_code
    assert "<html" in response.text
    assert 'role="alert"' in response.text
    assert title in response.text
    assert "secret internal detail" not in response.text
    assert "Traceback" not in response.text


@pytest.mark.parametrize("name, error_class, status_code, title", CASES)
def test_htmx_fragment(client, name, error_class, status_code, title):
    response = client.get(f"/_test/{name}", headers={"HX-Request": "true"})

    assert response.status_code == status_code
    assert "<html" not in response.text
    assert 'role="alert"' in response.text
    assert title in response.text
    assert "secret internal detail" not in response.text


def test_unknown_url_full_page(client):
    response = client.get("/does-not-exist")

    assert response.status_code == 404
    assert "<html" in response.text
    assert "Not found" in response.text
    assert '"detail"' not in response.text


def test_unknown_url_htmx_fragment(client):
    response = client.get("/does-not-exist", headers={"HX-Request": "true"})

    assert response.status_code == 404
    assert "<html" not in response.text
    assert "Not found" in response.text
    assert '"detail"' not in response.text
