"""Change wikipedia name type in geo taxonomy names

Revision ID: f17b65a9f5e9
Revises: c57e10a20ebc
Create Date: 2026-10-24 12:21:02.921113

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'f17b65a9f5e9'
down_revision: Union[str, Sequence[str], None] = 'c57e10a20ebc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _rename_name_type(old: str, new: str) -> None:
    # Renaming the value would silently relabel any existing rows, so
    # refuse unless they have been removed first.
    op.execute(f"""
        DO $$
        BEGIN
            IF EXISTS (
                SELECT 1 FROM geo_taxonomy_names WHERE name_type = '{old}'
            ) THEN
                RAISE EXCEPTION 'geo_taxonomy_names still has name_type = ''{old}'' rows; delete them before renaming the value to ''{new}''';
            END IF;
        END
        $$
    """)
    op.execute(f"ALTER TYPE geo_name_type RENAME VALUE '{old}' TO '{new}'")


def upgrade() -> None:
    """Upgrade schema."""
    _rename_name_type('wikipedia', 'concept')


def downgrade() -> None:
    """Downgrade schema."""
    _rename_name_type('concept', 'wikipedia')
