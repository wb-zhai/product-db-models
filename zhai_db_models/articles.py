from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB

from .base import Base


class ArticleQuery(Base):
    __tablename__ = "article_queries"

    # to be manually inserted
    id = Column(Integer, primary_key=True)
    body = Column(JSONB, nullable=False)


class ArticleUriResult(Base):
    __tablename__ = "article_uri_results"

    id = Column(Integer, primary_key=True, autoincrement=True)
    uri = Column(String, nullable=False, unique=True)
    query_id = Column(Integer, ForeignKey("article_queries.id"), nullable=False)
    weight = Column(Float, nullable=False)
    page_id = Column(Integer, nullable=False)
    queried_at = Column(DateTime, nullable=False)
    queried_at = Column(DateTime, nullable=False)


class ArticleUri(Base):
    __tablename__ = "article_uris"

    id = Column(Integer, primary_key=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    dtype = Column(String)
    value = Column(String)
    uri = Column(String)

    __table_args__ = (UniqueConstraint("uri", name="unique_uri"),)
