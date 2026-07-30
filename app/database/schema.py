import sqlite3

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS local_courses (
    course_id TEXT PRIMARY KEY,
    course_code TEXT NOT NULL,
    course_name TEXT NOT NULL,
    target_profile TEXT,
    fallback_rigor TEXT
);

CREATE TABLE IF NOT EXISTS syllabus_units (
    unit_id TEXT PRIMARY KEY,
    course_id TEXT,
    unit_number INTEGER NOT NULL,
    unit_title TEXT NOT NULL,
    FOREIGN KEY(course_id) REFERENCES local_courses(course_id)
);

CREATE TABLE IF NOT EXISTS core_concepts (
    concept_id TEXT PRIMARY KEY,
    unit_id TEXT,
    concept_title TEXT NOT NULL,
    textbook_definition TEXT NOT NULL,
    textbook_source_ref TEXT,
    simplified_analogy TEXT NOT NULL,
    FOREIGN KEY(unit_id) REFERENCES syllabus_units(unit_id)
);

CREATE TABLE IF NOT EXISTS concept_media (
    media_id TEXT PRIMARY KEY,
    concept_id TEXT,
    media_type TEXT NOT NULL,
    source_url TEXT,
    license_status TEXT NOT NULL,
    admin_approved INTEGER NOT NULL DEFAULT 0,
    local_path TEXT,
    FOREIGN KEY(concept_id) REFERENCES core_concepts(concept_id)
);

CREATE TABLE IF NOT EXISTS assessment_items (
    question_id TEXT PRIMARY KEY,
    unit_id TEXT,
    question_type TEXT NOT NULL,
    question_text TEXT NOT NULL,
    textbook_grounding_source TEXT,
    grading_method TEXT NOT NULL,
    structured_answer_key TEXT,
    FOREIGN KEY(unit_id) REFERENCES syllabus_units(unit_id)
);

CREATE TABLE IF NOT EXISTS matrix_options_pool (
    option_id TEXT PRIMARY KEY,
    question_id TEXT,
    option_text TEXT NOT NULL,
    is_correct_flag INTEGER NOT NULL,
    FOREIGN KEY(question_id) REFERENCES assessment_items(question_id)
);

CREATE TABLE IF NOT EXISTS progress (
    student_id TEXT NOT NULL,
    unit_id TEXT NOT NULL,
    concept_id TEXT,
    question_id TEXT,
    graded INTEGER NOT NULL DEFAULT 0,
    score REAL,
    PRIMARY KEY (student_id, unit_id, concept_id)
);

CREATE TABLE IF NOT EXISTS bucket_sessions (
    session_id TEXT PRIMARY KEY,
    student_id TEXT NOT NULL,
    unit_id TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bucket_responses (
    session_id TEXT NOT NULL,
    question_id TEXT NOT NULL,
    bucket TEXT,
    PRIMARY KEY (session_id, question_id)
);
"""


def init_db(conn: sqlite3.Connection) -> None:
    conn.executescript(SCHEMA_SQL)
    conn.commit()
