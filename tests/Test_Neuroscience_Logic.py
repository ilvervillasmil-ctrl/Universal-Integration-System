import pytest
import math
from formulas.neuroscience_logic import NeuroscienceLogic
from formulas.constants import ALPHA, BETA


class TestNeuralResonance:
    def test_equal_layers(self):
        """Equal activity = maximum resonance (ALPHA)."""
        result = NeuroscienceLogic.compute_neural_resonance(1.0, 1.0)
        assert math.isclose(result, ALPHA, rel_tol=1e-9)

    def test_both_zero(self):
        """Both zero = 0 resonance."""
        result = NeuroscienceLogic.compute_neural_resonance(0.0, 0.0)
        assert result == 0.0

    def test_one_zero(self):
        """One layer at zero = ALPHA - BETA."""
        result = NeuroscienceLogic.compute_neural_resonance(1.0, 0.0)
        assert math.isclose(result, ALPHA - BETA, rel_tol=1e-9)

    def test_symmetry(self):
        """Order doesn't matter."""
        r1 = NeuroscienceLogic.compute_neural_resonance(0.8, 0.3)
        r2 = NeuroscienceLogic.compute_neural_resonance(0.3, 0.8)
        assert math.isclose(r1, r2, rel_tol=1e-9)

    def test_closer_layers_higher_resonance(self):
        """Closer activities = higher resonance."""
        r_close = NeuroscienceLogic.compute_neural_resonance(0.9, 0.8)
        r_far = NeuroscienceLogic.compute_neural_resonance(0.9, 0.1)
        assert r_close > r_far

    def test_resonance_bounded(self):
        """Resonance never exceeds ALPHA."""
        result = NeuroscienceLogic.compute_neural_resonance(100.0, 100.0)
        assert result <= ALPHA

    def test_alpha_beta_sum(self):
        """When one layer is zero: result = ALPHA - BETA = 26/27 - 1/27 = 25/27."""
        result = NeuroscienceLogic.compute_neural_resonance(5.0, 0.0)
        assert math.isclose(result, 25/27, rel_tol=1e-9)


class TestNeuralDecay:
    def test_zero_time(self):
        """At t=0, frequency unchanged."""
        result = NeuroscienceLogic.simulate_neural_decay(440.0, 0.5, 0.0)
        assert math.isclose(result, 440.0, rel_tol=1e-9)

    def test_decay_reduces(self):
        """Frequency decreases over time."""
        f0 = NeuroscienceLogic.simulate_neural_decay(1.0, 0.5, 0.0)
        f1 = NeuroscienceLogic.simulate_neural_decay(1.0, 0.5, 1.0)
        assert f0 > f1

    def test_zero_decay_rate(self):
        """No decay = constant frequency."""
        result = NeuroscienceLogic.simulate_neural_decay(100.0, 0.0, 50.0)
        assert math.isclose(result, 100.0, rel_tol=1e-9)

    def test_large_time(self):
        """Large time → near zero."""
        result = NeuroscienceLogic.simulate_neural_decay(1.0, 1.0, 100.0)
        assert result < 1e-40

    def test_known_value(self):
        """f * e^(-1) at t=1, decay=1."""
        result = NeuroscienceLogic.simulate_neural_decay(1.0, 1.0, 1.0)
        assert math.isclose(result, math.exp(-1), rel_tol=1e-9)
