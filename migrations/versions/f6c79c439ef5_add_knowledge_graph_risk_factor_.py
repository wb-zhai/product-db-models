"""Add knowledge graph risk factor accounting

Revision ID: f6c79c439ef5
Revises: 6aed76f5eddf
Create Date: 2026-04-16 13:19:44.062469

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f6c79c439ef5'
down_revision: Union[str, Sequence[str], None] = '6aed76f5eddf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # 0. Ensure schema exists
    op.execute('CREATE SCHEMA IF NOT EXISTS knowledge_graph')

    # 1. Risk Factors
    op.create_table('risk_factors',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('version', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
        schema='knowledge_graph'
    )

    # 2. Location Tags
    op.create_table('article_location_tags',
        sa.Column('adm_code', sa.String(), nullable=False),
        sa.Column('article_position_group', sa.String(), nullable=False),
        sa.Column('article_position_start', sa.Integer(), nullable=False),
        sa.Column('article_position_end', sa.Integer(), nullable=True),
        sa.Column('article_uri', sa.String(), nullable=False),
        sa.Column('tag_method_id', sa.Integer(), nullable=False),
        # ADDED 'public.' prefixes below
        sa.ForeignKeyConstraint(['adm_code'], ['public.geo_taxonomy.adm_code'], name='fk_article_location_tags_adm_code', onupdate='CASCADE'),
        sa.ForeignKeyConstraint(['article_uri'], ['public.article_downloads_ref.uri'], name='fk_article_location_tags_article_uri'),
        sa.ForeignKeyConstraint(['tag_method_id'], ['public.tag_method_urls.method_id'], name='fk_article_location_tags_method_id'),
        sa.PrimaryKeyConstraint('tag_method_id', 'adm_code', 'article_uri', 'article_position_group', 'article_position_start', name='pk_article_location_tags'),
        schema='knowledge_graph'
    )
    # Kept the composite, removed the redundant single-column indexes for adm_code and tag_method_id
    op.create_index('ix_article_location_tags_adm_code_article_uri', 'article_location_tags', ['adm_code', 'article_uri'], unique=False, schema='knowledge_graph')
    op.create_index(op.f('ix_knowledge_graph_article_location_tags_article_uri'), 'article_location_tags', ['article_uri'], unique=False, schema='knowledge_graph')

    # 3. Risk Factor Tags
    op.create_table('article_risk_factor_tags',
        sa.Column('risk_factor', sa.Integer(), nullable=False),
        sa.Column('article_position_group', sa.String(), nullable=False),
        sa.Column('article_position_start', sa.Integer(), nullable=False),
        sa.Column('article_position_end', sa.Integer(), nullable=True),
        sa.Column('article_uri', sa.String(), nullable=False),
        sa.Column('tag_method_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['article_uri'], ['public.article_downloads_ref.uri'], name='fk_article_risk_factor_tags_article_uri'),
        sa.ForeignKeyConstraint(['risk_factor'], ['knowledge_graph.risk_factors.id'], name='fk_article_risk_factor_tags_risk_factor_id'),
        sa.ForeignKeyConstraint(['tag_method_id'], ['public.tag_method_urls.method_id'], name='fk_article_risk_factor_tags_method_id'),
        sa.PrimaryKeyConstraint('tag_method_id', 'risk_factor', 'article_uri', 'article_position_group', 'article_position_start', name='pk_article_risk_factor_tags'),
        schema='knowledge_graph'
    )
    op.create_index(op.f('ix_knowledge_graph_article_risk_factor_tags_article_uri'), 'article_risk_factor_tags', ['article_uri'], unique=False, schema='knowledge_graph')
    op.create_index(op.f('ix_knowledge_graph_article_risk_factor_tags_risk_factor'), 'article_risk_factor_tags', ['risk_factor'], unique=False, schema='knowledge_graph')

    # 4. Tagged Articles
    op.create_table('tagged_articles',
        sa.Column('article_uri', sa.String(), nullable=False),
        sa.Column('tag_method_id', sa.Integer(), nullable=False),
        sa.Column('tagged_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['article_uri'], ['public.article_downloads_ref.uri'], name='fk_tagged_articles_article_uri'),
        sa.ForeignKeyConstraint(['tag_method_id'], ['public.tag_method_urls.method_id'], name='fk_tagged_articles_method_id'),
        sa.PrimaryKeyConstraint('tag_method_id', 'article_uri', name='pk_tagged_articles'),
        schema='knowledge_graph'
    )
    op.create_index(op.f('ix_knowledge_graph_tagged_articles_article_uri'), 'tagged_articles', ['article_uri'], unique=False, schema='knowledge_graph')
