ZERO_CHARITY_AMOUNT = 0
LIFETIME_TOKEN = 3_600
NOT_FOUND_PROJECT = "Проект не найден!"
PROJECT_EXISTS = "Имя проекта не уникально!"
CLOSE_PROJECT_UPDATE = "Проект нельзя отредактировать, так как он уже закрыт!"
DELETE_START_INVEST_PROJECT = ("Вы не можете удалить проект, в который уже "
                               "внесены средства!")
INVALID_INVESTED_AMOUNT = ("Сумма сбора в проекте не может быть меньше "
                           "внесённой суммы!")
EXCLUDE_FIELDS = (
    "user_id",
    "invested_amount",
    "fully_invested",
    "close_date"
)
EXAMPLE_FULL_AMOUNT = 1_000_000
MIN_LEN_PASSWORD = 3

GOOGLE_SHEETS_URL = "https://docs.google.com/spreadsheets/d/"
FORMAT = "%Y/%m/%d %H:%M:%S"
SPREADSHEET_ROWCOUNT_DRAFT = 100
SPREADSHEET_COLUMNCOUNT_DRAFT = 11
SPREADSHEET_BODY = dict(
    properties=dict(
        title="Отчет на ",
        locale="ru_RU",
    ),
    sheets=[dict(properties=dict(
        sheetType="GRID",
        sheetId=0,
        title="Лист1",
        gridProperties=dict(
            rowCount=SPREADSHEET_ROWCOUNT_DRAFT,
            columnCount=SPREADSHEET_COLUMNCOUNT_DRAFT
        )
    ))]
)
TABLE_VALUES_DRAFT = [
    ["Отчет от", ],
    ["Топ проектов по скорости закрытия"],
    ["Название проекта", "Время сбора", "Описание"]
]
ROW_COLUMN_COUNT_TOO_BIG = ("В ваших данных строк - {rows_value}, а"
                            "столбцов - {columns_value}, но"
                            "количество строк не"
                            "должно превышать {rowcount_draft}, "
                            "a столбцов - {columncount_draft}")