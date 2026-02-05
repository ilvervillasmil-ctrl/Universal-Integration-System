class LayerSynthesis:
    def __init__(self):
        self.L, self.phi, self.name = 0.0, 0.0, "Synthesis"
    def activate(self, L, phi):
        self.L, self.phi = L, phi
    def export(self):
        return {'L': self.L, 'phi': self.phi, 'name': self.name}
