import { useEffect, useState } from 'react'
import { api } from '../api'
import { useToast } from '../context'

function MetricBlock({ label, value, unit = '', color = 'var(--accent)', description }) {
  return (
    <div style={{ background: 'var(--bg-elevated)', border: '1px solid var(--border)', borderRadius: 8, padding: 14 }}>
      <div style={{ fontSize: 11, color: 'var(--text-muted)', marginBottom: 4, textTransform: 'uppercase', letterSpacing: 0.5 }}>{label}</div>
      <div style={{ fontSize: 22, fontWeight: 700, color }}>{value}{unit}</div>
      {description && <div style={{ fontSize: 11, color: 'var(--text-secondary)', marginTop: 4 }}>{description}</div>}
    </div>
  )
}

function LangRow({ code, data }) {
  const barW = `${Math.round(data.accuracy_pct)}%`
  const color = data.accuracy_pct >= 97 ? '#10b981' : data.accuracy_pct >= 93 ? '#3b82f6' : data.accuracy_pct >= 88 ? '#f59e0b' : '#ef4444'
  return (
    <tr>
      <td><strong>{code.toUpperCase()}</strong></td>
      <td style={{ fontSize: 12, color: 'var(--text-secondary)' }}>{data.script}</td>
      <td>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <div style={{ flex: 1, height: 6, background: 'var(--border)', borderRadius: 3 }}>
            <div style={{ height: '100%', width: barW, background: color, borderRadius: 3, transition: 'width 0.8s' }} />
          </div>
          <span style={{ fontSize: 12, color, width: 40, textAlign: 'right' }}>{data.accuracy_pct}%</span>
        </div>
      </td>
      <td>{data.sample_count}</td>
    </tr>
  )
}

function SectorF1Row({ sector, data }) {
  const f1Color = data.f1 >= 0.92 ? '#10b981' : data.f1 >= 0.88 ? '#3b82f6' : '#f59e0b'
  return (
    <tr>
      <td style={{ fontSize: 12 }}>{sector.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}</td>
      <td style={{ fontSize: 12 }}>{(data.precision * 100).toFixed(0)}%</td>
      <td style={{ fontSize: 12 }}>{(data.recall * 100).toFixed(0)}%</td>
      <td>
        <span style={{ fontWeight: 700, color: f1Color }}>{(data.f1 * 100).toFixed(1)}%</span>
      </td>
      <td style={{ fontSize: 12, color: 'var(--text-muted)' }}>{data.test_cases}</td>
    </tr>
  )
}

