import datetime as dt

from sqlalchemy import Boolean, Column, DateTime, Integer

from app.constants import ZERO_CHARITY_AMOUNT
from app.core.db import Base


class CharityDonation(Base):
    """Родительский класс для моделей проектов и пожертвований."""
    __abstract__ = True

    full_amount = Column(Integer)
    invested_amount = Column(Integer, default=ZERO_CHARITY_AMOUNT)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=dt.datetime.utcnow)
    close_date = Column(DateTime)
