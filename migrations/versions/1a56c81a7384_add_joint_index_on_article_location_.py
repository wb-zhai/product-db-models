"""Add joint index on article_location_tags for adm_code and article_uri

Revision ID: 1a56c81a7384
Revises: 39ffbf6add68
Create Date: 2026-02-19 15:10:30.977596

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '1a56c81a7384'
down_revision: Union[str, Sequence[str], None] = '39ffbf6add68'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

INDEX_NAME = "ix_article_location_tags_adm_code_article_uri"

def upgrade() -> None:
    """Upgrade schema."""
    op.execute(f"CREATE INDEX CONCURRENTLY {INDEX_NAME} ON article_location_tags (adm_code, article_uri);")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(f"DROP INDEX CONCURRENTLY {INDEX_NAME};")