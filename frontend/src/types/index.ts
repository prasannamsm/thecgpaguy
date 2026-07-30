export interface Course {
  course_id: string
  course_code: string
  course_name: string
  target_profile: string | null
  fallback_rigor: string | null
}

export interface SyllabusUnit {
  unit_id: string
  course_id: string
  unit_number: number
  unit_title: string
}

export interface CoreConcept {
  concept_id: string
  unit_id: string
  concept_title: string
  textbook_definition: string
  textbook_source_ref: string | null
  simplified_analogy: string
}

export interface AssessmentItem {
  question_id: string
  unit_id: string
  question_type: string
  question_text: string
  textbook_grounding_source: string | null
  grading_method: string
  structured_answer_key: string | null
}
