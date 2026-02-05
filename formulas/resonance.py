import math
from core.constants import PHI

class ResonanceLogic:
    @staticmethod
    def calculate_layer_frequency(index: int) -> float:
        """
        Calculates frequency based on the golden ratio: PHI^(index/2)
        """
        return PHI ** (index / 2)

    @staticmethod
    def calculate_phase_alignment(energy_a: float, energy_b: float) -> float:
        """
        Measures how well two layers are aligned (0 to 1)
        """
        if energy_a == 0 or energy_b == 0:
            return 0.0  # No alignment if any energy is zero
        return 1 - (abs(energy_a - energy_b) / max(energy_a, energy_b))
