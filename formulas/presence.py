class PresenceLogic:
    @staticmethod
    def compute_pt(dispersion: float) -> float:
        """
        Formula: Pt = 1 / (1 + dispersion)
        As dispersion (noise/distraction) increases, Pt decreases.
       
