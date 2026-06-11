# NirogGyan Demo — Diagnostic Lab SaaS

Demo repository for evaluating CodeRabbit AI code review on a healthcare SaaS codebase.

## What This Simulates

This repo mimics the core backend of a diagnostic lab platform:

- **Risk Score Calculator** — Computes cardiovascular and diabetes risk scores (0-100) from lab values
- **Smart Report Generator** — Builds structured patient wellness reports from risk scores
- **LIMS Handler** — Ingests and normalizes lab results from external LIMS vendors
- **Patient Validator** — Validates patient profile data before risk processing

## Project Structure

```
src/
  risk_calculator.py     # Cardiovascular & diabetes risk scoring engine
  report_generator.py    # Patient wellness report builder
  lims_handler.py        # LIMS vendor integration & normalization
  patient_validator.py   # Input validation for patient data

tests/
  test_risk_calculator.py  # Unit tests for risk scoring
```

## Key Business Rules

- All risk scores must be in range 0-100
- All API responses must return `status`, `message`, and `data` keys
- `patient_id` is required on all operations
- Supported LIMS vendors: mylab, creliohealth, labsoft, lifepoint
- Risk levels: LOW (0-30), MODERATE (31-60), HIGH (61-80), CRITICAL (81-100)
