from pydantic import BaseModel


class CoreConcept(BaseModel):
    concept_id: str
    unit_id: str
    concept_title: str
    textbook_definition: str
    textbook_source_ref: str | None = None
    simplified_analogy: str


class ConceptMedia(BaseModel):
    media_id: str
    concept_id: str
    media_type: str
    source_url: str | None = None
    license_status: str
    admin_approved: bool = False
    local_path: str | None = None
