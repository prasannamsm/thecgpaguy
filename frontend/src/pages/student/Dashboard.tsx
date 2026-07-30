import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { api } from '../../api/client'
import { GlassCard } from '../../components/GlassCard'

export function StudentDashboard() {
  const [courses, setCourses] = useState<any[]>([])
  const navigate = useNavigate()

  useEffect(() => {
    api.runtime.courses().then(setCourses)
  }, [])

  return (
    <div>
      <div className="page-header">
        <h1>My Courses</h1>
        <p>Select a course to start learning</p>
      </div>
      <div className="card-grid">
        {courses.map(c => (
          <GlassCard key={c.course_id} className="card" onClick={() => navigate(`/student/courses/${c.course_id}`)} style={{ cursor: 'pointer' }}>
            <h3>{c.course_name}</h3>
            <p>{c.course_code}</p>
          </GlassCard>
        ))}
        {courses.length === 0 && (
          <div className="empty-state glass" style={{ gridColumn: '1 / -1', padding: '3rem' }}>
            <p style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>📚</p>
            <p>No published courses available yet.</p>
            <p style={{ fontSize: '0.85rem', marginTop: '0.5rem' }}>Ask your instructor to publish course content.</p>
          </div>
        )}
      </div>
    </div>
  )
}
