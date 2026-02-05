# File: tests/test_resonance_extended.py
from formulas.resonance_extended import AdvancedResonance

def test_multi_layer_resonance():
    value = AdvancedResonance.multi_layer_resonance([10, 8, 6])
    assert round(value, 5) == 0.75, f"Unexpected average resonance: {value}"

    # Edge cases
    value = AdvancedResonance.multi_layer_resonance([10])
    assert value == 0.0, "With one layer, resonance should be 0."

def test_enhanced_phase_alignment():
    value = AdvancedResonance.enhanced_phase_alignment(10, 8, 1.2)
    assert round(value, 5) == 0.96, f"Unexpected enhanced alignment: {value}"
