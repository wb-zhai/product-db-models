"""Add concept_type to ConceptUri

Revision ID: 00b44e406324
Revises: 4dd6973884db
Create Date: 2025-09-02 16:06:01.091434

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '00b44e406324'
down_revision: Union[str, Sequence[str], None] = '4dd6973884db'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

user_status_enum = postgresql.ENUM('wiki', 'person', 'loc', 'org', name='concept_enum')

def upgrade() -> None:
    """Upgrade schema."""
    user_status_enum.create(op.get_bind())
    op.add_column('concept_uris', sa.Column('concept_type', postgresql.ENUM('WIKI', 'PERSON', 'LOCATION', 'ORGANIZATION', name='concept_enum'), nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('concept_uris', 'concept_type')
    user_status_enum.drop(op.get_bind())
