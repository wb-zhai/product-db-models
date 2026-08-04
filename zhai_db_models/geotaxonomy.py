import enum

from geoalchemy2.types import Geometry
from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    Computed,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    PrimaryKeyConstraint,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import ARRAY, ENUM

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
        PrimaryKeyConstraint(
            "adm_code",
            "uri",
            name="pk_geo_taxonomy_concept_uris_direct_match",
        ),
    )

    adm_code = Column(
        String,
        ForeignKey(
            "geo_taxonomy.adm_code",
            name="fk_geo_taxonomy_concept_uris_direct_match_adm_code",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        nullable=False,
    )
    uri = Column(String, nullable=False)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    title = Column(String)
    wikidata_qid = Column(String)
    page_id = Column(Integer)
    rank = Column(Integer)
    confidence = Column(Float)
    resolution_method = Column(String)
    tie_reason = Column(String)
    wikidata_p31 = Column(ARRAY(String))


class GeotaxonomyPolygon(Base):
    # this is a read-only view
    __tablename__ = "geotaxonomy_polygons_fixed"
    __table_args__ = (
        {
            "schema": "shared",
            "info": {"skip_autogenerate": True}
        },
    )

    id = Column(Integer, primary_key=True)
    adm_code = Column(String)
    data_source = Column(String)
    adm0_code_iso_2 = Column(String)
    adm0_code_iso_3 = Column(String)
    adm_level = Column(Integer)
    geometry = Column(Geometry)
    is_preferred = Column(Boolean)


class GeoNameType(enum.Enum):
    display = "display"
    search = "search"
    wikipedia = "wikipedia"

class GeotaxonomyNames(Base):
    __tablename__ = "geo_taxonomy_names"
    __table_args__ = (
        PrimaryKeyConstraint(
            "adm_code",
            "name_type",
            "adm_name",
            name="pk_geo_taxonomy_names",
        ),
        Index(
            "idx_geo_taxonomy_names_adm_code",
            "adm_code",
        ),
        Index(
            "idx_geo_taxonomy_names_type_name",
            "name_type",
            "adm_name",
        ),
        Index(
            "idx_geo_taxonomy_names_name_trgm",
            "adm_name",
            postgresql_using="gin",
            postgresql_ops={
                "adm_name":
                "gin_trgm_ops",
            },
        ),
    )

    adm_code = Column(
        String,
        ForeignKey(
            "geo_taxonomy.adm_code",
            name="fk_geo_taxonomy_names_adm_code",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        nullable=False,
    )
    name_type = Column(
        ENUM(
            GeoNameType,
            name="geo_name_type",
            create_type=True,
        ),
        nullable=False,
    )
    adm_name = Column(
        String,
        nullable=False,
    )
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
