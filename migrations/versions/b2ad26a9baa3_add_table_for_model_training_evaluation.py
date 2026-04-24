"""Add table for model training evaluation

Revision ID: b2ad26a9baa3
Revises: f6c79c439ef5
Create Date: 2026-04-22 02:55:39.080366

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'b2ad26a9baa3'
down_revision: Union[str, Sequence[str], None] = 'f6c79c439ef5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(sa.text('CREATE SCHEMA IF NOT EXISTS modeling'))

    split_enum = postgresql.ENUM(
        'train',
        'val',
        'test',
        name='split_enum',
        schema='modeling',
    )
    metric_enum = postgresql.ENUM(
        'abs_error',
        'squared_error',
        name='metric_enum',
        schema='modeling',
    )
    bind = op.get_bind()
    split_enum.create(bind, checkfirst=True)
    metric_enum.create(bind, checkfirst=True)

    op.create_table(
        'modeling_regression_evaluation',
        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('now()'),
            nullable=False,
        ),
        sa.Column('cohort_id', sa.Uuid(), nullable=False),
        sa.Column('experiment_id', sa.Uuid(), nullable=False),
        sa.Column('dataset_url', sa.String(), nullable=False),
        sa.Column('run_name', sa.String(), nullable=False),
        sa.Column('date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('adm_code', sa.String(), nullable=False),
        sa.Column(
            'split',
            postgresql.ENUM(
                'train',
                'val',
                'test',
                name='split_enum',
                schema='modeling',
                create_type=False,
            ),
            nullable=False,
        ),
        sa.Column('y_true', sa.Float(), nullable=False),
        sa.Column('y_pred', sa.Float(), nullable=False),
        sa.Column(
            'metric',
            postgresql.ENUM(
                'abs_error',
                'squared_error',
                name='metric_enum',
                schema='modeling',
                create_type=False,
            ),
            nullable=False,
        ),
        sa.Column('score', sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(
            ['adm_code'],
            ['geo_taxonomy.adm_code'],
            name='fk_modeling_regression_evaluation_adm_code',
            onupdate='CASCADE',
        ),
        sa.PrimaryKeyConstraint(
            'cohort_id',
            'experiment_id',
            'run_name',
            'date',
            'adm_code',
            'split',
            'metric',
            name='pk_modeling_regression_evaluation',
        ),
        schema='modeling',
    )
    op.create_index(
        'ix_modeling_regression_evaluation_adm_code',
        'modeling_regression_evaluation',
        ['adm_code'],
        unique=False,
        schema='modeling',
    )


def downgrade() -> None:
    op.drop_index(
        'ix_modeling_regression_evaluation_adm_code',
        table_name='modeling_regression_evaluation',
        schema='modeling',
    )
    op.drop_table('modeling_regression_evaluation', schema='modeling')
    op.execute(sa.text('DROP TYPE IF EXISTS modeling.metric_enum CASCADE'))
    op.execute(sa.text('DROP TYPE IF EXISTS modeling.split_enum CASCADE'))
