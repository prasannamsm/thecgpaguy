import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { api } from '../../api/client'
import { GlassCard } from '../../components/GlassCard'

export function AdminDashboard() {
  const [staging, setStaging] = useState<any>(null)
  const [courses, setCourses] = useState<any[]>([])
  const navigate = useNavigate()

  useEffect(() => {
    api.staging.get().then(setStaging)
    api.courses.list().then(setCourses)
  }, [])

  return (
    <div>
      <div className="page-header">
        <h1>Admin Dashboard</h1>
        <p>Manage courses, content, and publishing</p>
      </div>
      <div className="card-grid mb-3">
        <GlassCard className="stat-card">
          <div className="value">{courses.length}</div>
          <div className="label">Courses</div>
        </GlassCard>
        <GlassCard className="stat-card">
          <div className="value">{staging?.pending_concepts ?? 0}</div>
          <div className="label">Pending Concepts</div>
        </GlassCard>
        <GlassCard className="stat-card">
          <div className="value">{staging?.pending_media ?? 0}</div>
          <div className="label">Pending Media</div>
        </GlassCard>
        <GlassCard className="stat-card">
          <div className="value">{staging?.pending_assessments ?? 0}</div>
          <div className="label">Pending Assessments</div>
        </GlassCard>
      </div>
      <div className="flex-between mb-3">
        <h2 style={{ fontSize: '1.2rem', fontWeight: 600 }}>Your Courses</h2>
        <button className="btn btn-primary" onClick={() => navigate('/admin/courses')}>Manage Courses</button>
      </div>
      <div className="card-grid">
        {courses.map(c => (
          <GlassCard key={c.course_id} className="card" onClick={() => navigate(`/admin/courses/${c.course_id}`)} style={{ cursor: 'pointer' }}>
            <h3>{c.course_name}</h3>
            <p>{c.course_code}</p>
          </GlassCard>
        ))}
        {courses.length === 0 && (
          <div className="empty-state glass" style={{ gridColumn: '1 / -1', padding: '3rem' }}>
            <p>No courses yet. Create your first course to get started.</p>
            <button className="btn btn-primary" onClick={() => navigate('/admin/courses')}>Create Course</button>
          </div>
        )}
      </div>
    </div>
  )
}
