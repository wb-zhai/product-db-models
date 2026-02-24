"""Create partitioned risk_factor_scores table

Revision ID: 1f0c7e30baff
Revises: 8e65a8f538e5
Create Date: 2026-02-23 16:06:40.931561

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '1f0c7e30baff'
down_revision: Union[str, Sequence[str], None] = '8e65a8f538e5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

PARENT_TABLE = "scores.risk_factor_scores"
VIEW_NAME = "public.risk_factor_scores"


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(f"""
        CREATE TABLE {PARENT_TABLE} (
            created_at TIMESTAMPTZ DEFAULT now(),
            risk_factor_id INTEGER NOT NULL,
            score INTEGER NOT NULL,
            adm_code VARCHAR NOT NULL,
            year_month DATE NOT NULL,
            CONSTRAINT chk_risk_factor_scores_month_first_day CHECK (EXTRACT(DAY FROM year_month) = 1),
            CONSTRAINT fk_risk_factor_scores_adm_code FOREIGN KEY (adm_code) REFERENCES geo_taxonomy(adm_code),
            CONSTRAINT fk_risk_factor_scores_risk_factor_id FOREIGN KEY (risk_factor_id) REFERENCES risk_factors(id),
            CONSTRAINT pk_risk_factor_scores PRIMARY KEY (adm_code, year_month, risk_factor_id)
        ) PARTITION BY RANGE (year_month);
    """)
    # start date for partitioning based on prior knowledge of available data
    op.execute(
        f"""
        SELECT partman.create_parent(
            p_parent_table  => '{PARENT_TABLE}',
            p_control       => 'year_month',
            p_interval      => '1 month',
            p_start_partition => '2013-12-01'
        );
        """
    )
    # create 2 month-partitions ahead of time
    op.execute(
        f"""
        UPDATE partman.part_config
        SET premake = 2  -- 2 month partitions ahead of time
        WHERE parent_table = '{PARENT_TABLE}';
        """
    )
    op.execute(f"CREATE VIEW {VIEW_NAME} AS SELECT * FROM {PARENT_TABLE};")

def downgrade() -> None:
    """Downgrade schema."""
    op.execute(f"DROP VIEW IF EXISTS {VIEW_NAME};")
    op.execute(f"DELETE FROM partman.part_config WHERE parent_table = '{PARENT_TABLE}';")
    op.drop_table(PARENT_TABLE)
