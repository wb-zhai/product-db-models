import enum

from geoalchemy2 import Geometry
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    PrimaryKeyConstraint,
    String,
    Table,
)
from sqlalchemy.dialects.postgresql import ENUM, JSONB, UUID, DATERANGE
from sqlalchemy.orm import relationship

from .base import Base


class ArticleQuery(Base):
    __tablename__ = "article_queries"

    uuid = Column(UUID(as_uuid=True), primary_key=True)
    body = Column(JSONB, nullable=False)


class ArticleUri(Base):
    __tablename__ = "article_uris"

    uri = Column(String, primary_key=True)
    query_uuid = Column(
        UUID(as_uuid=True),
        ForeignKey("article_queries.uuid", name="fk_article_uris_query_uuid"),
        nullable=False,
    )
    weight = Column(Float, nullable=False)
    page_id = Column(Integer, nullable=False)
    queried_at = Column(DateTime, nullable=False)
    request_id = Column(UUID(as_uuid=True), nullable=False)
    published_period = Column(DATERANGE) # , nullable=False)


article_concept_association = Table(
    "article_concept_association",
    Base.metadata,
    Column("article_uri", String, ForeignKey("article_downloads.uri", name="fk_article_concept_association_article_uri"), primary_key=True),
    Column("concept_uri", String, ForeignKey("concept_uris.concept_uri", name="fk_article_concept_association_concept_uri"), primary_key=True),
)

class ArticleType(enum.Enum):
    pr = 'pr'
    blog = 'blog'
    news = 'news'

class ArticleDownload(Base):
    __tablename__ = "article_downloads"

    uri = Column(String, primary_key=True)
    source_uri = Column(String)
    cloud_uri = Column(String, unique=True, nullable=False)
    language = Column(String, nullable=False)
    published_at = Column(DateTime, nullable=False)
    is_duplicate = Column(Boolean)
    article_type = Column(ENUM(
        ArticleType,
        name="article_enum",
        create_type=True,
    ))
    title = Column(String)
    body = Column(String)

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

    concept_uri = Column(String, primary_key=True)
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


class ArticleRiskFactorTags(Base):
    __tablename__ = "article_risk_factor_tags"
    __table_args__ = (
        PrimaryKeyConstraint(
            "article_uri",
            "risk_factor",
            "tag_method_url",
            name="pk_article_risk_factor_tags",
        ),
    )

    article_uri = Column(
        String,
        ForeignKey(
            "article_downloads.uri",
            name="fk_article_risk_factor_tags_article_uri",
        ),
        nullable=False,
        primary_key=True,
    )
    risk_factor = Column(
        Integer,
        ForeignKey(
            "risk_factors.id",
            name="fk_article_risk_factor_tags_risk_factor_id",
        ),
        nullable=False,
        primary_key=True,
    )
    strength = Column(Float)
    tag_method_url = Column(String, nullable=False, primary_key=True)


class ArticleLocationTags(Base):
    __tablename__ = "article_location_tags"
    __table_args__ = (
        PrimaryKeyConstraint(
            "article_uri",
            "adm_code",
            "tag_method_url",
            name="pk_article_location_tags",
        ),
    )

    article_uri = Column(
        String,
        ForeignKey(
            "article_downloads.uri",
            name="fk_article_location_tags_article_uri",
        ),
        nullable=False,
        primary_key=True,
    )
    adm_code = Column(
        String,
        ForeignKey(
            "geo_taxonomy.adm_code",
            name="fk_article_location_tags_adm_code",
        ),
        nullable=False,
        primary_key=True,
    )
    strength = Column(Float)
    tag_method_url = Column(String, nullable=False, primary_key=True)
