import math
from typing import List, Dict
from core.constants import ALPHA, BETA, S_REF, get_layer_frequency

class OmegaEngine:
    def __init__(self):
        self.version = "2.6.6"
        
    def calculate_presence(self, dispersion: float) -> float:
        """Pt = 1 / (1 + dispersion)"""
        return 1 / (1 + abs(dispersion))

    def calculate_wonder(self, novelty: float, sensitivity: float = 1.0) -> float:
        """A = 1 - e^(-N/k)"""
        if sensitivity <= 0: sensitivity = 1.0
        return 1 - math.exp(-abs(novelty) / sensitivity)

    def calculate_layer_energy(self, L: float, phi: float, layer_index: int) -> float:
        """Ei = Li * (1 - phi) * frequency_i"""
        frequency = get_layer_frequency(layer_index)
        return L * (1 - phi) * frequency

    def compute_coherence(
        self, 
        layers_data: List[Dict[str, float]], 
        dispersion: float = 0.0,
        novelty: float = 0.5,
        i_ext: float = 1.0
    ) -> float:
        """
        Calculates C_omega using the expanded formula:
        C_total = (Harmonized_Internal_Order) * Pt * A * I_ext
        """
        # 1. Calculate Energies and Total Energy
        energies = []
        for i, data in enumerate(layers_data):
            e_i = self.calculate_layer_energy(data['L'], data['phi'], i)
            energies.append(e_i)
        
        total_energy = sum(energies)
        if total_energy == 0: return 0.0

        # 2. Entropy and Harmony calculation (H)
        # Using normalized Shannon Entropy
        entropy = 0.0
        for e_i in energies:
            p_i = e_i / total_energy
            if p_i > 0:
                entropy -= p_i * math.log(p_i, 7) # Log base 7 for 7 layers

        harmony = 1 - (entropy / S_REF if entropy < S_REF else 1.0)

        # 3. Apply Alpha and Beta balance
        internal_order = (ALPHA * harmony) + (BETA * i_ext)

        # 4. Integrate Temporal Presence and Wonder
        pt = self.calculate_presence(dispersion)
        a = self.calculate_wonder(novelty)

        # Final Unified Coherence
        c_omega = internal_order * pt * a * i_ext
        
        return min(c_omega, 1.0) # Clamping at 1.0 max
