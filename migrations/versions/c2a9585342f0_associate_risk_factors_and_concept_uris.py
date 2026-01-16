"""Associate risk factors and concept URIs

Revision ID: c2a9585342f0
Revises: ba79db50c198
Create Date: 2026-01-15 14:37:59.406817

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c2a9585342f0'
down_revision: Union[str, Sequence[str], None] = 'ba79db50c198'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('risk_factor_concepts',
    sa.Column('risk_factor_id', sa.Integer(), nullable=False),
    sa.Column('concept_uri', sa.String(), nullable=False),
    sa.Column('source', sa.String(), nullable=False),
    sa.Column('version', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['concept_uri'], ['concept_uris.concept_uri'], name='fk_risk_factor_concepts_risk_concept_uri'),
    sa.ForeignKeyConstraint(['risk_factor_id'], ['risk_factors.id'], name='fk_risk_factor_concepts_risk_factor_id'),
    sa.PrimaryKeyConstraint('risk_factor_id', 'concept_uri')
    )
    op.create_index('ix_risk_factor_concepts_concept_uri', 'risk_factor_concepts', ['concept_uri'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index('ix_risk_factor_concepts_concept_uri', table_name='risk_factor_concepts')
    op.drop_table('risk_factor_concepts')
