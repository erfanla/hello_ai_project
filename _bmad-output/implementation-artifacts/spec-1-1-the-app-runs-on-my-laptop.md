---
title: 'Story 1.1: The app runs on my laptop'
type: 'chore'
created: '2026-11-12'
status: 'done'
baseline_commit: 'NO_VCS'
route: 'dispatch'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad-output/implementation-artifacts/epic-1-context.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** There is no app yet: no project, no folders, no tests. Every later story needs a working base that follows the architecture rules.

**Approach:** Create the project by hand with uv (no starter template): pinned dependencies, the architecture's source tree, a base layout with the Notte Pura design tokens, one "hello" page at `/`, the shared error handler, Alembic with an empty first migration on SQLite in WAL mode, the shared `UTCDateTime` type, pytest and a git repository.

## Boundaries & Constraints

**Always:** Pin exact versions: fastapi==0.162.5, python-multipart==0.0.33, sqlmodel==0.0.49, alembic==1.20.1, jinja2==3.1.6, pwdlib[argon2]==0.3.1, itsdangerous==2.2.0, pydantic-settings==2.16.2, pywebpush==2.5.0, uvicorn==0.54.0; dev: pytest==9.2.0, httpx==0.28.1. HTMX 2.0.11 is a local file in `app/static/`. AD-1 layer rule: routes → services → models; nothing imports from `routes`. All settings come from env vars through `app/config.py`. Logging goes to stdout, one line per event.

**Never:** No tables or models for User, Group etc. (later stories). No `fly.toml` and no deploy (Story 1.2). No CSS framework, no JS build step. Don't touch `first.py`, `brainstorm-notes.md`, `_bmad/`, `_bmad-output/`, `.claude/`. No `create_all` outside tests. No git commit (only `git init`).

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Hello page | GET `/` | 200, full page with base layout, tokens, fonts, `htmx.min.js` | N/A |
| Service raises `NotFound` / `NotAllowed` / `InvalidState` | normal request | full 404 / 403 / 409 page in the layout, friendly text, no stack trace | one handler in `main.py` |
| Same, HTMX request | header `HX-Request: true` | same status code, fragment only (no `<html>`) | same handler |
| `UTCDateTime` gets an aware datetime | e.g. 20:00 Europe/Rome | stored as 19:00 UTC, read back as aware UTC | N/A |
| `UTCDateTime` gets a naive datetime | `datetime(2026,11,21,20,0)` | refused | raises `ValueError` |

</frozen-after-approval>

## Code Map

- Project root is empty except for user files listed under **Never**. `first.py` is an empty file; leave it.
- `uv init --app` creates a default `main.py` and a `README.md` at the root → delete the root `main.py` (the app lives in `app/main.py`); keep the README.
- No existing code to reuse.

## Tasks & Acceptance

**Execution:**
- [x] `pyproject.toml`, `.python-version`, `uv.lock` -- `uv init --app --python 3.14`, then `uv add` / `uv add --dev` the pinned versions above -- reproducible installs
- [x] `.gitignore` -- exclude `.venv/`, `__pycache__/`, `.env`, `*.db`, `*.db-wal`, `*.db-shm`, `.pytest_cache/`; then `git init` -- no secrets or DB in git
- [x] `app/__init__.py` + empty packages `app/models/`, `app/services/`, `app/notifications/`, `app/jobs/`, `app/routes/` (each with `__init__.py`), `app/templates/fragments/`, `app/static/` -- the architecture's source tree
- [x] `app/config.py` -- pydantic-settings `Settings` (`database_url` default `sqlite:///./app.db`, `app_env` default `"dev"`), one `settings` object -- one place for config
- [x] `app/db.py` -- SQLModel engine from `settings.database_url`; on every SQLite connect set `PRAGMA journal_mode=WAL` and `PRAGMA foreign_keys=ON` -- WAL everywhere, also for Alembic
- [x] `app/services/errors.py` -- `NotFound`, `NotAllowed`, `InvalidState` (base `ServiceError`) -- the only errors services raise
- [x] `app/models/types.py` -- **written by Erfan, reviewed by Claude:** `UTCDateTime` SQLAlchemy `TypeDecorator` (impl `DateTime`, `cache_ok = True`): rejects naive datetimes, stores UTC, returns aware UTC -- AD-6
- [x] `app/routes/pages.py` -- `GET /` renders `hello.html` -- the hello page
- [x] `app/main.py` -- create FastAPI app, mount `/static`, include routers, set up stdout logging, register the one `ServiceError` handler (404/403/409; fragment template when `HX-Request` is present) -- app entry point
- [x] `app/templates/base.html`, `hello.html`, `error.html`, `fragments/error.html` -- base layout with Google Fonts (Gloock, Onest), `htmx.min.js`, `<body hx-headers='{}'>` placeholder for the CSRF header (Story 1.3); hello page: Gloock title "Hello" + muted Onest line
- [x] `app/static/app.css` -- all Notte Pura tokens as CSS variables (colors, type scale, spacing, radius, touch-min 44px), body `#000`, single 480px column with 20px gutter, `min-height: 44px` on buttons/links/inputs, 2px white `:focus-visible` ring, rem-based sizes so 200% zoom has no sideways scroll
- [x] `app/static/htmx.min.js` -- download htmx.org@2.0.11 `dist/htmx.min.js` from unpkg
- [x] `alembic.ini`, `migrations/` -- `alembic init migrations`; `env.py` reads the URL from `settings`, uses `SQLModel.metadata`, `render_as_batch=True`; one empty first revision -- AD-10
- [x] `tests/conftest.py`, `tests/test_hello.py`, `tests/test_errors.py`, `tests/test_utc_datetime.py`, `tests/test_migrations.py`, `tests/test_layers.py` -- cover the I/O matrix; error tests add throwaway routes to the app in a fixture; migration test runs `alembic upgrade head` on a temp SQLite file and checks `PRAGMA journal_mode` is `wal`; layer test parses imports with `ast` and fails if anything imports `app.routes` outside `app/routes/` and `app/main.py`, or if `app/models` imports `app.services`

