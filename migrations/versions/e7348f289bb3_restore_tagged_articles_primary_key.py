"""Restore tagged articles primary key

Revision ID: e7348f289bb3
Revises: 4b01bd504cb3
Create Date: 2025-12-17 16:47:16.559854

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e7348f289bb3'
down_revision: Union[str, Sequence[str], None] = '4b01bd504cb3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_primary_key(
        "pk_tagged_articles",
        "tagged_articles",
        [
            "tag_method_id",
            "article_uri",
        ],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        "pk_tagged_articles",
        "tagged_articles",
        type_="primary",
    )
