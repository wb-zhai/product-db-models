"""change risk-factor data type

Revision ID: 1d1201475170
Revises: 0bf057cec7fb
Create Date: 2025-10-20 12:39:23.784958

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1d1201475170'
down_revision: Union[str, Sequence[str], None] = '0bf057cec7fb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        'article_risk_factor_tags',
        'risk_factor',
        existing_type=sa.INTEGER(),
        type_=sa.String(),
        existing_nullable=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        'article_risk_factor_tags',
        'risk_factor',
        existing_type=sa.String(),
        type_=sa.INTEGER(),
        existing_nullable=False,
    )
