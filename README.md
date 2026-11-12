# Hello AI project

A low-pressure app to invite friends to plans, built with FastAPI, HTMX and SQLite.

## Run it

```sh
uv sync                                  # install the pinned dependencies
uv run alembic upgrade head              # create or update the database
uv run uvicorn app.main:app --reload     # start the app on http://127.0.0.1:8000
uv run pytest                            # run the tests
```

## Settings

Settings come from environment variables (or a `.env` file, which is not in git).

| Variable       | Default              | What it does              |
|----------------|----------------------|---------------------------|
| `DATABASE_URL` | `sqlite:///./app.db` | Where the database lives  |
| `APP_ENV`      | `dev`                | Which environment this is |
