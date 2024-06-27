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
        service.spreadsheets.create(json=SPREADSHEET_BODY)
    )
    spreadsheet_id = response["spreadsheetId"]
    return spreadsheet_id


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
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover("sheets", "v4")
    table_values = TABLE_VALUES_DRAFT.copy()
    table_values[0].append(now_date_time)
    table_values = [*table_values,
                    *[list(map(str,
                               [project.name,
                                project.close_date - project.create_date,
                                project.description])) for project in
                      charity_project]
                    ]
    update_body = {
        "majorDimension": "ROWS",
        "values": table_values
    }

    columns_value = max(len(items_to_count)
                        for items_to_count in table_values)
    rows_value = len(table_values)
    if (SPREADSHEET_ROWCOUNT_DRAFT < rows_value or
            SPREADSHEET_COLUMNCOUNT_DRAFT < columns_value):
        raise ValueError(ROW_COLUMN_COUNT_TOO_BIG.format(
            rows_value=rows_value,
            columns_value=columns_value,
            rowcount_draft=SPREADSHEET_ROWCOUNT_DRAFT,
            columncount_draft=SPREADSHEET_COLUMNCOUNT_DRAFT))

    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=f"R1C1:R{rows_value}C{columns_value}",
            valueInputOption="USER_ENTERED",
            json=update_body
        )
    )
    return spreadsheet_id
