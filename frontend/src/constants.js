// Language registry — single source of truth for the frontend
export const LANGUAGES = {
  en: { code: 'en', name: 'English', nativeName: 'English', script: 'Latin', font: "'Inter', sans-serif", dir: 'ltr', flag: '🇬🇧', sttQuality: 'Strong' },
  hi: { code: 'hi', name: 'Hindi', nativeName: 'हिन्दी', script: 'Devanagari', font: "'Noto Sans Devanagari', sans-serif", dir: 'ltr', flag: '🇮🇳', sttQuality: 'Strong' },
  kn: { code: 'kn', name: 'Kannada', nativeName: 'ಕನ್ನಡ', script: 'Kannada', font: "'Noto Sans Kannada', sans-serif", dir: 'ltr', flag: '🇮🇳', sttQuality: 'Moderate' },
  ta: { code: 'ta', name: 'Tamil', nativeName: 'தமிழ்', script: 'Tamil', font: "'Noto Sans Tamil', sans-serif", dir: 'ltr', flag: '🇮🇳', sttQuality: 'Moderate' },
  te: { code: 'te', name: 'Telugu', nativeName: 'తెలుగు', script: 'Telugu', font: "'Noto Sans Telugu', sans-serif", dir: 'ltr', flag: '🇮🇳', sttQuality: 'Moderate' },
  bn: { code: 'bn', name: 'Bengali', nativeName: 'বাংলা', script: 'Bengali', font: "'Noto Sans Bengali', sans-serif", dir: 'ltr', flag: '🇮🇳', sttQuality: 'Good' },
}

export const SECTOR_META = {
  water_sanitation: { name: 'Water & Sanitation', icon: '💧', color: '#3b82f6', bg: '#1e3a5f' },
  roads_transport: { name: 'Roads & Connectivity', icon: '🛣️', color: '#f59e0b', bg: '#451a03' },
  primary_healthcare: { name: 'Primary Healthcare', icon: '🏥', color: '#ef4444', bg: '#450a0a' },
  school_education: { name: 'Public Education', icon: '🎓', color: '#10b981', bg: '#052e16' },
  rural_electrification: { name: 'Rural Electrification', icon: '⚡', color: '#8b5cf6', bg: '#2e1065' },
  digital_connectivity: { name: 'Digital Connectivity', icon: '📡', color: '#06b6d4', bg: '#082f49' },
}

export const SEVERITY_META = {
  CRITICAL: { label: 'Critical', color: '#dc2626', bg: 'rgba(220,38,38,0.15)', border: 'rgba(220,38,38,0.4)' },
  HIGH: { label: 'High', color: '#f97316', bg: 'rgba(249,115,22,0.15)', border: 'rgba(249,115,22,0.4)' },
  MODERATE: { label: 'Moderate', color: '#eab308', bg: 'rgba(234,179,8,0.15)', border: 'rgba(234,179,8,0.4)' },
  LOW: { label: 'Low', color: '#22c55e', bg: 'rgba(34,197,94,0.15)', border: 'rgba(34,197,94,0.4)' },
}

export const SAMPLE_PROMPTS = {
  en: "Frequent drinking water pipeline leakages in Kalaburagi rural ward 4. Over 2,000 households without clean water for 2 weeks.",
  hi: "वाराणसी के शिवपुर ब्लॉक में मुख्य सड़क पूरी तरह टूट चुकी है। एम्बुलेंस आने में घंटों लग जाते हैं, कृपया तुरंत मरम्मत कराएं।",
  kn: "ಕಲಬುರಗಿ ತಾಲೂಕಿನ ಆಳಂದ ರಸ್ತೆಯ ಹಳ್ಳಿಗಳಲ್ಲಿ ಕುಡಿಯುವ ನೀರಿನ ಕೊಳವೆ ಒಡೆದು ೧೫ ದಿನಗಳಿಂದ ನೀರಿಲ್ಲ. ಮಹಿಳೆಯರು ದೂರದ ಬಾವಿಯಿಂದ ನೀರು ತರುತ್ತಿದ್ದಾರೆ.",
  ta: "மதுரை புறநகர் பகுதியில் உள்ள ஆரம்ப சுகாதார நிலையத்தில் மருந்து தட்டுப்பாடு மற்றும் மருத்துவர் பற்றாக்குறை உள்ளது.",
  te: "ఖమ్మం రూరల్ మండలంలో ప్రాథమిక ఆరోగ్య కేంద్రంలో అత్యవసర వైద్యులు మరియు మందులు లేక రోగులు ఇబ్బంది పడుతున్నారు.",
  bn: "মুর্শিদাবাদ জেলার ভগবানগোলা ব্লকে স্বাস্থ্যকেন্দ্রে চিকিৎসক নেই এবং পানীয় জলের পাইপলাইন নষ্ট হয়ে গেছে।",
}

export const API_BASE = '/api'
