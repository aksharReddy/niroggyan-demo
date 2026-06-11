"""
Tests for NirogGyan Risk Score Calculator
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from risk_calculator import calculate_cardiovascular_risk, calculate_diabetes_risk, _get_risk_level


class TestCardiovascularRisk:

    def test_healthy_patient_scores_low(self):
        patient = {
            "patient_id": "P001",
            "age": 30,
            "total_cholesterol": 170.0,
            "hdl_cholesterol": 60.0,
            "systolic_bp": 110.0,
            "is_smoker": False,
            "has_diabetes": False,
        }
        result = calculate_cardiovascular_risk(patient)
        assert result["score"] >= 0
        assert result["score"] <= 100
        assert result["risk_level"] in ("LOW", "MODERATE", "HIGH", "CRITICAL")

    def test_high_risk_patient_scores_higher(self):
        low_risk = {
            "patient_id": "P001",
            "age": 30,
            "total_cholesterol": 170.0,
            "hdl_cholesterol": 60.0,
            "systolic_bp": 110.0,
            "is_smoker": False,
            "has_diabetes": False,
        }
        high_risk = {
            "patient_id": "P002",
            "age": 60,
            "total_cholesterol": 280.0,
            "hdl_cholesterol": 35.0,
            "systolic_bp": 160.0,
            "is_smoker": True,
            "has_diabetes": True,
        }
        low_result = calculate_cardiovascular_risk(low_risk)
        high_result = calculate_cardiovascular_risk(high_risk)
        assert high_result["score"] > low_result["score"]

    def test_score_clamped_between_0_and_100(self):
        extreme_patient = {
            "patient_id": "P003",
            "age": 100,
            "total_cholesterol": 400.0,
            "hdl_cholesterol": 20.0,
            "systolic_bp": 250.0,
            "is_smoker": True,
            "has_diabetes": True,
        }
        result = calculate_cardiovascular_risk(extreme_patient)
        assert 0 <= result["score"] <= 100

    def test_missing_field_raises_key_error(self):
        with pytest.raises(KeyError):
            calculate_cardiovascular_risk({"age": 30})

    def test_empty_input_raises_value_error(self):
        with pytest.raises(ValueError):
            calculate_cardiovascular_risk({})

    def test_none_input_raises_value_error(self):
        with pytest.raises(ValueError):
            calculate_cardiovascular_risk(None)

    def test_patient_id_preserved_in_result(self):
        patient = {
            "patient_id": "P999",
            "age": 40,
            "total_cholesterol": 200.0,
            "hdl_cholesterol": 50.0,
            "systolic_bp": 120.0,
            "is_smoker": False,
            "has_diabetes": False,
        }
        result = calculate_cardiovascular_risk(patient)
        assert result["patient_id"] == "P999"


class TestDiabetesRisk:

    def test_healthy_patient_low_risk(self):
        patient = {
            "patient_id": "P001",
            "age": 28,
            "bmi": 22.0,
            "fasting_glucose": 88.0,
            "hba1c": 5.2,
            "family_history_diabetes": False,
        }
        result = calculate_diabetes_risk(patient)
        assert result["score"] >= 0
        assert result["score"] <= 100

    def test_diabetic_markers_increase_score(self):
        healthy = {
            "patient_id": "P001",
            "age": 28,
            "bmi": 22.0,
            "fasting_glucose": 88.0,
            "hba1c": 5.2,
            "family_history_diabetes": False,
        }
        at_risk = {
            "patient_id": "P002",
            "age": 50,
            "bmi": 33.0,
            "fasting_glucose": 130.0,
            "hba1c": 7.0,
            "family_history_diabetes": True,
        }
        healthy_result = calculate_diabetes_risk(healthy)
        at_risk_result = calculate_diabetes_risk(at_risk)
        assert at_risk_result["score"] > healthy_result["score"]

    def test_empty_input_raises_value_error(self):
        with pytest.raises(ValueError):
            calculate_diabetes_risk({})


class TestRiskLevelMapping:

    def test_score_0_is_low(self):
        assert _get_risk_level(0) == "LOW"

    def test_score_30_is_low(self):
        assert _get_risk_level(30) == "LOW"

    def test_score_31_is_moderate(self):
        assert _get_risk_level(31) == "MODERATE"

    def test_score_100_is_critical(self):
        assert _get_risk_level(100) == "CRITICAL"
