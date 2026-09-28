import { useEffect, useState } from 'react'
import { api } from '../api'
import { useToast } from '../context'

function ImpactTimeline({ study }) {
  const data = study.time_series_data || []
  const maxRequests = Math.max(...data.map(d => d.requests), 1)
  const preData = data.filter(d => d.phase.includes('Pre') || d.phase === 'Sanctioned')
  const postData = data.filter(d => !d.phase.includes('Pre') && d.phase !== 'Sanctioned')

  return (
    <div style={{ marginTop: 16 }}>
      {/* Bar Chart Visualization */}
      <div style={{ display: 'flex', alignItems: 'flex-end', gap: 4, height: 100, marginBottom: 8, padding: '0 8px' }}>
        {data.map((d, i) => {
          const isPre = d.phase.includes('Pre') || d.phase === 'Sanctioned' || d.phase === 'Adoption Baseline'
          const h = Math.round((d.requests / maxRequests) * 80) + 4
          return (
            <div key={i} style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 2 }}>
              <div style={{ fontSize: 10, color: 'var(--text-muted)' }}>{d.requests}</div>
              <div style={{
                width: '100%', height: h,
                background: isPre ? 'rgba(239,68,68,0.5)' : 'rgba(16,185,129,0.5)',
                borderRadius: '3px 3px 0 0',
                border: `1px solid ${isPre ? 'rgba(239,68,68,0.7)' : 'rgba(16,185,129,0.7)'}`,
                transition: 'height 0.5s'
              }} title={`${d.month}: ${d.requests} requests`} />
            </div>
          )
        })}
      </div>
      <div style={{ display: 'flex', gap: 4, overflow: 'hidden' }}>
        {data.map((d, i) => (
          <div key={i} style={{ flex: 1, fontSize: 9, color: 'var(--text-muted)', textAlign: 'center', lineHeight: 1.2 }}>
            {d.month.split(' ')[0]}
          </div>
        ))}
      </div>
      <div style={{ display: 'flex', gap: 16, marginTop: 10, fontSize: 11 }}>
        <span style={{ display: 'flex', alignItems: 'center', gap: 4, color: '#ef4444' }}>
          <span style={{ width: 10, height: 10, background: 'rgba(239,68,68,0.5)', display: 'inline-block', borderRadius: 2 }} />
          Pre-Adoption
        </span>
        <span style={{ display: 'flex', alignItems: 'center', gap: 4, color: '#10b981' }}>
          <span style={{ width: 10, height: 10, background: 'rgba(16,185,129,0.5)', display: 'inline-block', borderRadius: 2 }} />
          Post-Adoption
        </span>
      </div>
    </div>
  )
}

