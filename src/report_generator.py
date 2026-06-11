"""
NirogGyan Smart Report Generator v2
"""

from datetime import datetime

REPORT_SECTIONS = ["summary", "cardiovascular", "diabetes", "recommendations", "followup"]


def generate_patient_report(patient_id: str, risk_scores: dict, lab_results: dict) -> dict:
    """
    Generates a full wellness report for a patient.
    """
    if not patient_id:
        return {"status": "error", "message": "patient_id is required", "data": None}

    if not risk_scores:
        return {"status": "error", "message": "risk_scores are required", "data": None}

    if not lab_results:
        return {"status": "error", "message": "lab_results are required", "data": None}

    report = {
        "report_id": f"RPT-{patient_id}-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "patient_id": patient_id,
        "generated_at": datetime.now().isoformat(),
        "sections": {},
    }

    report["sections"]["summary"] = _build_summary(risk_scores)
    report["sections"]["cardiovascular"] = _build_cardiovascular_section(
        risk_scores.get("cardiovascular", {}), lab_results
    )
    report["sections"]["diabetes"] = _build_diabetes_section(
        risk_scores.get("diabetes", {}), lab_results
    )
    report["sections"]["recommendations"] = _build_recommendations(risk_scores)
    report["sections"]["followup"] = _build_followup_plan(risk_scores)

    return report


def _build_summary(risk_scores: dict) -> dict:
    cardio_score = risk_scores.get("cardiovascular", {}).get("score", 0)
    diabetes_score = risk_scores.get("diabetes", {}).get("score", 0)

    overall_score = round((cardio_score + diabetes_score) / 2, 2)
    overall_risk = _get_overall_risk_label(overall_score)

    return {
        "overall_score": overall_score,
        "overall_risk": overall_risk,
        "cardio_risk_level": risk_scores.get("cardiovascular", {}).get("risk_level", "UNKNOWN"),
        "diabetes_risk_level": risk_scores.get("diabetes", {}).get("risk_level", "UNKNOWN"),
    }


def _build_cardiovascular_section(cardio_scores: dict, lab_results: dict) -> dict:
    return {
        "score": cardio_scores.get("score", 0),
        "risk_level": cardio_scores.get("risk_level", "UNKNOWN"),
        "total_cholesterol": lab_results.get("total_cholesterol"),
        "hdl_cholesterol": lab_results.get("hdl_cholesterol"),
        "ldl_cholesterol": lab_results.get("ldl_cholesterol"),
        "triglycerides": lab_results.get("triglycerides"),
        "systolic_bp": lab_results.get("systolic_bp"),
    }


def _build_diabetes_section(diabetes_scores: dict, lab_results: dict) -> dict:
    return {
        "score": diabetes_scores.get("score", 0),
        "risk_level": diabetes_scores.get("risk_level", "UNKNOWN"),
        "fasting_glucose": lab_results.get("fasting_glucose"),
        "hba1c": lab_results.get("hba1c"),
        "bmi": lab_results.get("bmi"),
    }


def _build_recommendations(risk_scores: dict) -> list:
    recommendations = []

    cardio_level = risk_scores.get("cardiovascular", {}).get("risk_level", "LOW")
    diabetes_level = risk_scores.get("diabetes", {}).get("risk_level", "LOW")

    if cardio_level in ("HIGH", "CRITICAL"):
        recommendations.append({
            "category": "cardiovascular",
            "priority": "urgent",
            "text": "Consult a cardiologist within 2 weeks.",
        })
    elif cardio_level == "MODERATE":
        recommendations.append({
            "category": "cardiovascular",
            "priority": "moderate",
            "text": "Monitor cholesterol levels quarterly.",
        })

    if diabetes_level in ("HIGH", "CRITICAL"):
        recommendations.append({
            "category": "diabetes",
            "priority": "urgent",
            "text": "Consult an endocrinologist immediately.",
        })
    elif diabetes_level == "MODERATE":
        recommendations.append({
            "category": "diabetes",
            "priority": "moderate",
            "text": "Reduce refined carbohydrate intake.",
        })

    if not recommendations:
        recommendations.append({
            "category": "general",
            "priority": "low",
            "text": "Continue current lifestyle. Annual health checkup recommended.",
        })

    return recommendations


def _build_followup_plan(risk_scores: dict) -> dict:
    cardio_level = risk_scores.get("cardiovascular", {}).get("risk_level", "LOW")
    diabetes_level = risk_scores.get("diabetes", {}).get("risk_level", "LOW")

    if "CRITICAL" in (cardio_level, diabetes_level):
        interval_days = 30
    elif "HIGH" in (cardio_level, diabetes_level):
        interval_days = 90
    elif "MODERATE" in (cardio_level, diabetes_level):
        interval_days = 180
    else:
        interval_days = 365

    return {
        "next_checkup_in_days": interval_days,
        "tests_recommended": _get_recommended_tests(cardio_level, diabetes_level),
    }


def _get_recommended_tests(cardio_level: str, diabetes_level: str) -> list:
    tests = ["Complete Blood Count", "Lipid Panel"]

    if cardio_level in ("HIGH", "CRITICAL"):
        tests.extend(["ECG", "Echocardiogram", "Stress Test"])

    if diabetes_level in ("HIGH", "CRITICAL"):
        tests.extend(["HbA1c", "Fasting Insulin", "OGTT"])

    return tests


def _get_overall_risk_label(score: float) -> str:
    if score <= 30:
        return "LOW"
    elif score <= 60:
        return "MODERATE"
    elif score <= 80:
        return "HIGH"
    return "CRITICAL"
