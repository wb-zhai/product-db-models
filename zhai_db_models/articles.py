import enum

from geoalchemy2 import Geometry
from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Table,
)
from sqlalchemy.dialects.postgresql import ENUM, JSONB, UUID
from sqlalchemy.orm import relationship

from .base import Base


class ArticleQuery(Base):
    __tablename__ = "article_queries"

    uuid = Column(UUID(as_uuid=True), primary_key=True)
    body = Column(JSONB, nullable=False)


class ArticleUri(Base):
    __tablename__ = "article_uris"

    id = Column(Integer, primary_key=True, autoincrement=True)
    uri = Column(String, nullable=False)
    query_uuid = Column(
        UUID(as_uuid=True),
        ForeignKey("article_queries.uuid", name="fk_article_uris_query_uuid"),
        nullable=False,
    )
    weight = Column(Float, nullable=False)
    page_id = Column(Integer, nullable=False)
    queried_at = Column(DateTime, nullable=False)
    request_id = Column(UUID(as_uuid=True), nullable=False)


article_concept_association = Table(
    "article_concept_association",
    Base.metadata,
    Column("article_uri", String, ForeignKey("article_downloads.uri")),
    Column("concept_uri", String, ForeignKey("concept_uris.concept_uri")),
)


class ArticleDownload(Base):
    __tablename__ = "article_downloads"

    id = Column(Integer, primary_key=True, autoincrement=True)
    uri = Column(String, ForeignKey("article_uris.uri"), nullable=False, unique=True)
    cloud_uri = Column(String, unique=True, nullable=False)
    published_at = Column(DateTime, nullable=False)

    concept_uris = relationship(
        "ConceptUri",
        secondary=article_concept_association,
        back_populates="article_downloads",
    )

    def __repr__(self):
        return f"<ArticleDownload(uri='{self.uri}')>"


#
# Event Registry concept data model. See:
# https://github.com/EventRegistry/event-registry-python/wiki/Data-models#concept-data-model
#


class ConceptType(enum.Enum):
    wiki = "wiki"
    person = "person"
    loc = "loc"
    org = "org"


class ConceptUri(Base):
    __tablename__ = "concept_uris"

    __table_args__ = (
        Index("idx_concept_uris_latlon_geom", "geom", postgresql_using="gist"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    concept_uri = Column(String, unique=True, nullable=False)
    concept_type = Column(ENUM(ConceptType, name="concept_enum", create_type=True), nullable=False)
    geo_names_id = Column(Integer, nullable=True)
    geom = Column(Geometry("POINT", srid=4326), nullable=True)

    article_downloads = relationship(
        "ArticleDownload",
        secondary=article_concept_association,
        back_populates="concept_uris",
    )

    def __repr__(self):
        return f"<ConceptUri(concept_uri='{self.concept_uri}')>"

