from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.constants import EXCLUDE_FIELDS
from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud import donation_crud
from app.models import User
from app.schemas import DonationCreate, DonationDB
from app.services.donation_utils import allocate_donation_between_funds

router = APIRouter()


@router.get(
    "/",
    response_model=list[DonationDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session)
):
    """Получает все донаты. Доступно для суперпользователю."""
    return await donation_crud.get_multi(session=session)


@router.post(
    "/",
    response_model=DonationDB,
    response_model_exclude_none=True,
    response_model_exclude={*EXCLUDE_FIELDS},
)
async def create_donation(
        donation_in: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    """Создаёт пожертвование. Доступно для авторизованного пользователя."""
    new_donation = await donation_crud.create(
        donation_in, session, user
    )
    await allocate_donation_between_funds(new_donation, session)
    await session.refresh(new_donation)
    return new_donation


@router.get(
    "/my",
    response_model=list[DonationDB],
    response_model_exclude={*EXCLUDE_FIELDS},
)
async def get_user_donations(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    """
    Получает список пожертвований текущего пользователя.
    Доступно для авторизированного пользователя.
    """
    return await donation_crud.get_user_donations(user=user, session=session)
