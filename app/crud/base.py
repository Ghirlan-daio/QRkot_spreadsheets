from datetime import datetime
from typing import List, Optional, Union

from fastapi.encoders import jsonable_encoder
from sqlalchemy import false, select

from app.core.db import AsyncSession
from app.models import CharityDonation, User


class CRUDBase:

    def __init__(self, model):
        self.model = model

    async def get(self, obj_id, session: AsyncSession):
        db_obj = await session.execute(
            select(self.model).where(
                self.model.id == obj_id
            )
        )
        return db_obj.scalars().first()

    async def get_multi(self, session: AsyncSession):
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
            self,
            obj_in,
            session: AsyncSession,
            user: Optional[User] = None,
            commit_flag: Optional[bool] = True
    ):
        obj_in_data = obj_in.dict()
        if user is not None:
            obj_in_data["user_id"] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        if commit_flag:
            await session.commit()
            await session.refresh(db_obj)
        return db_obj

    async def update(self, db_obj, obj_in, session: AsyncSession):
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def delete(self, db_obj, session: AsyncSession):
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    def close_obj(obj: CharityDonation) -> None:
        """Закрывает благотворительный проект или пожертвование."""
        obj.fully_invested = True
        obj.close_date = datetime.now()

    async def get_all_open_obj(
            model: CharityDonation,
            session: AsyncSession,
    ) -> List[CharityDonation]:
        """Получает все открытые благ. проекты или пожертвования."""
        objects = await session.execute(
            select(model).where(
                model.fully_invested == false()
            ).order_by(model.create_date)
        )
        return objects.scalars().all()
