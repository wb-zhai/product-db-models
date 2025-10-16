"""add risk-factor and location tagging

Revision ID: e5a1d21a557a
Revises: 31304db02105
Create Date: 2025-10-16 18:09:48.392065

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e5a1d21a557a'
down_revision: Union[str, Sequence[str], None] = '31304db02105'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('article_location_tags',
    sa.Column('article_uri', sa.String(), nullable=False),
    sa.Column('adm_code', sa.String(), nullable=False),
    sa.Column('strength', sa.Float(), nullable=True),
    sa.Column('tag_method_url', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['adm_code'], ['geo_taxonomy.adm_code'], name='fk_article_location_tags_adm_code'),
    sa.ForeignKeyConstraint(['article_uri'], ['article_downloads.uri'], name='fk_article_location_tags_article_uri'),
    sa.PrimaryKeyConstraint('article_uri', 'adm_code', 'tag_method_url', name='pk_article_location_tags')
    )
    op.create_table('article_risk_factor_tags',
    sa.Column('article_uri', sa.String(), nullable=False),
    sa.Column('risk_factor', sa.Integer(), nullable=False),
    sa.Column('strength', sa.Float(), nullable=True),
    sa.Column('tag_method_url', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['article_uri'], ['article_downloads.uri'], name='fk_article_risk_factor_tags_article_uri'),
    sa.ForeignKeyConstraint(['risk_factor'], ['risk_factors.id'], name='fk_article_risk_factor_tags_risk_factor_id'),
    sa.PrimaryKeyConstraint('article_uri', 'risk_factor', 'tag_method_url', name='pk_article_risk_factor_tags')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('article_risk_factor_tags')
    op.drop_table('article_location_tags')
