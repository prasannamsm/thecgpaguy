from app.authoring.ingestion import create_core_concept, create_course, create_syllabus_unit, get_concepts_for_unit, list_courses


def test_create_and_list_courses():
    create_course("CS101", "CS101", "Data Structures")
    courses = list_courses()
    assert len(courses) == 1
    assert courses[0]["course_code"] == "CS101"


def test_create_unit_and_concept():
    create_course("CS101", "CS101", "Data Structures")
    unit_id = create_syllabus_unit("CS101", 1, "Arrays")
    concept_id = create_core_concept(unit_id, "Array", "A collection of elements", "Ch.1")
    concepts = get_concepts_for_unit(unit_id)
    assert len(concepts) == 1
    assert concepts[0]["concept_title"] == "Array"
