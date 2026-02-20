"""Change risk factor score from integer to decimal

Revision ID: e1157093ba08
Revises: c5bc6f95a217
Create Date: 2025-12-04 23:17:44.110411

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'e1157093ba08'
down_revision: Union[str, Sequence[str], None] = 'e7348f289bb3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass
    # op.alter_column(
    #     "risk_factor_scores",
    #     "score",
    #     existing_type=sa.Integer(),
    #     type_=sa.Numeric(precision=8, scale=4),
    #     existing_nullable=False,
    #     postgresql_using="score::numeric(8,4)",
    # )


def downgrade() -> None:
    """Downgrade schema."""
    pass
    # op.alter_column(
    #     "risk_factor_scores",
    #     "score",
    #     existing_type=sa.Numeric(precision=8, scale=4),
    #     type_=sa.Integer(),
    #     existing_nullable=False,
    #     postgresql_using="score::integer",
    # )
