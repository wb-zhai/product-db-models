"""Partition modeling_frontend_results by version

Revision ID: abb7d8ab3c89
Revises: 71f465f58478
Create Date: 2026-09-28 11:05:41.860488

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'abb7d8ab3c89'
down_revision: Union[str, Sequence[str], None] = '71f465f58478'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

TABLE = "modeling.modeling_frontend_results"
BACKUP = "modeling.modeling_frontend_results_unpartitioned"
DEFAULT_PARTITION = "modeling.modeling_frontend_results_default"


def upgrade() -> None:
    """Upgrade schema."""
    # Postgres has no ALTER TABLE ... PARTITION BY -- an existing table
    # can't be converted in place. Rename it out of the way instead of
    # dropping it, so whatever rows it currently holds aren't silently
    # lost; left for manual cleanup once confirmed unneeded.
    op.execute(f"ALTER TABLE {TABLE} RENAME TO modeling_frontend_results_unpartitioned")

    op.execute(f"""
        CREATE TABLE {TABLE} (
            date TIMESTAMPTZ NOT NULL,
            adm_code VARCHAR NOT NULL,
            version UUID NOT NULL,
            data_source data_source_enum NOT NULL,
            feature_type VARCHAR NOT NULL,
            feature_name VARCHAR,
            feature_value FLOAT,
            CONSTRAINT pk_modeling_frontend_results
                PRIMARY KEY (date, adm_code, feature_type, feature_name, version),
            CONSTRAINT fk_modeling_frontend_results_adm_code
                FOREIGN KEY (adm_code) REFERENCES geo_taxonomy (adm_code)
                ON UPDATE CASCADE
        ) PARTITION BY LIST (version);
    """)

    # Catches any write that lands without its own partition already
    # created. Expected to stay empty in normal operation -- see the
    # PR description for why one exists anyway and the tradeoffs of
    # relying on it.
    op.execute(f"CREATE TABLE {DEFAULT_PARTITION} PARTITION OF {TABLE} DEFAULT")

    # These become partitioned indexes: Postgres automatically extends
    # them to every partition attached later, including whatever
    # per-write partitions get created at write time, so nothing else
    # needs to recreate these per partition.
    op.execute(f"CREATE INDEX ix_modeling_frontend_results_version ON {TABLE} (version)")
    op.execute(f"CREATE INDEX ix_modeling_frontend_results_data_source ON {TABLE} (data_source)")
    op.execute(f"CREATE INDEX ix_modeling_frontend_results_feature_type ON {TABLE} (feature_type)")


def downgrade() -> None:
    """Downgrade schema."""
    # Dropping the partitioned parent drops every attached partition
    # -- the DEFAULT partition included -- with it.
    op.execute(f"DROP TABLE {TABLE}")
    op.execute(f"ALTER TABLE {BACKUP} RENAME TO modeling_frontend_results")
