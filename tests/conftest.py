import sqlite3
from collections.abc import Generator
from contextlib import contextmanager

import pytest

from app.database.schema import init_db


@pytest.fixture
def db_conn():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    init_db(conn)
    return conn


@pytest.fixture(autouse=True)
def _patch_db(monkeypatch, db_conn):
    @contextmanager
    def _authoring_db() -> Generator[sqlite3.Connection, None, None]:
        yield db_conn
        db_conn.commit()

    @contextmanager
    def _runtime_db() -> Generator[sqlite3.Connection, None, None]:
        yield db_conn
        db_conn.commit()

    import app.database.connection as conn_module
    monkeypatch.setattr(conn_module, "authoring_db", _authoring_db)
    monkeypatch.setattr(conn_module, "runtime_db", _runtime_db)
