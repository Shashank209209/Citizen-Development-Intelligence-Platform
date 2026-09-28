"""
Seed Script — populates the SQLite database with synthetic/demo data.
All data is explicitly labeled as synthetic. No real citizen PII is stored.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from backend.database.connection import engine, SessionLocal, init_db
from backend.database.models import (
    GeographyModel, DemographicsModel, InfrastructureModel,
    InvestmentPlanModel, HotspotModel, RecommendationModel,
    CitizenRequestModel, AuditLogModel, DatasetRegistryModel
)
from backend.adapters.india.geo_data import STATES_AND_DISTRICTS
from backend.adapters.india.demographics_data import DEMOGRAPHICS
from backend.adapters.india.infrastructure_data import INFRASTRUCTURE_DATA
from backend.adapters.india.investment_plans_data import INVESTMENT_PLANS
from backend.core.analytics_engine import analytics_engine
import uuid, datetime, random

def seed_all():
    print("[SEED] Initializing database schema...")
    init_db()
    db = SessionLocal()

    print("[SEED] Clearing existing demo data...")
    for Model in [CitizenRequestModel, HotspotModel, RecommendationModel,
                  AuditLogModel, GeographyModel, DemographicsModel,
                  InfrastructureModel, InvestmentPlanModel, DatasetRegistryModel]:
        db.query(Model).delete()
    db.commit()

    # --- Geography ---
    print("[SEED] Seeding geography...")
    for g in STATES_AND_DISTRICTS:
        db.add(GeographyModel(**g))
    db.commit()

    # --- Demographics ---
    print("[SEED] Seeding demographics...")
    for d in DEMOGRAPHICS:
        db.add(DemographicsModel(**d))
    db.commit()

    # --- Infrastructure ---
    print("[SEED] Seeding infrastructure indices...")
    for i in INFRASTRUCTURE_DATA:
        db.add(InfrastructureModel(**i))
    db.commit()

    # --- Investment Plans ---
    print("[SEED] Seeding investment plans...")
    for p in INVESTMENT_PLANS:
        db.add(InvestmentPlanModel(**p))
    db.commit()

    # --- Dataset Registry ---
    print("[SEED] Registering datasets...")
    registries = [
        DatasetRegistryModel(
            id="DSREG-001",
            name="India District Demographics (Synthetic 2024)",
            source="Synthetic generation aligned with Census 2011 + NFHS-5 trend projections",
            date="2024-01-01",
            license="CC0 1.0 Universal (Public Domain)",
            geographic_level="District",
            limitations="Synthetic data. Does not represent official census counts. Values used for demonstration of DPG analytics pipeline only.",
            is_synthetic=True
        ),
        DatasetRegistryModel(
            id="DSREG-002",
            name="Sector Development Index (SDI) — Infrastructure Baseline (Synthetic)",
            source="Composite index derived from NITI Aayog AISD methodology, MIS data patterns, and GovTech benchmarks",
            date="2024-06-01",
            license="CC0 1.0 Universal (Public Domain)",
            geographic_level="District × Sector",
            limitations="Synthetic composite index for hackathon/DPG prototype only. Not affiliated with MoRD, NITI Aayog or any official body.",
            is_synthetic=True
        ),
        DatasetRegistryModel(
            id="DSREG-003",
            name="Public Investment Plans (Synthetic — State Scheme Aligned)",
            source="Synthetic plans modeled after PMGSY, JJM, AMRUT, Ayushman Bharat scheme structures",
            date="2024-09-01",
            license="CC0 1.0 Universal (Public Domain)",
            geographic_level="District",
            limitations="Not linked to any live government MIS or e-procurement portal.",
            is_synthetic=True
        ),
        DatasetRegistryModel(
            id="DSREG-004",
            name="Citizen Demand Corpus (Synthetic — Multi-Language Demo)",
            source="Hand-authored synthetic civic grievance samples in 6 Indian languages",
            date="2024-09-15",
            license="Apache-2.0",
            geographic_level="District-level simulated civic intake",
            limitations="Fictional citizen voices. Used solely for NLP pipeline validation and DPG demonstration.",
            is_synthetic=True
        )
    ]
    for reg in registries:
        db.add(reg)
    db.commit()

    # --- Citizen Requests (synthetic seeded) ---
    print("[SEED] Seeding 48 synthetic citizen demand requests...")
    seed_requests = [
        # Karnataka - Kalaburagi - water (CRITICAL hotspot)
        ("hi", "kn", "water_sanitation", "Kalaburagi", "Karnataka", "High", "ಕಲಬುರಗಿ ತಾಲೂಕಿನ ಆಳಂದ ರಸ್ತೆ ಹಳ್ಳಿಗಳಲ್ಲಿ ಕುಡಿಯುವ ನೀರಿನ ಕೊಳವೆ ಒಡೆದಿದೆ", "Drinking water pipe broken in Aland Road villages, Kalaburagi. No water for 15 days.", 17.3297, 76.8343),
        ("kn", "kn", "water_sanitation", "Kalaburagi", "Karnataka", "High", "ನೀರಿನ ಪೈಪ್ ಒಡೆದಿದ್ದು ನಮ್ಮ ಊರಿನಲ್ಲಿ 2 ವಾರದಿಂದ ನೀರಿಲ್ಲ", "Water supply completely cut for 2 weeks in our village, Kalaburagi rural.", 17.33, 76.84),
        ("kn", "kn", "water_sanitation", "Kalaburagi", "Karnataka", "High", "ಕಲಬುರಗಿ ನಗರದ ಹೊರ ವಲಯದಲ್ಲಿ ನೀರಿನ ಸಮಸ್ಯೆ ತೀವ್ರವಾಗಿದೆ", "Severe drinking water shortage in Kalaburagi outskirts — 2,000 households affected.", 17.34, 76.82),
        ("en", "en", "water_sanitation", "Kalaburagi", "Karnataka", "High", "Water pipeline broken for 12 days in village near Kalaburagi", "Frequent drinking water pipeline leakages in Kalaburagi rural ward 4. Over 2,000 households without clean water.", 17.32, 76.85),
        ("kn", "kn", "water_sanitation", "Kalaburagi", "Karnataka", "High", "ಕುಡಿಯುವ ನೀರಿಲ್ಲ, ಮಹಿಳೆಯರು ದೂರದ ಬಾವಿ ಹೋಗಬೇಕಾಗಿದೆ", "Women walking 4km to fetch water from wells, Kalaburagi block.", 17.35, 76.80),

        # Karnataka - Belagavi - roads
        ("kn", "kn", "roads_transport", "Belagavi", "Karnataka", "Medium", "ಬೆಳಗಾವಿ ಸಕ್ಕರೆ ಕಾರ್ಖಾನೆ ರಸ್ತೆ ಗಂಭೀರ ರೀತಿ ಹಾಳಾಗಿದೆ", "Road near Belagavi sugar factory severely potholed, ambulances delayed.", 15.85, 74.50),
        ("en", "en", "roads_transport", "Belagavi", "Karnataka", "Medium", "Potholes on state highway 28 near Belagavi market causing accidents daily", "Dangerous potholes on state highway 28 near Belagavi agricultural market.", 15.84, 74.49),
        ("kn", "kn", "roads_transport", "Belagavi", "Karnataka", "Medium", "ಹುಕ್ಕೇರಿ ತಾಲೂಕಿನ ರಸ್ತೆ ಸ್ಥಿತಿ ಅಸಹ್ಯ", "Hukkeri taluk roads in deplorable state, no proper culverts.", 15.87, 74.55),

        # West Bengal - Murshidabad - healthcare (CRITICAL)
        ("bn", "bn", "primary_healthcare", "Murshidabad", "West Bengal", "High", "মুর্শিদাবাদ জেলার ভগবানগোলা ব্লকে স্বাস্থ্যকেন্দ্রে চিকিৎসক নেই", "No doctors at Bhagwangola health centre, Murshidabad for over 2 months.", 24.18, 88.27),
        ("bn", "bn", "primary_healthcare", "Murshidabad", "West Bengal", "High", "মুর্শিদাবাদ গ্রামীণ হাসপাতালে প্রসূতি বিভাগে জায়গা নেই", "Maternity ward in Murshidabad district hospital at full capacity — women turned away.", 24.19, 88.26),
        ("en", "en", "primary_healthcare", "Murshidabad", "West Bengal", "High", "Primary health centre in Murshidabad lacks emergency oxygen and maternal care", "PHC in Bhagwangola block has no oxygen supply and no gynecologist on duty.", 24.17, 88.28),
        ("bn", "bn", "primary_healthcare", "Murshidabad", "West Bengal", "High", "ডাক্তার নেই, ওষুধ নেই, অ্যাম্বুলেন্স নেই — মুর্শিদাবাদ ব্লক হেলথ সেন্টার", "No doctor, no medicine, no ambulance at Murshidabad block health centre.", 24.16, 88.29),
        ("bn", "bn", "primary_healthcare", "Murshidabad", "West Bengal", "High", "লালগোলা ব্লকে প্রসূতি মৃত্যু বৃদ্ধি পাচ্ছে, তাৎক্ষণিক চিকিৎসা দরকার", "Maternal mortality rising in Lalgola block, Murshidabad — emergency obstetric care required.", 24.20, 88.25),

        # UP - Varanasi - water/sanitation
        ("hi", "hi", "water_sanitation", "Varanasi", "Uttar Pradesh", "High", "वाराणसी के शिवपुर ब्लॉक में सड़क पूरी तरह टूट चुकी है", "Main road in Shivpur block, Varanasi is completely broken. Emergency vehicles delayed.", 25.32, 82.97),
        ("hi", "hi", "water_sanitation", "Varanasi", "Uttar Pradesh", "Medium", "गंगा किनारे के मोहल्लों में नाला उफान मार रहा है", "Drainage overflowing in Ganga riverside localities in Varanasi — dengue risk.", 25.33, 82.98),
        ("hi", "hi", "roads_transport", "Varanasi", "Uttar Pradesh", "Medium", "वाराणसी पुराने शहर में संकरी सड़कों पर गड्ढे हैं", "Old city narrow lanes in Varanasi have severe potholes and broken footpaths.", 25.31, 82.96),

        # UP - Lucknow - school
        ("hi", "hi", "school_education", "Lucknow", "Uttar Pradesh", "Medium", "लखनऊ के काकोरी प्राथमिक विद्यालय में पीने के पानी की किल्लत", "No drinking water at Kakori primary school, Lucknow — 300 children affected.", 26.85, 80.95),
        ("hi", "hi", "school_education", "Lucknow", "Uttar Pradesh", "Medium", "काकोरी स्कूल की छत से पानी टपकता है", "School classroom roof leaking in Kakori, Lucknow — students unable to sit during rains.", 26.84, 80.94),

        # Tamil Nadu - Madurai - water
        ("ta", "ta", "water_sanitation", "Madurai", "Tamil Nadu", "High", "மதுரை புறநகர் பகுதியில் குழாய் நீர் வராது", "No piped water in Madurai suburban locality for 10 days — 500 families at risk.", 9.93, 78.12),
        ("ta", "ta", "water_sanitation", "Madurai", "Tamil Nadu", "High", "மதுரை மாவட்டத்தில் குடிநீர் குழாய் உடைந்துள்ளது", "Water pipeline broken and sewage mixing in Madurai outskirts.", 9.92, 78.11),
        ("en", "en", "water_sanitation", "Madurai", "Tamil Nadu", "Medium", "Madurai suburban locality running dry — 10 days no tap water supply", "Drinking water supply disrupted for 10 days in Madurai rural blocks.", 9.94, 78.13),

        # Tamil Nadu - Tiruchirappalli - water
        ("ta", "ta", "water_sanitation", "Tiruchirappalli", "Tamil Nadu", "High", "திருச்சிராப்பள்ளி திருவெறும்பூர் பகுதியில் குடிநீர் குழாய் உடைந்து கழிவுநீர் கலக்கிறது", "Broken water pipeline mixing with sewage in Thiruverumbur, Tiruchirappalli. 500 families affected.", 10.79, 78.70),
        ("ta", "ta", "primary_healthcare", "Madurai", "Tamil Nadu", "High", "மதுரை ஆரம்ப சுகாதார நிலையத்தில் மருந்து தட்டுப்பாடு", "Medicine stockout at Madurai PHC — diabetics and hypertensives facing acute shortage.", 9.91, 78.10),

        # Telangana - Khammam - healthcare
        ("te", "te", "primary_healthcare", "Khammam", "Telangana", "High", "ఖమ్మం రూరల్ మండలంలో ప్రాథమిక ఆరోగ్య కేంద్రంలో వైద్యులు లేరు", "No emergency doctors at Khammam rural mandal health centre. Patients suffering.", 17.25, 80.15),
        ("te", "te", "primary_healthcare", "Khammam", "Telangana", "High", "ఖమ్మం గిరిజన ఏజెన్సీ ప్రాంతంలో మలేరియా వ్యాప్తి చెందుతోంది", "Malaria spreading in Khammam tribal agency area — no medicines at local PHC.", 17.24, 80.14),
        ("en", "en", "primary_healthcare", "Khammam", "Telangana", "High", "Khammam rural PHC lacks doctors and emergency medicine since 3 months", "Emergency specialists absent for 3 months at Khammam rural PHC.", 17.26, 80.16),

        # Telangana - Warangal - roads
        ("te", "te", "roads_transport", "Warangal", "Telangana", "Medium", "వరంగల్ సమీపంలో రహదారి గుంతలమయమై రవాణా స్తంభించింది", "Main arterial road near Warangal severely potholed, transport disrupted.", 17.97, 79.59),
        ("te", "te", "roads_transport", "Warangal", "Telangana", "Medium", "వరంగల్ గ్రామాల్లో వ్యవసాయ రోడ్లు దెబ్బతిన్నాయి", "Agricultural approach roads in Warangal villages damaged, farmers unable to transport produce.", 17.96, 79.58),

        # Telangana - Nizamabad - water
        ("te", "te", "water_sanitation", "Nizamabad", "Telangana", "High", "నిజామాబాద్ జిల్లాలో తాగునీటి సరఫరా మోటార్లు పాడయ్యాయి", "Drinking water pump motors burnt in Nizamabad district — 3 weeks no supply.", 18.67, 78.09),

        # West Bengal - Howrah - sanitation
        ("bn", "bn", "water_sanitation", "Howrah", "West Bengal", "High", "హaowrah গ্রামীণ অঞ্চলে ড্রেনেজ ব্যবস্থা ভেঙে পড়েছে", "Drainage collapsed in Howrah rural area — sewage flooding streets and dengue rising.", 22.60, 88.26),
        ("bn", "bn", "water_sanitation", "Howrah", "West Bengal", "High", "হাওড়া ব্লকে নর্দমার জল রাস্তায় জমছে", "Sewage water stagnating on roads in Howrah block — serious health hazard.", 22.59, 88.27),

        # West Bengal - North 24 Parganas - school
        ("bn", "bn", "school_education", "North 24 Parganas", "West Bengal", "Medium", "উত্তর ২৪ পরগনা গ্রামীণ বিদ্যালয়ের ছাদ ভেঙে জল পড়ছে", "School roof collapsed in North 24 Parganas rural — 250 students affected.", 22.72, 88.48),
        ("bn", "bn", "school_education", "North 24 Parganas", "West Bengal", "Medium", "স্কুলে পানীয় জলের ব্যবস্থা নেই", "No drinking water facility at government school in North 24 Parganas.", 22.71, 88.47),

        # Karnataka - Shivamogga - roads
        ("kn", "kn", "roads_transport", "Shivamogga", "Karnataka", "Medium", "ಶಿವಮೊಗ್ಗ ಗ್ರಾಮೀಣ ಭಾಗದಲ್ಲಿ ಮಳೆಗಾಲದ ರಸ್ತೆ ಹಾಳಾಗಿದೆ", "Monsoon rains damaged rural roads in Shivamogga — bus transit halted.", 13.93, 75.57),

        # Tamil Nadu - Salem - school
        ("ta", "ta", "school_education", "Salem", "Tamil Nadu", "Medium", "சேலம் கிராமப்புற பள்ளியில் வகுப்பறை கூரை சேதமடைந்துள்ளது", "Classroom roof damaged in Salem rural school — rain disrupts classes.", 11.66, 78.15),

        # Digital connectivity examples
        ("en", "en", "digital_connectivity", "Kalaburagi", "Karnataka", "Low", "BharatNet fiber down in 32 villages near Kalaburagi for 3 weeks", "BharatNet optical fiber offline in 32 gram panchayats, Kalaburagi — CSC services unavailable.", 17.31, 76.83),
        ("kn", "kn", "digital_connectivity", "Belagavi", "Karnataka", "Low", "ಬೆಳಗಾವಿ ಹಳ್ಳಿಗಳಲ್ಲಿ ಮೊಬೈಲ್ ನೆಟ್‌ವರ್ಕ್ ಸಿಗ್ನಲ್ ಇಲ್ಲ", "No mobile network signal in Belagavi rural hamlets — digital banking inaccessible.", 15.86, 74.52),

        # UP - Prayagraj - roads
        ("hi", "hi", "roads_transport", "Prayagraj", "Uttar Pradesh", "Medium", "प्रयागराज के ग्रामीण इलाकों में सड़कें टूटी हुई हैं", "Village roads in Prayagraj rural broken — school children and farmers face hardship daily.", 25.44, 81.85),

        # Electrification
        ("te", "te", "rural_electrification", "Nizamabad", "Telangana", "Medium", "నిజామాబాద్ లో వ్యవసాయ ట్రాన్స్‌ఫార్మర్లు కాలిపోతున్నాయి", "Agricultural transformers burning out repeatedly in Nizamabad — 6 burnt this month alone.", 18.68, 78.10),
        ("hi", "hi", "rural_electrification", "Varanasi", "Uttar Pradesh", "Low", "वाराणसी के गांवों में बिजली 8 घंटे से ज्यादा नहीं मिलती", "Villages in Varanasi getting barely 8 hours electricity — agricultural pumps failing.", 25.30, 82.97),

        # More from Murshidabad
        ("bn", "bn", "water_sanitation", "Murshidabad", "West Bengal", "High", "মুর্শিদাবাদে আর্সেনিক দূষিত জল পান করতে বাধ্য হচ্ছেন গ্রামবাসী", "Villagers in Murshidabad drinking arsenic-contaminated groundwater — safe supply pipeline broken.", 24.15, 88.26),
        ("bn", "bn", "water_sanitation", "Murshidabad", "West Bengal", "High", "জলের পাইপলাইন ভেঙে গেছে — মুর্শিদাবাদ গ্রামীণ এলাকায় খাওয়ার জল নেই", "Water pipeline broken in Murshidabad rural — no potable water in 8 villages.", 24.16, 88.27),

        # Additional Kalaburagi (to demonstrate CRITICAL hotspot clustering)
        ("kn", "kn", "water_sanitation", "Kalaburagi", "Karnataka", "High", "ಕಲಬುರಗಿ ಹಳ್ಳಿಗಳಲ್ಲಿ ಕೊಳವೆ ಬಾವಿ ಕೈ ಕೊಟ್ಟಿದೆ", "Borewells defunct in 7 Kalaburagi villages — water hauled in tankers at high cost.", 17.34, 76.82),
        ("kn", "kn", "primary_healthcare", "Kalaburagi", "Karnataka", "High", "ಕಲಬುರಗಿ PHC ದಲ್ಲಿ 3 ತಿಂಗಳಿಂದ ಡಾಕ್ಟರ್ ಇಲ್ಲ", "No doctor at Kalaburagi PHC for 3 months — patients travel 60km for care.", 17.33, 76.83),
    ]

    tracking_codes = []
    for i, (orig_lang, det_lang, category, district, state, urgency, orig_text, trans_text, lat, lng) in enumerate(seed_requests):
        code = f"CRQ-{str(uuid.uuid4()).upper()[:8]}"
        tracking_codes.append(code)
        req = CitizenRequestModel(
            tracking_code=code,
            channel=random.choice(["web_form", "messaging_chat", "voice_audio", "web_form", "web_form"]),
            original_language=orig_lang,
            original_text=orig_text,
            original_script="Devanagari" if orig_lang == "hi" else "Kannada" if orig_lang == "kn" else "Bengali" if orig_lang == "bn" else "Tamil" if orig_lang == "ta" else "Telugu" if orig_lang == "te" else "Latin",
            translated_text=trans_text,
            category_id=category,
            category_name={"water_sanitation": "Water & Sanitation", "roads_transport": "Roads & Rural Connectivity",
                           "primary_healthcare": "Primary Healthcare", "school_education": "Public School Education",
                           "rural_electrification": "Rural Electrification & Power", "digital_connectivity": "Digital Connectivity & CSC"}.get(category, category),
            extracted_location_text=district,
            state=state,
            district=district,
            lat=lat,
            lng=lng,
            urgency_level=urgency,
            urgency_rationale="Immediate safety or health risk" if urgency == "High" else "Routine maintenance",
            affected_population="1,500 - 3,000 residents",
            summary_for_policymaker=f"{category.replace('_', ' ').title()} demand in {district}, {state}. Urgency: {urgency}.",
            language_confidence=random.uniform(0.88, 0.99),
            stt_confidence=random.uniform(0.82, 0.97),
            translation_confidence=random.uniform(0.85, 0.98),
            category_confidence=random.uniform(0.85, 0.97),
            location_confidence=random.uniform(0.82, 0.96),
            status="LINKED_TO_HOTSPOT",
            corrections_history=[],
            created_at=datetime.datetime(2024, random.randint(7, 9), random.randint(1, 28), random.randint(6, 22), 0)
        )
        db.add(req)
    db.commit()
    print(f"[SEED] Seeded {len(seed_requests)} citizen requests.")

    # --- Hotspots (computed from demand clusters) ---
    print("[SEED] Seeding hotspots...")
    hotspot_definitions = [
        {"id": "HS-KA-KLB-WATER", "state": "Karnataka", "district": "Kalaburagi", "sector_id": "water_sanitation", "sector_name": "Water & Sanitation", "demand_volume": 87, "persistence_score": 0.92, "lat": 17.3297, "lng": 76.8343, "trend": "ACCELERATING"},
        {"id": "HS-WB-MSD-HEALTH", "state": "West Bengal", "district": "Murshidabad", "sector_id": "primary_healthcare", "sector_name": "Primary Healthcare", "demand_volume": 74, "persistence_score": 0.88, "lat": 24.1837, "lng": 88.2718, "trend": "ACCELERATING"},
        {"id": "HS-TG-KHM-HEALTH", "state": "Telangana", "district": "Khammam", "sector_id": "primary_healthcare", "sector_name": "Primary Healthcare", "demand_volume": 63, "persistence_score": 0.82, "lat": 17.2473, "lng": 80.1514, "trend": "STABLE"},
        {"id": "HS-KA-BLG-ROADS", "state": "Karnataka", "district": "Belagavi", "sector_id": "roads_transport", "sector_name": "Roads & Rural Connectivity", "demand_volume": 58, "persistence_score": 0.79, "lat": 15.8497, "lng": 74.4977, "trend": "STABLE"},
        {"id": "HS-TN-MDU-WATER", "state": "Tamil Nadu", "district": "Madurai", "sector_id": "water_sanitation", "sector_name": "Water & Sanitation", "demand_volume": 51, "persistence_score": 0.75, "lat": 9.9252, "lng": 78.1198, "trend": "STABLE"},
        {"id": "HS-UP-VNS-WATER", "state": "Uttar Pradesh", "district": "Varanasi", "sector_id": "water_sanitation", "sector_name": "Water & Sanitation", "demand_volume": 47, "persistence_score": 0.72, "lat": 25.3176, "lng": 82.9739, "trend": "DECLINING"},
        {"id": "HS-WB-MSD-WATER", "state": "West Bengal", "district": "Murshidabad", "sector_id": "water_sanitation", "sector_name": "Water & Sanitation", "demand_volume": 42, "persistence_score": 0.80, "lat": 24.18, "lng": 88.27, "trend": "ACCELERATING"},
        {"id": "HS-TG-WRG-ROADS", "state": "Telangana", "district": "Warangal", "sector_id": "roads_transport", "sector_name": "Roads & Rural Connectivity", "demand_volume": 39, "persistence_score": 0.68, "lat": 17.9689, "lng": 79.5941, "trend": "STABLE"},
        {"id": "HS-WB-HWR-WATER", "state": "West Bengal", "district": "Howrah", "sector_id": "water_sanitation", "sector_name": "Water & Sanitation", "demand_volume": 35, "persistence_score": 0.70, "lat": 22.5958, "lng": 88.2636, "trend": "STABLE"},
        {"id": "HS-UP-LKO-SCHOOL", "state": "Uttar Pradesh", "district": "Lucknow", "sector_id": "school_education", "sector_name": "Public School Education", "demand_volume": 30, "persistence_score": 0.60, "lat": 26.8467, "lng": 80.9462, "trend": "DECLINING"},
    ]

    for hs in hotspot_definitions:
        scoring = analytics_engine.compute_prioritization(
            demand_volume=hs["demand_volume"],
            persistence_score=hs["persistence_score"],
            district=hs["district"],
            state=hs["state"],
            sector_id=hs["sector_id"]
        )
        db.add(HotspotModel(
            id=hs["id"],
            state=hs["state"],
            district=hs["district"],
            sector_id=hs["sector_id"],
            sector_name=hs["sector_name"],
            demand_volume=hs["demand_volume"],
            persistence_score=hs["persistence_score"],
            priority_score=scoring["priority_score"],
            severity=scoring["severity"],
            lat=hs["lat"],
            lng=hs["lng"],
            trend=hs["trend"],
            supporting_indicators=scoring["factors"]
        ))
    db.commit()
    print(f"[SEED] Seeded {len(hotspot_definitions)} hotspots.")

    # --- Recommendations ---
    print("[SEED] Generating recommendations...")
    from backend.core.analytics_engine import analytics_engine as ae
    recs = ae.generate_recommendations(hotspot_definitions)
    for rec in recs[:8]:
        db.add(RecommendationModel(
            id=rec["id"],
            title=rec["title"],
            sector_id=rec["sector_id"],
            sector_name=rec["sector_name"],
            target_district=rec["district"],
            state=rec["state"],
            priority_score=rec["priority_score"],
            severity=rec["severity"],
            factor_breakdown=rec["factor_breakdown"],
            formula_output=rec["formula_output"],
            evidence_trail=rec["evidence_trail"],
            suggested_budget_cr_inr=rec["suggested_budget_range_cr_inr"],
            status="PROPOSED"
        ))
    db.commit()
    print(f"[SEED] Generated {min(8, len(recs))} recommendations.")

    db.close()
    print("\n[SEED] ✅ All synthetic data seeded successfully. Platform ready for demo.")
    print("[SEED] ⚠️  REMINDER: All datasets are synthetic/demo data. No real government or PII data included.")

if __name__ == "__main__":
    seed_all()
