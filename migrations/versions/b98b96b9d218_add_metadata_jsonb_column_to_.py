"""Add metadata jsonb column to geotaxonomy concept uri mapping table

Revision ID: b98b96b9d218
Revises: d6cbfb6ea652
Create Date: 2025-07-17 15:48:41.856103

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'b98b96b9d218'
down_revision: Union[str, Sequence[str], None] = 'd6cbfb6ea652'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('geo_taxonomy_concept_uris_direct_match', sa.Column('meta', postgresql.JSONB(astext_type=sa.Text()), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('geo_taxonomy_concept_uris_direct_match', 'meta')