**Acceptance Criteria:**
- Given the project, when I run `uv run uvicorn app.main:app --reload` and open `/`, then I see the black hello page with the Gloock title, and no sideways scroll at 360px
- Given a fresh clone, when I run `uv sync` then `uv run pytest`, then all tests pass
- Given the repository, when I run `git status`, then `.env` and `*.db` files never show up

## Implementation Notes

- `uv init` produced a `src/` package layout; it was removed so `app/` sits at the root. Added `pythonpath = ["."]` for pytest.
- Added `app/templating.py` (shared Jinja2 object) so the error handler in `main.py` does not import from `routes/` (AD-1).
- `UTCDateTime` written by Erfan step by step; all 4 UTC tests pass.

## Spec Change Log

## Review Triage Log

Review pass 1 (blind-hunter BH, edge-case-hunter EC, verification-gap VG).

| # | Finding | Verdict | Evidence | Route |
|---|---------|---------|----------|-------|
| 1 | VG/BH: `PRAGMA foreign_keys=ON` in `make_engine` not tested | medium (gap) | grep: no test touches `foreign_keys`; per-connection pragma, migration test can't see it | patch |
| 2 | VG/EC: bare `ServiceError` fallback (409) never exercised | low (gap) | `CASES` has only the 3 mapped subclasses | patch (one CASES row) |
| 3 | VG: error tests don't assert title/message per status | low (gap) | asserts only status, `role="alert"`, no leak | patch |
| 4 | BH/EC: HTMX 2 doesn't swap 4xx fragments by default | medium (unverified reach) | no `responseHandling` config in `base.html`; but no HTMX action exists yet in 1.1 | defer → first HTMX action (Story 2.3) |
| 5 | BH/EC: unknown URL / 405 return JSON, not friendly page | medium | `GET /does-not-exist` → 404 `application/json {"detail":"Not Found"}` (reproduced) | patch |
| 6 | BH: all `<a>` are 44px inline-flex, breaks inline links | low | no inline links in app copy; NFR-2 wants 44px targets anyway | reject (low) |
| 7 | BH: handler logs omit `str(exc)`; fallback duplicates InvalidState | low | service errors are expected flow; type+status+path is enough now | reject (low) |
| 8 | BH: stale TODO/`noqa` in `types.py` | low | docstring still says "Fill in the two methods" | patch (deletion) |
| 9 | BH: `process_result_value` overwrites tz from other DBs | false | AD-8: SQLite only, always returns naive | reject |
| 10 | BH: README empty, no `.env.example` | low | README.md is 0 bytes; developers meet it every clone | patch (short README) |
| 11 | BH/EC: cwd-relative `.env` / `app.db` / alembic `prepend_sys_path` | false | from another cwd `import app` already fails (`ModuleNotFoundError`, reproduced); can't reach a wrong DB | reject |
| 12 | BH: `app_env` free string | low | nothing reads it yet | reject (low) |
| 13 | BH: `"Hello" in html` passes via `<title>` | low (gap) | default title is "Hello" | patch |
| 14 | BH: no subprocess timeout / downgrade test | low | empty migration; unlikely hang | reject (low) |
| 15 | BH: pywebpush/itsdangerous pinned early, no ruff | false | spec Always pins them on purpose | reject |
| 16 | BH: `basicConfig` at import duplicates uvicorn logs | false | uvicorn's own loggers set `propagate: False`; root config doesn't duplicate | reject |
| 17 | EC: tzinfo with `utcoffset() None` | low | only exotic custom tzinfo; unreachable | reject (low) |
| 18 | EC: non-datetime value | false | fails loudly with AttributeError — correct behavior | reject |
| 19 | EC: env.py ignores `sqlalchemy.url` override | false | nothing sets it; URL comes from settings by design | reject |
| 20 | EC: engine not disposed on migration error | low | CLI process exits anyway | reject (low) |
| 21 | EC: test route default arg seen as query param | low | test-only throwaway routes, never queried | reject (low) |
| 22 | EC: layer test skips relative imports (`from ..routes import x`) | medium | reproduced: `ImportFrom.level>0` skipped; AD-1 silently bypassable | patch |
| 23 | EC: fragment only when `HX-Request == "true"` | false | htmx always sends exactly `true` | reject |

## Design Notes

`UTCDateTime` shape (Erfan fills the two methods):

```python
class UTCDateTime(TypeDecorator):
    impl = DateTime
    cache_ok = True
    def process_bind_param(self, value, dialect): ...    # Python → DB
    def process_result_value(self, value, dialect): ...  # DB → Python
```

SQLite stores datetimes without a timezone, so the type saves naive UTC and adds `timezone.utc` back when reading.

## Verification

**Commands:**
- `uv run pytest -q` -- expected: all tests pass
- `uv run alembic upgrade head` -- expected: runs with no error, creates `app.db`
- `uv run python -c "import app.main"` -- expected: no error

**Manual checks:**
- Open `http://127.0.0.1:8000/` in the browser with phone width 360px: black page, serif title, no sideways scroll.
