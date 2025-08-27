"""Add created_at to geo_taxonomy_concept_uris

Revision ID: 57797834a6ac
Revises: 27a78cdb1744
Create Date: 2025-07-09 08:54:32.169504

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '57797834a6ac'
down_revision: Union[str, Sequence[str], None] = '27a78cdb1744'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('geo_taxonomy_concept_uris', sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('geo_taxonomy_concept_uris', 'created_at')
