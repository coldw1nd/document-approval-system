# Сервис электронных заявлений

Веб-приложение для просмотра электронных заявлений, их статусов, документов, комментариев и пользователей. Проект продолжает результаты ПР1–ПР7: JSON-реализация сохранена, на ПР7 добавлена SQLite-база с SQL-запросами, на ПР9 основной веб-слой переведён на Django ORM.

## Возможности

- просмотр заявлений, карточек пользователей и документов;
- отображение статусов, документов и комментариев заявления;
- поиск по названию, описанию и заявителю;
- фильтрация по статусу, сортировка и пагинация;
- статистика по статусам;
- связи моделей Django и оптимизированное получение связанных объектов.

## Технологии

Python, Django 5.2, SQLite, Django ORM, Django Template Language, HTML, CSS, JavaScript, JSON, pytest, pytest-django, flake8.

## Структура данных

- `users.User` — пользователь;
- `applications.Status` — статус заявления;
- `applications.Application` — заявление;
- `documents.Document` — документ заявления;
- `applications.Comment` — комментарий к заявлению.

Связи: пользователь имеет несколько заявлений и комментариев; статус используется несколькими заявлениями; заявление содержит документы и комментарии. Внешние ключи защищают историю заявлений и пользователей от случайного удаления.

## Базы данных

- `data/applications.sqlite3` — исходная SQL-база ПР7, созданная из JSON;
- `db.sqlite3` — целевая база Django, управляемая миграциями и ORM.

Исходная база ПР7 не используется Django ORM напрямую и сохраняется как источник переноса.

## Установка и запуск

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python db/import_sqlite_to_orm.py
python manage.py runserver
```

Откройте `http://127.0.0.1:8000/`. Адрес административной панели `/admin/`; суперпользователь создаётся командой `python manage.py createsuperuser`.

## Проверка

```powershell
python manage.py check
python manage.py makemigrations --check
python manage.py showmigrations
pytest -v
flake8 . --extend-exclude=.venv,venv,env,__pycache__,migrations
```

## Контрольные SQL-запросы

Файл `sql/queries.sql` содержит примеры соединения таблиц, фильтрации, поиска, сортировки, LIMIT/OFFSET, агрегирования и группировки. Для просмотра записей исходной БД используйте `python db/inspect_source_db.py`.
