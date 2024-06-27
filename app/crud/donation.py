from typing import List

from sqlalchemy import select

from app.core.db import AsyncSession
from app.crud.base import CRUDBase
from app.models import Donation, User


class CRUDDonation(CRUDBase):

    async def get_user_donations(
            self, user: User,
            session: AsyncSession
    ) -> List[Donation]:
        """
        Возвращает список пожертвований пользователя, выполняющего запрос.
        """
        donations = await session.execute(
            select(self.model).where(
                self.model.user_id == user.id
            )
        )
        donations = donations.scalars().all()
        return donations


donation_crud = CRUDDonation(Donation)
