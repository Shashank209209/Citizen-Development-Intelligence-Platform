from typing import Dict, List, Any
from backend.adapters.base_country_adapter import BaseCountryAdapter
from backend.adapters.india.languages import SUPPORTED_LANGUAGES
from backend.adapters.india.taxonomy import SECTORS
from backend.adapters.india.geo_data import STATES_AND_DISTRICTS
from backend.adapters.india.demographics_data import DEMOGRAPHICS
from backend.adapters.india.infrastructure_data import INFRASTRUCTURE_DATA
from backend.adapters.india.investment_plans_data import INVESTMENT_PLANS

class IndiaAdapter(BaseCountryAdapter):
    """
    India Country Adapter for Citizen Development Intelligence Platform.
    Digital Public Good adapter implementation providing geographic hierarchy,
    6 core languages, sector taxonomies, and synthetic baseline datasets.
    """

    @property
    def country_code(self) -> str:
        return "IN"

    @property
    def country_name(self) -> str:
        return "India"

    @property
    def administrative_levels(self) -> List[str]:
        return ["National", "State", "District"]

    def get_supported_languages(self) -> Dict[str, Dict[str, Any]]:
        return SUPPORTED_LANGUAGES

    def get_sector_taxonomy(self) -> List[Dict[str, Any]]:
        return SECTORS

    def get_geographic_units(self) -> List[Dict[str, Any]]:
        return STATES_AND_DISTRICTS

    def get_synthetic_demographics(self) -> List[Dict[str, Any]]:
        return DEMOGRAPHICS

    def get_synthetic_infrastructure(self) -> List[Dict[str, Any]]:
        return INFRASTRUCTURE_DATA

    def get_synthetic_investment_plans(self) -> List[Dict[str, Any]]:
        return INVESTMENT_PLANS
