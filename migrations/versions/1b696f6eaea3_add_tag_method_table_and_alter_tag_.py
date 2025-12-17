"""Add tag method table and alter tag tables

Revision ID: 1b696f6eaea3
Revises: c5bc6f95a217
Create Date: 2025-12-17 06:22:13.697413

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1b696f6eaea3'
down_revision: Union[str, Sequence[str], None] = 'c5bc6f95a217'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('tag_method_urls',
                    sa.Column('method_id', sa.Integer(), nullable=False),
                    sa.Column('method_url', sa.String(), nullable=False, unique=True),
                    sa.PrimaryKeyConstraint('method_id')
                    )
    # op.create_foreign_key('fk_article_concept_association_concept_uri', 'article_concept_association', 'concept_uris', ['concept_uri'], ['concept_uri'])

    op.add_column('article_location_tags', sa.Column('tag_method_id', sa.Integer(), nullable=False))
    op.alter_column('article_location_tags', 'article_position_group',
                    existing_type=sa.VARCHAR(),
                    nullable=False)
    op.alter_column('article_location_tags', 'article_position_start',
                    existing_type=sa.INTEGER(),
                    nullable=False)
    op.drop_index(op.f('ix_article_location_tags_tag_method_url'), table_name='article_location_tags')
    op.create_index(op.f('ix_article_location_tags_tag_method_id'), 'article_location_tags', ['tag_method_id'], unique=False)
    op.create_foreign_key('fk_article_location_tags_method_id', 'article_location_tags', 'tag_method_urls', ['tag_method_id'], ['method_id'])
    op.drop_column('article_location_tags', 'strength')
    op.drop_column('article_location_tags', 'tag_method_url')

    op.add_column('article_risk_factor_tags', sa.Column('tag_method_id', sa.Integer(), nullable=False))
    op.alter_column('article_risk_factor_tags', 'article_position_group',
                    existing_type=sa.VARCHAR(),
                    nullable=False)
    op.alter_column('article_risk_factor_tags', 'article_position_start',
                    existing_type=sa.INTEGER(),
                    nullable=False)
    op.drop_index(op.f('ix_article_risk_factor_tags_tag_method_url'), table_name='article_risk_factor_tags')
    op.create_index(op.f('ix_article_risk_factor_tags_tag_method_id'), 'article_risk_factor_tags', ['tag_method_id'], unique=False)
    op.create_foreign_key('fk_article_risk_factor_tags_method_id', 'article_risk_factor_tags', 'tag_method_urls', ['tag_method_id'], ['method_id'])
    op.drop_column('article_risk_factor_tags', 'strength')
    op.drop_column('article_risk_factor_tags', 'tag_method_url')

    op.add_column('tagged_articles', sa.Column('tag_method_id', sa.Integer(), nullable=False))
    op.add_column('tagged_articles', sa.Column('tagged_at', sa.DateTime(), nullable=True))
    op.drop_index(op.f('ix_tagged_articles_tag_method_url'), table_name='tagged_articles')
    op.create_index(op.f('ix_tagged_articles_tag_method_id'), 'tagged_articles', ['tag_method_id'], unique=False)
    op.create_foreign_key('fk_tagged_articles_method_id', 'tagged_articles', 'tag_method_urls', ['tag_method_id'], ['method_id'])
    op.drop_column('tagged_articles', 'tag_method_url')

def downgrade() -> None:
    """Downgrade schema."""
    # Tagged Articles Cleanup
    op.add_column('tagged_articles', sa.Column('tag_method_url', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_constraint('fk_tagged_articles_method_id', 'tagged_articles', type_='foreignkey')
    op.drop_index(op.f('ix_tagged_articles_tag_method_id'), table_name='tagged_articles')
    op.create_index(op.f('ix_tagged_articles_tag_method_url'), 'tagged_articles', ['tag_method_url'], unique=False)
    op.drop_column('tagged_articles', 'tagged_at')
    op.drop_column('tagged_articles', 'tag_method_id')

    # Article Risk Factor Tags Cleanup
    op.add_column('article_risk_factor_tags', sa.Column('tag_method_url', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('article_risk_factor_tags', sa.Column('strength', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    op.drop_constraint('fk_article_risk_factor_tags_method_id', 'article_risk_factor_tags', type_='foreignkey')

    op.drop_index(op.f('ix_article_risk_factor_tags_tag_method_id'), table_name='article_risk_factor_tags')
    op.create_index(op.f('ix_article_risk_factor_tags_tag_method_url'), 'article_risk_factor_tags', ['tag_method_url'], unique=False)
    op.alter_column('article_risk_factor_tags', 'article_position_start', existing_type=sa.INTEGER(), nullable=True)
    op.alter_column('article_risk_factor_tags', 'article_position_group', existing_type=sa.VARCHAR(), nullable=True)
    op.drop_column('article_risk_factor_tags', 'tag_method_id')

    # Article Location Tags Cleanup
    op.add_column('article_location_tags', sa.Column('tag_method_url', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('article_location_tags', sa.Column('strength', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    op.drop_constraint('fk_article_location_tags_method_id', 'article_location_tags', type_='foreignkey')

    op.drop_index(op.f('ix_article_location_tags_tag_method_id'), table_name='article_location_tags')
    op.create_index(op.f('ix_article_location_tags_tag_method_url'), 'article_location_tags', ['tag_method_url'], unique=False)
    op.alter_column('article_location_tags', 'article_position_start', existing_type=sa.INTEGER(), nullable=True)
    op.alter_column('article_location_tags', 'article_position_group', existing_type=sa.VARCHAR(), nullable=True)
    op.drop_column('article_location_tags', 'tag_method_id')

    # Final Table Drops
    # op.drop_constraint('fk_article_concept_association_concept_uri', 'article_concept_association', type_='foreignkey')
    op.drop_table('tag_method_urls')
