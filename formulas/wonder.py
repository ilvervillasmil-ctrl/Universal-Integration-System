Run pytest tests/
============================= test session starts ==============================
platform linux -- Python 3.10.19, pytest-9.0.2, pluggy-1.6.0
rootdir: /home/runner/work/Universal-Integration-System/Universal-Integration-System
collected 40 items

tests/test_constants.py ..                                               [  5%]
tests/test_greetings.py ...........                                      [ 32%]
tests/test_presence.py .                                                 [ 35%]
tests/test_resonance.py ..                                               [ 40%]
tests/test_resonance_extended.py ..                                      [ 45%]
tests/test_resonance_processor.py .....................                  [ 97%]
tests/test_wonder.py F                                                   [100%]

=================================== FAILURES ===================================
________________________________ test_compute_a ________________________________

    def test_compute_a():
        value = WonderLogic.compute_a(10, 5)
        # Updated to reflect S_REF default sensitivity calibration (v3.0.0)
        assert round(value, 5) == 0.86466, f"Unexpected value: {value}"
    
        # Edge cases
        value = WonderLogic.compute_a(0, 1)
        assert value == 0.0, "Result should be 0 for zero novelty."
    
        value = WonderLogic.compute_a(5, -1)
        # Updated: When sensitivity <= 0, function uses S_REF (e/π) instead of 1.0
>       assert round(value, 5) == 0.99691, "Sensitivity must be treated as positive."
E       AssertionError: Sensitivity must be treated as positive.
E       assert 1.0 == 0.99691
E        +  where 1.0 = round(1.0, 5)

tests/test_wonder.py:15: AssertionError
=========================== short test summary info ============================
FAILED tests/test_wonder.py::test_compute_a - AssertionError: Sensitivity must be treated as positive.
assert 1.0 == 0.99691
 +  where 1.0 = round(1.0, 5)
========================= 1 failed, 39 passed in 0.11s =========================
Error: Process completed with exit code 1.
