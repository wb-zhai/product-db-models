"""Tag whether geotaxonomy place is covered by zhai

Revision ID: ad87fa84dacb
Revises: 8eede1e4a327
Create Date: 2025-07-02 10:32:21.922340

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "ad87fa84dacb"
down_revision: Union[str, Sequence[str], None] = "8eede1e4a327"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "geo_taxonomy",
        sa.Column(
            "is_zhai_covered",
            sa.Boolean(),
            nullable=False,
            server_default=sa.sql.false(),
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("geo_taxonomy", "is_zhai_covered")
