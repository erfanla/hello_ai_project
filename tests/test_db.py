"""make_engine turns on WAL mode and foreign keys for SQLite."""

from sqlalchemy import text

from app.db import make_engine


def test_sqlite_engine_has_wal_and_foreign_keys(tmp_path):
    engine = make_engine(f"sqlite:///{tmp_path / 'x.db'}")
    try:
        with engine.connect() as connection:
            foreign_keys = connection.execute(text("PRAGMA foreign_keys")).scalar_one()
            journal_mode = connection.execute(text("PRAGMA journal_mode")).scalar_one()
    finally:
        engine.dispose()

    assert foreign_keys == 1
    assert journal_mode == "wal"
