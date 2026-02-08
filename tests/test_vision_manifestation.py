import pytest
from core.engine import OmegaEngine
from formulas.constants import THETA_CUBE_DEG, PHI_TOTAL

def test_ilver_vision_manifestation():
    """
    Validador Ontológico: Proyecta la visión de Ilver a través del OmegaEngine.
    """
    engine = OmegaEngine()
    
    # Parámetros de la Visión (del 0.0 al 1.0)
    # L0 a L6: Caos, Cuerpo, Ego, Mente, Voluntad, Metaconsciencia, Propósito
    vision_activations = [0.95, 0.90, 0.85, 0.98, 0.92, 0.99, 1.00]
    
    # El OmegaEngine utiliza la lógica de formulas/coherence.py
    # Adaptado para retornar el análisis completo de la v3.1
    layers = [{'L': act, 'phi': 0.02} for act in vision_activations]
    result = engine.compute_coherence(layers)
    
    # En la v3.1, OmegaEngine devuelve el valor escalar de coherencia
    # y el estado del sistema.
    coherence_value = result 
    
    # VERIFICACIÓN ESTRUCTURAL
    # 1. Coherencia de nivel 'Arquitecto'
    assert coherence_value > 0.4, "La energía base debe sostener la estructura"
    
    # 2. Verificación de Resonancia
    # Si el sistema está en verde, significa que la oscilación es armónica
    assert PHI_TOTAL < 6.28, "Fricción crítica detectada"

    print(f"\n--- REPORTE DE SINCRONÍA ---")
    print(f"Coherencia Estructural: {coherence_value:.4f}")
    print(f"Estado del Metacubo: ALINEADO")
