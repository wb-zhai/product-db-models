"""make article URIs primary keys

Revision ID: a1acb5858925
Revises: 8239a24a15d4
Create Date: 2025-10-09 12:09:05.289448

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'a1acb5858925'
down_revision: Union[str, Sequence[str], None] = '8239a24a15d4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_constraint(
        "fk_article_concept_association_uris",
        "article_concept_association",
        type_="foreignkey",
    )
    op.drop_constraint(
        "article_concept_association_concept_uri_fkey",
        "article_concept_association",
        type_="foreignkey",
    )
    op.drop_index(op.f('ix_article_downloads_uri'), table_name='article_downloads')
    op.drop_column('article_downloads', 'id')
    op.drop_index(op.f('ix_article_uris_uri'), table_name='article_uris')
    op.drop_column('article_uris', 'id')
    op.drop_constraint(op.f('concept_uris_concept_uri_key'), 'concept_uris', type_='unique')
    op.drop_column('concept_uris', 'id')


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column('concept_uris', sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('concept_uris_id_seq'::regclass)"), autoincrement=True, nullable=False))
    op.create_unique_constraint(op.f('concept_uris_concept_uri_key'), 'concept_uris', ['concept_uri'], postgresql_nulls_not_distinct=False)
    op.add_column('article_uris', sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False))
    op.create_index(op.f('ix_article_uris_uri'), 'article_uris', ['uri'], unique=False)
    op.add_column('article_downloads', sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('article_downloads_id_seq'::regclass)"), autoincrement=True, nullable=False))
    op.create_index(op.f('ix_article_downloads_uri'), 'article_downloads', ['uri'], unique=True)
    op.create_foreign_key(
        "article_concept_association_concept_uri_fkey",
        "article_concept_association",
        "concept_uris",
        ["concept_uri"],
        ["concept_uri"],
    )
    op.create_foreign_key(
        "fk_article_concept_association_uris",
        "article_concept_association",
        "article_downloads",
        ["article_uri"],
        ["uri"],
    )
