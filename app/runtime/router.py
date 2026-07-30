from fastapi import APIRouter

from app.runtime.bootstrapper import (
    get_available_courses,
    get_concepts_with_media,
    get_units_for_course,
)
from app.runtime.bucket_sort import (
    create_bucket_session,
    get_bucket_results,
    submit_bucket,
)
from app.runtime.grading import semantic_check
from app.runtime.multicorrect import get_matrix_question, grade_matrix
from app.runtime.pedagogy import get_pedagogical_content, get_unit_progress

router = APIRouter()


@router.get("/courses")
async def list_courses():
    return get_available_courses()


@router.get("/courses/{course_id}/units")
async def list_units(course_id: str):
    return get_units_for_course(course_id)


@router.get("/units/{unit_id}/concepts")
async def list_concepts(unit_id: str):
    return get_concepts_with_media(unit_id)


@router.get("/concepts/{concept_id}")
async def concept_content(concept_id: str):
    return get_pedagogical_content(concept_id)


@router.get("/units/{unit_id}/progress")
async def unit_progress(student_id: str, unit_id: str):
    return get_unit_progress(student_id, unit_id)


@router.post("/grade")
async def grade_answer(student_answer: str, answer_key: str, max_score: float = 10.0):
    return semantic_check(student_answer, answer_key, max_score)


@router.post("/bucket/{unit_id}/start")
async def start_bucket(student_id: str, unit_id: str):
    session_id = create_bucket_session(student_id, unit_id)
    return {"session_id": session_id}


@router.post("/bucket/{session_id}/submit")
async def submit_bucket_answer(session_id: str, question_id: str, bucket: str):
    submit_bucket(session_id, question_id, bucket)
    return {"status": "submitted"}


@router.get("/bucket/{session_id}/results")
async def bucket_results(session_id: str):
    return get_bucket_results(session_id)


@router.get("/matrix/{question_id}")
async def get_matrix(question_id: str):
    return get_matrix_question(question_id)


@router.post("/matrix/{question_id}/grade")
async def grade_matrix_endpoint(question_id: str, selected_ids: list[str]):
    return grade_matrix(question_id, selected_ids)
