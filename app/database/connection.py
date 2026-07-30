import sqlite3
from collections.abc import Generator
from contextlib import contextmanager

from app.config import settings


def get_authoring_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(settings.authoring_db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def get_runtime_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(settings.runtime_db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


@contextmanager
def authoring_db() -> Generator[sqlite3.Connection, None, None]:
    conn = get_authoring_conn()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


@contextmanager
def runtime_db() -> Generator[sqlite3.Connection, None, None]:
    conn = get_runtime_conn()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
