import { API_BASE } from './constants'

const getHeaders = () => {
  const token = localStorage.getItem('cdip_token')
  return {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {})
  }
}

export const api = {
  login: (email, password) =>
    fetch(`${API_BASE}/auth/login`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ email, password }) }).then(r => r.json()),

  submitRequest: (body) =>
    fetch(`${API_BASE}/requests`, { method: 'POST', headers: getHeaders(), body: JSON.stringify(body) }).then(r => r.json()),

  previewExtraction: (body) =>
    fetch(`${API_BASE}/ai/process`, { method: 'POST', headers: getHeaders(), body: JSON.stringify(body) }).then(r => r.json()),

  trackRequest: (code) =>
    fetch(`${API_BASE}/requests/${code}`, { headers: getHeaders() }).then(r => r.json()),

  correctRequest: (code, body) =>
    fetch(`${API_BASE}/requests/${code}/correct`, { method: 'PATCH', headers: getHeaders(), body: JSON.stringify(body) }).then(r => r.json()),

  getHotspots: (params = {}) => {
    const qs = new URLSearchParams(Object.fromEntries(Object.entries(params).filter(([,v]) => v))).toString()
    return fetch(`${API_BASE}/hotspots${qs ? '?' + qs : ''}`, { headers: getHeaders() }).then(r => r.json())
  },

  getRecommendations: (params = {}) => {
    const qs = new URLSearchParams(Object.fromEntries(Object.entries(params).filter(([,v]) => v))).toString()
    return fetch(`${API_BASE}/recommendations${qs ? '?' + qs : ''}`, { headers: getHeaders() }).then(r => r.json())
  },

  adoptRecommendation: (id, body) =>
    fetch(`${API_BASE}/recommendations/${id}/adopt`, { method: 'PATCH', headers: getHeaders(), body: JSON.stringify(body) }).then(r => r.json()),

  getImpact: () =>
    fetch(`${API_BASE}/impact`, { headers: getHeaders() }).then(r => r.json()),

  getMetrics: () =>
    fetch(`${API_BASE}/evaluation-metrics`, { headers: getHeaders() }).then(r => r.json()),

  getAuditLog: () =>
    fetch(`${API_BASE}/audit-log`, { headers: getHeaders() }).then(r => r.json()),

  getInfrastructure: (params = {}) => {
    const qs = new URLSearchParams(Object.fromEntries(Object.entries(params).filter(([,v]) => v))).toString()
    return fetch(`${API_BASE}/infrastructure${qs ? '?' + qs : ''}`, { headers: getHeaders() }).then(r => r.json())
  },

  getRegions: () =>
    fetch(`${API_BASE}/regions`, { headers: getHeaders() }).then(r => r.json()),

  getDatasetRegistry: () =>
    fetch(`${API_BASE}/dataset-registry`, { headers: getHeaders() }).then(r => r.json()),

  listRequests: (params = {}) => {
    const qs = new URLSearchParams(Object.fromEntries(Object.entries(params).filter(([,v]) => v))).toString()
    return fetch(`${API_BASE}/requests${qs ? '?' + qs : ''}`, { headers: getHeaders() }).then(r => r.json())
  },
}
