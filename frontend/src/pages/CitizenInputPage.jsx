import { useState, useRef, useEffect } from 'react'
import { LANGUAGES, SAMPLE_PROMPTS, SECTOR_META } from '../constants'
import { api } from '../api'
import { useToast } from '../context'

function ConfidenceBar({ value, color = 'var(--accent)' }) {
  return (
    <div className="confidence-bar" style={{ marginTop: 6 }}>
      <div className="confidence-fill" style={{ width: `${Math.round(value * 100)}%`, background: color }} />
    </div>
  )
}

function ExtractionPreview({ data, onConfirm, onCorrect, langCode }) {
  const [correcting, setCorrecting] = useState(false)
  const [corrCategory, setCorrCategory] = useState(data.category_id)
  const [corrDistrict, setCorrDistrict] = useState(data.inferred_district)
  const [corrUrgency, setCorrUrgency] = useState(data.urgency_level)

  const sectors = Object.entries(SECTOR_META)
  const lang = LANGUAGES[langCode] || LANGUAGES.en

  return (
    <div className="extraction-card fade-in">
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 16 }}>
        <h3 style={{ fontSize: 15, fontWeight: 600 }}>🤖 AI Extraction Preview</h3>
        <div style={{ display: 'flex', gap: 4 }}>
          <span className="fact-tag">Extracted Fact</span>
          <span className="inference-tag">AI Inference</span>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
        <div className="extraction-field">
          <span className="extraction-key">Detected Language <span className="fact-tag">Fact</span></span>
          <span className="extraction-value" style={{ fontFamily: lang.font }}>
            {lang.nativeName} ({lang.name}) — {lang.script} script
          </span>
          <ConfidenceBar value={data.language_confidence} color="#818cf8" />
          <span style={{ fontSize: 11, color: 'var(--text-muted)', marginTop: 3 }}>{Math.round(data.language_confidence * 100)}% confidence · STT quality: {lang.sttQuality}</span>
          {data.acoustic_warning && <div style={{ marginTop: 6, padding: '6px 10px', background: 'rgba(245,158,11,0.1)', border: '1px solid rgba(245,158,11,0.2)', borderRadius: 6, fontSize: 11, color: 'var(--warning)' }}>⚠️ {data.acoustic_warning}</div>}
        </div>

        <div className="extraction-field">
          <span className="extraction-key">Category <span className="inference-tag">Inference</span></span>
          {correcting ? (
            <select className="form-select" value={corrCategory} onChange={e => setCorrCategory(e.target.value)}>
              {sectors.map(([id, s]) => <option key={id} value={id}>{s.icon} {s.name}</option>)}
            </select>
          ) : (
            <span className="extraction-value">
              {SECTOR_META[data.category_id]?.icon} {data.extracted_category}
            </span>
          )}
          <ConfidenceBar value={data.category_confidence} />
          <span style={{ fontSize: 11, color: 'var(--text-muted)', marginTop: 3 }}>{Math.round(data.category_confidence * 100)}% confidence</span>
        </div>

        <div className="extraction-field">
          <span className="extraction-key">Location <span className="inference-tag">Inference</span></span>
          {correcting ? (
            <input className="form-input" value={corrDistrict} onChange={e => setCorrDistrict(e.target.value)} placeholder="District name" />
          ) : (
            <span className="extraction-value">📍 {data.inferred_district}, {data.inferred_state}</span>
          )}
          <ConfidenceBar value={data.inferred_location_confidence} color={data.inferred_location_confidence > 0.85 ? '#10b981' : '#f59e0b'} />
          <span style={{ fontSize: 11, color: 'var(--text-muted)', marginTop: 3 }}>
            {Math.round(data.inferred_location_confidence * 100)}% confidence · Extracted: "{data.extracted_location_text}"
          </span>
        </div>

        <div className="extraction-field">
          <span className="extraction-key">Urgency <span className="inference-tag">Inference</span></span>
          {correcting ? (
            <select className="form-select" value={corrUrgency} onChange={e => setCorrUrgency(e.target.value)}>
              {['High', 'Medium', 'Low'].map(u => <option key={u} value={u}>{u}</option>)}
            </select>
          ) : (
            <span className="extraction-value">
              <span className={`badge badge-${data.urgency_level === 'High' ? 'critical' : data.urgency_level === 'Medium' ? 'moderate' : 'low'}`}>
                {data.urgency_level}
              </span>
              <span style={{ fontSize: 12, color: 'var(--text-secondary)', marginLeft: 8 }}>{data.urgency_rationale}</span>
            </span>
          )}
        </div>
      </div>

      <div className="extraction-field" style={{ marginTop: 12, background: 'var(--bg-card)', borderRadius: 8, padding: 12 }}>
        <span className="extraction-key">Original Text (preserved for audit) <span className="fact-tag">Source</span></span>
        <span className="extraction-value" style={{ fontFamily: LANGUAGES[langCode]?.font, fontSize: 15, lineHeight: 1.6 }}>{data.original_text}</span>
        {langCode !== 'en' && (
          <>
            <span className="extraction-key" style={{ marginTop: 10 }}>Translated to English (for backend analysis) <span className="inference-tag">AI Translation</span></span>
            <span className="extraction-value" style={{ color: 'var(--text-secondary)', fontStyle: 'italic' }}>{data.translated_text}</span>
            <ConfidenceBar value={data.translation_confidence} color="#10b981" />
          </>
        )}
      </div>

      <div style={{ display: 'flex', gap: 8, marginTop: 16 }}>
        {!correcting ? (
          <>
            <button className="btn btn-primary btn-sm" onClick={() => onConfirm({ corrCategory, corrDistrict, corrUrgency })}>
              ✅ Confirm & Submit
            </button>
            <button className="btn btn-ghost btn-sm" onClick={() => setCorrecting(true)}>
              ✏️ Correct AI Extraction
            </button>
          </>
        ) : (
          <>
            <button className="btn btn-primary btn-sm" onClick={() => { setCorrecting(false); onCorrect({ corrCategory, corrDistrict, corrUrgency }) }}>
              💾 Apply Correction & Submit
            </button>
            <button className="btn btn-ghost btn-sm" onClick={() => setCorrecting(false)}>Cancel</button>
          </>
        )}
      </div>
      <p style={{ fontSize: 11, color: 'var(--text-muted)', marginTop: 10 }}>
        Your correction will be logged in the audit trail and used to improve the model. No personal identifiers are stored.
      </p>
    </div>
  )
}

