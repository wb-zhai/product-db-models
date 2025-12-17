"""Ensure tag method ids are integers

Revision ID: 4b01bd504cb3
Revises: 1b696f6eaea3
Create Date: 2025-12-17 16:12:33.792943

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4b01bd504cb3'
down_revision: Union[str, Sequence[str], None] = '1b696f6eaea3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_primary_key(
        "pk_article_location_tags",
        "article_location_tags",
        [
            "tag_method_id",
            "adm_code",
            "article_uri",
            "article_position_group",
            "article_position_start",
        ],
    )

    op.create_primary_key(
        "pk_article_risk_factor_tags",
        "article_risk_factor_tags",
        [
            "tag_method_id",
            "risk_factor",
            "article_uri",
            "article_position_group",
            "article_position_start",
        ],
    )

def downgrade() -> None:
    """Downgrade schema."""
    # Drop the Primary Key for ArticleLocationTags
    op.drop_constraint(
        "pk_article_location_tags",
        "article_location_tags",
        type_="primary",
    )

    # Drop the Primary Key for ArticleRiskFactorTags
    op.drop_constraint(
        "pk_article_risk_factor_tags",
        "article_risk_factor_tags",
        type_="primary",
    )
