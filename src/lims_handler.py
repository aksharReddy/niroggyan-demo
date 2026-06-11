"""
NirogGyan LIMS Integration Handler
Handles ingestion of lab results from connected
Laboratory Information Management Systems (LIMS).
"""

import json
from datetime import datetime

SUPPORTED_LIMS_VENDORS = ["mylab", "creliohealth", "labsoft", "lifepoint"]

REQUIRED_LAB_FIELDS = [
    "patient_id",
    "lab_id",
    "test_date",
    "results",
]


def ingest_lab_results(raw_payload: dict, vendor: str) -> dict:
    """
    Ingests and normalizes lab results from a LIMS vendor.

    Args:
        raw_payload: Raw JSON payload from the LIMS
        vendor: LIMS vendor identifier (e.g. 'mylab', 'creliohealth')

    Returns:
        dict with keys: status, message, data (normalized lab results)
    """
    if not raw_payload:
        return {"status": "error", "message": "Empty payload received", "data": None}

    if vendor not in SUPPORTED_LIMS_VENDORS:
        return {
            "status": "error",
            "message": f"Unsupported LIMS vendor: {vendor}. Supported: {SUPPORTED_LIMS_VENDORS}",
            "data": None,
        }

    validation_result = _validate_payload(raw_payload)
    if not validation_result["valid"]:
        return {
            "status": "error",
            "message": f"Payload validation failed: {validation_result['errors']}",
            "data": None,
        }

    normalized = _normalize_payload(raw_payload, vendor)

    return {
        "status": "success",
        "message": "Lab results ingested successfully",
        "data": normalized,
    }


def _validate_payload(payload: dict) -> dict:
    errors = []

    for field in REQUIRED_LAB_FIELDS:
        if field not in payload:
            errors.append(f"Missing required field: {field}")

    if "results" in payload:
        if not isinstance(payload["results"], dict):
            errors.append("'results' must be a dict of test_name: value pairs")
        elif len(payload["results"]) == 0:
            errors.append("'results' cannot be empty")

    if "patient_id" in payload:
        if not isinstance(payload["patient_id"], str) or not payload["patient_id"].strip():
            errors.append("'patient_id' must be a non-empty string")

    return {"valid": len(errors) == 0, "errors": errors}


def _normalize_payload(payload: dict, vendor: str) -> dict:
    """Normalize vendor-specific field names to NirogGyan standard schema."""
    normalized = {
        "patient_id": payload["patient_id"],
        "lab_id": payload["lab_id"],
        "vendor": vendor,
        "test_date": payload["test_date"],
        "ingested_at": datetime.now().isoformat(),
        "results": {},
    }

    vendor_field_map = {
        "mylab": {
            "CHOL_T": "total_cholesterol",
            "CHOL_H": "hdl_cholesterol",
            "CHOL_L": "ldl_cholesterol",
            "TRIG": "triglycerides",
            "GLU_F": "fasting_glucose",
            "HBA1C": "hba1c",
            "BP_SYS": "systolic_bp",
            "BMI": "bmi",
        },
        "creliohealth": {
            "total_chol": "total_cholesterol",
            "hdl_chol": "hdl_cholesterol",
            "ldl_chol": "ldl_cholesterol",
            "trig": "triglycerides",
            "fasting_gluc": "fasting_glucose",
            "hba1c": "hba1c",
            "systolic": "systolic_bp",
            "bmi_val": "bmi",
        },
    }

    field_map = vendor_field_map.get(vendor, {})
    raw_results = payload["results"]

    for vendor_field, standard_field in field_map.items():
        if vendor_field in raw_results:
            normalized["results"][standard_field] = raw_results[vendor_field]

    # For vendors without a specific map, pass through as-is
    if not field_map:
        normalized["results"] = raw_results

    return normalized


def get_lims_connection_status(lab_id: str) -> dict:
    """
    Returns the current connection status for a lab's LIMS.
    In production this would ping the actual LIMS endpoint.
    """
    if not lab_id:
        return {"status": "error", "message": "lab_id is required", "data": None}

    # Simulated status for demo purposes
    return {
        "status": "success",
        "message": "LIMS connection active",
        "data": {
            "lab_id": lab_id,
            "connection": "active",
            "last_sync": datetime.now().isoformat(),
            "pending_results": 0,
        },
    }
