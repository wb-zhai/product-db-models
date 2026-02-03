"""Cascade geo_taxonomy.adm_code updates to article location tags

Revision ID: 0be48872e356
Revises: 1d7e3dfa1b7d
Create Date: 2026-02-03 16:10:28.653302

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '0be48872e356'
down_revision: Union[str, Sequence[str], None] = '1d7e3dfa1b7d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_constraint(op.f('fk_article_location_tags_adm_code'), 'article_location_tags', type_='foreignkey')
    op.create_foreign_key('fk_article_location_tags_adm_code', 'article_location_tags', 'geo_taxonomy', ['adm_code'], ['adm_code'], onupdate='CASCADE')


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('fk_article_location_tags_adm_code', 'article_location_tags', type_='foreignkey')
    op.create_foreign_key(op.f('fk_article_location_tags_adm_code'), 'article_location_tags', 'geo_taxonomy', ['adm_code'], ['adm_code'])
