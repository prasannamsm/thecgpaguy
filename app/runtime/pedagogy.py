from app.database import connection as _db


def get_pedagogical_content(concept_id: str) -> dict:
    with _db.runtime_db() as conn:
        concept = conn.execute(
            "SELECT * FROM core_concepts WHERE concept_id = ?",
            (concept_id,),
        ).fetchone()
        media = conn.execute(
            "SELECT * FROM concept_media WHERE concept_id = ? AND admin_approved = 1",
            (concept_id,),
        ).fetchall()
    if not concept:
        return {}
    return {
        "concept": dict(concept),
        "media": [dict(m) for m in media],
    }


def get_unit_progress(student_id: str, unit_id: str) -> dict:
    with _db.runtime_db() as conn:
        row = conn.execute(
            "SELECT COUNT(*) as total, "
            "SUM(CASE WHEN graded = 1 THEN 1 ELSE 0 END) as completed "
            "FROM progress WHERE unit_id = ? AND student_id = ?",
            (unit_id, student_id),
        ).fetchone()
    return dict(row) if row else {"total": 0, "completed": 0}
