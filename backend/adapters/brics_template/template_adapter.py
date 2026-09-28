"""
BRICS Country Adapter Template
Use this template to extend the Citizen Development Intelligence Platform
to another BRICS nation (e.g., Brazil, South Africa, Egypt, Ethiopia, UAE)
without modifying any core pipeline, analytics, or UI rendering logic.
"""

from typing import Dict, List, Any
from backend.adapters.base_country_adapter import BaseCountryAdapter

class BricsCountryAdapterTemplate(BaseCountryAdapter):
    """
    Template for creating a new BRICS nation adapter.
    Example: Brazil (Federative Republic of Brazil)
    Languages: Portuguese (pt), indigenous language co-official regions.
    Administrative levels: ['Federal', 'State (Estado)', 'Municipality (Município)']
    """

    @property
    def country_code(self) -> str:
        # Return 2 or 3-letter ISO code, e.g. "BR" or "ZA"
        return "BR"

    @property
    def country_name(self) -> str:
        return "Brazil"

    @property
    def administrative_levels(self) -> List[str]:
        # Return administrative units hierarchy
        return ["Federal", "State", "Municipality"]

    def get_supported_languages(self) -> Dict[str, Dict[str, Any]]:
        """
        Return the language registry dictionary.
        Must map language code to script, font, baseline STT confidence, etc.
        """
        return {
            "pt": {
                "code": "pt",
                "name": "Portuguese",
                "native_name": "Português",
                "script": "Latin",
                "font_family": "'Inter', sans-serif",
                "text_direction": "ltr",
                "stt_confidence_baseline": 0.94,
                "translation_engine": "Native Portuguese / Passthrough to EN",
                "acoustic_notes": "Trained on Brazilian Portuguese regional accents.",
                "sample_prompts": [
                    "Vazamento constante na rede de abastecimento de água no bairro periférico há 2 semanas."
                ]
            }
        }

    def get_sector_taxonomy(self) -> List[Dict[str, Any]]:
        """
        Return sector taxonomy for this country.
        E.g. Saneamento Básico, Transporte Público, Saúde Básica, Educação, Energia.
        """
        return [
            {
                "id": "water_sanitation",
                "name": "Basic Sanitation & Water",
                "icon": "Droplets",
                "sdg_alignment": "SDG 6",
                "subcategories": ["Water supply outage", "Open sewage", "Drainage"],
                "keywords": ["água", "esgoto", "vazamento", "saneamento", "torneira"]
            }
        ]

    def get_geographic_units(self) -> List[Dict[str, Any]]:
        """
        Return list of states/districts with lat, lng, and codes.
        """
        return [
            {
                "state": "São Paulo",
                "state_code": "SP",
                "district": "São Paulo (Zona Leste)",
                "district_code": "SP-ZL",
                "region": "Southeast",
                "lat": -23.5505,
                "lng": -46.6333,
                "is_aspirational_district": False
            }
        ]

    def get_synthetic_demographics(self) -> List[Dict[str, Any]]:
        return [
            {"state": "São Paulo", "district": "São Paulo (Zona Leste)", "population": 4200000, "density_per_sqkm": 8200, "rural_pct": 2.1, "literacy_rate": 96.5, "year": 2024}
        ]

    def get_synthetic_infrastructure(self) -> List[Dict[str, Any]]:
        return [
            {"state": "São Paulo", "district": "São Paulo (Zona Leste)", "sector": "water_sanitation", "score": 62.0, "coverage_desc": "Sabesp regional network coverage 88%", "year": 2024}
        ]

    def get_synthetic_investment_plans(self) -> List[Dict[str, Any]]:
        return [
            {
                "plan_id": "INV-BR-001",
                "state": "São Paulo",
                "district": "São Paulo (Zona Leste)",
                "sector": "water_sanitation",
                "project_name": "Programa Novo Rio Pinheiros / Billings Saneamento",
                "budget_cr_inr": 250.0,
                "timeline": "2024-2026",
                "status": "Under Construction",
                "scheme": "Plano Estadual de Saneamento"
            }
        ]
