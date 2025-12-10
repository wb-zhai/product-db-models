from geoalchemy2.types import Geometry
from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    Computed,
    DateTime,
    Index,
    Integer,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB

from .base import Base


class Geotaxonomy(Base):
    __tablename__ = "geo_taxonomy"
    __table_args__ = (
        Index(
            "idx_geotaxonomy_adm_name_trgm",
            "adm_name",
            postgresql_using="gin",
            postgresql_ops={"adm_name": "gin_trgm_ops"},
        ),
        UniqueConstraint("adm_code", name="unique_adm_code"),
        # comment the line below to generate migrations for this table
        {"info": {"skip_autogenerate": True}},
    )

    id = Column(Integer, primary_key=True)
    adm_level = Column(
        Integer,
        CheckConstraint("adm_level BETWEEN 0 AND 2", name="check_adm_level"),
        nullable=False,
    )
    adm0_code = Column(String, nullable=False)
    adm0_name = Column(String, nullable=False)
    adm1_code = Column(String)
    adm1_name = Column(String)
    adm2_code = Column(String)
    adm2_name = Column(String)
    adm_code = Column(
        String, Computed(func.coalesce(adm2_code, adm1_code, adm0_code), persisted=True)
    )
    adm_name = Column(
        String, Computed(func.coalesce(adm2_name, adm1_name, adm0_name), persisted=True)
    )
    # TODO: change to datetime
    reference_period_start = Column(String)
    reference_period_end = Column(String)
    is_zhai_covered = Column(Boolean, nullable=False, default=False)


class GeotaxonomyShape(Base):
    __tablename__ = "geo_taxonomy_shapes"
    __table_args__ = (
        UniqueConstraint("code", name="unique_code"),
        {"info": {"skip_autogenerate": True}},
    )

    id = Column(Integer, primary_key=True)
    code = Column(String)
    geom = Column(Geometry)
    has_ocha = Column(Boolean, nullable=False, default=False)
    adm_level = Column(Integer, nullable=False, default=-1)


class GeotaxonomyConceptUriDirectMatch(Base):
    __tablename__ = "geo_taxonomy_concept_uris_direct_match"
    __table_args__ = (
        UniqueConstraint("code", "uri", name="unique_code_uri_direct_match"),
    )

    id = Column(Integer, primary_key=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    code = Column(String)
    name = Column(String)
    uri = Column(String)
    country_uri = Column(String)
    meta = Column(JSONB)


class GeotaxonomyPolygon(Base):
    # this is a read-only view
    __tablename__ = "shared.geotaxonomy_polygons_fixed"
    __table_args__ = (
        {"info": {"skip_autogenerate": True}},
    )

    id = Column(Integer, primary_key=True)
    code = Column(String)
    data_source = Column(String)
    adm0_code_iso_2 = Column(String)
    adm0_code_iso_3 = Column(String)
    adm_level = Column(Integer)
    geometry = Column(Geometry)
