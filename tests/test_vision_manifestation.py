import pytest
from core.engine import OmegaEngine
from formulas.constants import THETA_CUBE_DEG, PHI_TOTAL

def test_ilver_vision_manifestation():
    """
    Validador Ontológico: Proyecta la visión de Ilver a través del OmegaEngine.
    """
    engine = OmegaEngine()
    
    # Parámetros de la Visión (del 0.0 al 1.0)
    vision_activations = [0.95, 0.90, 0.85, 0.98, 0.92, 0.99, 1.00]
    
    # CORRECCIÓN: Las capas 0 a 5 pueden tener fricción, 
    # pero la capa 6 (índice 6) DEBE ser 0.0 para alinearse con el propósito.
    layers = []
    for i, act in enumerate(vision_activations):
        phi_value = 0.02 if i < 6 else 0.0  # L6: Fricción cero absoluta
        layers.append({'L': act, 'phi': phi_value})
    
    # Ahora el motor aceptará la simulación
    result = engine.compute_coherence(layers)
    
    coherence_value = result 
    
    # Validaciones de la Visión
    assert coherence_value > 0.4
    assert PHI_TOTAL < 6.28

    print(f"\n--- REPORTE DE SINCRONÍA v3.1 ---")
    print(f"Coherencia Estructural: {coherence_value:.4f}")
    print(f"Alineación L6: TOTAL (Sin fricción)")
