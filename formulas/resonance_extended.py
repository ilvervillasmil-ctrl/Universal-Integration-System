import math

class AdvancedResonance:
    @staticmethod
    def multi_layer_resonance(energies: list) -> float:
        """
        Computes the average resonance across multiple layers based on energy alignment.

        energies: List of energy levels for layers
        """
        if len(energies) < 2:
            return 0.0  # Not enough layers to calculate resonance
        total_resonance = 0
        for i in range(len(energies) - 1):
            energy_a, energy_b = energies[i], energies[i + 1]
            alignment = 1 - (abs(energy_a - energy_b) / max(energy_a, energy_b))
            total_resonance += alignment
        return total_resonance / (len(energies) - 1)

    @staticmethod
    def enhanced_phase_alignment(energy_a: float, energy_b: float, factor: float = 1.0) -> float:
        """
        Extended alignment formula with a scaling factor.
        """
        base_alignment = 1 - abs(energy_a - energy_b) / max(energy_a, energy_b)
        return base_alignment * factor
