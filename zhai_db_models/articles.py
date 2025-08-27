from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB

from zhai_db_models.models import Base


class ArticleQuery(Base):
    __tablename__ = "article_queries"

    # to be manually provided
    id = Column(Integer, primary_key=True)
    body = Column(JSONB, nullable=False)


class ArticleUriResult(Base):
    __tablename__ = "article_uri_results"
    # __table_args__ = (UniqueConstraint("uri", name="uq_article_uri"),)

    id = Column(Integer, primary_key=True, autoincrement=True)
    uri = Column(String, nullable=False, unique=True)
    query_id = Column(Integer, ForeignKey("article_queries.id"), nullable=False)
    weight = Column(Float, nullable=False)
    page_id = Column(Integer, nullable=False)
    queried_at = Column(DateTime, nullable=False)
    queried_at = Column(DateTime, nullable=False)
