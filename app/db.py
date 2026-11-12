"""The database engine.

SQLite needs two settings on every new connection:
- `journal_mode=WAL`: readers and one writer can work at the same time.
- `foreign_keys=ON`: SQLite does not check foreign keys unless we ask.
"""

from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlmodel import create_engine

from app.config import settings


def make_engine(url: str) -> Engine:
    """Create an engine. For SQLite, turn on WAL and foreign keys."""
    is_sqlite = url.startswith("sqlite")
    connect_args = {"check_same_thread": False} if is_sqlite else {}
    new_engine = create_engine(url, connect_args=connect_args)

    if is_sqlite:

        @event.listens_for(new_engine, "connect")
        def _set_sqlite_pragmas(dbapi_connection, connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA journal_mode=WAL")
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

    return new_engine


engine = make_engine(settings.database_url)
