"""New concept URI direct match layout

Revision ID: 71f465f58478
Revises: c0d5e1da87b4
Create Date: 2026-09-01 16:44:06.448021

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '71f465f58478'
down_revision: Union[str, Sequence[str], None] = 'c0d5e1da87b4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

TABLE = "geo_taxonomy_concept_uris_direct_match"


def upgrade() -> None:
    """Upgrade schema."""
    # Promote the meta JSONB blob to typed columns and add the adm_code FK.
    op.add_column(TABLE, sa.Column("adm_code", sa.String(), nullable=False))
    op.add_column(TABLE, sa.Column("title", sa.String(), nullable=True))
    op.add_column(TABLE, sa.Column("wikidata_qid", sa.String(), nullable=True))
    op.add_column(TABLE, sa.Column("page_id", sa.Integer(), nullable=True))
    op.add_column(TABLE, sa.Column("rank", sa.Integer(), nullable=True))
    op.add_column(TABLE, sa.Column("confidence", sa.Float(), nullable=True))
    op.add_column(TABLE, sa.Column("resolution_method", sa.String(), nullable=True))
    op.add_column(TABLE, sa.Column("tie_reason", sa.String(), nullable=True))
    op.add_column(
        TABLE, sa.Column("wikidata_p31", postgresql.ARRAY(sa.String()), nullable=True)
    )

    op.alter_column(TABLE, "uri", existing_type=sa.VARCHAR(), nullable=False)

    # Swap the old (code, country_uri) unique + code FK for the adm_code FK
    # and a composite (adm_code, uri) primary key.
    op.drop_constraint(
        "geo_taxonomy_concept_uris_direct_match_staging_code_uri_key",
        TABLE,
        type_="unique",
    )
    op.drop_constraint(
        "fk_geo_taxonomy_concept_uris_direct_match_staging_code",
        TABLE,
        type_="foreignkey",
    )

    op.drop_column(TABLE, "meta")
    op.drop_column(TABLE, "code")
    op.drop_column(TABLE, "country_uri")
    op.drop_column(TABLE, "id")
    op.drop_column(TABLE, "name")

    op.create_primary_key(
        "pk_geo_taxonomy_concept_uris_direct_match", TABLE, ["adm_code", "uri"]
    )
    op.create_foreign_key(
        "fk_geo_taxonomy_concept_uris_direct_match_adm_code",
        TABLE,
        "geo_taxonomy",
        ["adm_code"],
        ["adm_code"],
        onupdate="CASCADE",
        ondelete="CASCADE",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        "fk_geo_taxonomy_concept_uris_direct_match_adm_code",
        TABLE,
        type_="foreignkey",
    )
    op.drop_constraint(
        "pk_geo_taxonomy_concept_uris_direct_match", TABLE, type_="primary"
    )

    op.add_column(
        TABLE, sa.Column("name", sa.VARCHAR(), autoincrement=False, nullable=True)
    )
    op.add_column(
        TABLE,
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
    )
    op.add_column(
        TABLE,
        sa.Column("country_uri", sa.VARCHAR(), autoincrement=False, nullable=True),
    )
    op.add_column(
        TABLE, sa.Column("code", sa.VARCHAR(), autoincrement=False, nullable=True)
    )
    op.add_column(
        TABLE,
        sa.Column(
            "meta",
            postgresql.JSONB(astext_type=sa.Text()),
            autoincrement=False,
            nullable=True,
        ),
    )
    op.create_primary_key(
        "geo_taxonomy_concept_uris_direct_match_pkey", TABLE, ["id"]
    )
    op.create_foreign_key(
        "fk_geo_taxonomy_concept_uris_direct_match_staging_code",
        TABLE,
        "geo_taxonomy",
        ["code"],
        ["adm_code"],
    )
    op.create_unique_constraint(
        "geo_taxonomy_concept_uris_direct_match_staging_code_uri_key",
        TABLE,
        ["code", "country_uri"],
    )

    op.alter_column(TABLE, "uri", existing_type=sa.VARCHAR(), nullable=True)

    op.drop_column(TABLE, "wikidata_p31")
    op.drop_column(TABLE, "tie_reason")
    op.drop_column(TABLE, "resolution_method")
    op.drop_column(TABLE, "confidence")
    op.drop_column(TABLE, "rank")
    op.drop_column(TABLE, "page_id")
    op.drop_column(TABLE, "wikidata_qid")
    op.drop_column(TABLE, "title")
    op.drop_column(TABLE, "adm_code")
