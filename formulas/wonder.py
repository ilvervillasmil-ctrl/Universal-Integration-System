import math


class WonderLogic:
    """
    Wonder/Awe: A = 1 - e^(-N/k)

    N = number of novel experiences
    k = saturation constant
    A -> 1 = beginner's mind (full wonder)
    A -> 0 = cynicism (structurally toxic)
    """

    @staticmethod
    def compute(novelty, sensitivity=5.0):
        """A = 1 - e^(-N/k)"""
        return 1.0 - math.exp(-max(0, novelty) / max(0.001, sensitivity))

    @staticmethod
    def from_state(curiosity=5, openness=5, routine=5):
        """Compute from human-readable values (0-10 scales)."""
        novelty = (curiosity + openness) / 2
        sensitivity = max(0.5, 10 - routine)
        return WonderLogic.compute(novelty, sensitivity)
