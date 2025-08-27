"""Create article query and uri models

Revision ID: 077a21dbd5de
Revises: b98b96b9d218
Create Date: 2025-08-27 18:55:47.175472

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "077a21dbd5de"
down_revision: Union[str, Sequence[str], None] = "b98b96b9d218"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "article_queries",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("body", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "article_uri_results",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("uri", sa.String(), nullable=False),
        sa.Column("query_id", sa.Integer(), nullable=False),
        sa.Column("weight", sa.Float(), nullable=False),
        sa.Column("page_id", sa.Integer(), nullable=False),
        sa.Column("queried_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["query_id"],
            ["article_queries.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("uri"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("article_uri_results")
    op.drop_table("article_queries")
