from typing import List, Optional

from sqlalchemy import select

from app.core.db import AsyncSession
from app.crud.base import CRUDBase
from app.models import CharityProject


class CRUDCharityProject(CRUDBase):

    async def get_charity_project_by_name(
            self, project_name: str,
            session: AsyncSession
    ) -> Optional[CharityProject]:
        """Получает объект проекта по его названию."""
        charity_project = await session.execute(
            select(self.model).where(
                self.model.name == project_name
            )
        )
        return charity_project.scalars().first()

    async def get_the_end_projects(
            self,
            session: AsyncSession,
    ) -> List[CharityProject]:
        """Получает завершённые проекты."""
        projects = await session.execute(
            select(CharityProject).where(
                CharityProject.fully_invested
            )
        )
        projects = projects.scalars().all()
        return projects


charity_project_crud = CRUDCharityProject(CharityProject)
