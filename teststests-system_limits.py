import pytest
import math
from formulas.constants import (
    ALPHA, BETA, PHI, S_REF, R_FIN,
    OMEGA_0, OMEGA_0_SQUARED,
    PHI_TOTAL, PHI_CRITICAL,
    OMEGA_D, ZETA,
    LAYER_FRICTION, NUM_LAYERS,
    GOLDEN_ANG, THETA_CUBE,
)
from formulas.entropy import EntropyTool
from formulas.fractality import Fractality
from formulas.coherence import CoherenceEngine
from formulas.interaction import compute_interaction
from formulas.presence import compute_presence
from formulas.wonder import compute_wonder


class TestInvariantsNeverBreak:
    """The absolute invariants: these must hold under ALL conditions."""

    def test_alpha_plus_beta_equals_one(self):
        """The supreme invariant. Structure + center = unity."""
        assert abs(ALPHA + BETA - 1.0) < 1e-10

    def test_sin_squared_theta_equals_beta(self):
        """Trigonometric identity from cube geometry."""
        assert abs(math.sin(THETA_CUBE)**2 - BETA) < 1e-10

    def test_cos_squared_theta_equals_alpha(self):
        """Trigonometric identity from cube geometry."""
        assert abs(math.cos(THETA_CUBE)**2 - ALPHA) < 1e-10

    def test_rfin_equals_one_plus_beta(self):
        """Refinement = 1 + the irreducible center."""
        assert abs(R_FIN - (1 + BETA)) < 1e-10

    def test_alpha_approximates_e_minus_beta(self):
        """The law of exponential decay: alpha ≈ e^(-beta)."""
        assert abs(ALPHA - math.exp(-BETA)) < 0.001


class TestCoherenceLimits:
    """The boundaries of coherence: where does it start, where does it end."""

    def test_dead_system_gives_geometric_residue(self):
        """Zero activations = structure without life = 0.438626."""
        engine = CoherenceEngine()
        layers = [{'L': 0.0, 'phi': f} for f in LAYER_FRICTION]
        layers[6]['phi'] = 0.0
        result = engine.compute_coherence(layers)
        assert math.isclose(result, 0.438626, rel_tol=1e-3)

    def test_coherence_never_reaches_one(self):
        """Because beta > 0, perfection is asymptotic."""
        engine = CoherenceEngine()
        layers = [{'L': 1.0, 'phi': f} for f in LAYER_FRICTION]
        layers[6]['phi'] = 0.0
        result = engine.compute_coherence(layers)
        assert result < 1.0

    def test_coherence_never_negative(self):
        """Coherence is clamped: minimum is 0."""
        engine = CoherenceEngine()
        layers = [{'L': 0.0, 'phi': f} for f in LAYER_FRICTION]
        layers[6]['phi'] = 0.0
        result = engine.compute_coherence(layers, C1=0.0, C2=0.0, theta=180)
        assert result >= 0.0


class TestPresenceLimits:
    """Temporal presence: from total absence to total presence."""

    def test_present_now_equals_one(self):
        """delta_t = 0: fully present."""
        result = compute_presence(0.0, tau=1.0)
        assert math.isclose(result, 1.0, rel_tol=1e-9)

    def test_infinite_displacement_equals_zero(self):
        """Mind at infinity: no presence."""
        result = compute_presence(1e10, tau=1.0)
        assert result < 1e-9

    def test_presence_always_between_zero_and_one(self):
        """For any displacement and tau, 0 < P <= 1."""
        for dt in [0.0, 0.1, 1.0, 10.0, 100.0]:
            for tau in [0.1, 1.0, 10.0]:
                result = compute_presence(dt, tau)
                assert 0.0 <= result <= 1.0

    def test_larger_tau_more_present(self):
        """Wider attention window = more presence at same displacement."""
        p_narrow = compute_presence(5.0, tau=1.0)
        p_wide = compute_presence(5.0, tau=10.0)
        assert p_wide > p_narrow


