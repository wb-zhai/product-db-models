import enum

from geoalchemy2 import Geometry
from sqlalchemy import (
    func,
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
    source_uri = Column(String, nullable=True)
    cloud_uri = Column(String, unique=True, nullable=False)
    language = Column(String, nullable=False, index=True)
    published_at = Column(DateTime, nullable=False)
    is_duplicate = Column(Boolean, nullable=True, default=False)
    article_type = Column(
        ENUM(
            ArticleType,
            name="article_enum",
            create_type=True,
        ),
        nullable=True,
        index=True,
    )
    title = Column(String, nullable=True)
    body = Column(String, nullable=True)

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
    concept_type = Column(
        ENUM(
            ConceptType,
            name="concept_enum",
            create_type=True,
        ),
        nullable=False,
        index=True,
    )
    geo_names_id = Column(Integer, nullable=True)
    geom = Column(Geometry("POINT", srid=4326), nullable=True)

    article_downloads = relationship(
        "ArticleDownload",
        secondary=article_concept_association,
        back_populates="concept_uris",
    )

    def __repr__(self):
        return f"<ConceptUri(concept_uri='{self.concept_uri}')>"


class TaggedMethods(Base):
    __tablename__ = "tag_method_urls"

    method_id = Column(Integer, primary_key=True)
    method_url = Column(String, nullable=False, unique=True)


class TaggedArticles(Base):
    __tablename__ = "tagged_articles"
    __table_args__ = (
        PrimaryKeyConstraint(
            "tag_method_id",
            "article_uri",
            name="pk_tagged_articles",
        ),
    )

    article_uri = Column(
        String,
        ForeignKey(
            "article_downloads.uri",
            name="fk_tagged_articles_article_uri",
        ),
        nullable=False,
        index=True,
    )
    tag_method_id = Column(
        Integer,
        ForeignKey(
            "tag_method_urls.method_id",
            name="fk_tagged_articles_method_id",
        ),
        nullable=False,
        index=True,
    )
    tagged_at = Column(DateTime, default=func.now())


class AbstractArticleTags(Base):
    __abstract__ = True

    article_uri = Column(
        String,
        ForeignKey(
            "article_downloads.uri",
            name="fk_%(table_name)s_article_uri",
        ),
        nullable=False,
        index=True,
    )
    tag_method_id = Column(
        Integer,
        ForeignKey(
            "tag_method_urls.method_id",
            name="fk_%(table_name)s_method_id",
        ),
        nullable=False,
        index=True,
    )
    article_position_group = Column(String, nullable=False)
    article_position_start = Column(Integer, nullable=False)
    article_position_end = Column(Integer)

class ArticleRiskFactorTags(AbstractArticleTags):
    __tablename__ = "article_risk_factor_tags"
    __table_args__ = (
        PrimaryKeyConstraint(
            "tag_method_id",
            "risk_factor",
            "article_uri",
            "article_position_group",
            "article_position_start",
            name="pk_article_risk_factor_tags",
        ),
    )

    risk_factor = Column(
        Integer,
        ForeignKey(
            "risk_factors.id",
            name="fk_article_risk_factor_tags_risk_factor_id",
        ),
        nullable=False,
        index=True,
    )

class ArticleLocationTags(AbstractArticleTags):
    __tablename__ = "article_location_tags"
    __table_args__ = (
        PrimaryKeyConstraint(
            "tag_method_id",
            "adm_code",
            "article_uri",
            "article_position_group",
            "article_position_start",
            name="pk_article_location_tags",
        ),
    )

    adm_code = Column(
        String,
        ForeignKey(
            "geo_taxonomy.adm_code",
            name="fk_article_location_tags_adm_code",
            onupdate="CASCADE",
        ),
        nullable=False,
        index=True,
    )
