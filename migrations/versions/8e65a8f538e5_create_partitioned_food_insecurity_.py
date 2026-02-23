"""Create partitioned food_insecurity_scores table

Revision ID: 8e65a8f538e5
Revises: 1a56c81a7384
Create Date: 2026-02-20 13:16:45.700880

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '8e65a8f538e5'
down_revision: Union[str, Sequence[str], None] = '1a56c81a7384'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

PARENT_TABLE = "scores.food_insecurity_scores"
VIEW_NAME = "public.food_insecurity_scores"


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("CREATE SCHEMA IF NOT EXISTS scores;")
    op.execute(
        f"""
        CREATE TABLE {PARENT_TABLE} (
            created_at TIMESTAMPTZ DEFAULT now(),
            score INTEGER NOT NULL,
            adm_code VARCHAR NOT NULL,
            year_month DATE NOT NULL,
            CONSTRAINT chk_month_first_day CHECK (EXTRACT(DAY FROM year_month) = 1),
            CONSTRAINT pk_food_insecurity_scores PRIMARY KEY (adm_code, year_month),
            CONSTRAINT fk_food_insecurity_scores_adm_code
                FOREIGN KEY (adm_code)
                REFERENCES public.geo_taxonomy(adm_code)
        ) PARTITION BY RANGE (year_month);
        """
    )
    op.execute(
        f"""
        CREATE INDEX idx_food_insecurity_scores_year_month_adm_code_score
        ON {PARENT_TABLE} (year_month, adm_code)
        INCLUDE (score);
        """
    )
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
    op.execute(f"DROP TABLE IF EXISTS {PARENT_TABLE};")
    # deliberately skip dropping the schema in case other tables populate it