from app.config import settings
from app.database.connection import get_authoring_conn, get_runtime_conn
from app.database.schema import init_db


def main() -> None:
    import os
    os.makedirs("./data", exist_ok=True)

    for name, path in [("authoring", settings.authoring_db_path), ("runtime", settings.runtime_db_path)]:
        conn = get_authoring_conn() if name == "authoring" else get_runtime_conn()
        try:
            init_db(conn)
            print(f"Initialized {name} database at {path}")
        finally:
            conn.close()


if __name__ == "__main__":
    main()
