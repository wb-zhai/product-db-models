"""Create a geotaxonomy to concept uri mapping table that are direct matches only

Revision ID: ea961d333fa3
Revises: 792b2f2c7406
Create Date: 2025-07-10 16:04:28.391738

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "ea961d333fa3"
down_revision: Union[str, Sequence[str], None] = "792b2f2c7406"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "geo_taxonomy_concept_uris_direct_match",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("code", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("uri", sa.String(), nullable=True),
        sa.Column("country_uri", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name", "uri", name="unique_name_uri_direct_match"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("geo_taxonomy_concept_uris_direct_match")
