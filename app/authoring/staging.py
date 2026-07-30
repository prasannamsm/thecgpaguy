from app.database import connection as _db


def get_pending_concepts() -> list[dict]:
    with _db.authoring_db() as conn:
        rows = conn.execute(
            "SELECT c.*, u.unit_title FROM core_concepts c "
            "JOIN syllabus_units u ON c.unit_id = u.unit_id "
            "WHERE c.simplified_analogy = '' OR c.simplified_analogy IS NULL"
        ).fetchall()
    return [dict(r) for r in rows]


def get_pending_media() -> list[dict]:
    with _db.authoring_db() as conn:
        rows = conn.execute(
            "SELECT * FROM concept_media WHERE admin_approved = 0"
        ).fetchall()
    return [dict(r) for r in rows]


def get_pending_assessments() -> list[dict]:
    with _db.authoring_db() as conn:
        rows = conn.execute(
            "SELECT * FROM assessment_items WHERE structured_answer_key IS NULL"
        ).fetchall()
    return [dict(r) for r in rows]


def get_staging_summary() -> dict:
    return {
        "pending_concepts": len(get_pending_concepts()),
        "pending_media": len(get_pending_media()),
        "pending_assessments": len(get_pending_assessments()),
    }
