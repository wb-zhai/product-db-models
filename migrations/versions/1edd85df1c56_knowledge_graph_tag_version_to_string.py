"""Knowledge graph tag version to string

Revision ID: 1edd85df1c56
Revises: b3cb18b66522
Create Date: 2026-06-09 11:47:44.854337

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '1edd85df1c56'
down_revision: Union[str, Sequence[str], None] = 'b3cb18b66522'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
def upgrade():
    op.alter_column(
        'risk_factors',               # table_name
        'version',                    # column_name
        type_=sa.String(),            # target type (SQLAlchemy
                                      # equivalent of varchar)
        schema='knowledge_graph'      # table schema
    )

def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        'risk_factors',               # table_name
        'version',                    # column_name
        type_=sa.Integer(),           # target type
        schema='knowledge_graph',     # table schema
        postgresql_using='version::integer' # explicit cast for existing data
    )
