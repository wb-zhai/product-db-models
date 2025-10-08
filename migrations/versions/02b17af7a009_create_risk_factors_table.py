"""Create risk factors table

Revision ID: 02b17af7a009
Revises: 0f42fa342707
Create Date: 2025-09-24 16:42:03.496528

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "02b17af7a009"
down_revision: Union[str, Sequence[str], None] = "0f42fa342707"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "risk_factors",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("risk_factors")
