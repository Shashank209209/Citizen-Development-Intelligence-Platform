"""
India Sector Taxonomy
Standardized development category definitions, subcategories, keywords,
and SDG alignment for Digital Public Infrastructure analytics.
"""

SECTORS = [
    {
        "id": "water_sanitation",
        "name": "Water & Sanitation",
        "icon": "Droplets",
        "sdg_alignment": "SDG 6: Clean Water and Sanitation",
        "subcategories": [
            "Drinking water pipeline leakage",
            "Borewell/handpump contamination",
            "Open drainage overflow",
            "Sewage treatment & public toilets",
            "Water supply timing & frequency"
        ],
        "keywords": ["water", "pipe", "pipeline", "drinking water", "drainage", "sewage", "leak", "borewell", "handpump", "toilet", "pani", "neeru", "tanni", "neellu", "jol", "nallah"]
    },
    {
        "id": "roads_transport",
        "name": "Roads & Rural Connectivity",
        "icon": "Route",
        "sdg_alignment": "SDG 9: Industry, Innovation and Infrastructure",
        "subcategories": [
            "Potholes & asphalt degradation",
            "Unpaved rural approach road",
            "Bridge/culvert repair",
            "Street lighting & road safety",
            "Public bus service frequency"
        ],
        "keywords": ["road", "pothole", "highway", "bridge", "culvert", "transport", "bus", "street light", "sadak", "raste", "salai", "daari", "rasta"]
    },
    {
        "id": "primary_healthcare",
        "name": "Primary Healthcare",
        "icon": "HeartPulse",
        "sdg_alignment": "SDG 3: Good Health and Well-being",
        "subcategories": [
            "PHC/CHC doctor absenteeism",
            "Emergency ambulance unavailability",
            "Medicine & vaccine stockouts",
            "Maternal & child health ward",
            "Diagnostic & blood testing facilities"
        ],
        "keywords": ["health", "hospital", "phc", "chc", "doctor", "ambulance", "medicine", "clinic", "swasthya", "arogya", "maruthuvamanai", "vaidya", "chikitsa"]
    },
    {
        "id": "school_education",
        "name": "Public School Education",
        "icon": "GraduationCap",
        "sdg_alignment": "SDG 4: Quality Education",
        "subcategories": [
            "Classroom roof & structural dilapidation",
            "Teacher vacancy in primary school",
            "Girls' toilet & clean drinking water",
            "Electricity & smart classroom equipment",
            "Mid-day meal quality & kitchen shed"
        ],
        "keywords": ["school", "education", "teacher", "classroom", "student", "shiksha", "vidyalaya", "shale", "palli", "badi", "bidyaloy"]
    },
    {
        "id": "rural_electrification",
        "name": "Rural Electrification & Power",
        "icon": "Zap",
        "sdg_alignment": "SDG 7: Affordable and Clean Energy",
        "subcategories": [
            "Frequent low voltage & power outages",
            "Burnt agricultural transformer replacement",
            "Hanging electric wires & safety hazard",
            "Feeder line maintenance",
            "Solar streetlights in hamlets"
        ],
        "keywords": ["electricity", "power", "transformer", "voltage", "outage", "bijli", "vidyut", "min", "karanthu", "biddut"]
    },
    {
        "id": "digital_connectivity",
        "name": "Digital Connectivity & CSC",
        "icon": "Wifi",
        "sdg_alignment": "SDG 9 & SDG 16: Effective, Accountable Institutions",
        "subcategories": [
            "BharatNet optical fiber link down",
            "Common Service Centre (CSC) overcharging/unavailability",
            "Mobile tower signal dead zone",
            "Ration card & DBT biometrics failure",
            "Digital land records kiosk access"
        ],
        "keywords": ["internet", "network", "csc", "mobile tower", "broadband", "fiber", "ration", "dbt", "biometric", "signal"]
    }
]