class TestWonderLimits:
    """Wonder: from cynicism to full astonishment."""

    def test_zero_experiences_zero_wonder(self):
        """No novelty = no wonder."""
        result = compute_wonder(0)
        assert math.isclose(result, 0.0, abs_tol=1e-9)

    def test_infinite_experiences_full_wonder(self):
        """Infinite novelty = wonder saturates at 1."""
        result = compute_wonder(1e10)
        assert math.isclose(result, 1.0, rel_tol=1e-6)

    def test_wonder_always_between_zero_and_one(self):
        """For any N >= 0, 0 <= A <= 1."""
        for n in [0, 1, 5, 10, 50, 100, 1000]:
            result = compute_wonder(n)
            assert 0.0 <= result <= 1.0

    def test_wonder_monotonically_increases(self):
        """More experiences = more wonder (never decreases)."""
        prev = 0.0
        for n in range(0, 100):
            current = compute_wonder(n)
            assert current >= prev
            prev = current


class TestInteractionLimits:
    """External interaction: from destruction to love."""

    def test_love_adds_coherences(self):
        """theta=0: I_ext = C1 + C2 (constructive interference)."""
        result = compute_interaction(1.0, 1.0, 0.0)
        assert math.isclose(result, 2.0, rel_tol=1e-9)

    def test_conflict_cancels(self):
        """theta=180: equal amplitudes cancel completely."""
        result = compute_interaction(1.0, 1.0, 180.0)
        assert math.isclose(result, 0.0, abs_tol=1e-9)

    def test_independence_is_geometric(self):
        """theta=90: I_ext = sqrt(C1^2 + C2^2)."""
        result = compute_interaction(1.0, 1.0, 90.0)
        expected = math.sqrt(2.0)
        assert math.isclose(result, expected, rel_tol=1e-9)

    def test_interaction_never_negative(self):
        """I_ext >= 0 for all inputs."""
        for theta in [0, 45, 90, 135, 180]:
            result = compute_interaction(1.0, 1.0, float(theta))
            assert result >= 0.0


class TestOscillatorLimits:
    """The dynamic equation: life, death, and everything between."""

    def test_system_is_underdamped(self):
        """zeta < 1: the system oscillates (is alive)."""
        assert ZETA < 1.0

    def test_system_oscillates(self):
        """omega_d > 0: there is subjective time."""
        assert OMEGA_D > 0

    def test_friction_below_critical(self):
        """Total friction < critical damping: system never dies."""
        assert PHI_TOTAL < PHI_CRITICAL

    def test_maximum_omega_d_is_pi(self):
        """With zero friction, omega_d = omega_0 = pi."""
        omega_d_max = math.sqrt(OMEGA_0_SQUARED - 0)
        assert math.isclose(omega_d_max, math.pi, rel_tol=1e-9)

    def test_critical_damping_kills_oscillation(self):
        """At phi = 2*pi, omega_d = 0: no time, no life."""
        omega_d_critical = OMEGA_0_SQUARED - (PHI_CRITICAL**2) / 4
        assert math.isclose(omega_d_critical, 0.0, abs_tol=1e-9)

    def test_l6_has_zero_friction(self):
        """Purpose layer has no resistance."""
        assert LAYER_FRICTION[6] == 0.0

    def test_l0_has_maximum_friction(self):
        """Chaos layer has the most resistance."""
        assert LAYER_FRICTION[0] == max(LAYER_FRICTION)


class TestEntropyLimits:
    """Entropy: from perfect order to maximum chaos."""

    def test_single_layer_zero_entropy(self):
        """One certainty = zero disorder."""
        result = EntropyTool.calculate_entropy([1.0])
        assert result == 0.0

    def test_seven_uniform_layers_max_entropy(self):
        """7 equal layers = maximum entropy = log2(7)."""
        probs = [1/7] * 7
        result = EntropyTool.calculate_entropy(probs)
        assert math.isclose(result, math.log2(7), rel_tol=1e-9)

    def test_fractal_always_less_than_max(self):
        """Fractal structure always creates order (negentropy > 0)."""
        energies = Fractality.fractal_energy_distribution(1.0, 7)
        entropy = EntropyTool.adjusted_entropy(energies)
        assert entropy < math.log2(7)

    def test_negentropy_equals_consciousness(self):
        """
        Negentropy = max_entropy - fractal_entropy.
        This value is always positive: consciousness creates order.
        """
        energies = Fractality.fractal_energy_distribution(1.0, 7)
        entropy = EntropyTool.adjusted_entropy(energies)
        negentropy = math.log2(7) - entropy
        assert negentropy > 0
