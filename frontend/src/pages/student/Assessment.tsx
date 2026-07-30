import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { api } from '../../api/client'
import { GlassCard } from '../../components/GlassCard'

export function StudentAssessment() {
  const { courseId, unitId } = useParams()
  const [questions, setQuestions] = useState<any[]>([])
  const [answers, setAnswers] = useState<Record<string, string>>({})
  const [results, setResults] = useState<Record<string, any>>({})

  useEffect(() => {
    api.runtime.concepts(unitId!).then(() => {
      api.blueprint.get(unitId!).then(setQuestions)
    })
  }, [unitId])

  const submitAnswer = async (qId: string, type: string) => {
    const answer = answers[qId] || ''
    if (type === 'SHORT_ANSWER' || type === 'DESCRIPTIVE_PROOF') {
      const result = await api.runtime.grade(answer, 'Expected answer key')
      setResults(prev => ({ ...prev, [qId]: result }))
    }
  }

  return (
    <div>
      <div className="page-header">
        <h1>Assessment</h1>
        <p>Unit {unitId?.substring(0, 8)}</p>
      </div>
      <div className="concept-list">
        {questions.map((q: any) => (
          <GlassCard key={q.question_id} style={{ padding: '1.5rem' }}>
            <div className="flex-between mb-2">
              <span className={`badge ${q.question_type === 'SHORT_ANSWER' ? 'badge-approved' : 'badge-pending'}`}>
                {q.question_type}
              </span>
            </div>
            <p className="mb-2">{q.question_text}</p>
            <textarea
              className="mb-2"
              rows={4}
              style={{ width: '100%', padding: '0.65rem', borderRadius: 'var(--radius-sm)', border: '1px solid rgba(0,0,0,0.1)', fontFamily: 'var(--font)', fontSize: '0.9rem' }}
              placeholder="Type your answer..."
              value={answers[q.question_id] || ''}
              onChange={e => setAnswers(prev => ({ ...prev, [q.question_id]: e.target.value }))}
            />
            <div className="flex-between">
              <button className="btn btn-accent" onClick={() => submitAnswer(q.question_id, q.question_type)}>Submit</button>
              {results[q.question_id] && (
                <div style={{ textAlign: 'right' }}>
                  <p style={{ fontWeight: 700, color: 'var(--success)' }}>Score: {results[q.question_id].score}</p>
                </div>
              )}
            </div>
          </GlassCard>
        ))}
        {questions.length === 0 && (
          <div className="empty-state glass"><p>No assessment questions yet.</p></div>
        )}
      </div>
    </div>
  )
}
