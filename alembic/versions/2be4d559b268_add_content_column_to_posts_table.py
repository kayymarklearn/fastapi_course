"""add content column to posts table

Revision ID: 2be4d559b268
Revises: b4114f032742
Create Date: 2026-06-21 15:42:24.011182

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2be4d559b268'
down_revision: Union[str, Sequence[str], None] = 'b4114f032742'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("posts", "content")
    pass
