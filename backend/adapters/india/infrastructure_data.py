"""
Infrastructure Index Data (Synthetic / Composite SDI Index)
Represents Sector Development Index (0 to 100) across 6 sectors.
Scores < 50 indicate acute deficits; 50-70 moderate; > 70 satisfactory.
"""

INFRASTRUCTURE_DATA = [
    # Kalaburagi (Acute deficit in Water & Sanitation and Healthcare)
    {"state": "Karnataka", "district": "Kalaburagi", "sector": "water_sanitation", "score": 38.5, "coverage_desc": "Only 34% functional household tap connection; frequent summer drying", "year": 2024},
    {"state": "Karnataka", "district": "Kalaburagi", "sector": "roads_transport", "score": 52.0, "coverage_desc": "State Highway connected; 43% rural habitations lack all-weather road", "year": 2024},
    {"state": "Karnataka", "district": "Kalaburagi", "sector": "primary_healthcare", "score": 44.0, "coverage_desc": "PHC doctor vacancy at 38%; maternal bed deficit in taluk hospitals", "year": 2024},
    {"state": "Karnataka", "district": "Kalaburagi", "sector": "school_education", "score": 55.0, "coverage_desc": "Pupil-teacher ratio 34:1; 28% schools require roof reconstruction", "year": 2024},
    {"state": "Karnataka", "district": "Kalaburagi", "sector": "rural_electrification", "score": 62.0, "coverage_desc": "7-hour single-phase agricultural supply; transformer burn rate 14%", "year": 2024},
    {"state": "Karnataka", "district": "Kalaburagi", "sector": "digital_connectivity", "score": 58.0, "coverage_desc": "BharatNet gram panchayat uptime 61%; 4G dead zones in 32 villages", "year": 2024},

    # Belagavi
    {"state": "Karnataka", "district": "Belagavi", "sector": "water_sanitation", "score": 64.0, "coverage_desc": "Krishna basin canals functional; summer shortages in hilly taluks", "year": 2024},
    {"state": "Karnataka", "district": "Belagavi", "sector": "roads_transport", "score": 46.5, "coverage_desc": "Heavy agricultural sugarcane truck transit causing chronic potholes", "year": 2024},
    {"state": "Karnataka", "district": "Belagavi", "sector": "primary_healthcare", "score": 68.0, "coverage_desc": "District civil hospital well-equipped; PHC coverage moderate", "year": 2024},
    {"state": "Karnataka", "district": "Belagavi", "sector": "school_education", "score": 71.0, "coverage_desc": "Good enrollment; bilingual border schools well supported", "year": 2024},
    {"state": "Karnataka", "district": "Belagavi", "sector": "rural_electrification", "score": 69.0, "coverage_desc": "Stable feeder network; sporadic distribution losses", "year": 2024},
    {"state": "Karnataka", "district": "Belagavi", "sector": "digital_connectivity", "score": 66.0, "coverage_desc": "CSC network active in 82% gram panchayats", "year": 2024},

    # Shivamogga (Monsoon road degradation)
    {"state": "Karnataka", "district": "Shivamogga", "sector": "water_sanitation", "score": 72.0, "coverage_desc": "Abundant water sources; distribution pipe maintenance required", "year": 2024},
    {"state": "Karnataka", "district": "Shivamogga", "sector": "roads_transport", "score": 45.0, "coverage_desc": "Western ghats heavy rainfall degrades culverts and asphalt yearly", "year": 2024},
    {"state": "Karnataka", "district": "Shivamogga", "sector": "primary_healthcare", "score": 74.0, "coverage_desc": "Medical college hospital accessible; rural mobile clinics functional", "year": 2024},
    {"state": "Karnataka", "district": "Shivamogga", "sector": "school_education", "score": 79.0, "coverage_desc": "High literacy; modern science labs in 65% secondary schools", "year": 2024},
    {"state": "Karnataka", "district": "Shivamogga", "sector": "rural_electrification", "score": 70.0, "coverage_desc": "Sharavathi hydro proximity; feeder lines affected by forest falls", "year": 2024},
    {"state": "Karnataka", "district": "Shivamogga", "sector": "digital_connectivity", "score": 62.0, "coverage_desc": "Optical fiber deployment constrained by forest clearances", "year": 2024},

    # Bengaluru Urban
    {"state": "Karnataka", "district": "Bengaluru Urban", "sector": "water_sanitation", "score": 58.0, "coverage_desc": "Cauvery Stage V commissioning ongoing; periphery relies on tankers", "year": 2024},
    {"state": "Karnataka", "district": "Bengaluru Urban", "sector": "roads_transport", "score": 54.0, "coverage_desc": "Metro expansion underway; severe arterial traffic bottlenecks", "year": 2024},
    {"state": "Karnataka", "district": "Bengaluru Urban", "sector": "primary_healthcare", "score": 85.0, "coverage_desc": "Tertiary super-specialty density highest in state; PHC crowding", "year": 2024},
    {"state": "Karnataka", "district": "Bengaluru Urban", "sector": "school_education", "score": 88.0, "coverage_desc": "Comprehensive private and government institutions", "year": 2024},
    {"state": "Karnataka", "district": "Bengaluru Urban", "sector": "rural_electrification", "score": 89.0, "coverage_desc": "BESCOM automated distribution; underground cabling", "year": 2024},
    {"state": "Karnataka", "district": "Bengaluru Urban", "sector": "digital_connectivity", "score": 94.0, "coverage_desc": "5G ubiquitous; municipal e-governance 99% digitized", "year": 2024},

    # Murshidabad (Acute deficit in Primary Healthcare & Water)
    {"state": "West Bengal", "district": "Murshidabad", "sector": "water_sanitation", "score": 41.0, "coverage_desc": "Arsenic contamination in shallow aquifers; pipeline gaps in 45% villages", "year": 2024},
    {"state": "West Bengal", "district": "Murshidabad", "sector": "roads_transport", "score": 53.0, "coverage_desc": "National Highway links; rural embankment roads vulnerable to flood", "year": 2024},
    {"state": "West Bengal", "district": "Murshidabad", "sector": "primary_healthcare", "score": 39.0, "coverage_desc": "Doctor-to-population ratio 1:3200; neonatal care centers overcrowded", "year": 2024},
    {"state": "West Bengal", "district": "Murshidabad", "sector": "school_education", "score": 52.0, "coverage_desc": "High student density; classroom-pupil ratio exceeds 1:55", "year": 2024},
    {"state": "West Bengal", "district": "Murshidabad", "sector": "rural_electrification", "score": 64.0, "coverage_desc": "Grid connectivity broad; low voltage complaints in irrigation season", "year": 2024},
    {"state": "West Bengal", "district": "Murshidabad", "sector": "digital_connectivity", "score": 54.0, "coverage_desc": "Gram panchayat connectivity 58%; digital ration authentication hiccups", "year": 2024},

    # Varanasi (Drainage & Tourism Roads backlog)
    {"state": "Uttar Pradesh", "district": "Varanasi", "sector": "water_sanitation", "score": 48.0, "coverage_desc": "Old city drainage overload; sewer revamp underway under Namami Gange", "year": 2024},
    {"state": "Uttar Pradesh", "district": "Varanasi", "sector": "roads_transport", "score": 59.0, "coverage_desc": "Ring road modern; dense historic ward lanes suffer severe congestion", "year": 2024},
    {"state": "Uttar Pradesh", "district": "Varanasi", "sector": "primary_healthcare", "score": 72.0, "coverage_desc": "BHU medical institute central hub; rural CHCs upgraded recently", "year": 2024},
    {"state": "Uttar Pradesh", "district": "Varanasi", "sector": "school_education", "score": 68.0, "coverage_desc": "Operation Kayakal renovated 80% primary school structures", "year": 2024},
    {"state": "Uttar Pradesh", "district": "Varanasi", "sector": "rural_electrification", "score": 71.0, "coverage_desc": "Smart meters installed in urban areas; rural feeder separation done", "year": 2024},
    {"state": "Uttar Pradesh", "district": "Varanasi", "sector": "digital_connectivity", "score": 75.0, "coverage_desc": "Integrated Command & Control Centre active; 4G across district", "year": 2024},

    # Khammam (Healthcare and School Infra deficit)
    {"state": "Telangana", "district": "Khammam", "sector": "water_sanitation", "score": 66.0, "coverage_desc": "Mission Bhagiratha piped supply to 85% habitations", "year": 2024},
    {"state": "Telangana", "district": "Khammam", "sector": "roads_transport", "score": 57.0, "coverage_desc": "Coal mining belt heavy vehicle transit requires continuous resurfacing", "year": 2024},
    {"state": "Telangana", "district": "Khammam", "sector": "primary_healthcare", "score": 43.5, "coverage_desc": "Tribal agency areas face seasonal malaria; specialist doctor shortage", "year": 2024},
    {"state": "Telangana", "district": "Khammam", "sector": "school_education", "score": 58.0, "coverage_desc": "Mana Ooru Mana Badi upgraded phase 1; phase 2 schools waiting", "year": 2024},
    {"state": "Telangana", "district": "Khammam", "sector": "rural_electrification", "score": 82.0, "coverage_desc": "24x7 free agricultural power scheme; stable distribution", "year": 2024},
    {"state": "Telangana", "district": "Khammam", "sector": "digital_connectivity", "score": 68.0, "coverage_desc": "T-Fiber broadband deployed to 70% gram panchayats", "year": 2024},

    # Madurai (Water and Urban Drainage backlog)
    {"state": "Tamil Nadu", "district": "Madurai", "sector": "water_sanitation", "score": 51.0, "coverage_desc": "Vaigai reservoir dependency; peri-urban areas face alternating supply", "year": 2024},
    {"state": "Tamil Nadu", "district": "Madurai", "sector": "roads_transport", "score": 67.0, "coverage_desc": "Well-connected state highways; ring road maintenance on schedule", "year": 2024},
    {"state": "Tamil Nadu", "district": "Madurai", "sector": "primary_healthcare", "score": 78.0, "coverage_desc": "Government Rajaji Hospital regional powerhouse; rural PHCs functional", "year": 2024},
    {"state": "Tamil Nadu", "district": "Madurai", "sector": "school_education", "score": 76.0, "coverage_desc": "Perasiriyar Anbazhagan school development scheme active", "year": 2024},
    {"state": "Tamil Nadu", "district": "Madurai", "sector": "rural_electrification", "score": 84.0, "coverage_desc": "TANGEDCO substation coverage extensive", "year": 2024},
    {"state": "Tamil Nadu", "district": "Madurai", "sector": "digital_connectivity", "score": 76.0, "coverage_desc": "TANFINET optical rollout progressing across rural blocks", "year": 2024}
]
