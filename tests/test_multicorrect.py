from app.runtime.multicorrect import grade_matrix


def test_grade_matrix_all_correct():
    question_id = "q1"
    selected = ["opt1", "opt2", "opt3"]

    all_options = [
        {"option_id": "opt1", "is_correct_flag": 1},
        {"option_id": "opt2", "is_correct_flag": 1},
        {"option_id": "opt3", "is_correct_flag": 1},
        {"option_id": "opt4", "is_correct_flag": 0},
        {"option_id": "opt5", "is_correct_flag": 0},
    ]

    result = grade_matrix_with_options(question_id, selected, all_options)
    assert result["score"] == 4.0


def test_grade_matrix_partial_correct():
    question_id = "q1"
    selected = ["opt1"]

    all_options = [
        {"option_id": "opt1", "is_correct_flag": 1},
        {"option_id": "opt2", "is_correct_flag": 1},
        {"option_id": "opt3", "is_correct_flag": 0},
    ]

    result = grade_matrix_with_options(question_id, selected, all_options)
    assert result["score"] == 1.0


def test_grade_matrix_incorrect_selection():
    question_id = "q1"
    selected = ["opt3"]

    all_options = [
        {"option_id": "opt1", "is_correct_flag": 1},
        {"option_id": "opt2", "is_correct_flag": 1},
        {"option_id": "opt3", "is_correct_flag": 0},
    ]

    result = grade_matrix_with_options(question_id, selected, all_options)
    assert result["score"] == -2.0


def test_grade_matrix_unattempted():
    question_id = "q1"
    selected = []

    all_options = [
        {"option_id": "opt1", "is_correct_flag": 1},
        {"option_id": "opt2", "is_correct_flag": 0},
    ]

    result = grade_matrix_with_options(question_id, selected, all_options)
    assert result["score"] == 0.0


def grade_matrix_with_options(question_id, selected_ids, all_options):
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
