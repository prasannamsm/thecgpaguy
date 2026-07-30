import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { api } from '../../api/client'
import { GlassCard } from '../../components/GlassCard'

export function AdminCourses() {
  const [courses, setCourses] = useState<any[]>([])
  const [showForm, setShowForm] = useState(false)
  const [form, setForm] = useState({ id: '', code: '', name: '' })
  const navigate = useNavigate()

  const load = () => api.courses.list().then(setCourses)
  useEffect(() => { load() }, [])

  const create = async () => {
    await api.courses.create(form.id, form.code, form.name)
    setShowForm(false)
    setForm({ id: '', code: '', name: '' })
    load()
  }

  return (
    <div>
      <div className="page-header flex-between">
        <div>
          <h1>Courses</h1>
          <p>Create and manage your courses</p>
        </div>
        <button className="btn btn-primary" onClick={() => setShowForm(true)}>+ New Course</button>
      </div>
      {showForm && (
        <GlassCard className="mb-3" style={{ padding: '1.5rem' }}>
          <div className="form-group">
            <label>Course ID</label>
            <input value={form.id} onChange={e => setForm({ ...form, id: e.target.value })} placeholder="e.g. CS301" />
          </div>
          <div className="form-group">
            <label>Course Code</label>
            <input value={form.code} onChange={e => setForm({ ...form, code: e.target.value })} placeholder="e.g. CS301" />
          </div>
          <div className="form-group">
            <label>Course Name</label>
            <input value={form.name} onChange={e => setForm({ ...form, name: e.target.value })} placeholder="e.g. Operating Systems" />
          </div>
          <div className="flex-center mt-2 gap-1">
            <button className="btn btn-primary" onClick={create}>Create</button>
            <button className="btn btn-outline" onClick={() => setShowForm(false)}>Cancel</button>
          </div>
        </GlassCard>
      )}
      <div className="card-grid">
        {courses.map(c => (
          <GlassCard key={c.course_id} className="card" onClick={() => navigate(`/admin/courses/${c.course_id}`)} style={{ cursor: 'pointer' }}>
            <h3>{c.course_name}</h3>
            <p style={{ marginBottom: '0.5rem' }}>{c.course_code}</p>
            <span className={`badge ${c.target_profile ? 'badge-approved' : 'badge-draft'}`}>
              {c.target_profile ? 'Ingested' : 'Draft'}
            </span>
          </GlassCard>
        ))}
      </div>
    </div>
  )
}
