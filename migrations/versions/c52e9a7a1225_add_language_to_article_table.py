"""add language to article table

Revision ID: c52e9a7a1225
Revises: 3734a324ea3b
Create Date: 2025-09-22 09:34:12.842908

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c52e9a7a1225'
down_revision: Union[str, Sequence[str], None] = '3734a324ea3b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('article_downloads', sa.Column('language', sa.String(), nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('article_downloads', 'language')
