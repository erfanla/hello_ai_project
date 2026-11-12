"""`alembic upgrade head` works on a fresh SQLite file and turns on WAL."""

import os
import sqlite3
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def test_upgrade_head_on_temp_sqlite_uses_wal(tmp_path):
    db_file = tmp_path / "test.db"
    env = {**os.environ, "DATABASE_URL": f"sqlite:///{db_file}"}

    result = subprocess.run(
        [sys.executable, "-m", "alembic", "upgrade", "head"],
        cwd=PROJECT_ROOT,
        env=env,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    assert db_file.exists()

    connection = sqlite3.connect(db_file)
    try:
        journal_mode = connection.execute("PRAGMA journal_mode").fetchone()[0]
        version = connection.execute("SELECT version_num FROM alembic_version").fetchone()
    finally:
        connection.close()

    assert journal_mode == "wal"
    assert version is not None
