from datetime import datetime
from typing import List, Type, TypeVar, Union

from sqlalchemy import false, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation

ModelType = TypeVar("ModelType", CharityProject, Donation)


async def close_obj(obj: Union[CharityProject, Donation]) -> None:
    """Закрывает благотворительный проект или пожертвование."""
    obj.fully_invested = True
    obj.close_date = datetime.now()


async def get_all_open_obj(
        model: Type[ModelType],
        session: AsyncSession,
) -> List[Union[CharityProject, Donation]]:
    """Получает все открытые благ. проекты или пожертвования."""
    objects = await session.execute(
        select(model).where(
            model.fully_invested == false()
        ).order_by(model.create_date)
    )
    return objects.scalars().all()


async def allocate_donation_between_funds(
        obj: Union[CharityProject, Donation],
        session: AsyncSession,
) -> None:
    """Распределяет сделанные пожертвования по благ. проектам."""
    models = (CharityProject, Donation)
    model = models[isinstance(obj, CharityProject)]
    objects = await get_all_open_obj(model, session)
    if objects:
        amount_invest = obj.full_amount
        for object in objects:
            amount = object.full_amount - object.invested_amount
            invested_amount = min(amount, amount_invest)
            object.invested_amount += invested_amount
            obj.invested_amount += invested_amount
            amount_invest -= invested_amount

            if object.full_amount == object.invested_amount:
                await close_obj(object)

            if not amount_invest:
                await close_obj(obj)
                break
        await session.commit()
