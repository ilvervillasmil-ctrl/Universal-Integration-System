# File: tests/test_wonder.py
from formulas.wonder import WonderLogic

def test_compute_a():
    value = WonderLogic.compute_a(10, 5)
    assert round(value, 5) == 0.86788, f"Unexpected value: {value}"

    # Edge cases
    value = WonderLogic.compute_a(0, 1)
    assert value == 0.0, "Result should be 0 for zero novelty."

    value = WonderLogic.compute_a(5, -1)
    assert round(value, 5) == 0.99326, "Sensitivity must be treated as positive."
