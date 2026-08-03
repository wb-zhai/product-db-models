"""Add geo taxonomy names table

Revision ID: c0d5e1da87b4
Revises: e6a275ad7368
Create Date: 2026-08-03 10:01:53.935677

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'c0d5e1da87b4'
down_revision: Union[str, Sequence[str], None] = 'e6a275ad7368'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('geo_taxonomy_names',
    sa.Column('adm_code', sa.String(), nullable=False),
    sa.Column('name_type', postgresql.ENUM('display', 'search', 'wikipedia', name='geo_name_type'), nullable=False),
    sa.Column('adm_name', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['adm_code'], ['geo_taxonomy.adm_code'], name='fk_geo_taxonomy_names_adm_code', onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('adm_code', 'name_type', 'adm_name', name='pk_geo_taxonomy_names')
    )
    op.create_index('idx_geo_taxonomy_names_adm_code', 'geo_taxonomy_names', ['adm_code'], unique=False)
    op.create_index('idx_geo_taxonomy_names_name_trgm', 'geo_taxonomy_names', ['adm_name'], unique=False, postgresql_using='gin', postgresql_ops={'adm_name': 'gin_trgm_ops'})
    op.create_index('idx_geo_taxonomy_names_type_name', 'geo_taxonomy_names', ['name_type', 'adm_name'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index('idx_geo_taxonomy_names_type_name', table_name='geo_taxonomy_names')
    op.drop_index('idx_geo_taxonomy_names_name_trgm', table_name='geo_taxonomy_names', postgresql_using='gin', postgresql_ops={'adm_name': 'gin_trgm_ops'})
    op.drop_index('idx_geo_taxonomy_names_adm_code', table_name='geo_taxonomy_names')
    op.drop_table('geo_taxonomy_names')