export default function CitizenInputPage() {
  const toast = useToast()
  const [selectedLang, setSelectedLang] = useState('en')
  const [inputMode, setInputMode] = useState('text') // text | voice | chat
  const [textInput, setTextInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [extraction, setExtraction] = useState(null)
  const [submittedCode, setSubmittedCode] = useState(null)
  const [recording, setRecording] = useState(false)
  const [recordTime, setRecordTime] = useState(0)
  const [chatMessages, setChatMessages] = useState([
    { role: 'bot', text: '🙏 Namaste! I am the CitizenConnect assistant. Please describe your development concern — in your preferred language. Type or use the mic. (यहाँ हिन्दी में भी लिख सकते हैं / ಕನ್ನಡದಲ್ಲಿ ಬರೆಯಿರಿ)', time: new Date() }
  ])
  const [chatInput, setChatInput] = useState('')
  const timerRef = useRef(null)
  const chatEndRef = useRef(null)

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [chatMessages])

  const lang = LANGUAGES[selectedLang]

  const handleLangSelect = (code) => {
    setSelectedLang(code)
    setTextInput(SAMPLE_PROMPTS[code] || '')
    setExtraction(null)
  }

  const handleTextPreview = async () => {
    if (!textInput.trim()) return toast('Please enter a description', 'error')
    setLoading(true)
    try {
      const res = await api.previewExtraction({ text: textInput, language_override: selectedLang })
      setExtraction(res.extraction)
    } catch {
      toast('Preview failed — is the backend running?', 'error')
    }
    setLoading(false)
  }

  const handleConfirmSubmit = async (corrections = {}) => {
    setLoading(true)
    try {
      const res = await api.submitRequest({
        text: textInput,
        language_override: selectedLang,
        channel: inputMode === 'chat' ? 'messaging_chat' : inputMode === 'voice' ? 'voice_audio' : 'web_form'
      })
      if (res.flagged && res.spam_score > 0.8) {
        toast('Submission blocked: ' + res.message, 'error')
      } else {
        const hasCorrections = corrections.corrCategory || corrections.corrDistrict || corrections.corrUrgency
        if (hasCorrections && res.tracking_code) {
          await api.correctRequest(res.tracking_code, {
            corrected_category: corrections.corrCategory,
            corrected_district: corrections.corrDistrict,
            corrected_urgency: corrections.corrUrgency,
            correction_reason: 'Citizen correction from extraction review'
          })
        }
        setSubmittedCode(res.tracking_code)
        toast('Request submitted! Tracking: ' + res.tracking_code, 'success')
        setExtraction(null)
      }
    } catch {
      toast('Submission failed', 'error')
    }
    setLoading(false)
  }

  const startRecording = () => {
    setRecording(true)
    setRecordTime(0)
    timerRef.current = setInterval(() => setRecordTime(t => t + 1), 1000)
  }
  const stopRecording = () => {
    setRecording(false)
    clearInterval(timerRef.current)
    const simulatedTranscript = SAMPLE_PROMPTS[selectedLang] || ''
    setTextInput(simulatedTranscript)
    toast('Voice captured! Review the transcript below.', 'success')
  }

  const sendChatMessage = async () => {
    if (!chatInput.trim()) return
    const userMsg = chatInput; setChatInput('')
    setChatMessages(prev => [...prev, { role: 'user', text: userMsg, time: new Date() }])
    setTimeout(async () => {
      try {
        const res = await api.previewExtraction({ text: userMsg, language_override: selectedLang })
        const ext = res.extraction
        const botReply = `I've received your message. Here's what I understood:\n• Category: ${ext.extracted_category}\n• Location: ${ext.inferred_district}, ${ext.inferred_state}\n• Urgency: ${ext.urgency_level}\n\nIs this correct? Type "yes" to submit, or describe the issue differently.`
        setChatMessages(prev => [...prev, { role: 'bot', text: botReply, time: new Date() }])
        setExtraction(ext)
        setTextInput(userMsg)
      } catch {
        setChatMessages(prev => [...prev, { role: 'bot', text: 'Sorry, I couldn\'t process that. Please try again or switch to text mode.', time: new Date() }])
      }
    }, 800)
  }

  if (submittedCode) return (
    <div className="page">
      <div style={{ maxWidth: 540, margin: '0 auto', textAlign: 'center', paddingTop: 40 }} className="fade-in">
        <div style={{ fontSize: 64, marginBottom: 20 }}>✅</div>
        <h2 style={{ fontSize: 22, fontWeight: 700, marginBottom: 8 }}>Request Submitted!</h2>
        <p style={{ color: 'var(--text-secondary)', marginBottom: 24 }}>Your civic demand has been received and is being processed. No personal data has been retained.</p>
        <div style={{ background: 'var(--bg-elevated)', border: '1px solid var(--border-accent)', borderRadius: 12, padding: 20, marginBottom: 24 }}>
          <p style={{ fontSize: 12, color: 'var(--text-muted)', marginBottom: 6 }}>TRACKING CODE</p>
          <p style={{ fontSize: 28, fontWeight: 800, color: 'var(--accent)', letterSpacing: 2 }}>{submittedCode}</p>
          <p style={{ fontSize: 12, color: 'var(--text-secondary)', marginTop: 8 }}>Save this code to track status of your request</p>
        </div>
        <div style={{ display: 'flex', gap: 10, justifyContent: 'center' }}>
          <button className="btn btn-primary" onClick={() => { setSubmittedCode(null); setTextInput('') }}>Submit Another</button>
          <button className="btn btn-ghost" onClick={() => { document.querySelector('[data-tab="track"]')?.click() }}>Track Request</button>
        </div>
      </div>
    </div>
  )

  return (
    <div className="page">
      <div className="disclaimer-banner">
        <span className="icon">⚠️</span>
        <span>This is a <strong>prototype / demo system</strong> using synthetic data. No real government integration. All AI extractions are decision-support only — not final determinations.</span>
      </div>

      <div style={{ maxWidth: 760, margin: '0 auto' }}>
        <div className="page-header">
          <h1 className="page-title">🗣️ Submit a Civic Development Request</h1>
          <p className="page-subtitle">Voice your development concern in any of 6 languages. AI will extract, translate, and categorize your input — always with human review.</p>
        </div>

        {/* Language Selector */}
        <div className="card card-body" style={{ marginBottom: 20 }}>
          <label className="form-label">🌐 Select Your Language / अपनी भाषा चुनें / ನಿಮ್ಮ ಭಾಷೆ ಆಯ್ಕೆ ಮಾಡಿ</label>
          <div className="lang-grid">
            {Object.values(LANGUAGES).map(l => (
              <button key={l.code} className={`lang-pill ${selectedLang === l.code ? 'active' : ''}`}
                onClick={() => handleLangSelect(l.code)} id={`lang-${l.code}`}>
                <span style={{ fontFamily: l.font }} className="lang-native">{l.nativeName}</span>
                <span style={{ fontSize: 11, color: selectedLang === l.code ? 'var(--accent)' : 'var(--text-muted)' }}>{l.name}</span>
                <span className={`lang-quality`} style={{ color: l.sttQuality === 'Strong' ? 'var(--success)' : l.sttQuality === 'Good' ? '#3b82f6' : 'var(--warning)' }}>
                  {l.sttQuality}
                </span>
              </button>
            ))}
          </div>
          <p style={{ fontSize: 11, color: 'var(--text-muted)', marginTop: 10 }}>STT quality indicators: <span style={{ color: 'var(--success)' }}>Strong</span> / <span style={{ color: '#3b82f6' }}>Good</span> / <span style={{ color: 'var(--warning)' }}>Moderate</span> — Lower confidence inputs will show warnings.</p>
        </div>

        {/* Input Mode */}
        <div className="card card-body" style={{ marginBottom: 20 }}>
          <div className="input-mode-tabs">
            {[['text', '📝 Text'], ['voice', '🎤 Voice'], ['chat', '💬 Chat (WhatsApp-style)']].map(([m, label]) => (
              <button key={m} className={`input-mode-tab ${inputMode === m ? 'active' : ''}`} onClick={() => { setInputMode(m); setExtraction(null) }}>
                {label}
              </button>
            ))}
          </div>

          {/* TEXT MODE */}
          {inputMode === 'text' && (
            <>
              <div className="form-group">
                <label className="form-label" style={{ fontFamily: lang.font }}>
                  {selectedLang === 'en' ? 'Describe your development concern' :
                   selectedLang === 'hi' ? 'अपनी समस्या यहाँ लिखें' :
                   selectedLang === 'kn' ? 'ನಿಮ್ಮ ಸಮಸ್ಯೆ ಇಲ್ಲಿ ಬರೆಯಿರಿ' :
                   selectedLang === 'ta' ? 'உங்கள் பிரச்னையை இங்கே எழுதுங்கள்' :
                   selectedLang === 'te' ? 'మీ సమస్య ఇక్కడ వ్రాయండి' :
                   'আপনার সমস্যা এখানে লিখুন'}
                </label>
                <textarea
                  className="form-textarea"
                  style={{ fontFamily: lang.font, fontSize: 15, minHeight: 120, direction: lang.dir }}
                  value={textInput}
                  onChange={e => { setTextInput(e.target.value); setExtraction(null) }}
                  placeholder={SAMPLE_PROMPTS[selectedLang]}
                  id="text-input-area"
                />
              </div>
              <div style={{ display: 'flex', gap: 8 }}>
                <button className="btn btn-primary" onClick={handleTextPreview} disabled={loading || !textInput.trim()} id="btn-preview">
                  {loading ? '⏳ Analyzing…' : '🔍 Preview AI Extraction'}
                </button>
                <button className="btn btn-ghost btn-sm" onClick={() => setTextInput(SAMPLE_PROMPTS[selectedLang])}>
                  Try Sample
                </button>
              </div>
            </>
          )}

          {/* VOICE MODE */}
          {inputMode === 'voice' && (
            <div className="voice-recorder">
              <button className={`record-btn ${recording ? 'recording' : ''}`}
                onClick={recording ? stopRecording : startRecording} id="btn-record">
                {recording ? '⏹' : '🎤'}
              </button>
              {recording && (
                <>
                  <div className="waveform">
                    {[16, 26, 34, 22, 30, 18, 28, 20].map((height, index) => <div key={index} className="waveform-bar" style={{ height: `${height}px` }} />)}
                  </div>
                  <p style={{ color: 'var(--danger)', fontSize: 13 }}>Recording… {recordTime}s — Tap to stop</p>
                </>
              )}
              {!recording && <p style={{ fontSize: 13, color: 'var(--text-secondary)', textAlign: 'center' }}>
                {textInput ? '✅ Transcript ready — review below' : `Tap the mic to record in ${lang.nativeName}.\nSpeak clearly about your development concern.`}
              </p>}
              {textInput && (
                <>
                  <textarea className="form-textarea" value={textInput} onChange={e => setTextInput(e.target.value)}
                    style={{ fontFamily: lang.font, fontSize: 14, width: '100%' }} />
                  <button className="btn btn-primary" onClick={handleTextPreview} disabled={loading} id="btn-voice-preview">
                    {loading ? '⏳ Analyzing…' : '🔍 Preview Extraction'}
                  </button>
                </>
              )}
              <p style={{ fontSize: 11, color: 'var(--text-muted)', textAlign: 'center' }}>
                Note: Voice capture in this prototype is simulated. In production, this integrates with Whisper/Azure/IndicSTT per language.
              </p>
            </div>
          )}

          {/* CHAT MODE */}
          {inputMode === 'chat' && (
            <>
              <div className="chat-container">
                <div className="chat-messages" id="chat-messages">
                  {chatMessages.map((m, i) => (
                    <div key={i} className={`chat-bubble ${m.role}`}>
                      <div style={{ fontFamily: m.role === 'user' ? lang.font : 'inherit', whiteSpace: 'pre-line' }}>{m.text}</div>
                      <div className="meta">{m.time.toLocaleTimeString()}</div>
                    </div>
                  ))}
                  <div ref={chatEndRef} />
                </div>
                <div className="chat-input-row">
                  <input className="chat-input" value={chatInput} onChange={e => setChatInput(e.target.value)}
                    onKeyDown={e => e.key === 'Enter' && sendChatMessage()}
                    placeholder={`Type in ${lang.nativeName}…`}
                    style={{ fontFamily: lang.font, direction: lang.dir }} id="chat-input" />
                  <button className="btn btn-primary btn-sm" onClick={sendChatMessage} id="btn-chat-send">Send</button>
                </div>
              </div>
            </>
          )}
        </div>

        {/* Extraction Preview */}
        {extraction && (
          <ExtractionPreview
            data={extraction}
            langCode={selectedLang}
            onConfirm={handleConfirmSubmit}
            onCorrect={(corr) => {
              toast('Correction logged. Submitting corrected request…', 'info')
              handleConfirmSubmit(corr)
            }}
          />
        )}
      </div>
    </div>
  )
}
