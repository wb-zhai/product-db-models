"""Move article_downloads to articles schema

Revision ID: 7ac3862c13d2
Revises: bc41f02a2341
Create Date: 2026-03-27 11:05:55.580273

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '7ac3862c13d2'
down_revision: Union[str, Sequence[str], None] = 'bc41f02a2341'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_constraint(
        'fk_tagged_articles_article_uri',
        'tagged_articles',
        type_='foreignkey',
    )
    op.create_foreign_key(
        'fk_tagged_articles_article_uri',
        'tagged_articles',
        'article_downloads',
        ['article_uri'],
        ['uri'],
        referent_schema='articles',
    )

    op.drop_constraint(
        'fk_article_concept_association_article_uri',
        'article_concept_association',
        type_='foreignkey',
    )
    op.create_foreign_key(
        'fk_article_concept_association_article_uri',
        'article_concept_association',
        'article_downloads',
        ['article_uri'],
        ['uri'],
        referent_schema='articles',
    )
    op.create_foreign_key(
        'fk_article_concept_association_article_uri',
        'article_concept_association',
        'concept_uris',
        ['article_uri'],
        ['uri'],
        referent_schema='articles'
    )

    op.drop_constraint(
        'fk_article_location_tags_article_uri',
        'article_location_tags',
        type_='foreignkey',
    )
    op.create_foreign_key(
        'fk_article_location_tags_article_uri',
        'article_location_tags',
        'article_downloads',
        ['article_uri'],
        ['uri'],
        referent_schema='articles',
    )

    op.drop_constraint(
        'fk_article_risk_factor_tags_article_uri',
        'article_risk_factor_tags',
        type_='foreignkey',
    )
    op.create_foreign_key(
        'fk_article_risk_factor_tags_article_uri',
        'article_risk_factor_tags',
        'article_downloads',
        ['article_uri'],
        ['uri'],
        referent_schema='articles',
    )

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        'fk_article_concept_association_concept_uri',
        'article_concept_association',
        type_='foreignkey',
    )

    op.drop_constraint(
        'fk_article_concept_association_article_uri',
        'article_concept_association',
        type_='foreignkey',
    )
    op.create_foreign_key(
        op.f('fk_article_concept_association_article_uri'),
        'article_concept_association',
        'article_downloads_bak',
        ['article_uri'],
        ['uri'],
    )
    op.drop_index(
        op.f('ix_articles_article_downloads_language'),
        table_name='article_downloads',
        schema='articles',
    )
    op.drop_index(
        op.f('ix_articles_article_downloads_article_type'),
        table_name='article_downloads',
        schema='articles',
    )
    op.drop_table(
        'article_downloads',
        schema='articles',
    )
