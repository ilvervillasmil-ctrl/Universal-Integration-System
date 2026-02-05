import math

class WonderLogic:
    @staticmethod
    def compute_a(novelty: float, sensitivity: float = 1.0) -> float:
        """
        Formula: A = 1 - e^(-N/k)
        N = Novelty, k = Sensitivity constant.
        This represents the system's capacity to be surprised.
        """
        if sensitivity <= 0:
            sensitivity = 1.0  # Ensure sensitivity is positive
        return 1.0 - math.exp(-abs(novelty) / sensitivity)
