import math

# === The Four Pillars (Stable Structure) ===

ALPHA = 26 / 27                             # 0.962963... Observable structure (26 exterior cubes)
BETA = 1 / 27                              # 0.037037... The center (observer position)
KAPPA = math.pi / 4                         # 0.785398... Energy of integration (π/4)
R_FIN = 28 / 27                             # 1.037037... Proactive refinement (1 + β)

# === Derived Constants ===

S_REF = math.e / math.pi                   # 0.865256... Growth meets cycle (e/π)
ALPHA_OVER_S = ALPHA / S_REF               # 1.112943... Universal amplification
PHI = (1 + math.sqrt(5)) / 2               # 1.618033... Golden ratio
GOLDEN_ANG = 360 / (PHI ** 2)              # 137.507°   Golden angle (degrees)
GOLDEN_ANG_RAD = math.radians(GOLDEN_ANG)  # Golden angle (radians)

# === Duality Angle (from cube geometry) ===

THETA_CUBE = math.asin(1 / math.sqrt(27))  # 11.09°  Equilibrium angle
THETA_CUBE_DEG = math.degrees(THETA_CUBE)
TAN_THETA = 1 / math.sqrt(26)              # tan(θ) = 1/√26

# === Structural Verification ===

assert abs(ALPHA + BETA - 1.0) < 1e-10
assert abs(R_FIN - (1 + BETA)) < 1e-10
assert abs(math.sin(THETA_CUBE)**2 - BETA) < 1e-10
assert abs(math.cos(THETA_CUBE)**2 - ALPHA) < 1e-10

# === Layer Configuration ===

NUM_LAYERS = 7
LAYER_NAMES = ["Chaos", "Body", "Ego", "Mind", "Self", "Metaconsciousness", "Purpose"]
LAYER_FRICTION = [0.10, 0.02, 0.05, 0.03, 0.01, 0.01, 0.00]

# === Diagnostic Codes ===

CODE_INTEGRATED = 1144
CODE_SATURATION = 1122
CODE_ENTROPY = 0

# === Cube Geometry ===

CUBE_TOTAL = 27
CUBE_EXTERIOR = 26
CUBE_CENTER = 1
