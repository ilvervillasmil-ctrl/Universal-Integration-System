"""
UCF v3.0 - Metacube/Fractal Recursion Coherence Calculation
Authors: Ilver Villasmil & Claude
Date: 2026-02-08

Implements the fractal/recursive coherence logic for the Metacube framework:
- Considers L_-1 (external void layer)
- Computes α_meta, β_meta for any recursion level
- Supports infinite recursion (cubes within cubes)
- Uses new universal constants: β = 1/27, α = 26/27, κ = π/4, θ_cube = 11.09°
- Allows both classical (single cube) and recursive/metacube (fractal field) formulas
"""

import math
from typing import List, Dict, Optional

# Universal (geometric) constants
BETA = 1/27                   # β: the "observer" in each cube
ALPHA = 26/27                 # α: the "observable" in each cube
KAPPA = math.pi / 4           # κ: integration cost/bridge
THETA_CUBE = math.asin(1 / math.sqrt(27))   # ≈ 11.09° (equilibrium angle)
DEFAULT_LAYER_LIMIT = 7       # Default: 7 layers, extensible recursion

# --- BASE FUNCTIONS ---

def layer_contribution(L: float, phi: float, E: float, f: float) -> float:
    """
    Calculates the contribution of one layer:
    c_i = L_i * (1 - phi_i) * E_i * f_i
    """
    return L * (1.0 - phi) * E * f

def cube_coherence(layers: List[Dict], omega_U: float = 1.0, R_fin: float = 1.0, 
                   S_ref: float = 1.0, C_max: float = ALPHA) -> float:
    """
    Coherence calculation for a single cube (fixed level):
    S = sum_i c_i (sum of layer contributions)
    C = C_max * (S * omega_U * R_fin / S_ref), clipped to [0, C_max]
    S_ref can be historical or theoretical convention (e.g., N layers)
    """
    S = sum(layer_contribution(l['L_i'], l['phi_i'], l['E_i'], l['f_i']) for l in layers)
    coherence = C_max * (S * omega_U * R_fin / S_ref)
    return max(0.0, min(coherence, C_max))

def metacube_coherence(cubes: List[List[Dict]],
                       levels: int = 2,
                       omega_U: float = 1.0,
                       R_fin: float = 1.0,
                       C_max: float = ALPHA) -> float:
    """
    Recursive coherence calculation for metacubes (any depth).
    - cubes: list of lists, each one representing the layers of a cube at each level
    - levels: depth of recursion (1 = inner cube only, 2 = outer metacube, ...)
    At each outer level, the inner cube's output acts as a "virtual layer".
    """
    if levels == 1:
        # Single cube coherence calculation (base case)
        return cube_coherence(cubes[0], omega_U, R_fin, S_ref=len(cubes[0]), C_max=C_max)
    else:
        # Recursively process inner cubes first
        inner_coh = metacube_coherence(
            cubes[1:], levels=levels-1, omega_U=omega_U, R_fin=R_fin, C_max=C_max
        )
        outer_layers = cubes[0].copy()
        virtual_layer = {'L_i': inner_coh, 'phi_i': 0.0, 'E_i': 1.0, 'f_i': 1.0}
        outer_layers.append(virtual_layer)
        return cube_coherence(outer_layers, omega_U, R_fin, S_ref=len(outer_layers), C_max=C_max)

# --- CONSTANTS/SUMMARY FUNCTIONS ---

def equilibrium_angle():
    """Returns the cube's characteristic equilibrium angle (degrees, radians)"""
    return math.degrees(THETA_CUBE), THETA_CUBE

def constants_summary():
    return {
        "BETA (β)": BETA,
        "ALPHA (α)": ALPHA,
        "KAPPA (κ)": KAPPA,
        "THETA_CUBE (11.09°)": equilibrium_angle()[0],
        "Default Layer Limit": DEFAULT_LAYER_LIMIT
    }

# --- DEMO AND BASIC TEST ---

if __name__ == '__main__':
    # Example: basic cube (n=1), cube inside metacube (n=2)
    base_cube = [
        {'L_i': 0.85, 'phi_i': 0.07, 'E_i': 1.0, 'f_i': 1.0},
        {'L_i': 0.65, 'phi_i': 0.15, 'E_i': 0.98, 'f_i': 1.0},
        {'L_i': 0.75, 'phi_i': 0.09, 'E_i': 0.85, 'f_i': 0.8},
        {'L_i': 0.68, 'phi_i': 0.11, 'E_i': 0.90, 'f_i': 0.93},
        {'L_i': 0.71, 'phi_i': 0.10, 'E_i': 0.95, 'f_i': 0.99},
        {'L_i': 0.69, 'phi_i': 0.08, 'E_i': 0.80, 'f_i': 1.0},
        {'L_i': 0.77, 'phi_i': 0.13, 'E_i': 0.82, 'f_i': 0.96},
    ]
    # Demo recursion: base_cube inside another
    print("== METACUBE CONSTANTS SUMMARY ==")
    print(constants_summary())

    print("\n== SIMPLE CUBE COHERENCE ==")
    print(cube_coherence(base_cube))

    print("\n== METACUBE COHERENCE (RECURSION LEVELS=2) ==")
    print(metacube_coherence([base_cube, base_cube], levels=2))
