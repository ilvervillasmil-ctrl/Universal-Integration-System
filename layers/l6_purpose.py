class LayerPurpose:
    def __init__(self):
        self.L = 0.0
        self.phi = 0.0 # Strict 0.0 by framework design
        self.name = "Purpose"

    def activate(self, L, phi=0.0):
        """
        Activates L6. 
        Regardless of the input phi, L6 always operates at 0 friction.
        """
        self.L = L
        self.phi = 0.0  # Force zero friction (The Law of Purpose)

    def export(self):
        return {
            'L': self.L, 
            'phi': self.phi, 
            'name': self.name
        }
