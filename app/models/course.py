from pydantic import BaseModel


class LocalCourse(BaseModel):
    course_id: str
    course_code: str
    course_name: str
    target_profile: str | None = None
    fallback_rigor: str | None = None


class SyllabusUnit(BaseModel):
    unit_id: str
    course_id: str
    unit_number: int
    unit_title: str
