"""Gin-index adm_name

Revision ID: aa6f20678a45
Revises: 00b44e406324
Create Date: 2025-09-07 21:19:09.403653

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'aa6f20678a45'
down_revision: Union[str, Sequence[str], None] = '00b44e406324'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute('CREATE EXTENSION IF NOT EXISTS pg_trgm;')
    op.create_index('idx_geotaxonomy_adm_name_trgm', 'geo_taxonomy', ['adm_name'], unique=False, postgresql_using='gin', postgresql_ops={'adm_name': 'gin_trgm_ops'})


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index('idx_geotaxonomy_adm_name_trgm', table_name='geo_taxonomy', postgresql_using='gin', postgresql_ops={'name': 'gin_trgm_ops'})
