# BRICS Country Adapter Extensibility Guide

This platform is architected as a **Digital Public Good (DPG)** following modular principles. The common AI core, analytics engine, prioritization math, and policymaker dashboard are strictly decoupled from country-specific assumptions.

## How to Add a New Country (e.g. South Africa, Brazil, Egypt):

1. **Subclass `BaseCountryAdapter`**:
   Create a new folder in `backend/adapters/<country_name>/` (e.g., `backend/adapters/south_africa/`).
   Implement `SouthAfricaAdapter(BaseCountryAdapter)`.

2. **Supply 5 Configs**:
   - `languages.py`: Supported national/regional languages with scripts, fonts, and baseline STT confidence.
   - `taxonomy.py`: Country-specific development sectors & subcategories with multilingual keywords.
   - `geo_data.py`: Administrative level hierarchy (Provinces/Municipalities/Districts) and GPS coordinates.
   - `demographics_data.py`: Population, density, rural percentages.
   - `infrastructure_data.py`: Sector-specific infrastructure indices (0-100 scale).

3. **Plug into Registry**:
   In `backend/adapters/__init__.py`, set the active adapter:
   ```python
   active_adapter = SouthAfricaAdapter()
   ```

No changes to the AI pipeline, scoring formulas, Leaflet map renderer, or dashboard components are required!
