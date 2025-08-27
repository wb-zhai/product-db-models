"""Enforce unique constraint on uri with admin code rather than name

Revision ID: d6cbfb6ea652
Revises: 59f9431b1905
Create Date: 2025-07-16 21:59:44.359283

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'd6cbfb6ea652'
down_revision: Union[str, Sequence[str], None] = '59f9431b1905'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_constraint(op.f('unique_name_uri_direct_match'), 'geo_taxonomy_concept_uris_direct_match', type_='unique')
    op.create_unique_constraint('unique_code_uri_direct_match', 'geo_taxonomy_concept_uris_direct_match', ['code', 'uri'])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('unique_code_uri_direct_match', 'geo_taxonomy_concept_uris_direct_match', type_='unique')
    op.create_unique_constraint(op.f('unique_name_uri_direct_match'), 'geo_taxonomy_concept_uris_direct_match', ['name', 'uri'], postgresql_nulls_not_distinct=False)
