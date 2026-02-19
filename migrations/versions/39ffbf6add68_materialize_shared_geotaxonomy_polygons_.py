"""Materialize shared.geotaxonomy_polygons_fixed along with pre-shifted bboxes

Revision ID: 39ffbf6add68
Revises: 0be48872e356
Create Date: 2026-02-19 11:42:09.190688

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '39ffbf6add68'
down_revision: Union[str, Sequence[str], None] = '0be48872e356'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


CREATE_MATERIALIZED_VIEW_SQL = """
CREATE MATERIALIZED VIEW IF NOT EXISTS shared.geotaxonomy_polygons_fixed AS
WITH geob_iso_coded AS (
  -- patch shapeID with shapeISO[-shapeID] as adm_code for geob-preferred countries
  SELECT
    id,
    data_source,
    adm0_code_iso2,
    adm0_code_iso3,
    gt_polygons.adm_level,
    COALESCE(geob.adm2_code, geob.adm1_code, geob.adm0_code) adm_code,
    geometry,
    is_preferred,
    geometry_fixed
  FROM shared.geotaxonomy_polygons gt_polygons
  JOIN staging.geotaxonomy_geob_master geob
  ON adm_code = shape_id
  WHERE data_source = 'geob' AND is_preferred
),
wof_hierarchy_coded AS (
  SELECT
    gt_polygons.id,
    data_source,
    adm0_code_iso2,
    adm0_code_iso3,
    gt_polygons.adm_level,
    COALESCE(wof.adm2_code, wof.adm1_code, wof.adm0_code) adm_code,
    geometry,
    is_preferred,
    geometry_fixed
  FROM shared.geotaxonomy_polygons gt_polygons
  JOIN staging.geotaxonomy_wof_master wof
  ON wof.id::VARCHAR = gt_polygons.adm_code
  WHERE data_source = 'wof' AND is_preferred
),
adm_code_patched AS (
  SELECT id, data_source, adm0_code_iso2, adm0_code_iso3, adm_level, adm_code, geometry, is_preferred, geometry_fixed FROM shared.geotaxonomy_polygons WHERE NOT (data_source IN ('geob', 'wof') AND is_preferred)
  UNION
  SELECT * FROM geob_iso_coded
  UNION
  SELECT * FROM wof_hierarchy_coded
),
crosses_antimeridian AS (
  SELECT
    id,
    data_source,
    adm0_code_iso2,
    adm0_code_iso3,
    adm_level,
    adm_code,
    st_split(
      COALESCE(geometry_fixed, geometry),
      st_setsrid(ST_MAKELINE(ST_Point(180, -90), ST_Point(180, 90)), 4326)
    ) geometry,
    is_preferred
  FROM
    adm_code_patched
  WHERE
    ST_INTERSECTS(
      COALESCE(geometry_fixed, geometry),
      st_setsrid(ST_MAKELINE(ST_Point(180, -90), ST_Point(180, 90)), 4326)
    )
)
SELECT * FROM crosses_antimeridian
UNION ALL
SELECT
  id,
  data_source,
  adm0_code_iso2,
  adm0_code_iso3,
  adm_level,
  adm_code,
  COALESCE(geometry_fixed, geometry) geometry,
  is_preferred
FROM
  adm_code_patched
WHERE
  NOT ST_INTERSECTS(
    COALESCE(geometry_fixed, geometry),
    st_setsrid(ST_MAKELINE(ST_Point(180, -90), ST_Point(180, 90)), 4326)
  );
"""


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(CREATE_MATERIALIZED_VIEW_SQL)
    op.execute("""CREATE INDEX idx_geotaxonomy_polygons_fixed_adm_code_preferred
        ON shared.geotaxonomy_polygons_fixed (adm_code, is_preferred);""")
    op.execute("""CREATE INDEX idx_geotaxonomy_polygons_fixed_geometry
        ON shared.geotaxonomy_polygons_fixed USING GIST (geometry);""")

def downgrade() -> None:
    """Downgrade schema."""
    # this will not work if another view depends on this materialized view
    op.execute("DROP MATERIALIZED VIEW shared.geotaxonomy_polygons_fixed;")