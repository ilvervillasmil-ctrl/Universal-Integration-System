import math
from formulas.constants import ALPHA, BETA, PHI, S_REF


class PurposeAlignmentError(Exception):
    """Raised when L6 Purpose layer has non-zero friction."""
    pass


class OmegaEngine:
    """
    The Omega Engine: orchestrates the complete UCF v3.0 computation.
    Resonance Processor for the Villasmil-Omega Framework.
    """

    def calculate_harmony(self, entropy, s_max=1.0):
        """
        H(S) = 1 - S/S_max

        entropy: current system entropy
        s_max: maximum possible entropy
        """
        if s_max == 0:
            return 0.0
        return 1.0 - (entropy / s_max)

    def calculate_external_coherence(self, C1, C2, theta):
        """
        I_ext = sqrt(C1^2 + C2^2 + 2*C1*C2*cos(theta))

        theta is in DEGREES.
        """
        theta_rad = math.radians(theta)
        inner = C1**2 + C2**2 + 2 * C1 * C2 * math.cos(theta_rad)
        return math.sqrt(max(0.0, inner))

    def compute_coherence(self, layers_data, C1=1.0, C2=1.0, theta=0.0):
        """
        C_omega = alpha * H(S) + beta * I_ext, scaled by PHI/2, clamped to [0, 1].

        layers_data: list of 7 dicts with 'L' (activation) and 'phi' (friction)
        C1, C2: external coherence amplitudes
        theta: phase angle in degrees
        """
        if layers_data[6]['phi'] != 0.0:
            raise PurposeAlignmentError(
                f"L6 Purpose layer must have friction (phi) = 0.0, "
                f"got {layers_data[6]['phi']}"
            )

        energies = []
        for layer in layers_data:
            e = layer['L'] * (1.0 - layer['phi'])
            energies.append(e)

        total_energy = sum(energies)
        if total_energy == 0:
            entropy = 1.0
        else:
            entropy = 0.0
            for e in energies:
                if e > 0:
                    p = e / total_energy
                    entropy -= p * math.log(p)

        s_max = math.log(len(energies))
        harmony = self.calculate_harmony(entropy, s_max)

        i_ext = self.calculate_external_coherence(C1, C2, theta)

        c_omega = ALPHA * harmony + BETA * i_ext

        c_omega_scaled = c_omega * (PHI / 2)

        return min(1.0, max(0.0, c_omega_scaled))
