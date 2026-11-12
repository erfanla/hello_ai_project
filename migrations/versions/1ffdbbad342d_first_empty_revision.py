"""first empty revision

Revision ID: 1ffdbbad342d
Revises: 
Create Date: 2026-11-12 13:40:34.429308

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel  # noqa: F401  (autogenerate may use sqlmodel types)


# revision identifiers, used by Alembic.
revision: str = '1ffdbbad342d'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
