from core.engine import OmegaEngine
from core.diagnostics import DiagnosticSystem

def run_integration():
    engine = OmegaEngine()
    diag = DiagnosticSystem()

    # Simulation: Initializing system with sample data
    # L: Activation (0-1), phi: Friction (0-1)
    mock_layers = [
        {'L': 0.9, 'phi': 0.01}, # L0
        {'L': 0.85, 'phi': 0.02}, # L1
        {'L': 0.92, 'phi': 0.05}, # L2
        {'L': 0.88, 'phi': 0.03}, # L3
        {'L': 0.90, 'phi': 0.01}, # L4
        {'L': 0.87, 'phi': 0.01}, # L5
        {'L': 0.93, 'phi': 0.00}, # L6
    ]

    # Calculate Coherence
    result = engine.compute_coherence(
        layers_data=mock_layers,
        dispersion=0.05, # High presence
        novelty=0.8,    # High wonder
        i_ext=0.981     # High synchronization
    )

    print(f"--- Universal Integration System v{engine.version} ---")
    print(f"Final Coherence (C_omega): {result:.4f}")
    print(f"Status: {diag.get_status_code(result)}")
    
    alerts = diag.check_layer_friction(mock_layers)
    for alert in alerts:
        print(alert)

if __name__ == "__main__":
    run_integration()
