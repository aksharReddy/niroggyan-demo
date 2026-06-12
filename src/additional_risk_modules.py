"""
NirogGyan Additional Risk Modules
Extended scoring functions for the NirogGyan diagnostic platform.
"""


def calculate_liver_risk(patient_data: dict) -> dict:
    """
    Calculates liver risk score (0-100).

    Required fields:
        - alt (float, U/L)
        - ast (float, U/L)
        - bilirubin (float, mg/dL)
        - has_fatty_liver (bool)
        - alcohol_units_per_week (int)
    """
    if not patient_data:
        raise ValueError("patient_data cannot be None or empty")

    required_fields = ["alt", "ast", "bilirubin", "has_fatty_liver", "alcohol_units_per_week"]
    for field in required_fields:
        if field not in patient_data:
            raise KeyError(f"Missing required field: {field}")

    score = 0
    alt = patient_data["alt"]
    ast = patient_data["ast"]
    bilirubin = patient_data["bilirubin"]

    if alt > 56:
        score += 25
    elif alt > 35:
        score += 10

    if ast > 40:
        score += 25
    elif ast > 25:
        score += 10

    if bilirubin > 2.0:
        score += 20
    elif bilirubin > 1.2:
        score += 8

    if patient_data["has_fatty_liver"]:
        score += 15

    alcohol = patient_data["alcohol_units_per_week"]
    if alcohol > 14:
        score += 15
    elif alcohol > 7:
        score += 8

    final_score = round(min(max(score, 0), 100), 2)

    return {
        "score": final_score,
        "risk_level": _get_risk_level(final_score),
        "patient_id": patient_data.get("patient_id"),
    }


def calculate_bmi_category(patient_data: dict) -> dict:
    """
    Calculates BMI and returns category with health risk context.

    Required fields:
        - weight_kg (float)
        - height_cm (float)
    """
    if not patient_data:
        raise ValueError("patient_data cannot be None or empty")

    required_fields = ["weight_kg", "height_cm"]
    for field in required_fields:
        if field not in patient_data:
            raise KeyError(f"Missing required field: {field}")

    weight = patient_data["weight_kg"]
    height_m = patient_data["height_cm"] / 100

    if height_m <= 0:
        raise ValueError("height_cm must be greater than 0")

    bmi = round(weight / (height_m ** 2), 2)

    if bmi < 18.5:
        category = "Underweight"
        risk_note = "Increased risk of nutritional deficiency"
    elif bmi < 25.0:
        category = "Normal"
        risk_note = "Healthy weight range"
    elif bmi < 30.0:
        category = "Overweight"
        risk_note = "Increased risk of cardiovascular disease and diabetes"
    else:
        category = "Obese"
        risk_note = "High risk of cardiovascular disease, diabetes, and joint issues"

    return {
        "score": bmi,
        "risk_level": category,
        "patient_id": patient_data.get("patient_id"),
        "details": risk_note,
    }


def _get_risk_level(score: float) -> str:
    if score <= 30:
        return "LOW"
    elif score <= 60:
        return "MODERATE"
    elif score <= 80:
        return "HIGH"
    return "CRITICAL"
