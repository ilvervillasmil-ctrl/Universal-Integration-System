import math

KAPPA = math.pi / 4            # Universal integration constant (π/4)
R_FIN = 1.0                    # Final radius reference (change as required)
THETA_CUBE = math.asin(1 / math.sqrt(27))  # Cube equilibrium angle (≈11.09°)
GOLDEN_ANG = (math.pi * (math.sqrt(5) - 1)) / 2   # Golden angle for fractal systems
TAN_THETA = math.tan(THETA_CUBE)             # Tangent of equilibrium angle

ALPHA = 26/27                  # Observable ratio
BETA = 1/27                    # Observer ratio
