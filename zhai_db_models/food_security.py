from sqlalchemy import (
    REAL,
    CheckConstraint,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    PrimaryKeyConstraint,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import relationship

from .base import Base


# TODO: delete this table once endpoints are refactored to use FoodInsecurityScore
class FoodSecurityDummy(Base):
    __tablename__ = "food_security_dummy"
    __table_args__ = (
        {"info": {"skip_autogenerate": True}},
    )

    id = Column(Integer, primary_key=True)
    country = Column(String, nullable=False)
    adm_level = Column(Integer, nullable=False)
    adm0_code = Column(String, nullable=False)
    adm1_code = Column(String, nullable=True)
    adm2_code = Column(String, nullable=True)
    adm_code = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    ipc_score = Column(REAL, nullable=False)


class FoodInsecurityScore(Base):
    __tablename__ = "food_insecurity_scores"
    __table_args__ = (
        PrimaryKeyConstraint("adm_code", "year_month", name="pk_food_insecurity_scores"),
        CheckConstraint("EXTRACT(DAY FROM year_month) = 1", name="chk_month_first_day"),
        Index(
            'food_insecurity_scores_year_month_idx',
            'year_month',
            info={'skip_autogenerate': True}
        ),
        Index(
            'idx_food_insecurity_scores_year_month_adm_code_score',
            'year_month', 'adm_code',
            postgresql_include=['score'],
            info={'skip_autogenerate': True}
        )
    )

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    score = Column(Integer, nullable=False)
    adm_code = Column(String, nullable=False)
    year_month = Column(Date, nullable=False)


class RiskFactor(Base):
    __tablename__ = "risk_factors"
    __table_args__ = (
        UniqueConstraint("name", "cluster", name="uq_risk_factors_name_cluster"),
    )

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    name = Column(String, nullable=False, unique=True)
    # TODO: create a dedicated cluster table
    cluster = Column(String, nullable=False)
    scores = relationship("RiskFactorScore", backref="risk_factors")


class RiskFactorScore(Base):
    __tablename__ = "risk_factor_scores"
    __table_args__ = (
        PrimaryKeyConstraint("risk_factor_id", "adm_code", "year_month", name="pk_risk_factor_scores"),
        CheckConstraint("EXTRACT(DAY FROM year_month) = 1", name="chk_risk_factor_scores_month_first_day"),
        Index(
            'risk_factor_scores_year_month_idx',
            'year_month',
            info={'skip_autogenerate': True}
        ),
    )

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    risk_factor_id = Column(Integer, ForeignKey("risk_factors.id"), nullable=False)
    score = Column(Integer, nullable=False)
    adm_code = Column(String, nullable=False)
    year_month = Column(Date, nullable=False)