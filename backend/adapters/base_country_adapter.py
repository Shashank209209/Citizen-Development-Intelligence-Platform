from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional

class BaseCountryAdapter(ABC):
    """
    Abstract Country Adapter contract for the Citizen Development Intelligence Platform.
    Ensures the core platform remains decoupled from country-specific geographic hierarchies,
    language registries, taxonomy mappings, and demographic indicators.
    """

    @property
    @abstractmethod
    def country_code(self) -> str:
        """ISO 3166-1 alpha-2 or alpha-3 code (e.g. 'IN', 'BRA', 'ZAF')"""
        pass

    @property
    @abstractmethod
    def country_name(self) -> str:
        """Display name of the country (e.g. 'India')"""
        pass

    @property
    @abstractmethod
    def administrative_levels(self) -> List[str]:
        """Hierarchical administrative levels (e.g. ['National', 'State', 'District'])"""
        pass

    @abstractmethod
    def get_supported_languages(self) -> Dict[str, Dict[str, Any]]:
        """
        Returns registry of supported languages with code, name, native script,
        font family, stt model support rating, and translation fallback.
        """
        pass

    @abstractmethod
    def get_sector_taxonomy(self) -> List[Dict[str, Any]]:
        """Standardized development sector taxonomy for this country"""
        pass

    @abstractmethod
    def get_geographic_units(self) -> List[Dict[str, Any]]:
        """Reference list of states/provinces and districts/municipalities with coordinates"""
        pass

    @abstractmethod
    def get_synthetic_demographics(self) -> List[Dict[str, Any]]:
        """Demographic indices (population, density, rural %)"""
        pass

    @abstractmethod
    def get_synthetic_infrastructure(self) -> List[Dict[str, Any]]:
        """Infrastructure index scores (0-100) per region and sector"""
        pass

    @abstractmethod
    def get_synthetic_investment_plans(self) -> List[Dict[str, Any]]:
        """Planned public works / capital budget allocations"""
        pass
