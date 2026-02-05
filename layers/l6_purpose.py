class LayerPurpose:
    def __init__(self):
        self.L = 0.0  # Initial magnitude
        self.phi = 0.0  # Always 0.0 as per Layer 6 (Purpose) law
        self.name = "Purpose"

    def activate(self, L, phi=0.0):
        """
        Sets specific values for the Purpose layer.
        Friction (phi) is forced to 0.0 in this layer.
        """
        self.L = L
        self.phi = 0.0  # Enforce phi to always remain 0.0

    def export(self):
        """
        Exports the layer's data for integration into the engine.
        """
        return {'L': self.L, 'phi': self.phi, 'name': self.name}
