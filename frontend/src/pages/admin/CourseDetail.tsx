import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { api } from '../../api/client'
import { GlassCard } from '../../components/GlassCard'

export function AdminCourseDetail() {
  const { courseId } = useParams()
  const [units, setUnits] = useState<any[]>([])
  const [concepts, setConcepts] = useState<Record<string, any[]>>({})
  const [file, setFile] = useState<File | null>(null)
  const [uploading, setUploading] = useState(false)
  const [newUnitTitle, setNewUnitTitle] = useState('')
  const [expandedUnit, setExpandedUnit] = useState<string | null>(null)

  const load = async () => {
    const u = await api.units.list(courseId!)
    setUnits(u)
    for (const unit of u) {
      const c = await api.concepts.list(unit.unit_id)
      setConcepts(prev => ({ ...prev, [unit.unit_id]: c }))
    }
  }

  useEffect(() => { load() }, [courseId])

  const handleUpload = async () => {
    if (!file) return
    setUploading(true)
    await api.courses.ingest(courseId!, file)
    setUploading(false)
    setFile(null)
  }

  const addUnit = async () => {
    if (!newUnitTitle) return
    await api.units.create(courseId!, units.length + 1, newUnitTitle)
    setNewUnitTitle('')
    load()
  }

  const generateContent = async (unitId: string, conceptId: string, title: string) => {
    const passage = prompt('Enter textbook passage for grounding:') || 'Default passage'
    await api.concepts.generate(conceptId, title, passage)
    load()
  }

  return (
    <div>
      <div className="page-header">
        <h1>Course: {courseId}</h1>
        <p>Upload materials, manage units, and generate content</p>
      </div>

      <GlassCard className="mb-3" style={{ padding: '1.5rem' }}>
        <h3 style={{ marginBottom: '1rem' }}>Upload Textbook PDF</h3>
        <div className="upload-zone" onClick={() => document.getElementById('pdf-input')?.click()}>
          <p style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>📄</p>
          <p>{file ? file.name : 'Click to select a PDF textbook'}</p>
          <input id="pdf-input" type="file" accept=".pdf" style={{ display: 'none' }} onChange={e => setFile(e.target.files?.[0] || null)} />
        </div>
        {file && (
          <button className="btn btn-primary mt-2" onClick={handleUpload} disabled={uploading}>
            {uploading ? 'Uploading...' : 'Upload & Ingest'}
          </button>
        )}
      </GlassCard>

      <GlassCard className="mb-3" style={{ padding: '1.5rem' }}>
        <div className="flex-between mb-2">
          <h3>Units</h3>
          <div className="flex-center gap-1">
            <input
              placeholder="New unit title"
              value={newUnitTitle}
              onChange={e => setNewUnitTitle(e.target.value)}
              style={{ padding: '0.5rem', borderRadius: 'var(--radius-sm)', border: '1px solid rgba(0,0,0,0.1)' }}
            />
            <button className="btn btn-accent" onClick={addUnit}>Add Unit</button>
          </div>
        </div>
        <div className="unit-list">
          {units.map((u: any) => {
            const unitConcepts = concepts[u.unit_id] || []
            const isExpanded = expandedUnit === u.unit_id
            return (
              <div key={u.unit_id}>
                <GlassCard
                  className="unit-item"
                  style={{ cursor: 'pointer', marginBottom: isExpanded && unitConcepts.length > 0 ? '0.75rem' : 0 }}
                  onClick={() => setExpandedUnit(isExpanded ? null : u.unit_id)}
                >
                  <div className="flex-center">
                    <div className="unit-number">{u.unit_number}</div>
                    <div className="unit-info">
                      <h4>{u.unit_title}</h4>
                      <p>{unitConcepts.length} concepts</p>
                    </div>
                  </div>
                  <span className="badge badge-draft">Draft</span>
                </GlassCard>
                {isExpanded && unitConcepts.length > 0 && (
                  <div style={{ paddingLeft: '2rem', display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                    {unitConcepts.map((c: any) => (
                      <GlassCard key={c.concept_id} className="concept-card" style={{ padding: '1rem' }}>
                        <div className="flex-between">
                          <div style={{ flex: 1 }}>
                            <h4 style={{ fontSize: '0.95rem' }}>{c.concept_title}</h4>
                            <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                              {c.textbook_definition?.substring(0, 150)}...
                            </p>
                          </div>
                          <button className="btn btn-accent" style={{ fontSize: '0.8rem', padding: '0.4rem 0.8rem', whiteSpace: 'nowrap', marginLeft: '1rem' }}
                            onClick={() => generateContent(u.unit_id, c.concept_id, c.concept_title)}>
                            Generate
                          </button>
                        </div>
                      </GlassCard>
                    ))}
                  </div>
                )}
                {isExpanded && unitConcepts.length === 0 && (
                  <p style={{ paddingLeft: '2rem', fontSize: '0.85rem', color: 'var(--text-muted)' }}>No concepts in this unit yet</p>
                )}
              </div>
            )
          })}
          {units.length === 0 && <p className="empty-state">No units added yet</p>}
        </div>
      </GlassCard>
    </div>
  )
}
