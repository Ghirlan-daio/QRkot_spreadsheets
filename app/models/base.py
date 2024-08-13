import datetime as dt

from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Integer

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
    __table_args__ = (
        CheckConstraint(f"full_amount > {ZERO_CHARITY_AMOUNT}",
                        name="check_full_amount_positive"),
        CheckConstraint("invested_amount <= full_amount",
                        name="check_invested_amount_not_exceed"),
        CheckConstraint(f"{ZERO_CHARITY_AMOUNT} <= invested_amount "
                        f"<= full_amount", name="check_invest_amt_positive"),
    )

    def __repr__(self):
        return (
            f"CharityDonation(full_amount={self.full_amount}, "
            f"invested_amount={self.invested_amount}, "
            f"create_date={self.create_date}, "
            f"close_date={self.close_date})"
        )
