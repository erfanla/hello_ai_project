"""UTCDateTime: aware datetimes are stored as UTC; naive ones are refused."""

from datetime import datetime, timezone
from zoneinfo import ZoneInfo

import pytest
from sqlalchemy import Column, Integer, MetaData, Table, create_engine, select, text
from sqlalchemy.exc import StatementError

from app.models.types import UTCDateTime

ROME = ZoneInfo("Europe/Rome")


@pytest.fixture
def table_and_engine():
    engine = create_engine("sqlite://")
    metadata = MetaData()
    table = Table(
        "things",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("at", UTCDateTime()),
    )
    metadata.create_all(engine)  # create_all is OK in tests
    yield table, engine
    engine.dispose()


def test_aware_datetime_is_stored_as_utc_and_read_back_aware(table_and_engine):
    table, engine = table_and_engine
    rome_evening = datetime(2026, 11, 21, 20, 0, tzinfo=ROME)  # 20:00 in Rome = 19:00 UTC

    with engine.begin() as conn:
        conn.execute(table.insert().values(id=1, at=rome_evening))
        raw = conn.execute(text("SELECT at FROM things WHERE id = 1")).scalar_one()
        value = conn.execute(select(table.c.at).where(table.c.id == 1)).scalar_one()

    assert raw.startswith("2026-11-21 19:00:00")  # stored as UTC in the DB
    assert value == datetime(2026, 11, 21, 19, 0, tzinfo=timezone.utc)
    assert value.tzinfo is not None
    assert value.utcoffset().total_seconds() == 0


def test_none_stays_none(table_and_engine):
    table, engine = table_and_engine
    with engine.begin() as conn:
        conn.execute(table.insert().values(id=1, at=None))
        value = conn.execute(select(table.c.at)).scalar_one()
    assert value is None


def test_naive_datetime_is_refused():
    with pytest.raises(ValueError):
        UTCDateTime().process_bind_param(datetime(2026, 11, 21, 20, 0), dialect=None)


def test_naive_datetime_is_refused_on_insert(table_and_engine):
    table, engine = table_and_engine
    with engine.begin() as conn:
        with pytest.raises(StatementError) as error_info:
            conn.execute(table.insert().values(id=1, at=datetime(2026, 11, 21, 20, 0)))
    assert isinstance(error_info.value.orig, ValueError)
