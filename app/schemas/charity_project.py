from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt

from app.constants import EXAMPLE_FULL_AMOUNT


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None)
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid
        min_anystr_length = 1


class CharityProjectCreate(CharityProjectBase):
    """Схема для создания объекта благотворительного проекта."""
    name: str = Field(..., max_length=100)
    description: str = Field(...)
    full_amount: PositiveInt

    class Config:
        schema_extra = {
            "example": {
                "name": "Голодающие котики: накормим их вместе!",
                "description": "Закупка корма для котиков.",
                "full_amount": EXAMPLE_FULL_AMOUNT
            }
        }


class CharityProjectUpdate(CharityProjectBase):
    """Схема для обновления объекта благотворительного проекта."""

    class Config:
        extra = Extra.forbid
        schema_extra = {
            "example": {
                "name": "Котики категории БОМЖ",
                "description": "Обустройство хвостатой колонии.",
                "full_amount": EXAMPLE_FULL_AMOUNT
            }
        }


class CharityProjectDB(CharityProjectCreate):
    """Схема для ответа при обращении к ручкам проектов."""
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
