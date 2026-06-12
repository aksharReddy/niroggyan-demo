"""
NirogGyan Risk Calculator v2
Simplified cardiovascular scoring based on updated clinical guidelines.
"""

RISK_LEVELS = {
    "LOW": (0, 30),
    "MODERATE": (31, 60),
    "HIGH": (61, 80),
    "CRITICAL": (81, 100),
}


def calculate_cardiovascular_risk(patient_data: dict) -> dict:
    """
    Calculates cardiovascular risk score using simplified v2 formula.
    Age weighting removed per updated clinical team guidance.
    """
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

    score = 0

    chol_ratio = total_chol / hdl
    score += chol_ratio * 3

    if systolic_bp > 120:
        score += (systolic_bp - 120) * 0.3

    if is_smoker:
        score *= 1.4

    if has_diabetes:
        score *= 1.3

    return round(min(max(score, 0), 100), 2)


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

    if age >= 45:
        score += 15
    elif age >= 35:
        score += 8

    if bmi >= 30:
        score += 20
    elif bmi >= 25:
        score += 10

    if fasting_glucose >= 126:
        score += 30
    elif fasting_glucose >= 100:
        score += 15

    if hba1c >= 6.5:
        score += 25
    elif hba1c >= 5.7:
        score += 12

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


DEFAULT_TEST_PATIENT = {
    "patient_id": "PAT-2024-00182",
    "age": 45,
    "total_cholesterol": 230,
    "hdl_cholesterol": 42,
    "systolic_bp": 145,
    "is_smoker": True,
    "has_diabetes": False,
    "name": "Rajesh Kumar",
    "phone": "9876543210"
}
