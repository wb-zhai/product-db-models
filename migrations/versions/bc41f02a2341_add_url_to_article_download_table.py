"""Add URL to article download table

Revision ID: bc41f02a2341
Revises: 1f0c7e30baff
Create Date: 2026-02-23 13:08:51.265915

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bc41f02a2341'
down_revision: Union[str, Sequence[str], None] = '1f0c7e30baff'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('article_downloads', sa.Column('url', sa.String(), nullable=True))

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('article_downloads', 'url')
