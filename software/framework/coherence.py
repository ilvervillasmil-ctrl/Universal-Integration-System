import math

# Constants (set based on the Villasmil-Ω Framework)
ALPHA = 26 / 27  # Visible proportion
BETA = 1 / 27    # Invisible proportion
S_REF = math.e / math.pi  # Relationship of growth and cycles
R = 28 / 27  # Refinement capacity

# Function to calculate coherence
def compute_coherence(energy_levels, e0, rho=1, p_t=1, a=1, i_ext=1):
    """
    Calculates the total coherence C_Ω of the system
    based on provided energy levels and constants.

    Parameters:
        energy_levels (list): Energy activity levels of each layer [E1, E2, ..., E6]
        e0 (float): Base energy reference
        rho (float): Resilience/refinement constant (default=1)
        p_t (float): Phase transition factor (default=1)
        a (float): Amplification constant (default=1)
        i_ext (float): External entanglement (default=1)

    Returns:
        float: Total coherence C_Ω
    """
    # Product of energy levels divided by base energy level
    energy_product = math.prod([E / e0 for E in energy_levels])
    
    # Calculate the total coherence
    coherence = energy_product * (ALPHA / S_REF) * R * rho * p_t * a * i_ext
    return coherence
