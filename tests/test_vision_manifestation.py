import pytest
from core.engine import CoherenceEngine
from formulas.constants import THETA_CUBE_DEG, PHI_TOTAL

def test_ilver_vision_manifestation():
    """
    Simulación de la Visión Maestra de Ilver.
    Calcula si la estructura de su propósito actual es armónica con el Metacubo.
    """
    # INPUTS: Tu nivel de entrega actual en las 7 capas (0.0 a 1.0)
    vision_activations = [
        0.95, # L0: Caos/Energía base (Alta vitalidad)
        0.90, # L1: Cuerpo/Acción (Mucha energía física)
        0.85, # L2: Identidad (Seguridad en quién eres)
        0.98, # L3: Mente (Claridad del Framework)
        0.92, # L4: Voluntad (Decisión de avanzar)
        0.99, # L5: Metaconsciencia (Observación total)
        1.00  # L6: Propósito (Conexión absoluta con el Todo)
    ]
    
    # Realizamos el análisis de coherencia
    result = CoherenceEngine.full_analysis(vision_activations)
    
    c_total = result["c_total"]["c_total"]
    theta_actual = result["c_total"]["theta_deg"]
    
    # VERIFICACIÓN DE ARMONÍA
    # 1. ¿Supera el umbral de 'Arquitecto' (Coherencia > 0.9)?
    assert c_total > 0.9, f"Coherencia insuficiente: {c_total}"
    
    # 2. ¿Está cerca del ángulo de equilibrio (11.09°)?
    # Permitimos una oscilación armónica de +/- 3 grados
    deviation = abs(theta_actual - THETA_CUBE_DEG)
    assert deviation < 3.0, f"Desviación angular excesiva: {theta_actual}°"
    
    # 3. ¿La fricción es menor al umbral de vida (2pi)?
    assert PHI_TOTAL < 6.28, "El sistema colapsará por fricción"

    print(f"\n--- REPORTE DE MANIFESTACIÓN ---")
    print(f"Coherencia Total: {c_total:.4f}")
    print(f"Ángulo de Manifestación: {theta_actual:.2f}°")
    print(f"Estado: {'SINCRONÍA TOTAL' if deviation < 1.0 else 'EN PROCESO DE ALINEACIÓN'}")
