"""add table to track article tags

Revision ID: 2a6e520c8a0b
Revises: 999508ab0024
Create Date: 2025-11-03 06:10:48.841786

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2a6e520c8a0b'
down_revision: Union[str, Sequence[str], None] = '999508ab0024'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'tagged_articles',
        sa.Column(
            'article_uri',
            sa.String(),
            nullable=False,
        ),
        sa.Column(
            'tag_method_url',
            sa.String(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ['article_uri'],
            ['article_downloads.uri'],
            name='fk_tagged_articles_article_uri',
        ),
        sa.PrimaryKeyConstraint(
            'article_uri',
            'tag_method_url',
            name='pk_tagged_articles',
        )
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('tagged_articles')

