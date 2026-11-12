"""Shared column types for all models.

UTCDateTime (AD-6: all datetimes are stored as UTC):
- Saving: a naive datetime (no tzinfo) is refused with `ValueError`.
  An aware datetime is converted to UTC and stored naive,
  because SQLite stores datetimes without a timezone.
- Reading: the naive UTC value is returned as an aware UTC datetime.
- `None` stays `None` both ways.
"""

from datetime import timezone

from sqlalchemy.types import DateTime, TypeDecorator


class UTCDateTime(TypeDecorator):
    impl = DateTime
    cache_ok = True

    def process_bind_param(self, value, dialect):  # Python -> DB
        if value is None:
            return None
        if value.tzinfo is None:
            raise ValueError("UTCDateTime needs a datetime with a timezone")
        utc_value = value.astimezone(timezone.utc)
        return utc_value.replace(tzinfo=None)

    def process_result_value(self, value, dialect):  # DB -> Python
        if value is None:
            return None
        return value.replace(tzinfo=timezone.utc)
