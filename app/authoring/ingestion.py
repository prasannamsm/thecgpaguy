import uuid
from pathlib import Path

import fitz  # PyMuPDF

from app.database import connection as _db


def extract_text_from_pdf(pdf_path: str) -> tuple[str, int]:
    doc = fitz.open(pdf_path)
    pages = doc.page_count
    text = "\n".join(page.get_text() for page in doc)
    doc.close()
    return text, pages


def create_course(course_id: str, course_code: str, course_name: str) -> str:
    with _db.authoring_db() as conn:
        conn.execute(
            "INSERT OR IGNORE INTO local_courses (course_id, course_code, course_name) VALUES (?, ?, ?)",
            (course_id, course_code, course_name),
        )
    return course_id


def list_courses() -> list[dict]:
    with _db.authoring_db() as conn:
        rows = conn.execute("SELECT * FROM local_courses").fetchall()
    return [dict(r) for r in rows]


def ingest_textbook(course_id: str, pdf_path: str) -> dict:
    text, page_count = extract_text_from_pdf(pdf_path)
    with _db.authoring_db() as conn:
        conn.execute(
            "UPDATE local_courses SET target_profile = ? WHERE course_id = ?",
            (f"textbook_ingested:{Path(pdf_path).name}", course_id),
        )
    return {"course_id": course_id, "pages": page_count, "chars": len(text)}


def create_syllabus_unit(
    course_id: str, unit_number: int, unit_title: str
) -> str:
    unit_id = str(uuid.uuid4())
    with _db.authoring_db() as conn:
        conn.execute(
            "INSERT INTO syllabus_units (unit_id, course_id, unit_number, unit_title) VALUES (?, ?, ?, ?)",
            (unit_id, course_id, unit_number, unit_title),
        )
    return unit_id


def create_core_concept(
    unit_id: str,
    concept_title: str,
    textbook_definition: str,
    textbook_source_ref: str | None = None,
    simplified_analogy: str = "",
) -> str:
    concept_id = str(uuid.uuid4())
    with _db.authoring_db() as conn:
        conn.execute(
            "INSERT INTO core_concepts (concept_id, unit_id, concept_title, textbook_definition, textbook_source_ref, simplified_analogy) VALUES (?, ?, ?, ?, ?, ?)",
            (concept_id, unit_id, concept_title, textbook_definition, textbook_source_ref, simplified_analogy),
        )
    return concept_id


def get_concepts_for_unit(unit_id: str) -> list[dict]:
    with _db.authoring_db() as conn:
        rows = conn.execute(
            "SELECT * FROM core_concepts WHERE unit_id = ?", (unit_id,)
        ).fetchall()
    return [dict(r) for r in rows]
