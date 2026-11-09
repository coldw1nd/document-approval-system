import sys
from pathlib import Path
from db.database import DATABASE_PATH, get_connection

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))


def inspect_database() -> None:
    if not DATABASE_PATH.exists():
        raise FileNotFoundError(DATABASE_PATH)
    with get_connection(DATABASE_PATH) as connection:
        tables = connection.execute(
            """SELECT name FROM sqlite_master
            WHERE type = 'table' AND name NOT LIKE 'sqlite_%'
            ORDER BY name"""
        ).fetchall()
        for row in tables:
            table_name = row["name"]
            print(f"\nТаблица: {table_name}")
            columns = connection.execute(
                f'PRAGMA table_info("{table_name}")'
            ).fetchall()
            for column in columns:
                print(dict(column))
            count = connection.execute(
                f'SELECT COUNT(*) FROM "{table_name}"'
            ).fetchone()[0]
            print(f"Количество записей: {count}")


if __name__ == "__main__":
    inspect_database()
