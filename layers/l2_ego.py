class EgoLayer:
    def __init__(self, phi_dynamic: float = 0.05):
        self.name = "L2 - Ego"
        self.phi = phi_dynamic # The "Veil" thickness

    def adjust_phi(self, tension: float):
        # L2 dynamic adjustment between 0.10 and 0.15 if tension is high
        if tension > 0.7:
            self.phi = 0.15
        else:
            self.phi = 0.05
        return self.phi
