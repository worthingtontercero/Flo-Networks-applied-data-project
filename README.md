# Flo Networks — Applied Data Project (Market Prioritization Lens)

This repository builds a **market prioritization lens** for Flo Networks by converting **public economic activity data** into **metro-level demand proxies**, then ranking U.S. CBSAs using:

1) A **baseline demand** ranking (demand proxy only)  
2) A **Flo Score** (demand + enterprise fit + cloud adjacency + resilience − capex friction)  
3) A **sensitivity test** to check whether rankings remain stable when weights change

The repo includes **outputs (CSVs + charts)** so a viewer can inspect results immediately without running the notebooks.

---

## Where to start (recommended reading order)

1) **Methodology & limitations**  
   - `docs/01_methodology_and_limitations.md`

2) **Results & output interpretation (tables + charts)**  
   - `docs/02_results_and_output_interpretation.md`

3) **Notebooks (full reproducibility)**
   - `notebooks/01_build_dataset.ipynb` — builds `data/processed/market_features.csv`  
   - `notebooks/02_scoring_and_sensitivity.ipynb` — generates rankings + sensitivity outputs into `outputs/`

---

## Repository structure

- `src/`  
  Core Python modules (config, ingestion helpers, feature logic)

- `data/`  
  - `raw/` — raw inputs (e.g., county→CBSA crosswalk)  
  - `processed/` — processed metro dataset (Notebook 01 output)

- `notebooks/`  
  - `01_build_dataset.ipynb`  
  - `02_scoring_and_sensitivity.ipynb`

- `outputs/`  
  CSV exports + figure images used in documentation  
  - `rankings_all.csv`  
  - `rankings_candidates.csv`  
  - `rankings_border_states.csv`  
  - `deliverable_scoring_table.csv`  
  - `sensitivity_results.csv`  
  - `figures/` (PNG charts/screenshots referenced in docs)

- `docs/`  
  Written deliverables (what a stakeholder should read)

---

## Quickstart (run locally)

### 1) Create environment + install deps
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
