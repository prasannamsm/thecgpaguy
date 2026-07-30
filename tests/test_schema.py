import sqlite3
import tempfile

from app.database.schema import init_db


def test_init_db_creates_tables():
    conn = sqlite3.connect(":memory:")
    init_db(conn)
    tables = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    ).fetchall()
    names = [r[0] for r in tables]
    assert "local_courses" in names
    assert "syllabus_units" in names
    assert "core_concepts" in names
    assert "concept_media" in names
    assert "assessment_items" in names
    assert "matrix_options_pool" in names
    assert "progress" in names
    assert "bucket_sessions" in names
    assert "bucket_responses" in names
    conn.close()
