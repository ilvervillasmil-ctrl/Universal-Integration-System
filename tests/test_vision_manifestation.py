import pytest
from core.engine import OmegaEngine
from formulas.constants import THETA_CUBE_DEG, PHI_TOTAL

def test_ilver_vision_manifestation():
    """
    Validador Ontológico: Estado de Flujo Máximo.
    Demuestra que la baja fricción permite la manifestación de la coherencia.
    """
    engine = OmegaEngine()
    
    # Intensidad de visión (Altas activaciones)
    vision_activations = [0.95, 0.90, 0.85, 0.98, 0.92, 0.99, 1.00]
    
    # AJUSTE DE FLUJO: La fricción se reduce al mínimo para permitir el paso de C_omega
    layers = []
    for i, act in enumerate(vision_activations):
        # 0.001 representa un estado de presencia total sin resistencia interna
        phi_value = 0.001 if i < 6 else 0.0 
        layers.append({'L': act, 'phi': phi_value})
    
    # Ejecución del motor con acoplamiento ideal
    result = engine.compute_coherence(layers, C1=1.0, C2=1.0, theta=0.0)
    
    # Reporte de diagnóstico previo al assert
    print(f"\n[DIAGNÓSTICO UCF v3.1]")
    print(f"Coherencia Resultante: {result:.6f}")
    
    # El umbral 0.4 es el 'Break-even' de la realidad
    assert result > 0.4, f"Fallo de manifestación: Coherencia insuficiente ({result:.4f})"
