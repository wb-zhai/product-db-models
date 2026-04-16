from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    PrimaryKeyConstraint,
    String,
    func,
)
from sqlalchemy.orm import declared_attr

from .base import Base

class KGRiskFactor(Base):
    __tablename__ = "risk_factors"
    __table_args__ = (
        {
            "schema": "knowledge_graph",
        },
    )

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now(),
        server_default=func.now(),
    )
    name = Column(String, nullable=False, unique=True)
    version = Column(Integer, nullable=False)

class KGTaggedArticles(Base):
    __tablename__ = "tagged_articles"
    __table_args__ = (
        PrimaryKeyConstraint(
            "tag_method_id",
            "article_uri",
            name="pk_tagged_articles",
        ),
        {
            "schema": "knowledge_graph",
        },
    )

    article_uri = Column(
        String,
        ForeignKey(
            "article_downloads_ref.uri",
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


class KGAbstractArticleTags(Base):
    __abstract__ = True

    @declared_attr
    def article_uri(cls):
        return Column(
            String,
            ForeignKey(
                "article_downloads_ref.uri",
                name=f"fk_{cls.__tablename__}_article_uri",
            ),
            nullable=False,
            index=True,
        )

    @declared_attr
    def tag_method_id(cls):
        return Column(
            Integer,
            ForeignKey(
                "tag_method_urls.method_id",
                name=f"fk_{cls.__tablename__}_method_id",
            ),
            nullable=False,
            index=True,
        )

    article_position_group = Column(String, nullable=False)
    article_position_start = Column(Integer, nullable=False)
    article_position_end = Column(Integer)

class KGArticleRiskFactorTags(KGAbstractArticleTags):
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
        {
            "schema": "knowledge_graph",
        },
    )

    risk_factor = Column(
        Integer,
        ForeignKey(
            "knowledge_graph.risk_factors.id",
            name="fk_article_risk_factor_tags_risk_factor_id",
        ),
        nullable=False,
        index=True,
    )

class KGArticleLocationTags(KGAbstractArticleTags):
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
        Index(
            "ix_article_location_tags_adm_code_article_uri",
            "adm_code",
            "article_uri",
        ),
        {
            "schema": "knowledge_graph",
        },
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
