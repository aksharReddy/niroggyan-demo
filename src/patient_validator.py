"""
NirogGyan Patient Data Validator
Validates incoming patient profile data before
it is processed by the risk scoring engine.
"""

VALID_GENDERS = ["male", "female", "other"]
MIN_AGE = 18
MAX_AGE = 120


def validate_patient_profile(profile: dict) -> dict:
    """
    Validates a patient profile dict.

    Returns:
        dict with keys: valid (bool), errors (list of str)
    """
    if not profile:
        return {"valid": False, "errors": ["Patient profile cannot be empty"]}

    errors = []

    # Validate age
    age = profile.get("age")
    if age is None:
        errors.append("age is required")
    elif not isinstance(age, int):
        errors.append("age must be an integer")
    elif age < MIN_AGE or age > MAX_AGE:
        errors.append(f"age must be between {MIN_AGE} and {MAX_AGE}")

    # Validate gender
    gender = profile.get("gender")
    if gender is None:
        errors.append("gender is required")
    elif gender.lower() not in VALID_GENDERS:
        errors.append(f"gender must be one of: {VALID_GENDERS}")

    # Validate BMI
    bmi = profile.get("bmi")
    if bmi is not None:
        if not isinstance(bmi, (int, float)):
            errors.append("bmi must be a number")
        elif bmi < 10 or bmi > 70:
            errors.append("bmi value is physiologically implausible (expected 10-70)")

    # Validate boolean flags
    for bool_field in ["is_smoker", "has_diabetes", "family_history_diabetes"]:
        val = profile.get(bool_field)
        if val is not None and not isinstance(val, bool):
            errors.append(f"{bool_field} must be a boolean (true/false)")

    # Validate cholesterol values (mg/dL ranges)
    cholesterol_fields = {
        "total_cholesterol": (100, 400),
        "hdl_cholesterol": (20, 100),
        "ldl_cholesterol": (30, 300),
        "triglycerides": (30, 1000),
    }
    for field, (min_val, max_val) in cholesterol_fields.items():
        val = profile.get(field)
        if val is not None:
            if not isinstance(val, (int, float)):
                errors.append(f"{field} must be a number")
            elif val < min_val or val > max_val:
                errors.append(f"{field} value {val} is outside expected range ({min_val}-{max_val} mg/dL)")

    # Validate blood pressure
    systolic_bp = profile.get("systolic_bp")
    if systolic_bp is not None:
        if not isinstance(systolic_bp, (int, float)):
            errors.append("systolic_bp must be a number")
        elif systolic_bp < 70 or systolic_bp > 250:
            errors.append("systolic_bp is outside expected range (70-250 mmHg)")

    return {"valid": len(errors) == 0, "errors": errors}
