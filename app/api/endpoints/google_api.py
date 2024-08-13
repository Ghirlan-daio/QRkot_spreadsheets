from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_google_api_set
from app.core.config import settings
from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud import charity_project_crud
from app.services.google_api import (set_user_permissions, spreadsheets_create,
                                     spreadsheets_update_value)

router = APIRouter()


@router.post("/", dependencies=[Depends(current_superuser)])
async def get_report(
        aiogoogle_object: Aiogoogle = Depends(get_service),
        session: AsyncSession = Depends(get_async_session)
):
    """Отчётность по закрытым проектам. Доступно только суперпользователям."""
    await check_google_api_set(settings=settings)
    projects = await charity_project_crud.get_the_end_projects(session)
    spreadsheet_id, spreadsheet_url = await spreadsheets_create(
        aiogoogle_object
    )
    await set_user_permissions(spreadsheet_id, aiogoogle_object)

    try:
        await spreadsheets_update_value(spreadsheet_id, projects,
                                        aiogoogle_object)
    except Exception as error:
        print(f"Произошла ошибка: {error}")

    return {"url": spreadsheet_url}
