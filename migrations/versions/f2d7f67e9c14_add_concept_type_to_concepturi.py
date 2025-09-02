"""Add concept_type to ConceptUri

Revision ID: f2d7f67e9c14
Revises: 4dd6973884db
Create Date: 2025-09-02 15:57:22.306165

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'f2d7f67e9c14'
down_revision: Union[str, Sequence[str], None] = '4dd6973884db'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('concept_uris', sa.Column('concept_type', sa.Enum('WIKI', 'PERSON', 'LOCATION', 'ORGANIZATION', name='concept_enum'), nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('concept_uris', 'concept_type')
