"""
Impact Measurement & Closed-Loop Governance
Tracks before-and-after time series when recommendations are marked Adopted/Funded.
Demonstrates measurable feedback loop while strictly disclaiming correlation vs causation.
"""

from typing import Dict, List, Any
import datetime

class ImpactTracker:
    """
    Tracks and analyzes post-adoption impact trajectories.
    Demonstrates Digital Public Infrastructure accountability.
    """

    def __init__(self):
        # Pre-seeded adopted projects showing before/after impact
        self.adopted_projects = [
            {
                "project_id": "REC-KA-KLB-001",
                "title": "Kalaburagi Rural Jal Suraksha - Piped Water Pipeline Overhaul",
                "district": "Kalaburagi",
                "state": "Karnataka",
                "sector_id": "water_sanitation",
                "sector_name": "Water & Sanitation",
                "adoption_date": "2024-03-15",
                "adopted_by": "Sri R. K. Patil (Principal Secretary, Rural Development)",
                "allocated_budget_cr_inr": 48.5,
                "status": "COMPLETED_EVALUATED",
                "pre_adoption_monthly_requests": [142, 168, 185],
                "post_adoption_monthly_requests": [120, 88, 54, 38],
                "pre_adoption_infra_score": 38.5,
                "post_adoption_infra_score": 62.0,
                "complaint_reduction_pct": -76.8,
                "infra_improvement_pts": +23.5,
                "months_elapsed": 6,
                "time_series_data": [
                    {"month": "Month -3 (Dec)", "requests": 142, "infra_score": 38.5, "phase": "Pre-Adoption"},
                    {"month": "Month -2 (Jan)", "requests": 168, "infra_score": 38.5, "phase": "Pre-Adoption"},
                    {"month": "Month -1 (Feb)", "requests": 185, "infra_score": 38.5, "phase": "Pre-Adoption"},
                    {"month": "Adoption (Mar)", "requests": 150, "infra_score": 42.0, "phase": "Project Sanctioned"},
                    {"month": "Month +1 (Apr)", "requests": 120, "infra_score": 48.0, "phase": "Implementation"},
                    {"month": "Month +2 (May)", "requests": 88, "infra_score": 54.0, "phase": "Implementation"},
                    {"month": "Month +3 (Jun)", "requests": 54, "infra_score": 58.0, "phase": "Stabilization"},
                    {"month": "Month +4 (Jul)", "requests": 38, "infra_score": 62.0, "phase": "Operational"}
                ],
                "summary": "Following project commissioning, water supply grievances dropped by 76.8% over 6 months across 14 taluk villages, while the district water SDI improved from 38.5 to 62.0.",
                "correlation_disclaimer": "EVALUATION NOTICE: This before-and-after trajectory represents observational correlation based on synthetic prototype data. Observed grievance reductions may also be influenced by seasonal monsoons and groundwater recharge rather than solely infrastructure intervention."
            },
            {
                "project_id": "REC-WB-MSD-002",
                "title": "Bhagwangola & Lalgola 24x7 Emergency Maternal PHC Upgrade",
                "district": "Murshidabad",
                "state": "West Bengal",
                "sector_id": "primary_healthcare",
                "sector_name": "Primary Healthcare",
                "adoption_date": "2024-05-10",
                "adopted_by": "Dr. S. Chatterjee (Director of Health Services)",
                "allocated_budget_cr_inr": 28.0,
                "status": "UNDER_IMPLEMENTATION",
                "pre_adoption_monthly_requests": [112, 128, 134],
                "post_adoption_monthly_requests": [95, 78],
                "pre_adoption_infra_score": 39.0,
                "post_adoption_infra_score": 49.5,
                "complaint_reduction_pct": -41.8,
                "infra_improvement_pts": +10.5,
                "months_elapsed": 3,
                "time_series_data": [
                    {"month": "Month -2 (Mar)", "requests": 112, "infra_score": 39.0, "phase": "Pre-Adoption"},
                    {"month": "Month -1 (Apr)", "requests": 128, "infra_score": 39.0, "phase": "Pre-Adoption"},
                    {"month": "Adoption (May)", "requests": 134, "infra_score": 39.0, "phase": "Sanctioned"},
                    {"month": "Month +1 (Jun)", "requests": 95, "infra_score": 44.0, "phase": "Implementation"},
                    {"month": "Month +2 (Jul)", "requests": 78, "infra_score": 49.5, "phase": "Active Delivery"}
                ],
                "summary": "Deployment of 6 medical officers and 2 standby ambulances reduced emergency healthcare complaints by 41.8% in Murshidabad rural blocks.",
                "correlation_disclaimer": "EVALUATION NOTICE: Correlation evidence from synthetic test data. True causal impact requires randomized control or synthetic control econometric modeling."
            }
        ]

    def get_all_impact_studies(self) -> List[Dict[str, Any]]:
        return self.adopted_projects

    def adopt_recommendation(
        self,
        recommendation: Dict[str, Any],
        policymaker_name: str,
        allocated_budget: float,
        notes: str
    ) -> Dict[str, Any]:
        """
        Marks a proposed recommendation as ADOPTED / FUNDED and initializes tracking.
        """
        now_str = datetime.date.today().isoformat()
        current_volume = recommendation.get("factor_breakdown", {}).get("demand_volume", {}).get("raw_count", 50)
        current_infra = recommendation.get("factor_breakdown", {}).get("infrastructure_gap", {}).get("infrastructure_index_score", 45.0)

        new_impact = {
            "project_id": recommendation["id"],
            "title": recommendation["title"],
            "district": recommendation["district"],
            "state": recommendation["state"],
            "sector_id": recommendation["sector_id"],
            "sector_name": recommendation["sector_name"],
            "adoption_date": now_str,
            "adopted_by": policymaker_name,
            "allocated_budget_cr_inr": allocated_budget,
            "status": "ADOPTED_IN_PLANNING",
            "pre_adoption_monthly_requests": [int(current_volume * 0.9), int(current_volume * 0.95), current_volume],
            "post_adoption_monthly_requests": [],
            "pre_adoption_infra_score": current_infra,
            "post_adoption_infra_score": current_infra,
            "complaint_reduction_pct": 0.0,
            "infra_improvement_pts": 0.0,
            "months_elapsed": 0,
            "time_series_data": [
                {"month": "Baseline", "requests": current_volume, "infra_score": current_infra, "phase": "Adoption Baseline"}
            ],
            "summary": f"Recommendation adopted on {now_str} by {policymaker_name} with budget allocation ₹{allocated_budget:.1f} Cr. Field baseline established.",
            "correlation_disclaimer": "EVALUATION NOTICE: Before-and-after metrics reflect observational correlation on synthetic prototype data. Final public policy outcomes must be validated via rigorous field surveys."
        }
        self.adopted_projects.insert(0, new_impact)
        return new_impact


impact_tracker = ImpactTracker()
