import enum
from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    Computed,
    DateTime,
    Float,
    ForeignKey,
    String,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import ENUM

from .base import Base

class TrainingSplit(enum.Enum):
    train = "train"
    val = "val"
    test = "test"

class EvalMetric(enum.Enum):
    abs_error = 'abs_error'
    squared_error = 'squared_error'

class ModelingRegressionEvaluation(Base):
    __tablename__ = "modeling_regression_evaluation"
    __table_args__ = (
        {
            "schema": "modeling",
        },
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    date = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
    adm_code = Column(
        String,
        ForeignKey(
            "geo_taxonomy.adm_code",
            name="fk_modeling_regression_evaluation_adm_code",
            onupdate="CASCADE",
        ),
        nullable=False,
        index=True,
    )
    split = Column(
        ENUM(
            TrainingSplit,
            name="split_enum",
            create_type=True,
        ),
        nullable=False,
        index=True,
    )
    y_true = Column(Float)
    y_pred = Column(Float)
    metric = Column(
        ENUM(
            EvalMetric,
            name="metric_enum",
            create_type=True,
        ),
        nullable=False,
        index=True,
    )
    score = Column(
        Float,
        Computed(
            text("""
            CASE
              WHEN metric = 'abs_error'     THEN ABS(y_pred - y_true)
              WHEN metric = 'squared_error' THEN POWER(y_pred - y_true, 2)
            ELSE NULL
            END
            """),
            persisted=True,
        )
    )
