import aiofiles
from fastapi import APIRouter, HTTPException, UploadFile

from app.authoring.blueprint import (
    SectionBlueprint,
    create_assessment_blueprint,
    get_blueprint_for_unit,
)
from app.authoring.generation import (
    generate_assessment_question,
    generate_definition,
    generate_multi_correct_pool,
)
from app.authoring.ingestion import (
    create_course,
    create_syllabus_unit,
    get_concepts_for_unit,
    ingest_textbook,
    list_courses,
)
from app.authoring.media_sourcing import (
    approve_media,
    reject_media,
    search_and_stage_concept_media,
)
from app.authoring.staging import (
    get_pending_assessments,
    get_pending_concepts,
    get_pending_media,
    get_staging_summary,
)

router = APIRouter()


@router.get("/courses")
async def get_courses():
    return list_courses()


@router.post("/courses")
async def add_course(course_id: str, course_code: str, course_name: str):
    create_course(course_id, course_code, course_name)
    return {"course_id": course_id}


@router.post("/courses/{course_id}/ingest")
async def ingest_pdf(course_id: str, file: UploadFile):
    if not file.filename or not file.filename.endswith(".pdf"):
        raise HTTPException(400, "Only PDF files accepted")
    content = await file.read()
    tmp_path = f"/tmp/{file.filename}"
    async with aiofiles.open(tmp_path, "wb") as f:
        await f.write(content)
    result = ingest_textbook(course_id, tmp_path)
    return result


@router.post("/courses/{course_id}/units")
async def add_unit(course_id: str, unit_number: int, unit_title: str):
    unit_id = create_syllabus_unit(course_id, unit_number, unit_title)
    return {"unit_id": unit_id}


@router.get("/units/{unit_id}/concepts")
async def list_concepts(unit_id: str):
    return get_concepts_for_unit(unit_id)


@router.post("/concepts/{concept_id}/generate")
async def generate_content(concept_id: str, concept_title: str, textbook_passage: str):
    definition = generate_definition(concept_title, textbook_passage)
    return {"definition": definition}


@router.post("/concepts/{concept_id}/media/search")
async def search_media(concept_id: str, concept_title: str):
    return search_and_stage_concept_media(concept_id, concept_title)


@router.post("/media/{media_id}/approve")
async def approve(media_id: str):
    approve_media(media_id)
    return {"status": "approved"}


@router.post("/media/{media_id}/reject")
async def reject(media_id: str):
    reject_media(media_id)
    return {"status": "rejected"}


@router.post("/concepts/{concept_id}/assess/generate")
async def generate_question(concept_id: str, concept_title: str, definition: str, question_type: str = "SHORT_ANSWER"):
    return generate_assessment_question(concept_title, definition, question_type)


@router.post("/assess/multi-correct/generate")
async def generate_multi_correct(concept_title: str, num_options: int = 15):
    return generate_multi_correct_pool(concept_title, num_options)


@router.post("/units/{unit_id}/blueprint")
async def create_blueprint(unit_id: str):
    section_a = SectionBlueprint("A", 10, "SHORT_ANSWER", 2.0)
    section_b = SectionBlueprint("B", 5, "DESCRIPTIVE_PROOF", 5.0)
    section_c = SectionBlueprint("C", 5, "MULTI_CORRECT_MATRIX", 4.0)
    ids = create_assessment_blueprint(unit_id, section_a, section_b, section_c)
    return {"question_ids": ids}


@router.get("/units/{unit_id}/blueprint")
async def read_blueprint(unit_id: str):
    return get_blueprint_for_unit(unit_id)


@router.get("/staging")
async def staging_summary():
    return get_staging_summary()


@router.get("/staging/concepts")
async def staging_concepts():
    return get_pending_concepts()


@router.get("/staging/media")
async def staging_media():
    return get_pending_media()


@router.get("/staging/assessments")
async def staging_assessments():
    return get_pending_assessments()
