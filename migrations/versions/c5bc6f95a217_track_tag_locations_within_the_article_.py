"""Track tag locations within the article body

Revision ID: c5bc6f95a217
Revises: d0349b892ef1
Create Date: 2025-12-01 09:36:44.129115

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c5bc6f95a217'
down_revision: Union[str, Sequence[str], None] = 'd0349b892ef1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('article_location_tags', sa.Column('article_position_group', sa.String(), nullable=True))
    op.add_column('article_location_tags', sa.Column('article_position_start', sa.Integer(), nullable=True))
    op.add_column('article_location_tags', sa.Column('article_position_end', sa.Integer(), nullable=True))
    op.add_column('article_risk_factor_tags', sa.Column('article_position_group', sa.String(), nullable=True))
    op.add_column('article_risk_factor_tags', sa.Column('article_position_start', sa.Integer(), nullable=True))
    op.add_column('article_risk_factor_tags', sa.Column('article_position_end', sa.Integer(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('article_risk_factor_tags', 'article_position_end')
    op.drop_column('article_risk_factor_tags', 'article_position_start')
    op.drop_column('article_risk_factor_tags', 'article_position_group')
    op.drop_column('article_location_tags', 'article_position_end')
    op.drop_column('article_location_tags', 'article_position_start')
    op.drop_column('article_location_tags', 'article_position_group')
    # ### end Alembic commands ###
