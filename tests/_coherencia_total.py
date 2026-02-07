import math
import pandas as pd
from src.coherencia import estimate_beta_from_domain

ESTRUCTURA = 1.0 / 27.0
KAPPA = math.pi / 4.0
BETA_TEO = ESTRUCTURA * KAPPA
EPSILON = 0.0004  # 0.04%

def assert_coherencia_domain(path_csv: str):
    datos = pd.read_csv(path_csv)
    beta_emp = estimate_beta_from_domain(datos)
    rel_error = abs(beta_emp - BETA_TEO) / BETA_TEO
    assert rel_error < EPSILON, (
        f"Dominio {path_csv} error {rel_error:.8f} NO cumple la ley universal! "
        f"BETA empírico: {beta_emp:.8f} BETA teórico: {BETA_TEO:.8f}"
    )

def test_coherencia_ia():
    assert_coherencia_domain("data/ia_metrics.csv")
