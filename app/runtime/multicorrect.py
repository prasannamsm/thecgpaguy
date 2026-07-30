from app.database import connection as _db


def get_matrix_question(question_id: str) -> dict | None:
    with _db.runtime_db() as conn:
        question = conn.execute(
            "SELECT * FROM assessment_items WHERE question_id = ?",
            (question_id,),
        ).fetchone()
        if not question:
            return None
        options = conn.execute(
            "SELECT * FROM matrix_options_pool WHERE question_id = ?",
            (question_id,),
        ).fetchall()
    return {**dict(question), "options": [dict(o) for o in options]}


def grade_matrix(question_id: str, selected_ids: list[str]) -> dict:
    with _db.runtime_db() as conn:
        all_options = conn.execute(
            "SELECT option_id, is_correct_flag FROM matrix_options_pool WHERE question_id = ?",
            (question_id,),
        ).fetchall()

    correct_ids = {o["option_id"] for o in all_options if o["is_correct_flag"]}
    selected = set(selected_ids)
    total_correct = len(correct_ids)

    if not selected:
        score = 0.0
    elif selected == correct_ids:
        score = 4.0
    elif selected.issubset(correct_ids):
        score = 1.0
    elif selected & (correct_ids ^ selected):
        score = -2.0
    else:
        score = 0.0

    return {
        "score": score,
        "total_correct": total_correct,
        "selected_correct": len(selected & correct_ids),
        "selected_incorrect": len(selected - correct_ids),
    }
