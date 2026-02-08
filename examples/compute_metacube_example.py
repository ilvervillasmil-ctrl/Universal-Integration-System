"""
Example script for UCF v3.0 Metacube Coherence Calculation

Shows:
- How to calculate coherence for a single cube and a recursive metacube
- How to model virtual layers and fractal field extension
- How to print constants and result interpretations
"""

from src.compute_coherence_metacube import cube_coherence, metacube_coherence, constants_summary

def main():
    # Example: 7 layers typical cube (values can be replaced/adapted as needed)
    base_cube = [
        {'L_i': 0.88, 'phi_i': 0.06, 'E_i': 1.00, 'f_i': 1.00},
        {'L_i': 0.66, 'phi_i': 0.14, 'E_i': 0.96, 'f_i': 1.00},
        {'L_i': 0.72, 'phi_i': 0.08, 'E_i': 0.90, 'f_i': 0.85},
        {'L_i': 0.70, 'phi_i': 0.10, 'E_i': 0.92, 'f_i': 0.98},
        {'L_i': 0.74, 'phi_i': 0.09, 'E_i': 0.93, 'f_i': 1.00},
        {'L_i': 0.68, 'phi_i': 0.07, 'E_i': 0.81, 'f_i': 0.99},
        {'L_i': 0.78, 'phi_i': 0.12, 'E_i': 0.83, 'f_i': 0.95},
    ]

    print("--- METACUBE CONSTANTS SUMMARY ---")
    print(constants_summary())
    print()

    # Simple (level 1)
    simple_coh = cube_coherence(base_cube)
    print("Coherence for single cube (level 1):", f"{simple_coh:.4f}")

    # Recursive (level 2: metacube = outer cube adds virtual layer from inner cube)
    recursive_coh = metacube_coherence([base_cube, base_cube], levels=2)
    print("Coherence for metacube recursion (level 2):", f"{recursive_coh:.4f}")
    print()

    # Advanced: change inner/outer cubes, or go deeper into recursion

if __name__ == "__main__":
    main()
