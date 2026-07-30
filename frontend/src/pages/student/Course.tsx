import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { api } from '../../api/client'
import { GlassCard } from '../../components/GlassCard'

export function StudentCourse() {
  const { courseId } = useParams()
  const [units, setUnits] = useState<any[]>([])
  const navigate = useNavigate()

  useEffect(() => {
    api.units.list(courseId!).then(setUnits)
  }, [courseId])

  return (
    <div>
      <div className="page-header">
        <h1>{courseId}</h1>
        <p>Units & Progress</p>
      </div>
      <div className="unit-list">
        {units.map((u: any) => (
          <GlassCard key={u.unit_id} className="unit-item" style={{ cursor: 'pointer' }} onClick={() => navigate(`/student/courses/${courseId}/units/${u.unit_id}`)}>
            <div className="flex-center">
              <div className="unit-number">{u.unit_number}</div>
              <div className="unit-info">
                <h4>{u.unit_title}</h4>
                <p>Click to start learning</p>
              </div>
            </div>
            <span className="badge badge-draft">Not started</span>
          </GlassCard>
        ))}
        {units.length === 0 && (
          <div className="empty-state glass"><p>No units available for this course yet.</p></div>
        )}
      </div>
    </div>
  )
}
