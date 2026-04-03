# WOD Block Builder (MVP Foundation)

This repository now contains the initial Streamlit foundation for the **WOD Block Builder** product.

## What is included

- App scaffolding for a clean MVP layout
- Sidebar inputs for future deterministic block generation
- Main sections for:
  - 4-week block preview
  - progression signals/charts placeholders
  - explanation placeholder
  - WOD explorer placeholder with filters
- Minimal modern dark theme styling

## Run locally

```bash
streamlit run app/Home.py
```

## Current scope

This first step is only UI foundation and project structure.
No real programming logic, dataset integration, LLM usage, or Airtable integration is included yet.

## Local dataset (MVP)

The MVP uses a local CSV dataset at:

- `data/wod_dataset.csv`

The dataset schema is defined in `app/utils/dataset_schema.py`, and loaded with:

- `load_wod_dataset()` in `app/utils/data_loader.py`
