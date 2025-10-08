"""Create risk factor scores table

Revision ID: 8239a24a15d4
Revises: 02b17af7a009
Create Date: 2025-10-07 09:57:23.356733

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "8239a24a15d4"
down_revision: Union[str, Sequence[str], None] = "02b17af7a009"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "risk_factor_scores",
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
        sa.Column("risk_factor_id", sa.Integer(), nullable=False),
        sa.Column("score", sa.Integer(), nullable=False),
        sa.Column("adm_code", sa.String(), nullable=False),
        sa.Column("year_month", sa.Date(), nullable=False),
        sa.CheckConstraint(
            "EXTRACT(DAY FROM year_month) = 1",
            name="chk_risk_factor_scores_month_first_day",
        ),
        sa.ForeignKeyConstraint(
            ["risk_factor_id"],
            ["risk_factors.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "risk_factor_id", "year_month", "adm_code", name="uq_risk_factor_scores"
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("risk_factor_scores")
