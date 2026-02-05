import math
from core.constants import S_REF

class WonderLogic:
    @staticmethod
    def compute_a(novelty: float, sensitivity: float = S_REF) -> float:
        """
        Formula: A = 1 - e^(-N/k)
        N = Novelty, k = Sensitivity constant.
        This represents the system's capacity to be surprised.
        
        Calibrated to use S_REF (e/π) as default sensitivity for resonance with universal constants.
        """
        if sensitivity <= 0:
            sensitivity = S_REF  # Use S_REF instead of 1.0 for universal alignment
        return 1.0 - math.exp(-abs(novelty) / sensitivity)