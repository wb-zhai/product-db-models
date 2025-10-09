"""Regenerate foreign key constraints of article_concept_association with explicit names

Revision ID: 5e70cbc96191
Revises: a1acb5858925
Create Date: 2025-10-09 18:09:06.303898

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "5e70cbc96191"
down_revision: Union[str, Sequence[str], None] = "a1acb5858925"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_primary_key(
        "pk_article_downloads", "article_downloads", ["uri"]
    )
    op.create_primary_key(
        "pk_concept_uris", "concept_uris", ["concept_uri"]
    )
    op.create_foreign_key(
        "fk_article_concept_association_concept_uri",
        "article_concept_association",
        "concept_uris",
        ["concept_uri"],
        ["concept_uri"],
    )
    op.create_foreign_key(
        "fk_article_concept_association_article_uri",
        "article_concept_association",
        "article_downloads",
        ["article_uri"],
        ["uri"],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        "fk_article_concept_association_article_uri",
        "article_concept_association",
        type_="foreignkey",
    )
    op.drop_constraint(
        "fk_article_concept_association_concept_uri",
        "article_concept_association",
        type_="foreignkey",
    )
    op.drop_constraint("pk_concept_uris", "concept_uris", type_="primary")
    op.drop_constraint("pk_article_downloads", "article_downloads", type_="primary")
