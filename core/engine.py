import math
from typing import List, Dict
from functools import wraps
from core.constants import ALPHA, BETA, S_REF, get_layer_frequency, PHI

# Custom Exception for L6 Purpose Alignment
class PurposeAlignmentError(Exception):
    """Exception raised when L6 friction (phi) is not 0.0"""
    pass

def validate_L6_friction(func):
    """
    Decorator to validate that L6 (Purpose layer) has friction = 0.0
    Raises PurposeAlignmentError if L6 friction is not 0.0
    """
    @wraps(func)
    def wrapper(self, layers_data: List[Dict[str, float]], *args, **kwargs):
        # L6 is the last layer (index 6)
        if len(layers_data) >= 7:
            l6_friction = layers_data[6].get('phi', 0.0)
            if l6_friction != 0.0:
                raise PurposeAlignmentError(
                    f"L6 Purpose layer must have friction (phi) = 0.0, but got {l6_friction}"
                )
        return func(self, layers_data, *args, **kwargs)
    return wrapper


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
    
    def calculate_external_coherence(self, C1: float, C2: float, theta: float) -> float:
        """
        I_ext = √(C₁² + C₂² + 2·C₁·C₂·cos(θ))
        External coherence dependent on phase
        """
        import math
        cos_theta = math.cos(math.radians(theta))
        i_ext_squared = C1**2 + C2**2 + 2 * C1 * C2 * cos_theta
        return math.sqrt(max(0, i_ext_squared))  # Ensure non-negative
    
    def calculate_harmony(self, entropy: float, s_max: float = 1.0) -> float:
        """
        H(S) = 1 - S/S_max
        Harmony as a function of entropy
        """
        if s_max == 0:
            return 0.0
        return max(0, 1 - (entropy / s_max))

    @validate_L6_friction
    def compute_coherence(
        self, 
        layers_data: List[Dict[str, float]], 
        dispersion: float = 0.0,
        novelty: float = 0.5,
        C1: float = 0.5,
        C2: float = 0.5,
        theta: float = 0.0,
        s_max: float = None
    ) -> float:
        """
        Calculates C_Ω using the Villasmil-Ω advanced formula:
        C_Ω = α·H(S) + β·I_ext
        
        Where:
        - H(S) = 1 - S/S_max (harmony based on entropy)
        - I_ext = √(C₁² + C₂² + 2·C₁·C₂·cos(θ)) (external coherence)
        - Golden ratio (PHI) is used as a scaling factor
        
        The coherence is scaled by PHI for universal alignment.
        """
        # 1. Calculate Energies and Total Energy
        energies = []
        for i, data in enumerate(layers_data):
            e_i = self.calculate_layer_energy(data['L'], data['phi'], i)
            energies.append(e_i)
        
        total_energy = sum(energies)
        if total_energy == 0: return 0.0

        # 2. Entropy calculation (Shannon Entropy)
        entropy = 0.0
        for e_i in energies:
            p_i = e_i / total_energy
            if p_i > 0:
                entropy -= p_i * math.log(p_i, 7) # Log base 7 for 7 layers

        # 3. Calculate Harmony H(S) using the new formula
        # Use S_REF as s_max if not provided
        if s_max is None:
            s_max = S_REF
        harmony = self.calculate_harmony(entropy, s_max)

        # 4. Calculate External Coherence I_ext with phase dependency
        i_ext = self.calculate_external_coherence(C1, C2, theta)

        # 5. Apply Villasmil-Ω Master Formula
        # C_Ω = α·H(S) + β·I_ext
        c_omega = (ALPHA * harmony) + (BETA * i_ext)
        
        # 6. Scale with Golden Ratio (PHI) for universal alignment
        # PHI acts as a harmonic scaling factor to align layers with universal proportions
        c_omega_scaled = c_omega * (PHI / 2.0)  # Normalize by PHI/2 to keep values reasonable
        
        return min(c_omega_scaled, 1.0) # Clamping at 1.0 max
