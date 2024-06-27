# Благотворительный фонд поддержки котиков QRKot

#### Автор проекта: [Dmitry Stepanov](https://github.com/Ghirlan-daio)

### Описание сервиса

Фонд собирает пожертвования на различные целевые проекты: на медицинское обслуживание нуждающихся хвостатых, на обустройство кошачьей колонии в подвале, на корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции.

В Фонде QRKot может быть открыто несколько целевых проектов. У каждого проекта есть название, описание и сумма, которую планируется собрать. После того, как нужная сумма собрана — проект закрывается.

Каждый пользователь может сделать пожертвование и сопроводить его комментарием. Пожертвования не целевые: они вносятся в фонд, а не в конкретный проект. Каждое полученное пожертвование автоматически добавляется в первый открытый проект, который ещё не набрал нужную сумму. Если пожертвование больше нужной суммы или же в Фонде нет открытых проектов — оставшиеся деньги ждут открытия следующего проекта. При создании нового проекта все неинвестированные пожертвования автоматически вкладываются в новый проект.

### Google API

Сервис поддерживает возможность формирования отчёта в Google-spreadsheet. В таблице транслируются уже закрытые проекты, отсортированные по скорости сбора средств.

### Используемый стек
- Python
- FastAPi
- SQLAlchemy
- Uvicorn
- Alembic

### Подготовка к запуску проекта
#### Клонируйте репозиторий и перейдите в него:

```
git@github.com:Ghirlan-daio/cat_charity_fund.git
```

```
cd cat_charity_fund
```

#### Создайте и активируйте виртуальное окружение:

```
python -m venv venv
```

```
source venv/Scripts/activate
```

#### Установите зависимости проекта:

```
pip install -r requirements.py
```

#### Создайте и заполните файл .env в корневой директории проекта по образцу:

```
APP_TITLE=Благотворительный фонд поддержки котиков QRKot

DESCRIPTION=Фонд собирает пожертвования на различные целевые проекты: на медицинское обслуживание нуждающихся хвостатых, на обустройство кошачьей колонии в подвале, на корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции.

DATABASE_URL=sqlite+aiosqlite:///./fastapi.db

SECRET=very_secret

FIRST_SUPERUSER_EMAIL=mail@mail.ru

FIRST_SUPERUSER_PASSWORD=123
```

#### Создайте миграцию

```
alembic revision --autogenerate -m "Message"
```

#### Примените миграций
```
alembic upgrade head
```

#### Запустите проект
```
uvicorn app.main:app --reload
```

#### После запуска проект будет доступен по адресу: http://127.0.0.1:8000

Документация к API досупна в следующих форматах и адресах:

- Swagger: http://127.0.0.1:8000/docs
- Redoc: http://127.0.0.1:8000/redoc