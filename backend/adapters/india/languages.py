"""
India Language Registry - Config-Driven Single Source of Truth
Supports the 6 mandatory core languages across North, South, and East India:
English, Hindi, Kannada, Tamil, Telugu, Bengali.
"""

SUPPORTED_LANGUAGES = {
    "en": {
        "code": "en",
        "name": "English",
        "native_name": "English",
        "script": "Latin",
        "font_family": "'Inter', 'Segoe UI', system-ui, sans-serif",
        "text_direction": "ltr",
        "stt_confidence_baseline": 0.96,
        "translation_engine": "Native Reference / Passthrough",
        "acoustic_notes": "Standard Indian English acoustic model; handles Indian accent variations.",
        "sample_prompts": [
            "Frequent drinking water pipeline leakages in Kalaburagi rural ward 4. Over 2,000 households without clean water for 2 weeks.",
            "Dangerous potholes on state highway 28 near Belagavi agricultural market causing accidents daily.",
            "Primary health centre in Murshidabad lacks emergency oxygen and maternal care facilities."
        ]
    },
    "hi": {
        "code": "hi",
        "name": "Hindi",
        "native_name": "हिन्दी",
        "script": "Devanagari",
        "font_family": "'Noto Sans Devanagari', 'Mangal', sans-serif",
        "text_direction": "ltr",
        "stt_confidence_baseline": 0.92,
        "translation_engine": "AI Neural Translation (Devanagari -> EN)",
        "acoustic_notes": "High accuracy on standard Hindi; moderate variation with regional Bhojpuri/Awadhi influences.",
        "sample_prompts": [
            "वाराणसी के शिवपुर ब्लॉक में मुख्य सड़क पूरी तरह टूट चुकी है। एम्बुलेंस आने में घंटों लग जाते हैं, कृपया तुरंत मरम्मत कराएं।",
            "लखनऊ के काकोरी प्राथमिक विद्यालय में पीने के पानी और बिजली की भारी किल्लत है। 300 बच्चों की पढ़ाई प्रभावित हो रही है।",
            "कानपुर देहात के सामुदायिक स्वास्थ्य केंद्र में पिछले तीन महीने से डॉक्टर उपलब्ध नहीं हैं।"
        ]
    },
    "kn": {
        "code": "kn",
        "name": "Kannada",
        "native_name": "ಕನ್ನಡ",
        "script": "Kannada",
        "font_family": "'Noto Sans Kannada', 'Tunga', sans-serif",
        "text_direction": "ltr",
        "stt_confidence_baseline": 0.84,
        "translation_engine": "AI Neural Translation (Kannada -> EN)",
        "acoustic_notes": "Regional dialect variation between Old Mysuru and North Karnataka (Kalyana-Karnataka); confidence warning flagged for fast colloquial speech.",
        "sample_prompts": [
            "ಕಲಬುರಗಿ ತಾಲೂಕಿನ ಆಳಂದ ರಸ್ತೆಯ ಹಳ್ಳಿಗಳಲ್ಲಿ ಕುಡಿಯುವ ನೀರಿನ ಕೊಳವೆ ಒಡೆದು ೧೫ ದಿನಗಳಿಂದ ನೀರಿಲ್ಲ. ಮಹಿಳೆಯರು ದೂರದ ಬಾವಿಯಿಂದ ನೀರು ತರುತ್ತಿದ್ದಾರೆ.",
            "ಬೆಳಗಾವಿ ಜಿಲ್ಲೆಯ ಹುಕ್ಕೇರಿ ತಾಲೂಕಿನಲ್ಲಿ ಪ್ರಾಥಮಿಕ ಆರೋಗ್ಯ ಕೇಂದ್ರದಲ್ಲಿ ತುರ್ತು ಚಿಕಿತ್ಸೆ ಮತ್ತು ಆಂಬ್ಯುಲೆನ್ಸ್ ಸೌಲಭ್ಯ ಇಲ್ಲ.",
            "ಶಿವಮೊಗ್ಗ ಗ್ರಾಮೀಣ ಭಾಗದಲ್ಲಿ ಮಳೆಗಾಲದ ರಸ್ತೆ ಹಾಳಾಗಿದ್ದು ಬಸ್ ಸಂಚಾರ ಸ್ಥಗಿತಗೊಂಡಿದೆ."
        ]
    },
    "ta": {
        "code": "ta",
        "name": "Tamil",
        "native_name": "தமிழ்",
        "script": "Tamil",
        "font_family": "'Noto Sans Tamil', 'Latha', sans-serif",
        "text_direction": "ltr",
        "stt_confidence_baseline": 0.85,
        "translation_engine": "AI Neural Translation (Tamil -> EN)",
        "acoustic_notes": "High performance on formal Tamil; colloquial spoken Tamil requires phonetic normalizer.",
        "sample_prompts": [
            "மதுரை புறநகர் பகுதியில் உள்ள ஆரம்ப சுகாதார நிலையத்தில் மருந்து தட்டுப்பாடு மற்றும் மருத்துவர் பற்றாக்குறை உள்ளது.",
            "திருச்சிராப்பள்ளி திருவெறும்பூர் பகுதியில் குடிநீர் குழாய் உடைந்து கழிவுநீர் கலக்கிறது. 500 குடும்பங்கள் பாதிக்கப்பட்டுள்ளன.",
            "சேலம் கிராமப்புற பகுதியில் அரசு பள்ளியில் வகுப்பறை கூரை சேதமடைந்துள்ளது, மழை பெய்தால் வகுப்புகள் நடத்த முடியாது."
        ]
    },
    "te": {
        "code": "te",
        "name": "Telugu",
        "native_name": "తెలుగు",
        "script": "Telugu",
        "font_family": "'Noto Sans Telugu', 'Gautami', sans-serif",
        "text_direction": "ltr",
        "stt_confidence_baseline": 0.86,
        "translation_engine": "AI Neural Translation (Telugu -> EN)",
        "acoustic_notes": "Handles Telangana and Coastal Andhra cadence; code-mixed English tech words parsed via acoustic dictionary.",
        "sample_prompts": [
            "ఖమ్మం రూరల్ మండలంలో ప్రాథమిక ఆరోగ్య కేంద్రంలో అత్యవసర వైద్యులు మరియు మందులు లేక రోగులు ఇబ్బంది పడుతున్నారు.",
            "వరంగల్ సమీపంలోని గ్రామాల్లో ప్రధాన రహదారి గుంతలమయమై రవాణా స్తంభించింది. వెంటనే బీటీ రోడ్డు వేయాలి.",
            "నిజామాబాద్ జిల్లాలో తాగునీటి సరఫరా మోటార్లు పాడై మూడు వారాలుగా ప్రజలు తీవ్ర ఇబ్బందులు ఎదుర్కొంటున్నారు."
        ]
    },
    "bn": {
        "code": "bn",
        "name": "Bengali",
        "native_name": "বাংলা",
        "script": "Bengali",
        "font_family": "'Noto Sans Bengali', 'Vrinda', sans-serif",
        "text_direction": "ltr",
        "stt_confidence_baseline": 0.88,
        "translation_engine": "AI Neural Translation (Bengali -> EN)",
        "acoustic_notes": "Strong phoneme coverage; handles Rarh and Varendra regional phonetics gracefully.",
        "sample_prompts": [
            "মুর্শিদাবাদ জেলার ভগবানগোলা ব্লকে স্বাস্থ্যকেন্দ্রে চিকিৎসক নেই এবং পানীয় জলের পাইপলাইন নষ্ট হয়ে গেছে।",
            "উত্তর ২৪ পরগনা গ্রামীণ প্রাথমিক বিদ্যালয়ে ছাদ ভেঙে জল পড়ছে, প্রায় ২৫০ ছাত্রছাত্রী চরম সমস্যায়।",
            "হাওড়া গ্রামীণ অঞ্চলে ড্রেনেজ ব্যবস্থা ভেঙে পড়ে রাস্তায় নর্দমার জল জমছে, ডেঙ্গুর প্রকোপ বাড়ছে।"
        ]
    }
}
