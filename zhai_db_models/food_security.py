from sqlalchemy import REAL, Column, Integer, String

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