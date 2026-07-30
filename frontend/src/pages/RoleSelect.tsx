import { useNavigate } from 'react-router-dom'
import { GlassCard } from '../components/GlassCard'

export function RoleSelect() {
  const navigate = useNavigate()
  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: '2rem' }}>
      <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
        <h1 style={{ fontSize: '2.5rem', fontWeight: 800, color: 'var(--primary)', letterSpacing: '-0.03em' }}>thecgpaguy</h1>
        <p style={{ color: 'var(--text-muted)', marginTop: '0.5rem' }}>Syllabus-Anchored AI Learning Platform</p>
      </div>
      <div className="role-grid">
        <GlassCard className="role-card" onClick={() => navigate('/admin')}>
          <div className="icon">🎓</div>
          <h2>Admin</h2>
          <p>Upload syllabi, generate content, review and publish course materials</p>
        </GlassCard>
        <GlassCard className="role-card" onClick={() => navigate('/student')}>
          <div className="icon">📚</div>
          <h2>Student</h2>
          <p>Study published courses, take assessments, track your progress</p>
        </GlassCard>
      </div>
    </div>
  )
}
