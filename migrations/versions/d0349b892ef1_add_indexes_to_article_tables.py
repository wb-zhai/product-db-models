"""add indexes to article tables

Revision ID: d0349b892ef1
Revises: 2a6e520c8a0b
Create Date: 2025-11-06 06:10:42.797206

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd0349b892ef1'
down_revision: Union[str, Sequence[str], None] = '2a6e520c8a0b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_foreign_key('fk_article_concept_association_concept_uri', 'article_concept_association', 'concept_uris', ['concept_uri'], ['concept_uri'])
    op.create_index(op.f('ix_article_downloads_article_type'), 'article_downloads', ['article_type'], unique=False)
    op.create_index(op.f('ix_article_downloads_language'), 'article_downloads', ['language'], unique=False)
    op.create_index(op.f('ix_article_location_tags_adm_code'), 'article_location_tags', ['adm_code'], unique=False)
    op.create_index(op.f('ix_article_location_tags_article_uri'), 'article_location_tags', ['article_uri'], unique=False)
    op.create_index(op.f('ix_article_location_tags_tag_method_url'), 'article_location_tags', ['tag_method_url'], unique=False)
    op.create_index(op.f('ix_article_risk_factor_tags_article_uri'), 'article_risk_factor_tags', ['article_uri'], unique=False)
    op.create_index(op.f('ix_article_risk_factor_tags_risk_factor'), 'article_risk_factor_tags', ['risk_factor'], unique=False)
    op.create_index(op.f('ix_article_risk_factor_tags_tag_method_url'), 'article_risk_factor_tags', ['tag_method_url'], unique=False)
    op.create_index(op.f('ix_concept_uris_concept_type'), 'concept_uris', ['concept_type'], unique=False)
    op.create_index(op.f('ix_tagged_articles_article_uri'), 'tagged_articles', ['article_uri'], unique=False)
    op.create_index(op.f('ix_tagged_articles_tag_method_url'), 'tagged_articles', ['tag_method_url'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_tagged_articles_tag_method_url'), table_name='tagged_articles')
    op.drop_index(op.f('ix_tagged_articles_article_uri'), table_name='tagged_articles')
    op.drop_index(op.f('ix_concept_uris_concept_type'), table_name='concept_uris')
    op.drop_index(op.f('ix_article_risk_factor_tags_tag_method_url'), table_name='article_risk_factor_tags')
    op.drop_index(op.f('ix_article_risk_factor_tags_risk_factor'), table_name='article_risk_factor_tags')
    op.drop_index(op.f('ix_article_risk_factor_tags_article_uri'), table_name='article_risk_factor_tags')
    op.drop_index(op.f('ix_article_location_tags_tag_method_url'), table_name='article_location_tags')
    op.drop_index(op.f('ix_article_location_tags_article_uri'), table_name='article_location_tags')
    op.drop_index(op.f('ix_article_location_tags_adm_code'), table_name='article_location_tags')
    op.drop_index(op.f('ix_article_downloads_language'), table_name='article_downloads')
    op.drop_index(op.f('ix_article_downloads_article_type'), table_name='article_downloads')
    op.drop_constraint('fk_article_concept_association_concept_uri', 'article_concept_association', type_='foreignkey')
