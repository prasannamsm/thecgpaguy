const BASE = ''

async function request<T>(url: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${url}`, {
    headers: { 'Content-Type': 'application/json', ...options?.headers },
    ...options,
  })
  if (!res.ok) throw new Error(`API error: ${res.status} ${res.statusText}`)
  return res.json()
}

export const api = {
  courses: {
    list: () => request<any[]>('/authoring/courses'),
    create: (id: string, code: string, name: string) =>
      request<any>(`/authoring/courses?course_id=${id}&course_code=${code}&course_name=${name}`, { method: 'POST' }),
    ingest: (courseId: string, file: File) => {
      const form = new FormData()
      form.append('file', file)
      return fetch(`${BASE}/authoring/courses/${courseId}/ingest`, { method: 'POST', body: form }).then(r => r.json())
    },
  },
  units: {
    list: (courseId: string) => request<any[]>(`/runtime/courses/${courseId}/units`),
    create: (courseId: string, number: number, title: string) =>
      request<any>(`/authoring/courses/${courseId}/units?unit_number=${number}&unit_title=${encodeURIComponent(title)}`, { method: 'POST' }),
  },
  concepts: {
    list: (unitId: string) => request<any[]>(`/authoring/units/${unitId}/concepts`),
    generate: (conceptId: string, title: string, passage: string) =>
      request<any>(`/authoring/concepts/${conceptId}/generate?concept_title=${encodeURIComponent(title)}&textbook_passage=${encodeURIComponent(passage)}`, { method: 'POST' }),
  },
  staging: {
    get: () => request<any>('/authoring/staging'),
    concepts: () => request<any[]>('/authoring/staging/concepts'),
    media: () => request<any[]>('/authoring/staging/media'),
    assessments: () => request<any[]>('/authoring/staging/assessments'),
  },
  media: {
    approve: (id: string) => request<any>(`/authoring/media/${id}/approve`, { method: 'POST' }),
    reject: (id: string) => request<any>(`/authoring/media/${id}/reject`, { method: 'POST' }),
    search: (conceptId: string, title: string) =>
      request<any>(`/authoring/concepts/${conceptId}/media/search?concept_title=${encodeURIComponent(title)}`, { method: 'POST' }),
  },
  blueprint: {
    create: (unitId: string) => request<any>(`/authoring/units/${unitId}/blueprint`, { method: 'POST' }),
    get: (unitId: string) => request<any[]>(`/authoring/units/${unitId}/blueprint`),
  },
  runtime: {
    courses: () => request<any[]>('/runtime/courses'),
    concepts: (unitId: string) => request<any[]>(`/runtime/units/${unitId}/concepts`),
    conceptDetail: (id: string) => request<any>(`/runtime/concepts/${id}`),
    progress: (studentId: string, unitId: string) =>
      request<any>(`/runtime/units/${unitId}/progress?student_id=${studentId}`),
    grade: (answer: string, key: string, maxScore = 10) =>
      request<any>(`/runtime/grade?student_answer=${encodeURIComponent(answer)}&answer_key=${encodeURIComponent(key)}&max_score=${maxScore}`, { method: 'POST' }),
    matrix: (id: string) => request<any>(`/runtime/matrix/${id}`),
    gradeMatrix: (id: string, selected: string[]) =>
      request<any>(`/runtime/matrix/${id}/grade`, { method: 'POST', body: JSON.stringify(selected) }),
  },
}
