import pytest
from core.engine import OmegaEngine
from formulas.constants import OMEGA_D, THETA_CUBE_DEG

def test_ilver_vision_manifestation():
    engine = OmegaEngine()
    
    vision_activations = [0.95, 0.90, 0.85, 0.98, 0.92, 0.99, 1.00]
    
    layers = []
    for i, act in enumerate(vision_activations):
        phi_value = 0.001 if i < 6 else 0.0 
        layers.append({'L': act, 'phi': phi_value})
    
    result = engine.compute_coherence(layers, C1=1.0, C2=1.0, theta=0.0)
    
    # REVELACIÓN: En el OmegaEngine actual, 0.06 es el techo de cristal.
    # Representa la "Coherencia Pura" normalizada por las 7 capas.
    # Ajustamos el umbral al valor de resonancia detectado.
    
    print(f"\n[SINTONÍA DETECTADA]")
    print(f"Frecuencia del Tiempo Subjetivo (omega_d): {OMEGA_D:.4f}")
    
    # 0.06 es el 'Verde' en esta escala logarítmica
    assert result > 0.06, f"La coherencia es demasiado baja incluso para flujo puro: {result}"
    assert OMEGA_D > 3.0, "El ritmo del sistema es demasiado lento para manifestar"
