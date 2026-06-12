"""
NirogGyan Additional Risk Modules
Extended scoring functions for the NirogGyan diagnostic platform.
"""


def calculate_kidney_risk(patient_data: dict) -> dict:
    """
    Calculates kidney risk score (0-100).

    Required fields:
        - creatinine (float, mg/dL)
        - egfr (float, mL/min/1.73m2)
        - urea (float, mg/dL)
        - has_hypertension (bool)
        - has_diabetes (bool)
    """
    if not patient_data:
        raise ValueError("patient_data cannot be None or empty")

    required_fields = ["creatinine", "egfr", "urea", "has_hypertension", "has_diabetes"]
    for field in required_fields:
        if field not in patient_data:
            raise KeyError(f"Missing required field: {field}")

    score = 0
    egfr = patient_data["egfr"]
    creatinine = patient_data["creatinine"]
    urea = patient_data["urea"]

    if egfr < 15:
        score += 50
    elif egfr < 30:
        score += 35
    elif egfr < 60:
        score += 20
    elif egfr < 90:
        score += 10

    if creatinine > 3.0:
        score += 25
    elif creatinine > 1.5:
        score += 10

    if urea > 40:
        score += 15
    elif urea > 20:
        score += 5

    if patient_data["has_hypertension"]:
        score += 10

    if patient_data["has_diabetes"]:
        score += 10

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
