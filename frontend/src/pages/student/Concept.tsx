import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { api } from '../../api/client'
import { GlassCard } from '../../components/GlassCard'

export function StudentConcept() {
  const { courseId, unitId } = useParams()
  const [concepts, setConcepts] = useState<any[]>([])
  const [selected, setSelected] = useState<any | null>(null)
  const navigate = useNavigate()

  useEffect(() => {
    api.runtime.concepts(unitId!).then(setConcepts)
  }, [unitId])

  return (
    <div>
      <div className="page-header flex-between">
        <div>
          <h1>Unit Overview</h1>
          <p>Learn each concept step by step</p>
        </div>
        <button className="btn btn-primary" onClick={() => navigate(`/student/courses/${courseId}/units/${unitId}/assessment`)}>
          Take Assessment
        </button>
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>
        <div className="concept-list">
          {concepts.map((c: any) => (
            <GlassCard
              key={c.concept_id}
              className="concept-card"
              onClick={() => setSelected(c)}
              style={{ cursor: 'pointer', border: selected?.concept_id === c.concept_id ? '2px solid var(--primary)' : undefined }}
            >
              <h4>{c.concept_title}</h4>
              <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>Click to view details</p>
            </GlassCard>
          ))}
          {concepts.length === 0 && (
            <div className="empty-state glass"><p>No concepts available yet.</p></div>
          )}
        </div>
        <div>
          {selected ? (
            <GlassCard style={{ padding: '1.5rem' }}>
              <h3 style={{ marginBottom: '1rem' }}>{selected.concept_title}</h3>
              <div className="mb-2">
                <h4 style={{ fontSize: '0.85rem', color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: '0.35rem' }}>Definition</h4>
                <p>{selected.textbook_definition}</p>
              </div>
              {selected.textbook_source_ref && (
                <div className="mb-2">
                  <h4 style={{ fontSize: '0.85rem', color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: '0.35rem' }}>Source</h4>
                  <p style={{ fontSize: '0.85rem', fontStyle: 'italic' }}>{selected.textbook_source_ref}</p>
                </div>
              )}
              {selected.simplified_analogy && (
                <div className="mb-2">
                  <h4 style={{ fontSize: '0.85rem', color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: '0.35rem' }}>Analogy</h4>
                  <p>{selected.simplified_analogy}</p>
                </div>
              )}
            </GlassCard>
          ) : (
            <GlassCard style={{ padding: '2rem', textAlign: 'center', color: 'var(--text-muted)' }}>
              <p style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>👆</p>
              <p>Select a concept to view its details</p>
            </GlassCard>
          )}
        </div>
      </div>
    </div>
  )
}