export default function ImpactPage() {
  const [studies, setStudies] = useState([])
  const [loading, setLoading] = useState(true)
  const toast = useToast()

  useEffect(() => {
    api.getImpact().then(res => {
      setStudies(res.impact_studies || [])
      setLoading(false)
    }).catch(() => { toast('Failed to load impact data', 'error'); setLoading(false) })
  }, [])

  if (loading) return <div className="page"><p style={{ color: 'var(--text-secondary)' }}>Loading impact studies…</p></div>

  return (
    <div className="page">
      <div className="page-header">
        <h1 className="page-title">📈 Impact Measurement & Feedback Loop</h1>
        <p className="page-subtitle">Before/after tracking for adopted recommendations. Demonstrates the closed-loop governance model.</p>
      </div>

      <div className="disclaimer-banner" style={{ borderColor: 'rgba(59,130,246,0.3)', background: 'rgba(59,130,246,0.05)' }}>
        <span className="icon" style={{ color: '#3b82f6' }}>ℹ️</span>
        <span><strong style={{ color: '#3b82f6' }}>Correlation, not Causation.</strong> The before/after trajectories below represent observational correlation based on <strong>synthetic prototype data</strong>. Observed improvements may also reflect seasonal or external factors. Real causal evaluation requires rigorous field surveys and control studies.</span>
      </div>

      {studies.length === 0 && (
        <div style={{ textAlign: 'center', padding: 60, color: 'var(--text-secondary)' }}>
          <div style={{ fontSize: 48, marginBottom: 16 }}>📊</div>
          <p>No adopted projects yet. Mark recommendations as Adopted from the Dashboard to start tracking.</p>
        </div>
      )}

      <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
        {studies.map((study, i) => (
          <div key={i} className="card card-body">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: 12, marginBottom: 16 }}>
              <div>
                <div style={{ display: 'flex', gap: 6, marginBottom: 6 }}>
                  <span className={`badge ${study.status === 'COMPLETED_EVALUATED' ? 'badge-success' : 'badge-info'}`}>
                    {study.status === 'COMPLETED_EVALUATED' ? '✅ Completed & Evaluated' : '🔄 Under Implementation'}
                  </span>
                  <span className="badge badge-neutral">📍 {study.district}, {study.state}</span>
                </div>
                <h2 style={{ fontSize: 16, fontWeight: 700, marginBottom: 4 }}>{study.title}</h2>
                <p style={{ fontSize: 12, color: 'var(--text-secondary)' }}>
                  Adopted: {study.adoption_date} · {study.adopted_by} · ₹{study.allocated_budget_cr_inr} Cr
                </p>
              </div>
              <div style={{ display: 'flex', gap: 16 }}>
                <div style={{ textAlign: 'center' }}>
                  <div style={{ fontSize: 24, fontWeight: 800, color: study.complaint_reduction_pct < 0 ? 'var(--success)' : 'var(--danger)' }}>
                    {study.complaint_reduction_pct > 0 ? '+' : ''}{study.complaint_reduction_pct.toFixed(1)}%
                  </div>
                  <div style={{ fontSize: 11, color: 'var(--text-muted)' }}>Complaint Change</div>
                </div>
                <div style={{ textAlign: 'center' }}>
                  <div style={{ fontSize: 24, fontWeight: 800, color: study.infra_improvement_pts > 0 ? 'var(--success)' : 'var(--text-secondary)' }}>
                    +{study.infra_improvement_pts?.toFixed(1)}pts
                  </div>
                  <div style={{ fontSize: 11, color: 'var(--text-muted)' }}>SDI Improvement</div>
                </div>
              </div>
            </div>

            <div className="grid-2">
              <div>
                <p style={{ fontSize: 12, color: 'var(--text-secondary)', fontWeight: 600, marginBottom: 4 }}>Monthly Citizen Requests Timeline</p>
                <ImpactTimeline study={study} />
              </div>
              <div>
                <p style={{ fontSize: 12, color: 'var(--text-secondary)', fontWeight: 600, marginBottom: 8 }}>Infrastructure Index</p>
                <div style={{ display: 'flex', gap: 16, marginBottom: 12 }}>
                  <div>
                    <div style={{ fontSize: 11, color: 'var(--text-muted)' }}>Before</div>
                    <div style={{ fontSize: 24, fontWeight: 700, color: 'var(--danger)' }}>{study.pre_adoption_infra_score}/100</div>
                  </div>
                  <div style={{ fontSize: 20, color: 'var(--text-muted)', alignSelf: 'center' }}>→</div>
                  <div>
                    <div style={{ fontSize: 11, color: 'var(--text-muted)' }}>After ({study.months_elapsed}mo)</div>
                    <div style={{ fontSize: 24, fontWeight: 700, color: 'var(--success)' }}>{study.post_adoption_infra_score}/100</div>
                  </div>
                </div>
                <div style={{ height: 8, background: 'var(--border)', borderRadius: 4, overflow: 'hidden', marginBottom: 8 }}>
                  <div style={{ height: '100%', width: `${study.post_adoption_infra_score}%`, background: 'var(--gradient-accent)', borderRadius: 4, transition: 'width 1s' }} />
                </div>
                <p style={{ fontSize: 12, color: 'var(--text-secondary)', lineHeight: 1.5 }}>{study.summary}</p>
                <div style={{ marginTop: 12, padding: '8px 12px', background: 'rgba(245,158,11,0.06)', border: '1px solid rgba(245,158,11,0.15)', borderRadius: 6, fontSize: 11, color: 'var(--warning)' }}>
                  {study.correlation_disclaimer}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
