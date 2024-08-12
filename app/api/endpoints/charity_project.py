from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_charity_project_before_delete,
                                check_charity_project_closed,
                                check_charity_project_exists,
                                check_charity_project_name_unique,
                                check_correct_full_amount_for_update)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import charity_project_crud
from app.crud.base import CRUDBase
from app.models import Donation
from app.schemas import (CharityProjectCreate, CharityProjectDB,
                         CharityProjectUpdate)
from app.services.donation_utils import allocate_donation_between_funds

router = APIRouter()


@router.get(
    "/",
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
        session: AsyncSession = Depends(get_async_session)
):
    """
    Получает список всех благотворительных проектов.
    Доступно для всех пользователей сервиса (в том числе анонимных).
    """
    return await charity_project_crud.get_multi(session)


@router.post(
    "/",
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session)
):
    """Создаёт благотворительный проект. Доступно для суперпользователей."""
    await check_charity_project_name_unique(
        charity_project.name, session
    )
    new_charity_project = await charity_project_crud.create(
        charity_project, session
    )
    update_donations = allocate_donation_between_funds(
        new_charity_project,
        sources=await CRUDBase.get_all_open_obj(Donation, session=session)
    )
    session.add_all(update_donations)
    await session.commit()
    await session.refresh(new_charity_project)
    return new_charity_project


@router.delete(
    "/{project_id}",
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def delete_charity_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    """Удаляет благотворительный проект. Доступно для суперпользователей."""
    charity_project = await check_charity_project_before_delete(
        project_id, session
    )
    deleted_charity_project = await charity_project_crud.delete(
        charity_project, session
    )
    return deleted_charity_project


@router.patch(
    "/{project_id}",
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charity_project(
        project_id: int,
        object_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """
    Редактирует благотворительный проект.
    Доступно для суперпользователей.
    """
    charity_project = await check_charity_project_exists(
        project_id, session
    )
    check_charity_project_closed(charity_project)

    if object_in.full_amount is not None:
        await check_correct_full_amount_for_update(
            project_id, session, object_in.full_amount
        )

    if object_in.name is not None:
        await check_charity_project_name_unique(
            object_in.name, session
        )

    charity_project = await charity_project_crud.update(
        charity_project, object_in, session
    )
    update_donations = allocate_donation_between_funds(
        charity_project,
        sources=await CRUDBase.get_all_open_obj(Donation, session=session)
    )
    session.add_all(update_donations)
    await session.commit()
    await session.refresh(charity_project)
    return charity_project
