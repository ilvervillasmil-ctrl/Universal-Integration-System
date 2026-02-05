# File: tests/test_constants.py
from formulas.constants import PHI, ALPHA, BETA, S_REF

def test_constants():
    assert round(PHI, 5) == 1.61803, "PHI constant is incorrect!"
    assert round(ALPHA, 5) == 0.96296, "ALPHA constant is incorrect!"
    assert round(BETA, 5) == 0.03704, "BETA constant is incorrect!"
    assert round(S_REF, 5) == 0.86526, "S_REF constant is incorrect!"
