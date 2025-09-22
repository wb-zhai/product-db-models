"""enforce unique article-concept association

Revision ID: 3734a324ea3b
Revises: 3a640e38e6f4
Create Date: 2025-09-19 14:55:54.624852

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "3734a324ea3b"
down_revision: Union[str, Sequence[str], None] = "3a640e38e6f4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        "article_concept_association",
        "article_uri",
        existing_type=sa.VARCHAR(),
        nullable=False,
    )
    op.alter_column(
        "article_concept_association",
        "concept_uri",
        existing_type=sa.VARCHAR(),
        nullable=False,
    )
    op.create_foreign_key(
        "fk_article_concept_association_uris",
        "article_concept_association",
        "article_downloads",
        ["article_uri"],
        ["uri"],
    )
    op.create_primary_key(
        "pk_article_concept_association", "article_concept_association", ["article_uri", "concept_uri"]
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        "pk_article_concept_association",
        "article_concept_association",
        type_="primary"
    )
    op.drop_constraint(
        "fk_article_concept_association_uris",
        "article_concept_association",
        type_="foreignkey",
    )
    op.alter_column(
        "article_concept_association",
        "concept_uri",
        existing_type=sa.VARCHAR(),
        nullable=True,
    )
    op.alter_column(
        "article_concept_association",
        "article_uri",
        existing_type=sa.VARCHAR(),
        nullable=True,
    )
