import os
import sqlite3
import sys
from datetime import date
from pathlib import Path

import django
BASE_DIR = Path(__file__).resolve().parent.parent
SOURCE_DB = BASE_DIR / "data" / "applications.sqlite3"
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()


def import_records() -> None:
    from django.db import transaction

    from applications.models import Application, Comment, Status
    from documents.models import Document
    from users.models import User

    if not SOURCE_DB.exists():
        raise FileNotFoundError(SOURCE_DB)
    with sqlite3.connect(SOURCE_DB) as connection:
        connection.row_factory = sqlite3.Row
        source_users = connection.execute(
            "SELECT id, full_name, email FROM users ORDER BY id"
        ).fetchall()
        source_statuses = connection.execute(
            "SELECT id, name, is_final FROM statuses ORDER BY id"
        ).fetchall()
        source_applications = connection.execute(
            """SELECT id, title, description, user_id, status_id, created_at
            FROM applications ORDER BY id"""
        ).fetchall()
        source_documents = connection.execute(
            """SELECT id, application_id, name, description, uploaded_at
            FROM documents ORDER BY id"""
        ).fetchall()
        source_comments = connection.execute(
            """SELECT id, application_id, author_id, text, created_at
            FROM comments ORDER BY id"""
        ).fetchall()

    with transaction.atomic():
        for row in source_users:
            User.objects.update_or_create(
                pk=row["id"],
                defaults={
                    "full_name": row["full_name"],
                    "email": row["email"],
                },
            )
        status_codes = {
            "Черновик": Status.Code.DRAFT,
            "На рассмотрении": Status.Code.REVIEW,
            "Одобрено": Status.Code.APPROVED,
            "Отклонено": Status.Code.REJECTED,
        }
        for row in source_statuses:
            Status.objects.update_or_create(
                pk=row["id"],
                defaults={
                    "name": row["name"],
                    "is_final": bool(row["is_final"]),
                    "code": status_codes.get(
                        row["name"], f"status-{row['id']}"
                    ),
                },
            )
        for row in source_applications:
            Application.objects.update_or_create(
                pk=row["id"],
                defaults={
                    "title": row["title"],
                    "description": row["description"],
                    "applicant_id": row["user_id"],
                    "status_id": row["status_id"],
                    "created_at": date.fromisoformat(row["created_at"]),
                },
            )
        for row in source_documents:
            Document.objects.update_or_create(
                pk=row["id"],
                defaults={
                    "application_id": row["application_id"],
                    "name": row["name"],
                    "description": row["description"],
                    "uploaded_at": date.fromisoformat(row["uploaded_at"]),
                },
            )
        for row in source_comments:
            Comment.objects.update_or_create(
                pk=row["id"],
                defaults={
                    "application_id": row["application_id"],
                    "author_id": row["author_id"],
                    "text": row["text"],
                    "created_at": date.fromisoformat(row["created_at"]),
                },
            )

    print("Перенос из SQLite ПР7 в Django ORM завершён")
    print(f"Пользователи: {User.objects.count()}")
    print(f"Статусы: {Status.objects.count()}")
    print(f"Заявления: {Application.objects.count()}")
    print(f"Документы: {Document.objects.count()}")
    print(f"Комментарии: {Comment.objects.count()}")


if __name__ == "__main__":
    import_records()