export default function EvaluationPage() {
  const [metrics, setMetrics] = useState(null)
  const [auditLog, setAuditLog] = useState([])
  const [tab, setTab] = useState('metrics')
  const toast = useToast()

  useEffect(() => {
    Promise.all([api.getMetrics(), api.getAuditLog()]).then(([m, a]) => {
      setMetrics(m)
      setAuditLog(a.audit_log || [])
    }).catch(() => toast('Failed to load evaluation metrics', 'error'))
  }, [])

  if (!metrics) return <div className="page"><p style={{ color: 'var(--text-secondary)' }}>Loading metrics…</p></div>

  const ld = metrics.language_detection_metrics
  const stt = metrics.speech_to_text_quality
  const nlp = metrics.nlp_taxonomy_classification
  const loc = metrics.location_extraction_accuracy
  const hitl = metrics.human_in_the_loop_governance
  const latency = metrics.overall_system_latency_ms
  const hotspot = metrics.hotspot_detection_precision

  return (
    <div className="page">
      <div className="page-header">
        <h1 className="page-title">🔬 Evaluation Metrics & Audit Log</h1>
        <p className="page-subtitle">Transparent AI model performance, per-language confidence, and complete governance audit trail.</p>
      </div>

      <div className="tabs">
        {[['metrics', '📊 Model Metrics'], ['audit', '📋 Audit Trail'], ['datasets', '🗂️ Dataset Registry']].map(([id, label]) => (
          <button key={id} className={`tab-btn ${tab === id ? 'active' : ''}`} onClick={() => setTab(id)}>{label}</button>
        ))}
      </div>

      {tab === 'metrics' && (
        <div className="fade-in">
          {/* Latency */}
          <h3 style={{ fontSize: 14, fontWeight: 600, marginBottom: 12, color: 'var(--text-secondary)' }}>⏱️ End-to-End Pipeline Latency</h3>
          <div className="grid-4" style={{ marginBottom: 28 }}>
            <MetricBlock label="Median E2E Latency" value={latency.median_end_to_end_latency_ms} unit="ms" description="From submission to structured extraction" />
            <MetricBlock label="P95 Latency" value={latency.p95_latency_ms} unit="ms" color="var(--warning)" description="95th percentile" />
            <MetricBlock label="Lang Detection" value={latency.language_detection_median_ms} unit="ms" color="var(--success)" />
            <MetricBlock label="NLP Extraction" value={latency.nlp_extraction_median_ms} unit="ms" color="#3b82f6" />
          </div>

          {/* Language Detection */}
          <h3 style={{ fontSize: 14, fontWeight: 600, marginBottom: 12, color: 'var(--text-secondary)' }}>🌐 Language Detection Accuracy (n={ld.test_sample_size})</h3>
          <div className="card card-body" style={{ marginBottom: 28 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
              <span style={{ fontSize: 13, color: 'var(--text-secondary)' }}>Overall: <strong style={{ color: 'var(--success)', fontSize: 16 }}>{ld.overall_accuracy_pct}%</strong></span>
            </div>
            <table className="data-table">
              <thead><tr><th>Language</th><th>Script</th><th>Accuracy</th><th>Sample n</th></tr></thead>
              <tbody>
                {Object.entries(ld.per_language_accuracy).map(([code, d]) => <LangRow key={code} code={code} data={d} />)}
              </tbody>
            </table>
          </div>

          {/* STT WER */}
          <h3 style={{ fontSize: 14, fontWeight: 600, marginBottom: 12, color: 'var(--text-secondary)' }}>🎤 Speech-to-Text Quality (Word Error Rate)</h3>
          <div className="card card-body" style={{ marginBottom: 28 }}>
            <p style={{ fontSize: 12, color: 'var(--text-muted)', marginBottom: 12 }}>{stt.metric}</p>
            <table className="data-table">
              <thead><tr><th>Language</th><th>WER ↓</th><th>Confidence</th><th>Quality</th></tr></thead>
              <tbody>
                {Object.entries(stt.per_language_stt).map(([code, d]) => (
                  <tr key={code}>
                    <td><strong>{code.toUpperCase()}</strong></td>
                    <td style={{ color: d.wer_pct <= 8 ? 'var(--success)' : d.wer_pct <= 13 ? 'var(--warning)' : 'var(--danger)' }}>
                      {d.wer_pct}%
                    </td>
                    <td>
                      <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                        <div style={{ width: 60, height: 4, background: 'var(--border)', borderRadius: 2 }}>
                          <div style={{ height: '100%', width: `${d.baseline_confidence * 100}%`, background: 'var(--accent)', borderRadius: 2 }} />
                        </div>
                        <span style={{ fontSize: 12 }}>{Math.round(d.baseline_confidence * 100)}%</span>
                      </div>
                    </td>
                    <td style={{ fontSize: 12, color: d.status.includes('Strong') ? 'var(--success)' : d.status.includes('Good') ? '#3b82f6' : 'var(--warning)' }}>
                      {d.status}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* NLP Classification F1 */}
          <h3 style={{ fontSize: 14, fontWeight: 600, marginBottom: 12, color: 'var(--text-secondary)' }}>🏷️ NLP Taxonomy Classification (Precision / Recall / F1)</h3>
          <div className="card card-body" style={{ marginBottom: 28 }}>
            <div style={{ display: 'flex', gap: 20, marginBottom: 16 }}>
              <MetricBlock label="Macro Precision" value={`${(nlp.macro_precision * 100).toFixed(1)}%`} color="var(--success)" />
              <MetricBlock label="Macro Recall" value={`${(nlp.macro_recall * 100).toFixed(1)}%`} color="#3b82f6" />
              <MetricBlock label="Macro F1" value={`${(nlp.macro_f1_score * 100).toFixed(1)}%`} color="var(--accent)" />
            </div>
            <table className="data-table">
              <thead><tr><th>Sector</th><th>Precision</th><th>Recall</th><th>F1</th><th>Test Cases</th></tr></thead>
              <tbody>
                {Object.entries(nlp.sector_breakdown).map(([sector, d]) => <SectorF1Row key={sector} sector={sector} data={d} />)}
              </tbody>
            </table>
          </div>

          {/* HITL & Hotspot */}
          <div className="grid-2" style={{ marginBottom: 24 }}>
            <div className="card card-body">
              <h3 style={{ fontSize: 14, fontWeight: 600, marginBottom: 12 }}>🔍 Location Extraction</h3>
              <MetricBlock label="Explicit Mention Accuracy" value={loc.explicit_mention_accuracy_pct + '%'} color="var(--success)" />
              <div style={{ marginTop: 8 }}>
                <MetricBlock label="Overall Location Accuracy" value={loc.overall_accuracy_pct + '%'} color="var(--accent)" />
              </div>
            </div>
            <div className="card card-body">
              <h3 style={{ fontSize: 14, fontWeight: 600, marginBottom: 12 }}>🏛️ Human-in-the-Loop</h3>
              <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
                <MetricBlock label="Total Requests" value={hitl.total_requests_processed} />
                <MetricBlock label="Citizen Correction Rate" value={hitl.citizen_self_correction_rate_pct + '%'} color="var(--warning)" description="Human corrections of AI extraction" />
                <MetricBlock label="Policymaker Override Rate" value={hitl.policymaker_override_rate_pct + '%'} color="#8b5cf6" />
                <MetricBlock label="Audit Trail Coverage" value={hitl.audit_trail_coverage_pct + '%'} color="var(--success)" />
              </div>
            </div>
          </div>

          <div className="card card-body">
            <h3 style={{ fontSize: 14, fontWeight: 600, marginBottom: 12 }}>🔥 Hotspot Detection Precision</h3>
            <div className="grid-2">
              <MetricBlock label="Precision vs. Seeded Ground Truth" value={hotspot.precision_against_seeded_ground_truth_pct + '%'} color="var(--success)" />
              <MetricBlock label="False Positive Rate" value={hotspot.false_positive_rate_pct + '%'} color="var(--warning)" description="False hotspot signals on synthetic testbed" />
            </div>
          </div>
        </div>
      )}

      {tab === 'audit' && (
        <div className="fade-in">
          <p style={{ fontSize: 12, color: 'var(--text-secondary)', marginBottom: 16 }}>
            Complete immutable audit trail of all AI actions, citizen corrections, policymaker overrides, and adoption events.
          </p>
          {auditLog.length === 0 ? (
            <p style={{ color: 'var(--text-muted)' }}>No audit events yet. Submit a request to generate entries.</p>
          ) : (
            <div className="card" style={{ overflow: 'hidden' }}>
              <table className="data-table">
                <thead>
                  <tr><th>Timestamp</th><th>Entity</th><th>Action</th><th>Actor</th><th>Changes</th></tr>
                </thead>
                <tbody>
                  {auditLog.map((row, i) => (
                    <tr key={i}>
                      <td style={{ fontSize: 11, fontFamily: 'monospace' }}>{row.timestamp?.substring(0, 19).replace('T', ' ')}</td>
                      <td style={{ fontSize: 11 }}>{row.entity_type}<br/><span style={{ color: 'var(--text-muted)' }}>{row.entity_id?.substring(0, 16)}</span></td>
                      <td>
                        <span className={`badge ${row.action === 'AI_CLASSIFICATION' ? 'badge-purple' : row.action === 'ADOPTED_RECOMMENDATION' ? 'badge-success' : 'badge-warning badge-moderate'}`}>
                          {row.action}
                        </span>
                      </td>
                      <td style={{ fontSize: 12 }}>
                        <span className={`badge ${row.actor_role === 'CITIZEN' ? 'badge-info' : row.actor_role === 'AI_ENGINE' ? 'badge-purple' : 'badge-high'}`}>{row.actor_role}</span>
                      </td>
                      <td style={{ fontSize: 11, color: 'var(--text-muted)' }}>
                        {row.reason || (row.new_value ? JSON.stringify(row.new_value).substring(0, 60) + '…' : '—')}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}

      {tab === 'datasets' && <DatasetRegistryTab />}
    </div>
  )
}

function DatasetRegistryTab() {
  const [datasets, setDatasets] = useState([])
  const toast = useToast()
  useEffect(() => {
    api.getDatasetRegistry().then(r => setDatasets(r.datasets || [])).catch(() => toast('Failed to load registry', 'error'))
  }, [])
  return (
    <div className="fade-in">
      <p style={{ fontSize: 13, color: 'var(--text-secondary)', marginBottom: 16 }}>
        All datasets used in this platform are registered here with source, license, and limitations.
      </p>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
        {datasets.map(d => (
          <div key={d.id} className="card card-body">
            <div style={{ display: 'flex', justifyContent: 'space-between', flexWrap: 'wrap', gap: 8, marginBottom: 8 }}>
              <h3 style={{ fontSize: 14, fontWeight: 600 }}>{d.name}</h3>
              {d.is_synthetic && <span className="badge badge-warning badge-moderate">⚠️ SYNTHETIC / DEMO DATA</span>}
            </div>
            <div className="grid-2" style={{ gap: 12 }}>
              <div>
                <div style={{ fontSize: 11, color: 'var(--text-muted)' }}>Source</div>
                <div style={{ fontSize: 12, color: 'var(--text-secondary)' }}>{d.source}</div>
              </div>
              <div>
                <div style={{ fontSize: 11, color: 'var(--text-muted)' }}>License · Geographic Level · Date</div>
                <div style={{ fontSize: 12, color: 'var(--text-secondary)' }}>{d.license} · {d.geographic_level} · {d.date}</div>
              </div>
            </div>
            <div style={{ marginTop: 8, padding: '8px 10px', background: 'rgba(245,158,11,0.05)', border: '1px solid rgba(245,158,11,0.15)', borderRadius: 6, fontSize: 12, color: 'var(--text-muted)' }}>
              ⚠️ Limitations: {d.limitations}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
