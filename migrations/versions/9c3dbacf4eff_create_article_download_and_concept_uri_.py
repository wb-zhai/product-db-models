"""Create article download and concept uri models

Revision ID: 9c3dbacf4eff
Revises: 077a21dbd5de
Create Date: 2025-08-27 19:48:14.989909

"""

from typing import Sequence, Union

import geoalchemy2
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "9c3dbacf4eff"
down_revision: Union[str, Sequence[str], None] = "077a21dbd5de"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "concept_uris",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("concept_uri", sa.String(), nullable=False),
        sa.Column("geo_names_id", sa.Integer(), nullable=True),
        sa.Column(
            "geom",
            geoalchemy2.types.Geometry(
                geometry_type="POINT",
                srid=4326,
                dimension=2,
                from_text="ST_GeomFromEWKT",
                name="geometry",
            ),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("concept_uri"),
    )
    op.create_index(
        "idx_concept_uris_latlon",
        "concept_uris",
        ["geom"],
        unique=False,
        postgresql_using="gist",
    )
    op.create_table(
        "article_downloads",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("uri", sa.String(), nullable=False),
        sa.Column("cloud_uri", sa.String(), nullable=False),
        sa.Column("published_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["uri"],
            ["article_uris.uri"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("cloud_uri"),
        sa.UniqueConstraint("uri"),
    )
    op.create_table(
        "article_concept_association",
        sa.Column("article_uri", sa.String(), nullable=True),
        sa.Column("concept_uri", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(
            ["article_uri"],
            ["article_downloads.uri"],
        ),
        sa.ForeignKeyConstraint(
            ["concept_uri"],
            ["concept_uris.concept_uri"],
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("article_concept_association")
    op.drop_table("article_downloads")
    op.drop_index(
        "idx_concept_uris_latlon", table_name="concept_uris", postgresql_using="gist"
    )
    op.drop_table("concept_uris")
