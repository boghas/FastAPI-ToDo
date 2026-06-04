"""Create phone number for user column

Revision ID: 4cce4b8846da
Revises: f0570739909e
Create Date: 2026-06-04 15:23:33.903529

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4cce4b8846da'
down_revision: Union[str, Sequence[str], None] = 'f0570739909e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users', 'phone_number')
