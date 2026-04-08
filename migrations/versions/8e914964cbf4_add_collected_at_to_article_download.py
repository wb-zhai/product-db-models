"""Add collected_at to article_download

Revision ID: 8e914964cbf4
Revises: 6aed76f5eddf
Create Date: 2026-04-01 10:09:42.020096

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8e914964cbf4'
down_revision: Union[str, Sequence[str], None] = '6aed76f5eddf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_foreign_key('fk_article_concept_association_concept_uri', 'article_concept_association', 'concept_uris', ['concept_uri'], ['concept_uri'])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('fk_article_concept_association_concept_uri', 'article_concept_association', type_='foreignkey')
