import { useEffect, useState } from 'react'
import { useAuth, useToast } from './context'
import LoginPage from './pages/LoginPage'
import CitizenInputPage from './pages/CitizenInputPage'
import DashboardPage from './pages/DashboardPage'
import ImpactPage from './pages/ImpactPage'
import EvaluationPage from './pages/EvaluationPage'
import TrackPage from './pages/TrackPage'
import { Landmark } from 'lucide-react'

export default function App() {
  const { user, logout } = useAuth()
  const toast = useToast()
  const isPolicymaker = user && ['policymaker', 'analyst'].includes(user.role)
  const [currentPage, setCurrentPage] = useState(() => isPolicymaker ? 'dashboard' : 'submit')

  useEffect(() => {
    setCurrentPage(isPolicymaker ? 'dashboard' : 'submit')
  }, [isPolicymaker])

  if (!user) return <LoginPage />

  const nav = [
    { id: 'submit', label: '📝 Submit Request', show: !isPolicymaker },
    { id: 'track', label: '🔎 Track Request', show: true, dataProp: 'data-tab' },
    { id: 'dashboard', label: '🗺️ Dashboard', show: isPolicymaker },
    { id: 'impact', label: '📈 Impact', show: isPolicymaker },
    { id: 'evaluation', label: '🔬 Evaluation', show: isPolicymaker },
  ].filter(n => n.show)

  return (
    <div className="app">
      <nav className="nav">
        <a className="nav-logo" href="#">
          <div className="logo-icon"><Landmark size={17} strokeWidth={2.2} /></div>
          <span>CDIP</span>
          <span className="nav-product-name">Citizen Development Intelligence</span>
        </a>

        <div className="nav-tabs">
          {nav.map(n => (
            <button key={n.id} className={`nav-tab ${currentPage === n.id ? 'active' : ''}`}
              onClick={() => setCurrentPage(n.id)} data-tab={n.id}>
              {n.label}
            </button>
          ))}
        </div>

        <div className="nav-right">
          <span className="nav-badge">
            {user.role === 'policymaker' ? '🏛️ Policymaker' : user.role === 'analyst' ? '📊 Analyst' : '👤 Citizen'}
          </span>
          <span style={{ fontSize: 13, color: 'var(--text-secondary)' }}>{user.name}</span>
          <button className="btn btn-ghost btn-sm" onClick={() => { logout(); toast('Logged out', 'info') }}>Logout</button>
          <span className="nav-badge" style={{ background: 'rgba(245,158,11,0.1)', color: 'var(--warning)', borderColor: 'rgba(245,158,11,0.3)', fontSize: 10 }}>
            SYNTHETIC DATA
          </span>
        </div>
      </nav>

      <main style={{ flex: 1 }}>
        {currentPage === 'submit' && <CitizenInputPage />}
        {currentPage === 'track' && <TrackPage />}
        {currentPage === 'dashboard' && isPolicymaker && <DashboardPage />}
        {currentPage === 'impact' && isPolicymaker && <ImpactPage />}
        {currentPage === 'evaluation' && isPolicymaker && <EvaluationPage />}
        {!isPolicymaker && ['dashboard','impact','evaluation'].includes(currentPage) && (
          <div className="page" style={{ textAlign: 'center', paddingTop: 60 }}>
            <p style={{ fontSize: 48, marginBottom: 16 }}>🔒</p>
            <p style={{ color: 'var(--text-secondary)' }}>This section requires Policymaker or Analyst access.</p>
            <button className="btn btn-ghost" style={{ marginTop: 16 }} onClick={() => setCurrentPage('submit')}>← Back to Submit</button>
          </div>
        )}
      </main>

      <footer style={{ padding: '16px 24px', borderTop: '1px solid var(--border)', background: 'var(--bg-card)', display: 'flex', justifyContent: 'space-between', flexWrap: 'wrap', gap: 8 }}>
        <span style={{ fontSize: 11, color: 'var(--text-muted)' }}>
          CDIP — Citizen Development Intelligence Platform · India Prototype · Digital Public Good (DPG) · License: Apache-2.0
        </span>
        <span style={{ fontSize: 11, color: 'var(--warning)' }}>
          ⚠️ All datasets are synthetic. No real government integration. Decision-support only.
        </span>
      </footer>
    </div>
  )
}
