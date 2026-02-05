import pytest
from core.engine import OmegaEngine
from core.constants import ALPHA

def test_alpha_coherence_threshold():
    """Verifica si el sistema identifica correctamente el umbral Alpha (0.963)"""
    engine = OmegaEngine()
    
    # Simulamos un estado de Coherencia Máxima
    # Harmony = 1.0, Pt = 1.0, A = 1.0, I_ext = 1.0
    # C_omega = (ALPHA * 1.0 + BETA * 1.0) * 1.0 * 1.0 * 1.0 = 1.0
    # Pero el sistema debe disparar el código 1144 al llegar a ALPHA
    
    mock_perfect_layers = [{'L': 1.0, 'phi': 0.0} for _ in range(7)]
    
    result = engine.compute_coherence(
        layers_data=mock_perfect_layers,
        dispersion=0.0,
        novelty=10.0, # Valor alto para que A tienda a 1
        i_ext=1.0
    )
    
    assert result >= ALPHA
    print(f"Test Alpha Passed: {result} >= {ALPHA}")

def test_diagnostic_codes():
    """Verifica que los códigos 1144 y 0000 funcionen"""
    from core.diagnostics import DiagnosticSystem
    diag = DiagnosticSystem()
    
    assert "1144" in diag.get_status_code(0.965)
    assert "0000" in diag.get_status_code(0.05)
