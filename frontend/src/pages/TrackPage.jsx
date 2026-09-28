import { useState } from 'react'
import { api } from '../api'
import { useToast } from '../context'

export default function TrackPage() {
  const [code, setCode] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const toast = useToast()

  const track = async () => {
    if (!code.trim()) return
    setLoading(true)
    try {
      const res = await api.trackRequest(code.trim())
      if (res.detail) toast('Tracking code not found', 'error')
      else setResult(res)
    } catch { toast('Tracking failed', 'error') }
    setLoading(false)
  }

  const statusColors = {
    RECEIVED: '#6366f1', UNDER_ANALYSIS: '#3b82f6', LINKED_TO_HOTSPOT: '#f59e0b',
    LINKED_TO_PROJECT: '#10b981', RESOLVED: '#22c55e'
  }

  return (
    <div className="page">
      <div style={{ maxWidth: 560, margin: '0 auto' }}>
        <div className="page-header">
          <h1 className="page-title">🔎 Track Your Request</h1>
          <p className="page-subtitle">Enter your tracking code to check the current status of your civic request.</p>
        </div>
        <div className="card card-body">
          <div className="form-group">
            <label className="form-label">Tracking Code</label>
            <input className="form-input" value={code} onChange={e => { setCode(e.target.value); setResult(null) }}
              placeholder="e.g. CRQ-A1B2C3D4" style={{ fontFamily: 'monospace', letterSpacing: 2 }}
              onKeyDown={e => e.key === 'Enter' && track()} id="track-input" />
          </div>
          <button className="btn btn-primary" onClick={track} disabled={loading || !code.trim()} id="btn-track">
            {loading ? '⏳ Searching…' : '🔍 Track Request'}
          </button>
        </div>

        {result && (
          <div className="card card-body fade-in" style={{ marginTop: 20 }}>
            <div style={{ textAlign: 'center', marginBottom: 20 }}>
              <div style={{ fontSize: 48, marginBottom: 8 }}>
                {result.status === 'RESOLVED' ? '✅' : result.status === 'LINKED_TO_PROJECT' ? '🏛️' : result.status === 'LINKED_TO_HOTSPOT' ? '🔥' : '📋'}
              </div>
              <div style={{ fontFamily: 'monospace', fontSize: 18, fontWeight: 700, color: 'var(--accent)', marginBottom: 4 }}>{result.tracking_code}</div>
              <span className="badge" style={{ background: (statusColors[result.status] || '#888') + '20', color: statusColors[result.status] || '#888', border: `1px solid ${(statusColors[result.status] || '#888')}40`, fontSize: 13, padding: '4px 12px' }}>
                {result.status?.replace(/_/g, ' ')}
              </span>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>
              <div><div style={{ fontSize: 11, color: 'var(--text-muted)' }}>Category</div><div style={{ fontSize: 13, fontWeight: 500 }}>{result.category}</div></div>
              <div><div style={{ fontSize: 11, color: 'var(--text-muted)' }}>Urgency</div><div style={{ fontSize: 13 }}><span className={`badge badge-${result.urgency === 'High' ? 'critical' : result.urgency === 'Medium' ? 'moderate' : 'low'}`}>{result.urgency}</span></div></div>
              <div><div style={{ fontSize: 11, color: 'var(--text-muted)' }}>Location</div><div style={{ fontSize: 13 }}>{result.district}, {result.state}</div></div>
              <div><div style={{ fontSize: 11, color: 'var(--text-muted)' }}>Submitted</div><div style={{ fontSize: 13 }}>{result.submitted_at?.substring(0, 10)}</div></div>
            </div>

            {result.linked_hotspot_id && (
              <div style={{ marginTop: 16, padding: '10px 14px', background: 'rgba(245,158,11,0.08)', border: '1px solid rgba(245,158,11,0.2)', borderRadius: 8, fontSize: 12 }}>
                🔥 Your request has been linked to a <strong>demand hotspot</strong> ({result.linked_hotspot_id}) and is being reviewed by policymakers.
              </div>
            )}
            {result.linked_project_id && (
              <div style={{ marginTop: 8, padding: '10px 14px', background: 'rgba(16,185,129,0.08)', border: '1px solid rgba(16,185,129,0.2)', borderRadius: 8, fontSize: 12 }}>
                🏛️ A related <strong>development project</strong> has been adopted. Impact tracking has begun.
              </div>
            )}
            <p style={{ fontSize: 11, color: 'var(--text-muted)', marginTop: 12, textAlign: 'center' }}>
              This is a prototype system with synthetic data. Status updates simulate real-world pipeline behavior.
            </p>
          </div>
        )}
      </div>
    </div>
  )
}
