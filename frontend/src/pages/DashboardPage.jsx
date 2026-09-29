import { useEffect, useState } from 'react'
import { MapContainer, TileLayer, CircleMarker, Popup, Tooltip } from 'react-leaflet'
import 'leaflet/dist/leaflet.css'
import { api } from '../api'
import { SECTOR_META, SEVERITY_META } from '../constants'
import { useToast } from '../context'

// Mini bar chart component (no external chart lib needed)
function MiniBarChart({ data, colorKey = 'color', labelKey = 'name', valueKey = 'count' }) {
  const max = Math.max(...data.map(d => d[valueKey]), 1)
  return (
    <div style={{ display: 'flex', alignItems: 'flex-end', gap: 6, height: 80 }}>
      {data.map((d, i) => (
        <div key={i} style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 4 }}>
          <div style={{ fontSize: 11, color: 'var(--text-secondary)' }}>{d[valueKey]}</div>
          <div style={{ width: '100%', height: Math.round((d[valueKey] / max) * 60) + 4, background: d[colorKey] || 'var(--accent)', borderRadius: '3px 3px 0 0', transition: 'height 0.5s' }} />
          <div style={{ fontSize: 10, color: 'var(--text-muted)', textAlign: 'center', lineHeight: 1.2 }}>{d[labelKey]}</div>
        </div>
      ))}
    </div>
  )
}

function PriorityRing({ score, size = 72 }) {
  const radius = (size - 12) / 2
  const circ = 2 * Math.PI * radius
  const offset = circ - (score / 100) * circ
  const color = score >= 75 ? '#dc2626' : score >= 60 ? '#f97316' : score >= 45 ? '#eab308' : '#22c55e'
  return (
    <svg width={size} height={size} style={{ transform: 'rotate(-90deg)' }}>
      <circle cx={size/2} cy={size/2} r={radius} fill="none" stroke="rgba(255,255,255,0.08)" strokeWidth={8} />
      <circle cx={size/2} cy={size/2} r={radius} fill="none" stroke={color} strokeWidth={8}
        strokeDasharray={circ} strokeDashoffset={offset} strokeLinecap="round"
        style={{ transition: 'stroke-dashoffset 1s' }} />
      <text x={size/2} y={size/2} textAnchor="middle" dominantBaseline="central"
        style={{ fill: color, fontSize: 14, fontWeight: 700, transform: 'rotate(90deg)', transformOrigin: '50% 50%' }}>
        {Math.round(score)}
      </text>
    </svg>
  )
}

function HotspotMap({ hotspots }) {
  return (
    <MapContainer
      center={[22.9734, 78.6569]}
      zoom={5}
      scrollWheelZoom
      className="map-container"
      style={{ height: 480, width: '100%' }}
    >
      <TileLayer
        url="https://tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution="&copy; OpenStreetMap contributors"
      />
      {hotspots.map(h => {
        const severity = SEVERITY_META[h.severity] || SEVERITY_META.LOW
        const sector = SECTOR_META[h.sector_id] || {}
        const statusColor = h.request_status === 'COMPLETED'
          ? '#22c55e'
          : h.request_status === 'MIXED'
            ? '#f59e0b'
            : severity.color
        const radius = Math.max(8, Math.min(28, 8 + h.demand_volume / 10))

        return (
          <CircleMarker
            key={h.id}
            center={[h.lat, h.lng]}
            radius={radius}
            pathOptions={{ color: statusColor, fillColor: statusColor, fillOpacity: 0.5, className: `hotspot-marker hotspot-${h.severity.toLowerCase()}` }}
          >
            <Tooltip direction="top" offset={[0, -8]} opacity={1}>
              <div className="hotspot-tooltip">
                <strong>{h.district}, {h.state}</strong>
                <span>{sector.icon || '📍'} {h.sector_name}</span>
                <span><b style={{ color: statusColor }}>{h.severity}</b> · Priority {h.priority_score}/100</span>
              </div>
            </Tooltip>
            <Popup>
              <strong>{sector.icon || '📍'} {h.district}, {h.state}</strong><br />
              {h.sector_name}<br />
              Severity: {h.severity} · Score: {h.priority_score}<br />
              {h.demand_volume} total requests · Trend: {h.trend}<br />
              Pending: {h.pending_count} · Completed: {h.completed_count}<br />
              Status: {h.request_status}
            </Popup>
          </CircleMarker>
        )
      })}
    </MapContainer>
  )
}

