"""add request_id to ArticleUri; make ArticleQuery id UUID type

Revision ID: 8d2e7079291f
Revises: 9c3dbacf4eff
Create Date: 2025-09-01 11:07:06.197861

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8d2e7079291f'
down_revision: Union[str, Sequence[str], None] = '9c3dbacf4eff'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('article_queries', sa.Column('uuid', sa.UUID(), nullable=False))
    op.drop_column('article_queries', 'id')
    op.add_column('article_uris', sa.Column('request_id', sa.UUID(), nullable=False))
    op.alter_column('article_uris', 'query_id',
               existing_type=sa.INTEGER(),
               type_=sa.UUID(),
               existing_nullable=False)
    op.drop_constraint(op.f('article_uris_query_id_fkey'), 'article_uris', type_='foreignkey')
    op.create_foreign_key(None, 'article_uris', 'article_queries', ['query_id'], ['uuid'])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, 'article_uris', type_='foreignkey')
    op.create_foreign_key(op.f('article_uris_query_id_fkey'), 'article_uris', 'article_queries', ['query_id'], ['id'])
    op.alter_column('article_uris', 'query_id',
               existing_type=sa.UUID(),
               type_=sa.INTEGER(),
               existing_nullable=False)
    op.drop_column('article_uris', 'request_id')
    op.add_column('article_queries', sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False))
    op.drop_column('article_queries', 'uuid')
