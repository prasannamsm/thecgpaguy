import uuid

from app.database import connection as _db


class SectionBlueprint:
    def __init__(
        self,
        section_label: str,
        num_questions: int,
        question_type: str,
        marks_per_question: float,
    ):
        self.section_label = section_label
        self.num_questions = num_questions
        self.question_type = question_type
        self.marks_per_question = marks_per_question
        self.total_marks = num_questions * marks_per_question


def create_assessment_blueprint(
    unit_id: str,
    section_a: SectionBlueprint,
    section_b: SectionBlueprint | None = None,
    section_c: SectionBlueprint | None = None,
) -> list[str]:
    question_ids = []
    sections = [s for s in [section_a, section_b, section_c] if s]

    for section in sections:
        for _ in range(section.num_questions):
            qid = str(uuid.uuid4())
            with _db.authoring_db() as conn:
                conn.execute(
                    "INSERT INTO assessment_items (question_id, unit_id, question_type, question_text, grading_method) VALUES (?, ?, ?, ?, ?)",
                    (
                        qid,
                        unit_id,
                        section.question_type,
                        f"[{section.section_label}] Placeholder question",
                        section.question_type,
                    ),
                )
            question_ids.append(qid)

    return question_ids


def get_blueprint_for_unit(unit_id: str) -> list[dict]:
    with _db.authoring_db() as conn:
        rows = conn.execute(
            "SELECT * FROM assessment_items WHERE unit_id = ?", (unit_id,)
        ).fetchall()
    return [dict(r) for r in rows]
