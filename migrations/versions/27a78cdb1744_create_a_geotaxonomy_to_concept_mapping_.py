"""Create a geotaxonomy to concept mapping table

Revision ID: 27a78cdb1744
Revises: ad87fa84dacb
Create Date: 2025-07-03 11:18:42.692970

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "27a78cdb1744"
down_revision: Union[str, Sequence[str], None] = "ad87fa84dacb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "geo_taxonomy_concept_uris",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("code", sa.String(), nullable=True),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("uri", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name", "uri", name="unique_name_uri"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("geo_taxonomy_concept_uris")
