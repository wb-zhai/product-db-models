"""Expand risk factor concept keys

Revision ID: 1626d4f9f312
Revises: c2a9585342f0
Create Date: 2026-01-16 10:22:47.861517

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1626d4f9f312'
down_revision: Union[str, Sequence[str], None] = 'c2a9585342f0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_constraint(
        'risk_factor_concepts_pkey',
        'risk_factor_concepts',
        type_='primary',
    )

    op.create_primary_key(
        'risk_factor_concepts_pkey',
        'risk_factor_concepts',
        [
            'risk_factor_id',
            'concept_uri',
            'source',
            'version',
        ],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        'risk_factor_concepts_pkey',
        'risk_factor_concepts',
        type_='primary',
    )
    op.create_primary_key(
        'risk_factor_concepts_pkey',
        'risk_factor_concepts',
        [
            'risk_factor_id',
            'concept_uri',
        ],
    )
