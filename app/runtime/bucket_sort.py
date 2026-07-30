import uuid

from app.database import connection as _db


def create_bucket_session(student_id: str, unit_id: str) -> str:
    session_id = str(uuid.uuid4())
    with _db.runtime_db() as conn:
        conn.execute(
            "INSERT INTO bucket_sessions (session_id, student_id, unit_id) VALUES (?, ?, ?)",
            (session_id, student_id, unit_id),
        )
        questions = conn.execute(
            "SELECT question_id FROM assessment_items WHERE unit_id = ?",
            (unit_id,),
        ).fetchall()
        for q in questions:
            conn.execute(
                "INSERT INTO bucket_responses (session_id, question_id) VALUES (?, ?)",
                (session_id, q["question_id"]),
            )
    return session_id


def submit_bucket(session_id: str, question_id: str, bucket: str) -> None:
    with _db.runtime_db() as conn:
        conn.execute(
            "UPDATE bucket_responses SET bucket = ? WHERE session_id = ? AND question_id = ?",
            (bucket, session_id, question_id),
        )


def get_bucket_results(session_id: str) -> list[dict]:
    with _db.runtime_db() as conn:
        rows = conn.execute(
            "SELECT q.question_text, r.bucket "
            "FROM bucket_responses r "
            "JOIN assessment_items q ON r.question_id = q.question_id "
            "WHERE r.session_id = ?",
            (session_id,),
        ).fetchall()
    return [dict(r) for r in rows]
