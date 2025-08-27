"""Add derived columns adm_name and adm_code; add some constraints

Revision ID: 792b2f2c7406
Revises: 57797834a6ac
Create Date: 2025-07-10 10:06:46.639848

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '792b2f2c7406'
down_revision: Union[str, Sequence[str], None] = '57797834a6ac'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('geo_taxonomy', sa.Column('adm_code', sa.String(), sa.Computed('coalesce(adm2_code, adm1_code, adm0_code)', persisted=True), nullable=False))
    op.add_column('geo_taxonomy', sa.Column('adm_name', sa.String(), sa.Computed('coalesce(adm2_name, adm1_name, adm0_name)', persisted=True), nullable=False))
    op.alter_column('geo_taxonomy', 'adm_level',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('geo_taxonomy', 'adm0_code',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('geo_taxonomy', 'adm0_name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.create_check_constraint(
        constraint_name='check_adm_level',
        table_name='geo_taxonomy',
        condition=(sa.column("adm_level") in (0, 1, 2)),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('check_adm_level', 'geo_taxonomy', type_='check')
    op.alter_column('geo_taxonomy', 'adm0_name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('geo_taxonomy', 'adm0_code',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('geo_taxonomy', 'adm_level',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_column('geo_taxonomy', 'adm_name')
    op.drop_column('geo_taxonomy', 'adm_code')
