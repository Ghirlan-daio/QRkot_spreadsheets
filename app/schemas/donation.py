from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, PositiveInt

from app.constants import EXAMPLE_FULL_AMOUNT


class DonationBase(BaseModel):
    full_amount: Optional[PositiveInt]
    comment: Optional[str]

    class Config:
        extra = Extra.forbid


class DonationCreate(DonationBase):
    """Схема для создания объекта пожертвования."""
    full_amount: PositiveInt

    class Config:
        schema_extra = {
            "example": {
                "comment": "Для котиков не жалко!",
                "full_amount": EXAMPLE_FULL_AMOUNT
            }
        }


class DonationDB(DonationCreate):
    """Cхема для ответа при обращении к ручкам пожертвований."""
    id: int
    create_date: datetime
    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
