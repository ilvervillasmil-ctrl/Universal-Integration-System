import sys
import os

# Asegura que Python pueda encontrar el paquete src/
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.compute_coherence_metacube import cube_coherence, metacube_coherence

def test_simple_vs_metacube():
    base_cube = [
        {'L_i': 0.8, 'phi_i': 0.1, 'E_i': 1.0, 'f_i': 1.0},
        {'L_i': 0.7, 'phi_i': 0.2, 'E_i': 0.9, 'f_i': 0.95},
        {'L_i': 0.9, 'phi_i': 0.05, 'E_i': 0.97, 'f_i': 1.0},
        {'L_i': 0.6, 'phi_i': 0.08, 'E_i': 0.95, 'f_i': 0.98},
        {'L_i': 0.75, 'phi_i': 0.09, 'E_i': 0.99, 'f_i': 0.97},
        {'L_i': 0.73, 'phi_i': 0.04, 'E_i': 0.85, 'f_i': 1.0},
        {'L_i': 0.85, 'phi_i': 0.12, 'E_i': 0.87, 'f_i': 0.92},
    ]
    coh1 = cube_coherence(base_cube)
    coh2 = metacube_coherence([base_cube, base_cube], levels=2)
    assert coh2 <= coh1, "Metacube coherence should not exceed simple cube coherence by definition."

if __name__ == "__main__":
    test_simple_vs_metacube()
    print("Test passed: metacube coherence is bounded as expected.")
