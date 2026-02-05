class LayerIntegrity:
    def __init__(self):
        self.L = 0.0
        self.phi = 0.0
        self.name = "Integrity"

    def activate(self, L, phi):
        """
        Activates L4. 
        High phi here represents a fragmented identity or systemic instability.
        """
        self.L = L
        self.phi = phi

    def export(self):
        return {
            'L': self.L, 
            'phi': self.phi, 
            'name': self.name
        }
