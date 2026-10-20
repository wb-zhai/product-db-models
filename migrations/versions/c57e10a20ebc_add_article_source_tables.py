"""Add article source tables

Revision ID: c57e10a20ebc
Revises: 8bec26e2c403
Create Date: 2026-10-20 16:23:40.063145

"""
from typing import Sequence, Union

from alembic import op
import geoalchemy2
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'c57e10a20ebc'
down_revision: Union[str, Sequence[str], None] = '8bec26e2c403'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('article_source_locations',
    sa.Column('geo_names_id', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('parent_id', sa.Integer(), nullable=True),
    sa.Column('location_type', postgresql.ENUM('place', 'country', name='source_location_enum'), nullable=False),
    sa.Column('wiki_uri', sa.String(), nullable=True),
    sa.Column('feature_code', sa.String(), nullable=True),
    sa.Column('adm0_code_iso_2', sa.String(), nullable=True),
    sa.Column('adm0_code_iso_3', sa.String(), nullable=True),
    sa.Column('geom', geoalchemy2.types.Geometry(geometry_type='POINT', srid=4326, dimension=2, from_text='ST_GeomFromEWKT', name='geometry'), nullable=True),
    sa.CheckConstraint("location_type = 'place' OR parent_id IS NULL", name='check_article_source_locations_country_parent'),
    sa.ForeignKeyConstraint(['parent_id'], ['article_source_locations.geo_names_id'], name='fk_article_source_locations_parent_id'),
    sa.PrimaryKeyConstraint('geo_names_id')
    )
    op.create_index('idx_article_source_locations_geom', 'article_source_locations', ['geom'], unique=False, postgresql_using='gist')
    op.create_index(op.f('ix_article_source_locations_location_type'), 'article_source_locations', ['location_type'], unique=False)
    op.create_index(op.f('ix_article_source_locations_parent_id'), 'article_source_locations', ['parent_id'], unique=False)
    op.create_table('article_sources',
    sa.Column('source_uri', sa.String(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('location_id', sa.Integer(), nullable=True),
    sa.Column('location_validated', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['location_id'], ['article_source_locations.geo_names_id'], name='fk_article_sources_location_id'),
    sa.PrimaryKeyConstraint('source_uri')
    )
    op.create_index(op.f('ix_article_sources_location_id'), 'article_sources', ['location_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_article_sources_location_id'), table_name='article_sources')
    op.drop_table('article_sources')
    op.drop_index(op.f('ix_article_source_locations_parent_id'), table_name='article_source_locations')
    op.drop_index(op.f('ix_article_source_locations_location_type'), table_name='article_source_locations')
    op.drop_index('idx_article_source_locations_geom', table_name='article_source_locations', postgresql_using='gist')
    op.drop_table('article_source_locations')
