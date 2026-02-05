class BodyLayer:
    def __init__(self):
        self.name = "L1 - Body"
        
    def calculate_integrity(self, hardware_health: float, energy_stability: float) -> float:
        # Average of physical factors
        return (hardware_health + energy_stability) / 2
