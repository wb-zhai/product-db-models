"""Allow non UUID versions in modeling_frontend_results

Revision ID: 8bec26e2c403
Revises: abb7d8ab3c89
Create Date: 2026-09-28 13:54:27.362803

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '8bec26e2c403'
down_revision: Union[str, Sequence[str], None] = 'abb7d8ab3c89'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

SCHEMA = "modeling"
TABLE = "modeling.modeling_frontend_results"
BACKUP_NAME = "modeling_frontend_results_uuid_version"
BACKUP = f"modeling.{BACKUP_NAME}"
DEFAULT_PARTITION = "modeling.modeling_frontend_results_default"

# Same naming-collision issue as abb7d8ab3c89, for the same reason
# (constraint/index names are unique per schema, not per table) --
# see that migration for the full explanation. Also new this time:
# the table being renamed away is *itself* already a partitioned
# parent (from abb7d8ab3c89), and its DEFAULT partition keeps its own
# name on a parent rename (only the parent's name changes), so that
# name has to be freed too before the new table can reuse it.
_PK_RENAME = ("pk_modeling_frontend_results", "pk_modeling_frontend_results_uuid_version")
_FK_RENAME = (
    "fk_modeling_frontend_results_adm_code",
    "fk_modeling_frontend_results_adm_code_uuid_version",
)
_DEFAULT_PARTITION_RENAME = (
    "modeling_frontend_results_default",
    "modeling_frontend_results_default_uuid_version",
)


def _secondary_index_names(conn, table_name: str) -> list[str]:
    rows = conn.execute(
        sa.text("""
            SELECT indexname FROM pg_indexes
            WHERE schemaname = :schema AND tablename = :table
              AND indexname !~ '^pk_'
        """),
        {"schema": SCHEMA, "table": table_name},
    )
    return [row[0] for row in rows]


def upgrade() -> None:
    """Upgrade schema."""
    conn = op.get_bind()

    # version is switching from UUID to an arbitrary string (no format
    # constraint -- the writer's exact scheme for it is still settling)
    # -- it's also the partition key, so this isn't a plain
    # ALTER COLUMN TYPE. Same rename-away-and-recreate approach as
    # abb7d8ab3c89: nothing under the old (UUID) scheme is real
    # production data yet.
    op.execute(f"ALTER TABLE {TABLE} RENAME TO {BACKUP_NAME}")
    op.execute(f"ALTER TABLE {BACKUP} RENAME CONSTRAINT {_PK_RENAME[0]} TO {_PK_RENAME[1]}")
    op.execute(f"ALTER TABLE {BACKUP} RENAME CONSTRAINT {_FK_RENAME[0]} TO {_FK_RENAME[1]}")
    op.execute(
        f'ALTER TABLE modeling."{_DEFAULT_PARTITION_RENAME[0]}" '
        f'RENAME TO "{_DEFAULT_PARTITION_RENAME[1]}"'
    )
    for name in _secondary_index_names(conn, BACKUP_NAME):
        op.execute(f'DROP INDEX {SCHEMA}."{name}"')

    op.execute(f"""
        CREATE TABLE {TABLE} (
            date TIMESTAMPTZ NOT NULL,
            adm_code VARCHAR NOT NULL,
            version VARCHAR NOT NULL,
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

    # See abb7d8ab3c89 for why one exists and the tradeoffs of relying
    # on it.
    op.execute(f"CREATE TABLE {DEFAULT_PARTITION} PARTITION OF {TABLE} DEFAULT")

    # Partitioned indexes, same as abb7d8ab3c89 -- Postgres extends
    # them to every partition attached later automatically.
    op.execute(f"CREATE INDEX ix_modeling_frontend_results_version ON {TABLE} (version)")
    op.execute(f"CREATE INDEX ix_modeling_frontend_results_data_source ON {TABLE} (data_source)")
    op.execute(f"CREATE INDEX ix_modeling_frontend_results_feature_type ON {TABLE} (feature_type)")


def downgrade() -> None:
    """Downgrade schema."""
    # Dropping the partitioned parent drops every attached partition
    # -- the DEFAULT partition included -- with it.
    op.execute(f"DROP TABLE {TABLE}")

    op.execute(f"ALTER TABLE {BACKUP} RENAME TO modeling_frontend_results")
    op.execute(f"ALTER TABLE {TABLE} RENAME CONSTRAINT {_PK_RENAME[1]} TO {_PK_RENAME[0]}")
    op.execute(f"ALTER TABLE {TABLE} RENAME CONSTRAINT {_FK_RENAME[1]} TO {_FK_RENAME[0]}")
    op.execute(
        f'ALTER TABLE modeling."{_DEFAULT_PARTITION_RENAME[1]}" '
        f'RENAME TO "{_DEFAULT_PARTITION_RENAME[0]}"'
    )
