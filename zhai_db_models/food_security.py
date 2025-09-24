from sqlalchemy import (
    REAL,
    CheckConstraint,
    Column,
    Date,
    DateTime,
    Integer,
    String,
    UniqueConstraint,
    func,
)

from .base import Base


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
        CheckConstraint("EXTRACT(DAY FROM year_month) = 1", name="chk_month_first_day"),
        UniqueConstraint("year_month", "adm_code", name="uq_food_insecurity_scores")
    )

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    score = Column(Integer, nullable=False)
    adm_code = Column(String, nullable=False)
    year_month = Column(Date, nullable=False)