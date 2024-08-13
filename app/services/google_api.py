from datetime import datetime

from aiogoogle import Aiogoogle

from app.constants import (FORMAT, ROW_COLUMN_COUNT_TOO_BIG, SPREADSHEET_BODY,
                           SPREADSHEET_COLUMNCOUNT_DRAFT,
                           SPREADSHEET_ROWCOUNT_DRAFT, TABLE_VALUES_DRAFT)
from app.core.config import settings
from app.models import CharityProject


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    """Создаёт документ."""
    date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover("sheets", "v4")
    spreadsheets_body = SPREADSHEET_BODY.copy()
    spreadsheets_body["properties"]["title"] += date_time
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheets_body)
    )
    return (response["spreadsheetId"], response["spreadsheetUrl"])


async def set_user_permissions(
        spreadsheetid: str,
        wrapper_services: Aiogoogle
) -> None:
    """Предоставляет права доступа."""
    permissions = {"type": "user",
                   "role": "writer",
                   "emailAddress": settings.email}
    service = await wrapper_services.discover("drive", "v3")
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid,
            json=permissions,
            fields="id"
        )
    )


async def spreadsheets_update_value(
        spreadsheet_id: str,
        charity_project: list[CharityProject],
        wrapper_services: Aiogoogle
) -> str:
    """Заполняет документ данными."""
    sorted_projects = sorted(
        charity_project,
        key=lambda obj: obj.close_date - obj.create_date
    )
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover("sheets", "v4")
    table = TABLE_VALUES_DRAFT.copy()
    table[0].append(now_date_time)
    table = [
        *table,
        *[
            list(map(str, [
                project.name,
                project.close_date - project.create_date,
                project.description
            ]))
            for project in sorted_projects
        ]
    ]
    update_body = {
        "majorDimension": "ROWS",
        "values": table
    }

    columns = max(map(len, table))
    rows = len(table)
    if (
        SPREADSHEET_ROWCOUNT_DRAFT < rows or
        SPREADSHEET_COLUMNCOUNT_DRAFT < columns
    ):  # flake8 ругается, если убрать сдвиг
        raise ValueError(ROW_COLUMN_COUNT_TOO_BIG.format(
            rows_value=rows,
            columns_value=columns
        ))

    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=f"R1C1:R{rows}C{columns}",
            valueInputOption="USER_ENTERED",
            json=update_body
        )
    )
    return spreadsheet_id