function FactorBar({ label, value, weight, contributed, color }) {
  return (
    <div className="score-row">
      <div className="score-row-label">{label}</div>
      <div className="score-row-bar">
        <div className="score-row-fill" style={{ width: `${value}%`, background: color }} />
      </div>
      <div className="score-row-value" style={{ color }}>{Math.round(value)}</div>
      <div style={{ fontSize: 11, color: 'var(--text-muted)', width: 80 }}>×{weight.toFixed(2)} = {contributed.toFixed(1)}pts</div>
    </div>
  )
}

function RecommendationCard({ rec, onAdopt }) {
  const [expanded, setExpanded] = useState(false)
  const [adopting, setAdopting] = useState(false)
  const [adoptName, setAdoptName] = useState('')
  const [adoptBudget, setAdoptBudget] = useState(rec.suggested_budget_cr_inr || 30)
  const toast = useToast()
  const sm = SEVERITY_META[rec.severity] || SEVERITY_META.LOW
  const sectorMeta = SECTOR_META[rec.sector_id] || {}
  const fb = rec.factor_breakdown || {}

  const handleAdopt = async () => {
    if (!adoptName) return toast('Please enter policymaker name', 'error')
    const res = await api.adoptRecommendation(rec.id, { policymaker_name: adoptName, allocated_budget_cr_inr: +adoptBudget, notes: '' })
    toast('Recommendation adopted! Impact tracking initialized.', 'success')
    onAdopt && onAdopt()
    setAdopting(false)
  }

  return (
    <div className="card card-body" style={{ borderLeft: `3px solid ${sm.color}`, marginBottom: 12 }}>
      <div style={{ display: 'flex', alignItems: 'flex-start', gap: 16 }}>
        <PriorityRing score={rec.priority_score} />
        <div style={{ flex: 1 }}>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6, marginBottom: 6 }}>
            <span className={`badge badge-${rec.severity.toLowerCase()}`}>{rec.severity}</span>
            <span className="badge badge-purple">{sectorMeta.icon} {rec.sector_name}</span>
            <span className="badge badge-info">📍 {rec.district}, {rec.state}</span>
            <span className={`badge ${rec.status === 'ADOPTED' ? 'badge-success' : 'badge-neutral'}`}>{rec.status}</span>
          </div>
          <h3 style={{ fontSize: 15, fontWeight: 600, marginBottom: 4 }}>{rec.title}</h3>
          <p style={{ fontSize: 12, color: 'var(--text-secondary)' }}>
            Suggested Budget: ₹{rec.suggested_budget_cr_inr?.toFixed(1)} Cr · ID: {rec.id}
          </p>
          <p style={{ fontSize: 11, color: 'var(--text-muted)', marginTop: 4, fontStyle: 'italic' }}>
            ⚖️ {rec.disclaimer}
          </p>
        </div>
        <button className="btn btn-ghost btn-sm" onClick={() => setExpanded(!expanded)}>
          {expanded ? '▲ Less' : '▼ Evidence'}
        </button>
      </div>

      {expanded && (
        <div style={{ marginTop: 16, borderTop: '1px solid var(--border)', paddingTop: 16 }} className="fade-in">
          {/* Score Formula */}
          <p style={{ fontSize: 12, color: 'var(--text-secondary)', marginBottom: 10 }}>
            Formula: <code style={{ background: 'var(--bg-elevated)', padding: '2px 6px', borderRadius: 4, fontSize: 11 }}>{rec.formula_output}</code>
          </p>
          <div className="score-visual" style={{ marginBottom: 16 }}>
            {fb.demand_volume && <FactorBar label="Demand Volume" value={fb.demand_volume.normalized_score} weight={fb.demand_volume.weight_applied} contributed={fb.demand_volume.points_contributed} color="#6366f1" />}
            {fb.persistence && <FactorBar label="Persistence" value={fb.persistence.normalized_score} weight={fb.persistence.weight_applied} contributed={fb.persistence.points_contributed} color="#8b5cf6" />}
            {fb.infrastructure_gap && <FactorBar label="Infra Gap" value={fb.infrastructure_gap.gap_score} weight={fb.infrastructure_gap.weight_applied} contributed={fb.infrastructure_gap.points_contributed} color="#ef4444" />}
            {fb.demographic_relevance && <FactorBar label="Demographics" value={fb.demographic_relevance.demographic_score} weight={fb.demographic_relevance.weight_applied} contributed={fb.demographic_relevance.points_contributed} color="#f59e0b" />}
          </div>

          {/* Evidence trail */}
          <div style={{ marginBottom: 16 }}>
            <p style={{ fontSize: 12, fontWeight: 600, marginBottom: 8, color: 'var(--text-secondary)' }}>📋 Evidence Trail</p>
            {(rec.evidence_trail || []).map((e, i) => (
              <div key={i} style={{ display: 'flex', gap: 8, marginBottom: 6, fontSize: 12, color: 'var(--text-secondary)' }}>
                <span style={{ color: 'var(--accent)', flexShrink: 0 }}>{i + 1}.</span>
                <span>{e}</span>
              </div>
            ))}
          </div>

          {/* Infrastructure detail */}
          {fb.infrastructure_gap && (
            <div style={{ background: 'var(--bg-elevated)', borderRadius: 8, padding: 12, marginBottom: 16, fontSize: 12 }}>
              <p style={{ color: 'var(--text-muted)', marginBottom: 4 }}>Infrastructure Assessment</p>
              <p style={{ color: 'var(--text-primary)', marginBottom: 4 }}>SDI Score: <strong>{fb.infrastructure_gap.infrastructure_index_score}/100</strong> · Gap: <strong style={{ color: 'var(--danger)' }}>{fb.infrastructure_gap.gap_score?.toFixed(1)}</strong></p>
              {fb.infrastructure_gap.active_investment_plans?.length > 0 && (
                <p style={{ color: 'var(--success)' }}>✅ Existing plan: {fb.infrastructure_gap.active_investment_plans[0]}</p>
              )}
              {!fb.infrastructure_gap.has_existing_funded_plan && (
                <p style={{ color: 'var(--danger)' }}>❌ No active funded project — Gap penalty applied</p>
              )}
            </div>
          )}

          {/* Adopt button */}
          {rec.status !== 'ADOPTED' && (
            <div>
              {!adopting ? (
                <button className="btn btn-success btn-sm" onClick={() => setAdopting(true)} id={`btn-adopt-${rec.id}`}>
                  🏛️ Mark as Adopted / Funded
                </button>
              ) : (
                <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap', alignItems: 'flex-end' }}>
                  <div style={{ flex: 1, minWidth: 160 }}>
                    <label className="form-label">Policymaker Name</label>
                    <input className="form-input" value={adoptName} onChange={e => setAdoptName(e.target.value)} placeholder="Sri / Dr. Name, Designation" />
                  </div>
                  <div style={{ width: 140 }}>
                    <label className="form-label">Budget (₹ Cr)</label>
                    <input className="form-input" type="number" value={adoptBudget} onChange={e => setAdoptBudget(e.target.value)} />
                  </div>
                  <button className="btn btn-success btn-sm" onClick={handleAdopt}>Confirm Adoption</button>
                  <button className="btn btn-ghost btn-sm" onClick={() => setAdopting(false)}>Cancel</button>
                </div>
              )}
              <p style={{ fontSize: 11, color: 'var(--text-muted)', marginTop: 6 }}>
                Adoption triggers impact monitoring. All decisions require standard human approval processes.
              </p>
            </div>
          )}
          {rec.status === 'ADOPTED' && rec.adoption_metadata && (
            <div style={{ background: 'rgba(16,185,129,0.08)', border: '1px solid rgba(16,185,129,0.2)', borderRadius: 8, padding: 10, fontSize: 12, color: 'var(--success)' }}>
              ✅ Adopted by {rec.adoption_metadata.adopted_by} · ₹{rec.adoption_metadata.allocated_budget_cr_inr} Cr allocated
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default function DashboardPage() {
  const [tab, setTab] = useState('overview')
  const [hotspots, setHotspots] = useState([])
  const [recs, setRecs] = useState([])
  const [requests, setRequests] = useState([])
  const [infra, setInfra] = useState([])
  const [loading, setLoading] = useState(true)
  const [weights, setWeights] = useState({ w1: 0.35, w2: 0.25, w3: 0.25, w4: 0.15 })
  const [filterState, setFilterState] = useState('')
  const [filterSector, setFilterSector] = useState('')
  const toast = useToast()

  const loadData = async () => {
    setLoading(true)
    try {
      const [hRes, rRes, reqRes, iRes] = await Promise.all([
        api.getHotspots({ state: filterState, sector: filterSector }),
        api.getRecommendations({ state: filterState, ...weights }),
        api.listRequests({ state: filterState, limit: 50 }),
        api.getInfrastructure()
      ])
      setHotspots(hRes.hotspots || [])
      setRecs(rRes.recommendations || [])
      setRequests(reqRes.requests || [])
      setInfra(iRes.infrastructure || [])
    } catch { toast('Failed to load dashboard data', 'error') }
    setLoading(false)
  }

  useEffect(() => { loadData() }, [filterState, filterSector, weights])

  const totalRequests = requests.length
  const criticalHotspots = hotspots.filter(h => h.severity === 'CRITICAL').length
  const adoptedRecs = recs.filter(r => r.status === 'ADOPTED').length

  const sectorBreakdown = Object.entries(SECTOR_META).map(([id, s]) => ({
    name: s.icon + ' ' + s.name.split(' ')[0],
    count: requests.filter(r => r.category_name?.includes(s.name.split(' ')[0]) || r.category_name === s.name).length,
    color: s.color
  })).filter(d => d.count > 0)

  const langBreakdown = ['en', 'hi', 'kn', 'ta', 'te', 'bn'].map(code => ({
    name: code.toUpperCase(),
    count: requests.filter(r => r.original_language === code).length,
    color: 'var(--accent)'
  })).filter(d => d.count > 0)

  const states = [...new Set([...hotspots.map(h => h.state), ...recs.map(r => r.state)])]

  return (
    <div className="page">
      <div className="disclaimer-banner">
        <span className="icon">⚠️</span>
        <strong style={{ color: 'var(--warning)' }}>Decision Support Tool Only</strong>
        <span style={{ marginLeft: 4 }}>Final project sanctions, budget approvals, and development decisions rest with authorized human policymakers. All data is synthetic.</span>
      </div>

      {/* Filter bar */}
      <div style={{ display: 'flex', gap: 10, flexWrap: 'wrap', marginBottom: 20, alignItems: 'center' }}>
        <select className="form-select" style={{ width: 'auto' }} value={filterState} onChange={e => setFilterState(e.target.value)}>
          <option value="">All States</option>
          {states.map(s => <option key={s}>{s}</option>)}
        </select>
        <select className="form-select" style={{ width: 'auto' }} value={filterSector} onChange={e => setFilterSector(e.target.value)}>
          <option value="">All Sectors</option>
          {Object.entries(SECTOR_META).map(([id, s]) => <option key={id} value={id}>{s.icon} {s.name}</option>)}
        </select>
        <button className="btn btn-ghost btn-sm" onClick={loadData}>🔄 Refresh</button>
        <div style={{ fontSize: 12, color: 'var(--text-muted)' }}>
          {loading ? '⏳ Loading…' : `${hotspots.length} hotspots · ${recs.length} recommendations`}
        </div>
      </div>

      <div className="tabs">
        {[['overview', '📊 Overview'], ['map', '🗺️ Hotspot Map'], ['recommendations', '🏛️ Recommendations'], ['requests', '📥 Citizen Requests']].map(([id, label]) => (
          <button key={id} className={`tab-btn ${tab === id ? 'active' : ''}`} onClick={() => setTab(id)}>{label}</button>
        ))}
      </div>

      {/* OVERVIEW TAB */}
      {tab === 'overview' && (
        <div className="fade-in">
          <div className="grid-4" style={{ marginBottom: 24 }}>
            <div className="stat-card">
              <div className="stat-value">{totalRequests}</div>
              <div className="stat-label">Citizen Requests (Synthetic)</div>
            </div>
            <div className="stat-card">
              <div className="stat-value" style={{ color: 'var(--danger)' }}>{criticalHotspots}</div>
              <div className="stat-label">Critical Hotspots</div>
            </div>
            <div className="stat-card">
              <div className="stat-value" style={{ color: 'var(--accent)' }}>{hotspots.length}</div>
              <div className="stat-label">Active Hotspots</div>
            </div>
            <div className="stat-card">
              <div className="stat-value" style={{ color: 'var(--success)' }}>{adoptedRecs}</div>
              <div className="stat-label">Recommendations Adopted</div>
            </div>
          </div>

          <div className="grid-2" style={{ marginBottom: 24 }}>
            <div className="card card-body">
              <h3 className="card-title">📊 Demand by Sector</h3>
              <div style={{ marginTop: 12 }}>
                <MiniBarChart data={sectorBreakdown} />
              </div>
            </div>
            <div className="card card-body">
              <h3 className="card-title">🌐 Requests by Language</h3>
              <div style={{ marginTop: 12 }}>
                <MiniBarChart data={langBreakdown} />
              </div>
            </div>
          </div>

          {/* Top Hotspots */}
          <div className="card card-body" style={{ marginBottom: 24 }}>
            <h3 className="card-title" style={{ marginBottom: 16 }}>🔥 Top Demand Hotspots</h3>
            <table className="data-table">
              <thead>
                <tr>
                  <th>Severity</th>
                  <th>District / State</th>
                  <th>Sector</th>
                  <th>Demand Vol.</th>
                  <th>Priority Score</th>
                  <th>Trend</th>
                </tr>
              </thead>
              <tbody>
                {hotspots.slice(0, 8).map(h => {
                  const sm = SEVERITY_META[h.severity] || SEVERITY_META.LOW
                  const sec = SECTOR_META[h.sector_id] || {}
                  return (
                    <tr key={h.id}>
                      <td><span className={`badge badge-${h.severity.toLowerCase()}`}>{h.severity}</span></td>
                      <td><strong>{h.district}</strong><br/><span style={{ fontSize: 11, color: 'var(--text-muted)' }}>{h.state}</span></td>
                      <td>{sec.icon} {h.sector_name}</td>
                      <td>{h.demand_volume}</td>
                      <td><strong style={{ color: sm.color }}>{h.priority_score}</strong>/100</td>
                      <td><span className={`badge ${h.trend === 'ACCELERATING' ? 'badge-critical' : h.trend === 'STABLE' ? 'badge-info' : 'badge-low'}`}>{h.trend}</span></td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>

          {/* Prioritization Weights */}
          <div className="card card-body">
            <h3 className="card-title" style={{ marginBottom: 4 }}>⚙️ Prioritization Formula Weights</h3>
            <p style={{ fontSize: 12, color: 'var(--warning)', marginBottom: 16 }}>⚠️ These are prototype assumptions only — not official government policy. Adjust to explore different prioritization strategies.</p>
            <div className="grid-4">
              {[['w1', 'Demand Volume', 'var(--accent)'], ['w2', 'Persistence', '#8b5cf6'], ['w3', 'Infra Gap', 'var(--danger)'], ['w4', 'Demographics', 'var(--warning)']].map(([key, label, color]) => (
                <div key={key}>
                  <label className="form-label">{label} (w={weights[key].toFixed(2)})</label>
                  <input type="range" min="0" max="1" step="0.05" value={weights[key]}
                    onChange={e => setWeights(prev => ({ ...prev, [key]: +e.target.value }))}
                    style={{ width: '100%', accentColor: color }} />
                  <div style={{ height: 4, background: color, borderRadius: 2, width: `${weights[key] * 100}%`, transition: 'width 0.3s' }} />
                </div>
              ))}
            </div>
            <p style={{ fontSize: 12, color: 'var(--text-muted)', marginTop: 12 }}>
              Formula: <code style={{ fontSize: 11 }}>Score = (w1 × demand) + (w2 × persistence) + (w3 × infra_gap) + (w4 × demographics)</code>
            </p>
          </div>
        </div>
      )}

      {/* MAP TAB */}
      {tab === 'map' && (
        <div className="fade-in">
          <div style={{ marginBottom: 12, display: 'flex', gap: 12, flexWrap: 'wrap', alignItems: 'center' }}>
            {Object.entries(SEVERITY_META).map(([s, m]) => (
              <span key={s} style={{ display: 'flex', alignItems: 'center', gap: 6, fontSize: 12, color: m.color }}>
                <span style={{ width: 12, height: 12, borderRadius: '50%', background: m.color, display: 'inline-block' }} />
                {s}
              </span>
            ))}
            <span style={{ fontSize: 12, color: 'var(--text-muted)' }}>· Bubble size = current request count</span>
            <span style={{ fontSize: 12, color: '#f59e0b' }}>🟠 Pending / mixed</span>
            <span style={{ fontSize: 12, color: '#22c55e' }}>🟢 Completed</span>
          </div>
          <HotspotMap hotspots={hotspots} />
          <p style={{ fontSize: 11, color: 'var(--text-muted)', marginTop: 8, textAlign: 'center' }}>
            Map: © OpenStreetMap contributors, © CARTO. Hotspot positions represent district centroids (synthetic). Click any hotspot for details.
          </p>
        </div>
      )}

      {/* RECOMMENDATIONS TAB */}
      {tab === 'recommendations' && (
        <div className="fade-in">
          <p style={{ fontSize: 13, color: 'var(--text-secondary)', marginBottom: 16 }}>
            Recommendations ranked by transparent prioritization score. Each card shows the full mathematical evidence trail.
          </p>
          {recs.map(rec => <RecommendationCard key={rec.id} rec={rec} onAdopt={loadData} />)}
        </div>
      )}

      {/* REQUESTS TAB */}
      {tab === 'requests' && (
        <div className="fade-in">
          <table className="data-table">
            <thead>
              <tr>
                <th>Code</th><th>Language</th><th>Category</th><th>District</th><th>Urgency</th><th>Channel</th><th>Conf.</th><th>Status</th>
              </tr>
            </thead>
            <tbody>
              {requests.map(r => (
                <tr key={r.id}>
                  <td style={{ fontFamily: 'monospace', fontSize: 11 }}>{r.tracking_code}</td>
                  <td><span className="badge badge-info">{r.original_language?.toUpperCase()}</span></td>
                  <td style={{ fontSize: 12 }}>{r.category_name}</td>
                  <td style={{ fontSize: 12 }}>{r.district}<br/><span style={{ fontSize: 10, color: 'var(--text-muted)' }}>{r.state}</span></td>
                  <td><span className={`badge badge-${r.urgency_level === 'High' ? 'critical' : r.urgency_level === 'Medium' ? 'moderate' : 'low'}`}>{r.urgency_level}</span></td>
                  <td style={{ fontSize: 11, color: 'var(--text-muted)' }}>{r.channel}</td>
                  <td style={{ fontSize: 12 }}>
                    <div style={{ width: 50, height: 4, background: 'var(--border)', borderRadius: 2 }}>
                      <div style={{ width: `${Math.round((r.category_confidence || 0.9) * 100)}%`, height: '100%', background: 'var(--accent)', borderRadius: 2 }} />
                    </div>
                    <span style={{ fontSize: 10, color: 'var(--text-muted)' }}>{Math.round((r.category_confidence || 0.9) * 100)}%</span>
                  </td>
                  <td><span className="badge badge-neutral" style={{ fontSize: 10 }}>{r.status}</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
