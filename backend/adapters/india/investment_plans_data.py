"""
Public Investment Plans Data (Synthetic / State & Central Scheme Aligned)
Represents planned or approved capital budget outlays.
Used by the Development Gap Analysis engine:
Gap exists when Citizen Demand is High, Infrastructure Index is Low,
AND no active funded project exists for that district/sector!
"""

INVESTMENT_PLANS = [
    # Karnataka Plans
    {
        "plan_id": "INV-KA-001",
        "state": "Karnataka",
        "district": "Kalaburagi",
        "sector": "roads_transport",
        "project_name": "Kalyana Patha State Highway SH-19 Bypass Widening",
        "budget_cr_inr": 85.5,
        "timeline": "2024-2026",
        "status": "Under Construction",
        "scheme": "State Highway Development Project"
    },
    {
        "plan_id": "INV-KA-002",
        "state": "Karnataka",
        "district": "Bengaluru Urban",
        "sector": "water_sanitation",
        "project_name": "Cauvery Water Supply Scheme Stage V Periphery Piping",
        "budget_cr_inr": 450.0,
        "timeline": "2023-2025",
        "status": "Under Construction",
        "scheme": "BWSSB Mega Project"
    },
    {
        "plan_id": "INV-KA-003",
        "state": "Karnataka",
        "district": "Belagavi",
        "sector": "roads_transport",
        "project_name": "Sugar Belt Rural Freight Corridor Culvert Modernization",
        "budget_cr_inr": 42.0,
        "timeline": "2024-2025",
        "status": "Planned",
        "scheme": "PMGSY Phase IV"
    },
    {
        "plan_id": "INV-KA-004",
        "state": "Karnataka",
        "district": "Shivamogga",
        "sector": "school_education",
        "project_name": "Model Smart School Laboratories Cluster",
        "budget_cr_inr": 18.2,
        "timeline": "2024-2025",
        "status": "Approved",
        "scheme": "Samagra Shiksha Abhiyan"
    },

    # West Bengal Plans
    {
        "plan_id": "INV-WB-001",
        "state": "West Bengal",
        "district": "Murshidabad",
        "sector": "roads_transport",
        "project_name": "Ganga Embankment Protective Bund Road Upgradation",
        "budget_cr_inr": 62.0,
        "timeline": "2024-2026",
        "status": "Under Construction",
        "scheme": "Pathashree Prakalpa"
    },
    {
        "plan_id": "INV-WB-002",
        "state": "West Bengal",
        "district": "North 24 Parganas",
        "sector": "water_sanitation",
        "project_name": "Sundarbans Salinity Resistant Surface Water Filtration Plant",
        "budget_cr_inr": 115.0,
        "timeline": "2024-2027",
        "status": "Approved",
        "scheme": "Jal Jeevan Mission"
    },

    # Uttar Pradesh Plans
    {
        "plan_id": "INV-UP-001",
        "state": "Uttar Pradesh",
        "district": "Varanasi",
        "sector": "primary_healthcare",
        "project_name": "Rural Tele-Medicine and 5 CHC Diagnostic Modernization",
        "budget_cr_inr": 35.0,
        "timeline": "2024-2025",
        "status": "Under Construction",
        "scheme": "Ayushman Bharat Health Infrastructure Mission"
    },
    {
        "plan_id": "INV-UP-002",
        "state": "Uttar Pradesh",
        "district": "Lucknow",
        "sector": "water_sanitation",
        "project_name": "Gomti Drainage Interceptor Sewer Phase II",
        "budget_cr_inr": 180.0,
        "timeline": "2024-2026",
        "status": "Under Construction",
        "scheme": "AMRUT 2.0"
    },

    # Telangana Plans
    {
        "plan_id": "INV-TG-001",
        "state": "Telangana",
        "district": "Warangal",
        "sector": "roads_transport",
        "project_name": "Kakatiya Urban Development Authority Radial Road Link",
        "budget_cr_inr": 78.0,
        "timeline": "2024-2026",
        "status": "Approved",
        "scheme": "State Infrastructure Fund"
    },
    {
        "plan_id": "INV-TG-002",
        "state": "Telangana",
        "district": "Hyderabad",
        "sector": "water_sanitation",
        "project_name": "Strategic Nala Development Programme (SNDP) Phase 2",
        "budget_cr_inr": 290.0,
        "timeline": "2023-2025",
        "status": "Under Construction",
        "scheme": "GHMC Municipal Works"
    }
]
