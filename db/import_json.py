import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

DATA_DIR = BASE_DIR / "data"
DATABASE_PATH = DATA_DIR / "applications.sqlite3"


def read_json(filename: str) -> list[dict]:
    path = DATA_DIR / filename
    with path.open("r", encoding="utf-8") as source:
        records = json.load(source)
    if not isinstance(records, list):
        raise ValueError(f"Файл {filename} должен содержать список записей")
    return records


def import_json_data() -> None:
    from db.database import create_database, get_connection

    create_database(DATABASE_PATH)
    users = read_json("users.json")
    statuses = read_json("statuses.json")
    applications = read_json("applications.json")
    documents = read_json("documents.json")
    comments = read_json("comments.json")

    with get_connection(DATABASE_PATH) as connection:
        connection.execute("DELETE FROM comments")
        connection.execute("DELETE FROM documents")
        connection.execute("DELETE FROM applications")
        connection.execute("DELETE FROM statuses")
        connection.execute("DELETE FROM users")
        connection.executemany(
            "INSERT INTO users (id, full_name, email) VALUES (?, ?, ?)",
            [(row["id"], row["full_name"], row["email"]) for row in users],
        )
        connection.executemany(
            "INSERT INTO statuses (id, name, is_final) VALUES (?, ?, ?)",
            [
                (row["id"], row["name"], int(row.get("is_final", False)))
                for row in statuses
            ],
        )
        connection.executemany(
            """INSERT INTO applications
            (id, title, description, user_id, status_id, created_at)
            VALUES (?, ?, ?, ?, ?, ?)""",
            [
                (
                    row["id"],
                    row["title"],
                    row.get("description", ""),
                    row["user_id"],
                    row["status_id"],
                    row["created_at"],
                )
                for row in applications
            ],
        )
        connection.executemany(
            """INSERT INTO documents
            (id, application_id, name, description, uploaded_at)
            VALUES (?, ?, ?, ?, ?)""",
            [
                (
                    row["id"],
                    row["application_id"],
                    row["name"],
                    row.get("description", ""),
                    row["uploaded_at"],
                )
                for row in documents
            ],
        )
        connection.executemany(
            """INSERT INTO comments
            (id, application_id, author_id, text, created_at)
            VALUES (?, ?, ?, ?, ?)""",
            [
                (
                    row["id"],
                    row["application_id"],
                    row["author_id"],
                    row["text"],
                    row["created_at"],
                )
                for row in comments
            ],
        )

    print(f"Данные JSON перенесены в {DATABASE_PATH}")
    for table in (
        "users", "statuses", "applications", "documents", "comments"
    ):
        with get_connection(DATABASE_PATH) as connection:
            count = connection.execute(
                f"SELECT COUNT(*) FROM {table}"
            ).fetchone()[0]
        print(f"{table}: {count}")


if __name__ == "__main__":
    import_json_data()
