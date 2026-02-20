"""Create food insecurity score table

Revision ID: 0f42fa342707
Revises: c52e9a7a1225
Create Date: 2025-09-22 14:18:49.421571

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0f42fa342707"
down_revision: Union[str, Sequence[str], None] = "c52e9a7a1225"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass
    # op.create_table(
    #     "food_insecurity_scores",
    #     sa.Column("id", sa.Integer(), nullable=False),
    #     sa.Column(
    #         "created_at",
    #         sa.DateTime(timezone=True),
    #         server_default=sa.func.now(),
    #         nullable=True,
    #     ),
    #     sa.Column(
    #         "updated_at",
    #         sa.DateTime(timezone=True),
    #         server_default=sa.func.now(),
    #         nullable=True,
    #     ),
    #     sa.Column("score", sa.Integer(), nullable=False),
    #     sa.Column("adm_code", sa.String(), nullable=False),
    #     sa.Column("year_month", sa.Date(), nullable=False),
    #     sa.CheckConstraint(
    #         "EXTRACT(DAY FROM year_month) = 1", name="chk_month_first_day"
    #     ),
    #     sa.PrimaryKeyConstraint("id"),
    #     sa.UniqueConstraint("year_month", "adm_code", name="uq_food_insecurity_scores"),
    # )


def downgrade() -> None:
    """Downgrade schema."""
    pass
    # op.drop_table("food_insecurity_scores")
