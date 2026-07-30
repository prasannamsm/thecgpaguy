import { useEffect, useState } from 'react'
import { api } from '../../api/client'
import { GlassCard } from '../../components/GlassCard'

export function AdminStaging() {
  const [summary, setSummary] = useState<any>(null)
  const [pendingConcepts, setPendingConcepts] = useState<any[]>([])
  const [pendingMedia, setPendingMedia] = useState<any[]>([])
  const [tab, setTab] = useState<'concepts' | 'media' | 'assessments'>('concepts')

  useEffect(() => {
    api.staging.get().then(setSummary)
    api.staging.concepts().then(setPendingConcepts)
    api.staging.media().then(setPendingMedia)
  }, [])

  const approve = async (id: string) => {
    await api.media.approve(id)
    api.staging.media().then(setPendingMedia)
    api.staging.get().then(setSummary)
  }

  const reject = async (id: string) => {
    await api.media.reject(id)
    api.staging.media().then(setPendingMedia)
    api.staging.get().then(setSummary)
  }

  const tabs = ['concepts', 'media', 'assessments'] as const

  return (
    <div>
      <div className="page-header">
        <h1>Review Workspace</h1>
        <p>Review and approve generated content before publishing</p>
      </div>
      {summary && (
        <div className="card-grid mb-3">
          <GlassCard className="stat-card">
            <div className="value">{summary.pending_concepts}</div>
            <div className="label">Pending Concepts</div>
          </GlassCard>
          <GlassCard className="stat-card">
            <div className="value">{summary.pending_media}</div>
            <div className="label">Pending Media</div>
          </GlassCard>
          <GlassCard className="stat-card">
            <div className="value">{summary.pending_assessments}</div>
            <div className="label">Pending Assessments</div>
          </GlassCard>
        </div>
      )}
      <div className="flex-center gap-1 mb-3">
        {tabs.map(t => (
          <button key={t} className={`btn ${tab === t ? 'btn-primary' : 'btn-outline'}`} onClick={() => setTab(t)}>
            {t.charAt(0).toUpperCase() + t.slice(1)}
          </button>
        ))}
      </div>
      {tab === 'media' && (
        <div className="concept-list">
          {pendingMedia.map((m: any) => (
            <GlassCard key={m.media_id} className="concept-card">
              <div className="flex-between">
                <div>
                  <p><strong>Type:</strong> {m.media_type}</p>
                  <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>{m.source_url}</p>
                  <span className={`badge ${m.license_status === 'OPEN' ? 'badge-approved' : 'badge-pending'}`}>
                    {m.license_status}
                  </span>
                </div>
                <div className="flex-center gap-1">
                  <button className="btn btn-success" onClick={() => approve(m.media_id)}>Approve</button>
                  <button className="btn btn-danger" onClick={() => reject(m.media_id)}>Reject</button>
                </div>
              </div>
            </GlassCard>
          ))}
          {pendingMedia.length === 0 && <div className="empty-state glass"><p>No pending media items</p></div>}
        </div>
      )}
      {tab === 'concepts' && (
        <div className="concept-list">
          {pendingConcepts.map((c: any) => (
            <GlassCard key={c.concept_id} className="concept-card">
              <h4>{c.concept_title}</h4>
              <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>{c.textbook_definition?.substring(0, 200)}...</p>
            </GlassCard>
          ))}
          {pendingConcepts.length === 0 && <div className="empty-state glass"><p>No pending concepts</p></div>}
        </div>
      )}
      {tab === 'assessments' && (
        <div className="empty-state glass"><p>No pending assessments</p></div>
      )}
    </div>
  )
}
