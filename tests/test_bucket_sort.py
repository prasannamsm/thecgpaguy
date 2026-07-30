import pytest

from app.runtime.bucket_sort import create_bucket_session, get_bucket_results, submit_bucket


def test_bucket_session(db_conn):
    db_conn.execute(
        "INSERT INTO local_courses (course_id, course_code, course_name) VALUES (?, ?, ?)",
        ("c1", "CS101", "Test"),
    )
    db_conn.execute(
        "INSERT INTO syllabus_units (unit_id, course_id, unit_number, unit_title) VALUES (?, ?, ?, ?)",
        ("u1", "c1", 1, "Test Unit"),
    )
    db_conn.execute(
        "INSERT INTO assessment_items (question_id, unit_id, question_type, question_text, grading_method) VALUES (?, ?, ?, ?, ?)",
        ("q1", "u1", "SHORT_ANSWER", "Test?", "MANUAL"),
    )

    session_id = create_bucket_session("student1", "u1")
    assert session_id is not None

    submit_bucket(session_id, "q1", "confident")
    results = get_bucket_results(session_id)
    assert len(results) == 1
    assert results[0]["bucket"] == "confident"
