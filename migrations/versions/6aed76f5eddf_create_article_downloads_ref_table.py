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

TABLES_TO_REPOINT = [
    "article_location_tags",
    "article_risk_factor_tags",
    "article_concept_association",
    "tagged_articles"
]

def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
        CREATE TABLE IF NOT EXISTS articles.article_downloads (
            LIKE public.article_downloads INCLUDING DEFAULTS INCLUDING CONSTRAINTS
        ) PARTITION BY RANGE (published_at);

        ALTER TABLE articles.article_downloads ADD PRIMARY KEY (uri, published_at);

        WITH bounds AS (
            SELECT
                MIN(published_at::date)::text AS start_partition,
                (
                    EXTRACT(YEAR FROM age(MAX(published_at::date), MIN(published_at::date))) * 12 +
                    EXTRACT(MONTH FROM age(MAX(published_at::date), MIN(published_at::date))) + 3
                )::int AS premake
            FROM public.article_downloads
        )
        SELECT partman.create_parent(
            p_parent_table    => 'articles.article_downloads',
            p_control         => 'published_at',
            p_interval        => '1 month',
            p_start_partition => bounds.start_partition,
            p_premake         => bounds.premake
        )
        FROM bounds;
    """)
    op.create_table('article_downloads_ref',
        sa.Column('uri', sa.String(), nullable=False),
        sa.Column('published_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('uri')
    )
    # The following assumes partitioned articles.article_downloads is already backfilled
    op.execute("""
        INSERT INTO article_downloads_ref (uri, published_at)
        SELECT uri, published_at
        FROM articles.article_downloads
    """)
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
    op.execute("""
        CREATE TRIGGER article_downloads_ref_sync
        BEFORE INSERT OR DELETE ON articles.article_downloads
        FOR EACH ROW EXECUTE FUNCTION sync_article_downloads_ref();
    """)
    for table in TABLES_TO_REPOINT:
         op.execute(f"""
            ALTER TABLE {table}
            DROP CONSTRAINT fk_{table}_article_uri
        """)
         op.execute(f"""
            ALTER TABLE {table}
            ADD CONSTRAINT fk_{table}_article_uri
            FOREIGN KEY (article_uri) REFERENCES article_downloads_ref(uri) NOT VALID
        """)
        # TODO:
        # op.execute(f"""
        #    ALTER TABLE {table} VALIDATE CONSTRAINT fk_{table}_article_uri;
        # """)


def downgrade() -> None:
    """Downgrade schema."""
    for table in TABLES_TO_REPOINT:
         op.execute(f"""
            ALTER TABLE {table}
            DROP CONSTRAINT fk_{table}_article_uri
        """)
         op.execute(f"""
            ALTER TABLE {table}
            ADD CONSTRAINT fk_{table}_article_uri
            FOREIGN KEY (article_uri) REFERENCES public.article_downloads(uri)
        """)
    op.drop_table('articles.article_downloads')
    op.execute("DROP TRIGGER article_downloads_ref_sync ON articles.article_downloads")
    op.execute("DROP FUNCTION sync_article_downloads_ref()")
    op.drop_table('article_downloads_ref')
