from geoalchemy2 import Geometry
from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Table,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

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


article_concept_association = Table('article_concept_association', Base.metadata,
    Column('article_uri', String, ForeignKey('article_downloads.uri')),
    Column('concept_uri', String, ForeignKey('concept_uris.concept_uri'))
)

class ArticleDownload(Base):
    __tablename__ = "article_downloads"

    id = Column(Integer, primary_key=True, autoincrement=True)
    uri = Column(String, ForeignKey("article_uri_results.uri"), nullable=False, unique=True)
    cloud_uri = Column(String, unique=True, nullable=False)
    published_at = Column(DateTime, nullable=False)

    concepts = relationship('ConceptUri', secondary=article_concept_association, back_populates='article_downloads')

    def __repr__(self):
        return f"<ArticleDownload(uri='{self.uri}')>"


class ConceptUri(Base):
    __tablename__ = "concept_uris"

    id = Column(Integer, primary_key=True, autoincrement=True)
    concept_uri = Column(String, unique=True, nullable=False)
    geo_names_id = Column(Integer, nullable=True)
    geom = Column(Geometry('POINT', srid=4326), nullable=True)

    articles = relationship('ArticleDownload',  secondary=article_concept_association, back_populates='concept_uris')

    def __repr__(self):
        return f"<ConceptUri(concept_uri='{self.concept_uri}')>"


# todo: decommission and reclaim table name for ArticleUriResult
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
