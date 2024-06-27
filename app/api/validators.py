from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.constants import (CLOSE_PROJECT_UPDATE, DELETE_START_INVEST_PROJECT,
                           INVALID_INVESTED_AMOUNT, NOT_FOUND_PROJECT,
                           PROJECT_EXISTS, ZERO_CHARITY_AMOUNT)
from app.core.config import Settings
from app.crud import charity_project_crud
from app.models import CharityProject


async def check_charity_project_exists(
        charity_project_id: int,
        session: AsyncSession
) -> CharityProject:
    """Проверяет существование благотворительного проекта по его id."""
    charity_project = await charity_project_crud.get(
        charity_project_id, session
    )
    if charity_project is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=NOT_FOUND_PROJECT
        )
    return charity_project


async def check_charity_project_name_unique(
        charity_project_name: str,
        session: AsyncSession
) -> None:
    """Проверяет благотворительный проект на уникальность."""
    charity_project = await charity_project_crud.get_charity_project_by_name(
        charity_project_name, session
    )
    if charity_project is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=PROJECT_EXISTS
        )


async def check_charity_project_before_delete(
        charity_project_id: int,
        session: AsyncSession
) -> CharityProject:
    """Проверяет наличие инвест. средств в благотворительном проекте."""
    charity_project = await check_charity_project_exists(
        charity_project_id, session
    )
    if charity_project.invested_amount > ZERO_CHARITY_AMOUNT:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=DELETE_START_INVEST_PROJECT
        )
    return charity_project


async def check_charity_project_closed(project: CharityProject) -> None:
    """Проверяет закрытие благотворительного проекта."""
    if project.fully_invested:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=CLOSE_PROJECT_UPDATE,
        )


async def check_correct_full_amount_for_update(
        project_id: int,
        session: AsyncSession,
        full_amount_update: int
):
    """Проверяет возможность редактирования проекта"""
    charity_project = await check_charity_project_exists(
        project_id, session
    )
    if charity_project.invested_amount > full_amount_update:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=INVALID_INVESTED_AMOUNT
        )


async def check_google_api_set(settings: Settings):
    """Проверка параметров Google API."""
    if not all([settings.type,
                settings.project_id,
                settings.private_key_id,
                settings.private_key,
                settings.client_email,
                settings.client_id,
                settings.auth_uri,
                settings.token_uri,
                settings.auth_provider_x509_cert_url,
                settings.client_x509_cert_url,
                settings.email]):
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=("При формировании отчёта возникла ошибка "
                    "Проверьте параметры Google API.")
        )
