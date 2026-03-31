"""Create article_downloads_ref table

Revision ID: 6aed76f5eddf
Revises: bc41f02a2341
Create Date: 2026-03-30 16:51:12.251351

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '6aed76f5eddf'
down_revision: Union[str, Sequence[str], None] = 'bc41f02a2341'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('article_downloads_ref',
        sa.Column('uri', sa.String(), nullable=False),
        sa.Column('published_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('uri')
    )
    op.execute("""
       CREATE OR REPLACE FUNCTION sync_article_downloads_ref()
        RETURNS TRIGGER AS $$
        BEGIN
            IF TG_OP = 'INSERT' THEN
                INSERT INTO article_downloads_ref (id)
                VALUES (NEW.id)
                ON CONFLICT DO NOTHING;

            ELSIF TG_OP = 'DELETE' THEN
                DELETE FROM article_downloads_ref WHERE id = OLD.id;
            END IF;

            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)
    # assumes partitioned articles.article_downloads already exists
    op.execute("""
        CREATE TRIGGER article_downloads_ref_sync
        AFTER INSERT OR DELETE ON article_downloads
        FOR EACH ROW EXECUTE FUNCTION sync_article_downloads_ref();
    """)

def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP TRIGGER article_downloads_ref_sync ON article_downloads")
    op.execute("DROP FUNCTION sync_article_downloads_ref()")
    op.drop_table('article_downloads_ref')
