"""Indicate whether food insecurity scores are modeled or ground truth

Revision ID: b3cb18b66522
Revises: b2ad26a9baa3
Create Date: 2026-04-30 12:49:04.013240

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'b3cb18b66522'
down_revision: Union[str, Sequence[str], None] = 'b2ad26a9baa3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "food_insecurity_scores",
        sa.Column("is_ground_truth", sa.Boolean(), nullable=False, server_default=sa.false()),
        schema="scores",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("food_insecurity_scores", "is_ground_truth", schema="scores")
