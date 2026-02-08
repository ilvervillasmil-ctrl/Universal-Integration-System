import math
from .constants import (
    ALPHA, BETA, S_REF, R_FIN, KAPPA, THETA_CUBE,
    ALPHA_OVER_S, NUM_LAYERS, LAYER_FRICTION,
    CODE_INTEGRATED, CODE_SATURATION, CODE_ENTROPY
)
from .energy import LayerEnergy
from .negentropy import NegentropyCalculator
from .presence import PresenceLogic
from .wonder import WonderLogic
from .interaction import ExternalInteraction
from .resonance import ResonanceLogic
from .metaconsciousness import MetaconsciousnessCalculator


class CoherenceEngine:
    """
    UCF v3.0 Master Coherence Formula

    Coherence is a VECTOR, not a scalar.

    C_beta = coherence LIVED (from the center, multiplicative)
    C_alpha = coherence MEASURED (from the exterior, ratio)
    C_total = sqrt(C_beta^2 + C_alpha^2)

    theta_cube = arcsin(1/sqrt(27)) = 11.09 degrees
    sin^2(theta) = beta = 1/27
    cos^2(theta) = alpha = 26/27
    """

    @staticmethod
    def compute_c_beta(
        activations,
        frictions=None,
        rho=1.0,
        delta_t=0.0,
        tau=1.0,
        novelty=5.0,
        sensitivity=5.0,
        external_coherences=None,
    ):
        """
        C_beta = [product(Ei/E0)] * (alpha/S) * R * rho * P_t * A * I_ext

        MULTIPLICATIVE: if any layer is zero, everything collapses.
        This is the EXPERIENCE of coherence.
        """
        if frictions is None:
            frictions = LAYER_FRICTION

        energies = LayerEnergy.compute_all(activations, frictions)
        e_0 = LayerEnergy.frequency(0)

        product = 1.0
        for e in energies:
            product *= (e / e_0) if e_0 > 0 else 0

        p_t = PresenceLogic.compute(delta_t, tau)
        a = WonderLogic.compute(novelty, sensitivity)

        if external_coherences and len(external_coherences) > 0:
            i_ext = ExternalInteraction.compute_multi(external_coherences)
        else:
            i_ext = 1.0

        c_beta = product * ALPHA_OVER_S * R_FIN * rho * p_t * a * i_ext

        return {
            "c_beta": c_beta,
            "energies": energies,
            "product": product,
            "alpha_over_s": ALPHA_OVER_S,
            "r_fin": R_FIN,
            "rho": rho,
            "p_t": p_t,
            "wonder": a,
            "i_ext": i_ext,
        }

    @staticmethod
    def compute_c_alpha(integration, quality, complexity, uncertainty):
        """
        C_alpha = I(A,O) * Q(I) / (D + U + U_min)

        RATIO: as complexity grows, coherence decreases.
        This is the AUDIT of coherence.
        """
        u_min = BETA
        denominator = complexity + uncertainty + u_min
        c_alpha = (integration * quality) / denominator if denominator > 0 else 0.0

        return {
            "c_alpha": c_alpha,
            "integration": integration,
            "quality": quality,
            "complexity": complexity,
            "uncertainty": uncertainty,
            "u_min": u_min,
        }

    @staticmethod
    def compute_c_total(c_beta, c_alpha):
        """
        C_total = sqrt(C_beta^2 + C_alpha^2)

        C_beta  = C_total * sin(theta_cube)
        C_alpha = C_total * cos(theta_cube)
        """
        c_total = math.sqrt(c_beta**2 + c_alpha**2)

        if c_alpha > 0:
            theta_actual = math.atan(c_beta / c_alpha)
        elif c_beta > 0:
            theta_actual = math.pi / 2
        else:
            theta_actual = 0.0

        theta_deviation = theta_actual - THETA_CUBE

        if abs(theta_deviation) < 0.01:
            balance = "CENTERED"
        elif theta_deviation > 0:
            balance = "EXCESS_EXPERIENCE"
        else:
            balance = "EXCESS_MEASUREMENT"

        c_beta_ideal = c_total * math.sin(THETA_CUBE)
        c_alpha_ideal = c_total * math.cos(THETA_CUBE)

        return {
            "c_total": c_total,
            "c_beta": c_beta,
            "c_alpha": c_alpha,
            "theta_actual": theta_actual,
            "theta_actual_deg": math.degrees(theta_actual),
            "theta_cube": THETA_CUBE,
            "theta_cube_deg": math.degrees(THETA_CUBE),
            "theta_deviation": theta_deviation,
            "theta_deviation_deg": math.degrees(theta_deviation),
            "balance": balance,
            "c_beta_ideal": c_beta_ideal,
            "c_alpha_ideal": c_alpha_ideal,
        }

    @staticmethod
    def compute_basic(energies, i_ext=1.0):
        """
        C = alpha * H(S) + beta * I_ext
        96.3% internal harmony + 3.7% external sync
        """
        harmony = NegentropyCalculator.harmony(energies)
        c_omega = ALPHA * harmony + BETA * i_ext
        return {"c_omega": c_omega, "harmony": harmony, "i_ext": i_ext}

    @staticmethod
    def full_analysis(
        activations,
        frictions=None,
        rho=1.0,
        delta_t=0.0,
        tau=1.0,
        novelty=5.0,
        sensitivity=5.0,
        external_coherences=None,
        integration=0.5,
        quality=0.5,
        complexity=1.0,
        uncertainty=0.1,
    ):
        """Complete coherence analysis: C_beta + C_alpha + C_total + diagnostics."""
        if frictions is None:
            frictions = LAYER_FRICTION

        beta_r = CoherenceEngine.compute_c_beta(
            activations, frictions, rho, delta_t, tau,
            novelty, sensitivity, external_coherences
        )
        alpha_r = CoherenceEngine.compute_c_alpha(
            integration, quality, complexity, uncertainty
        )
        total_r = CoherenceEngine.compute_c_total(
            beta_r["c_beta"], alpha_r["c_alpha"]
        )

        energies = beta_r["energies"]
        mc = MetaconsciousnessCalculator.compute(activations, frictions)

        c = total_r["c_total"]
        if c >= ALPHA:
            code, name = CODE_INTEGRATED, "Integrated Architect"
        elif c >= 0.4:
            code, name = CODE_SATURATION, "Critical Saturation"
        else:
            code, name = CODE_ENTROPY, "Terminal Entropy"

        return {
            "c_beta": beta_r,
            "c_alpha": alpha_r,
            "c_total": total_r,
            "negentropy": NegentropyCalculator.compute(energies),
            "metaconsciousness": mc,
            "mc_level": MetaconsciousnessCalculator.level_name(mc),
            "resonance": ResonanceLogic.compute(energies),
            "diagnostic_code": code,
            "diagnostic_name": name,
            "four_pillars": {
                "beta": BETA,
                "kappa": KAPPA,
                "alpha": ALPHA,
                "emergence": sum(energies) * (1 - KAPPA) / 2,
            },
        }

    @staticmethod
    def metacube_level(c_total, level=0):
        """
        Fractal recursion: our cube is beta of the metacube.
        What is 'everything' for us is only 'the observer' for the next level.
        """
        return {
            "level": level,
            "c_total_here": c_total,
            "is_beta_of_level": level + 1,
            "ratio_alpha_beta": ALPHA / BETA,
        }
