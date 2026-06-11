"""
NirogGyan Risk Score Calculator
Computes cardiovascular, diabetes, and general wellness risk scores
for patients based on lab test results and profile data.
"""

RISK_LEVELS = {
    "LOW": (0, 30),
    "MODERATE": (31, 60),
    "HIGH": (61, 80),
    "CRITICAL": (81, 100),
}


def calculate_cardiovascular_risk(patient_data: dict) -> dict:
    """
    Calculates cardiovascular risk score (0-100).

    Required fields in patient_data:
        - age (int)
        - total_cholesterol (float, mg/dL)
        - hdl_cholesterol (float, mg/dL)
        - systolic_bp (float, mmHg)
        - is_smoker (bool)
        - has_diabetes (bool)
    """
    if not patient_data:
        raise ValueError("patient_data cannot be None or empty")

    required_fields = ["age", "total_cholesterol", "hdl_cholesterol", "systolic_bp", "is_smoker", "has_diabetes"]
    for field in required_fields:
        if field not in patient_data:
            raise KeyError(f"Missing required field: {field}")

    age = patient_data["age"]
    total_chol = patient_data["total_cholesterol"]
    hdl = patient_data["hdl_cholesterol"]
    systolic_bp = patient_data["systolic_bp"]
    is_smoker = patient_data["is_smoker"]
    has_diabetes = patient_data["has_diabetes"]

    # Base score from age
    score = (age - 20) * 0.5

    # Cholesterol ratio contribution
    if hdl > 0:
        chol_ratio = total_chol / hdl
        score += chol_ratio * 3

    # Blood pressure contribution
    if systolic_bp > 120:
        score += (systolic_bp - 120) * 0.3

    # Risk multipliers
    if is_smoker:
        score *= 1.4

    if has_diabetes:
        score *= 1.3

    # Clamp score to 0-100
    final_score = round(min(max(score, 0), 100), 2)

    return {
        "score": final_score,
        "risk_level": _get_risk_level(final_score),
        "patient_id": patient_data.get("patient_id"),
    }


def calculate_diabetes_risk(patient_data: dict) -> dict:
    """
    Calculates diabetes risk score (0-100).

    Required fields in patient_data:
        - age (int)
        - bmi (float)
        - fasting_glucose (float, mg/dL)
        - hba1c (float, %)
        - family_history_diabetes (bool)
    """
    if not patient_data:
        raise ValueError("patient_data cannot be None or empty")

    required_fields = ["age", "bmi", "fasting_glucose", "hba1c", "family_history_diabetes"]
    for field in required_fields:
        if field not in patient_data:
            raise KeyError(f"Missing required field: {field}")

    age = patient_data["age"]
    bmi = patient_data["bmi"]
    fasting_glucose = patient_data["fasting_glucose"]
    hba1c = patient_data["hba1c"]
    family_history = patient_data["family_history_diabetes"]

    score = 0

    # Age factor
    if age >= 45:
        score += 15
    elif age >= 35:
        score += 8

    # BMI factor
    if bmi >= 30:
        score += 20
    elif bmi >= 25:
        score += 10

    # Fasting glucose factor (normal < 100 mg/dL)
    if fasting_glucose >= 126:
        score += 30
    elif fasting_glucose >= 100:
        score += 15

    # HbA1c factor (normal < 5.7%)
    if hba1c >= 6.5:
        score += 25
    elif hba1c >= 5.7:
        score += 12

    # Family history
    if family_history:
        score += 10

    final_score = round(min(max(score, 0), 100), 2)

    return {
        "score": final_score,
        "risk_level": _get_risk_level(final_score),
        "patient_id": patient_data.get("patient_id"),
    }


def _get_risk_level(score: float) -> str:
    for level, (low, high) in RISK_LEVELS.items():
        if low <= score <= high:
            return level
    return "UNKNOWN"
