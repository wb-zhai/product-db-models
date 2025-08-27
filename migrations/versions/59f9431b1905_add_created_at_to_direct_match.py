"""Add created at to geotaxonomy-concept mapping table with filtering heuristics

Revision ID: 59f9431b1905
Revises: ea961d333fa3
Create Date: 2025-07-14 14:48:51.313965

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "59f9431b1905"
down_revision: Union[str, Sequence[str], None] = "ea961d333fa3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        "geo_taxonomy_concept_uris",
        "created_at",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=False,
        existing_server_default=sa.text("now()"),
    )
    op.add_column(
        "geo_taxonomy_concept_uris_direct_match",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )
    op.alter_column(
        "geo_taxonomy_concept_uris_direct_match",
        "code",
        existing_type=sa.VARCHAR(),
        nullable=True,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        "geo_taxonomy_concept_uris_direct_match",
        "code",
        existing_type=sa.VARCHAR(),
        nullable=False,
    )
    op.drop_column("geo_taxonomy_concept_uris_direct_match", "created_at")
    op.alter_column(
        "geo_taxonomy_concept_uris",
        "created_at",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=True,
        existing_server_default=sa.text("now()"),
    )
