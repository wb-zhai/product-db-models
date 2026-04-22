import enum

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Index,
    PrimaryKeyConstraint,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import ENUM, UUID

from .base import Base


class TrainingSplit(enum.Enum):
    train = "train"
    val = "val"
    test = "test"


class EvalMetric(enum.Enum):
    abs_error = "abs_error"
    squared_error = "squared_error"


class ModelingRegressionEvaluation(Base):
    __tablename__ = "modeling_regression_evaluation"
    __table_args__ = (
        PrimaryKeyConstraint(
            "cohort_id",
            "experiment_id",
            "run_name",
            "date",
            "adm_code",
            "split",
            "metric",
            name="pk_modeling_regression_evaluation",
        ),
        Index(
            "ix_modeling_regression_evaluation_adm_code",
            "adm_code",
        ),
        {
            "schema": "modeling",
        },
    )

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    cohort_id = Column(UUID(as_uuid=True), nullable=False)
    experiment_id = Column(UUID(as_uuid=True), nullable=False)
    dataset_url = Column(String, nullable=False)
    run_name = Column(String, nullable=False)
    date = Column(DateTime(timezone=True), nullable=False)
    adm_code = Column(
        String,
        ForeignKey(
            "geo_taxonomy.adm_code",
            name="fk_modeling_regression_evaluation_adm_code",
            onupdate="CASCADE",
        ),
        nullable=False,
    )
    split = Column(
        ENUM(
            TrainingSplit,
            name="split_enum",
            create_type=True,
        ),
        nullable=False,
    )
    y_true = Column(Float, nullable=False)
    y_pred = Column(Float, nullable=False)
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
    score = Column(Float, nullable=False)
