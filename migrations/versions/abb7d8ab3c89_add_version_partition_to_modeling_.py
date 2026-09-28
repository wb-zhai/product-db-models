"""Partition modeling_frontend_results by version

Revision ID: abb7d8ab3c89
Revises: 71f465f58478
Create Date: 2026-09-28 11:05:41.860488

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'abb7d8ab3c89'
down_revision: Union[str, Sequence[str], None] = '71f465f58478'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

SCHEMA = "modeling"
TABLE = "modeling.modeling_frontend_results"
BACKUP_NAME = "modeling_frontend_results_unpartitioned"
BACKUP = f"modeling.{BACKUP_NAME}"
DEFAULT_PARTITION = "modeling.modeling_frontend_results_default"

# Explicit, ORM-declared names -- reliable, unlike the auto-generated
# secondary index names below.
_PK_RENAME = ("pk_modeling_frontend_results", "pk_modeling_frontend_results_unpartitioned")
_FK_RENAME = (
    "fk_modeling_frontend_results_adm_code",
    "fk_modeling_frontend_results_adm_code_unpartitioned",
)


def _secondary_index_names(conn, table_name: str) -> list[str]:
    """Whatever non-PK indexes currently exist on `table_name`.

    zhai_db_models declares exactly three (version, data_source,
    feature_type -- Column(index=True), no explicit Index()), but
    their auto-generated names don't reliably match SQLAlchemy's
    documented ix_<table>_<column> convention against every live DB
    (confirmed the hard way -- a first attempt at this migration
    guessed wrong). Discovering them by querying pg_indexes instead
    of hardcoding names avoids repeating that mistake.
    """
    rows = conn.execute(
        sa.text("""
            SELECT indexname FROM pg_indexes
            WHERE schemaname = :schema AND tablename = :table
              AND indexname NOT LIKE 'pk\\_%' ESCAPE '\\'
        """),
        {"schema": SCHEMA, "table": table_name},
    )
    return [row[0] for row in rows]


def upgrade() -> None:
    """Upgrade schema."""
    conn = op.get_bind()

    # Postgres has no ALTER TABLE ... PARTITION BY -- an existing table
    # can't be converted in place. Rename it out of the way instead of
    # dropping it, so whatever rows it currently holds aren't silently
    # lost; left for manual cleanup once confirmed unneeded.
    #
    # Constraint/index names are unique per schema, not per table, so
    # renaming the table alone isn't enough -- its PK/FK and secondary
    # indexes stay under their original names and would collide with
    # the new table below. Rename the PK/FK (known names); the three
    # secondary indexes aren't needed on an inert backup table, so
    # just drop them instead of guessing what to rename them to.
    op.execute(f"ALTER TABLE {TABLE} RENAME TO {BACKUP_NAME}")
    op.execute(f"ALTER TABLE {BACKUP} RENAME CONSTRAINT {_PK_RENAME[0]} TO {_PK_RENAME[1]}")
    op.execute(f"ALTER TABLE {BACKUP} RENAME CONSTRAINT {_FK_RENAME[0]} TO {_FK_RENAME[1]}")
    for name in _secondary_index_names(conn, BACKUP_NAME):
        op.execute(f'DROP INDEX {SCHEMA}."{name}"')

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
    # -- the DEFAULT partition included -- with it. Its indexes go
    # with it too, so there's nothing to recreate on the backup table
    # (they were dropped, not renamed, in upgrade()).
    op.execute(f"DROP TABLE {TABLE}")

    op.execute(f"ALTER TABLE {BACKUP} RENAME TO modeling_frontend_results")
    op.execute(f"ALTER TABLE {TABLE} RENAME CONSTRAINT {_PK_RENAME[1]} TO {_PK_RENAME[0]}")
    op.execute(f"ALTER TABLE {TABLE} RENAME CONSTRAINT {_FK_RENAME[1]} TO {_FK_RENAME[0]}")
