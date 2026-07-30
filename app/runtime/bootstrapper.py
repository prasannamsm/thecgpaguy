from app.database import connection as _db


def get_available_courses() -> list[dict]:
    with _db.runtime_db() as conn:
        rows = conn.execute(
            "SELECT * FROM local_courses"
        ).fetchall()
    return [dict(r) for r in rows]


def get_units_for_course(course_id: str) -> list[dict]:
    with _db.runtime_db() as conn:
        rows = conn.execute(
            "SELECT * FROM syllabus_units WHERE course_id = ? ORDER BY unit_number",
            (course_id,),
        ).fetchall()
    return [dict(r) for r in rows]


def get_concepts_with_media(unit_id: str) -> list[dict]:
    with _db.runtime_db() as conn:
        rows = conn.execute(
            "SELECT c.*, m.media_id, m.media_type, m.local_path "
            "FROM core_concepts c "
            "LEFT JOIN concept_media m ON c.concept_id = m.concept_id AND m.admin_approved = 1 "
            "WHERE c.unit_id = ?",
            (unit_id,),
        ).fetchall()
    return [dict(r) for r in rows]
