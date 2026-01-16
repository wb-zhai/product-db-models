"""Remove risk_factor_concepts depedence on concept_uris

Revision ID: 1d7e3dfa1b7d
Revises: 1626d4f9f312
Create Date: 2026-01-16 10:40:07.866246

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1d7e3dfa1b7d'
down_revision: Union[str, Sequence[str], None] = '1626d4f9f312'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.drop_constraint(
        'fk_risk_factor_concepts_risk_concept_uri',
        'risk_factor_concepts',
        type_='foreignkey',
    )
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
    op.create_foreign_key(
        'fk_risk_factor_concepts_risk_concept_uri',
        'risk_factor_concepts',
        'concept_uris',
        ['concept_uri'],
        ['concept_uri'],
    )
