# File: tests/test_wonder.py
from formulas.wonder import WonderLogic

def test_compute_a():
    value = WonderLogic.compute_a(10, 5)
    # Updated to reflect S_REF default sensitivity calibration (v3.0.0)
    assert round(value, 5) == 0.86466, f"Unexpected value: {value}"

    # Edge cases
    value = WonderLogic.compute_a(0, 1)
    assert value == 0.0, "Result should be 0 for zero novelty."

    value = WonderLogic.compute_a(5, -1)
    # Updated: When sensitivity <= 0, function uses S_REF (e/π) instead of 1.0
    assert round(value, 5) == 0.99691, "Sensitivity must be treated as positive."
