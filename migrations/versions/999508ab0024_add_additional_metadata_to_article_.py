"""add additional metadata to article downloads

Revision ID: 999508ab0024
Revises: da8738ea23c5
Create Date: 2025-10-27 09:45:40.984321

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '999508ab0024'
down_revision: Union[str, Sequence[str], None] = 'da8738ea23c5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

article_enum = postgresql.ENUM('pr', 'blog', 'news', name='article_enum')

def upgrade() -> None:
    """Upgrade schema."""
    op.create_foreign_key('fk_article_concept_association_concept_uri', 'article_concept_association', 'concept_uris', ['concept_uri'], ['concept_uri'])
    article_enum.create(op.get_bind())
    op.add_column('article_downloads', sa.Column('source_uri', sa.String(), nullable=True))
    op.add_column('article_downloads', sa.Column('is_duplicate', sa.Boolean(), nullable=True))
    op.add_column('article_downloads', sa.Column('article_type', article_enum, nullable=True))
    op.add_column('article_downloads', sa.Column('title', sa.String(), nullable=True))
    op.add_column('article_downloads', sa.Column('body', sa.String(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('article_downloads', 'body')
    op.drop_column('article_downloads', 'title')
    op.drop_column('article_downloads', 'article_type')
    op.drop_column('article_downloads', 'is_duplicate')
    op.drop_column('article_downloads', 'source_uri')
    article_enum.drop(op.get_bind())
    op.drop_constraint('fk_article_concept_association_concept_uri', 'article_concept_association', type_='foreignkey')
