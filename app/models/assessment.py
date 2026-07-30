from pydantic import BaseModel


class AssessmentItem(BaseModel):
    question_id: str
    unit_id: str
    question_type: str
    question_text: str
    textbook_grounding_source: str | None = None
    grading_method: str
    structured_answer_key: str | None = None


class MatrixOption(BaseModel):
    option_id: str
    question_id: str
    option_text: str
    is_correct_flag: bool
