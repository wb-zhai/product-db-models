"""remove article download foreign key constraint

Revision ID: 891188dccaac
Revises: aa6f20678a45
Create Date: 2025-09-09 11:13:34.019188

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '891188dccaac'
down_revision: Union[str, Sequence[str], None] = 'aa6f20678a45'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_constraint(op.f('article_downloads_uri_key'), 'article_downloads', type_='unique')
    op.create_index(op.f('ix_article_downloads_uri'), 'article_downloads', ['uri'], unique=True)
    op.drop_constraint(op.f('article_downloads_uri_fkey'), 'article_downloads', type_='foreignkey')
    op.drop_constraint(op.f('article_uris_uri_key'), 'article_uris', type_='unique')
    op.create_index(op.f('ix_article_uris_uri'), 'article_uris', ['uri'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_article_uris_uri'), table_name='article_uris')
    op.create_unique_constraint(op.f('article_uris_uri_key'), 'article_uris', ['uri'], postgresql_nulls_not_distinct=False)
    op.create_foreign_key(op.f('article_downloads_uri_fkey'), 'article_downloads', 'article_uris', ['uri'], ['uri'])
    op.drop_index(op.f('ix_article_downloads_uri'), table_name='article_downloads')
    op.create_unique_constraint(op.f('article_downloads_uri_key'), 'article_downloads', ['uri'], postgresql_nulls_not_distinct=False)
