"""Use covering index to fetch scores

Revision ID: ba79db50c198
Revises: e1157093ba08
Create Date: 2025-12-23 13:13:09.179750

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "ba79db50c198"
down_revision: Union[str, Sequence[str], None] = "e1157093ba08"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        CREATE INDEX idx_food_insecurity_scores_year_month_adm_code_score
        ON food_insecurity_scores (year_month, adm_code) INCLUDE (score);)
    """)


def downgrade() -> None:
    op.execute("DROP INDEX idx_food_insecurity_scores_year_month_adm_code_score;")
