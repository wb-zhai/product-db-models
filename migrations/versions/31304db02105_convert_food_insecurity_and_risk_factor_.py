"""Convert food insecurity and risk factor score tables into hypertables

Revision ID: 31304db02105
Revises: 5e70cbc96191
Create Date: 2025-10-11 10:45:57.471323

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "31304db02105"
down_revision: Union[str, Sequence[str], None] = "5e70cbc96191"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass
    # Change food_insecurity_scores from incrementing integer pk
    # to composite pk of (adm_code, year_month)
    # op.drop_constraint(
    #     "food_insecurity_scores_pkey", "food_insecurity_scores", type_="primary"
    # )
    # op.drop_constraint(
    #     op.f("uq_food_insecurity_scores"), "food_insecurity_scores", type_="unique"
    # )

    # op.drop_column("food_insecurity_scores", "id")
    # op.create_primary_key(
    #     "pk_food_insecurity_scores",
    #     "food_insecurity_scores",
    #     ["adm_code", "year_month"],
    # )

    # Change risk_factor_scores from incrementing integer pk
    # to composite pk of (risk_factor_id, adm_code, year_month)
    # op.drop_constraint(
    #     op.f("risk_factor_scores_pkey"), "risk_factor_scores", type_="primary"
    # )
    # op.drop_column("risk_factor_scores", "id")
    # op.drop_constraint(
    #     op.f("uq_risk_factor_scores"), "risk_factor_scores", type_="unique"
    # )
    # op.create_primary_key(
    #     "pk_risk_factor_scores",
    #     "risk_factor_scores",
    #     ["adm_code", "year_month", "risk_factor_id"],
    # )

    # op.execute("""
    #     SELECT create_hypertable('food_insecurity_scores', 'year_month', chunk_time_interval => INTERVAL '1 month', migrate_data => true);
    # """)
    # op.execute("""
    #     SELECT create_hypertable('risk_factor_scores', 'year_month', chunk_time_interval => INTERVAL '1 month', migrate_data => true);
    # """)


def downgrade() -> None:
    """Downgrade schema."""
    pass
    # TODO: convert risk_factor_scores and food_insecurity_scores hypertable back to regular table
    # op.drop_constraint("pk_risk_factor_scores", "risk_factor_scores", type_="primary")
    # op.add_column(
    #     "risk_factor_scores",
    #     sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
    # )
    # op.create_primary_key(op.f("risk_factor_scores_pkey"), "risk_factor_scores", ["id"])
    # op.create_unique_constraint(
    #     op.f("uq_risk_factor_scores"),
    #     "risk_factor_scores",
    #     ["adm_code", "year_month", "risk_factor_id"],
    #     postgresql_nulls_not_distinct=False,
    # )

    # op.drop_constraint(
    #     "pk_food_insecurity_scores", "food_insecurity_scores", type_="primary"
    # )
    # op.add_column(
    #     "food_insecurity_scores",
    #     sa.Column(
    #         "id", sa.INTEGER(), autoincrement=True, nullable=False, primary_key=True
    #     ),
    # )
    # op.create_unique_constraint(
    #     op.f("uq_food_insecurity_scores"),
    #     "food_insecurity_scores",
    #     ["adm_code", "year_month"],
    #     postgresql_nulls_not_distinct=False,
    # )
    # op.create_primary_key(
    #     op.f("food_insecurity_scores_pkey"), "food_insecurity_scores", ["id"]
    # )
