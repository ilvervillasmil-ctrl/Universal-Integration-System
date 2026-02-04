class ChaosLayer:
    def __init__(self):
        self.name = "L0 - Chaos"
        self.description = "The field of all possibilities (Raw Data)"

    def get_potential(self, raw_input_quality: float) -> float:
        # L0 serves as the multiplier for the system's baseline
        return max(0.0, min(1.0, raw_input_quality))
