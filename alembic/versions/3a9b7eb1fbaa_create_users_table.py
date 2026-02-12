"""create users table

Revision ID: 3a9b7eb1fbaa
Revises:
Create Date: 2026-02-10 00:31:22.922250

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3a9b7eb1fbaa'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'users',
        sa.Column('id', sa.BigInteger, primary_key=True, autoincrement=False),
        sa.Column('full_name', sa.String(50)),
        sa.Column('phone', sa.String(20), nullable=True),
        sa.Column('email', sa.String(255), nullable=True)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table()
