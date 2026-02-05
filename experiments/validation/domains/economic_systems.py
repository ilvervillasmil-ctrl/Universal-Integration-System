"""
Economic Systems Domain Validator

Validates β using economic system measurements.
"""

import numpy as np
from typing import Dict, List, Optional
from ..synthetic_data import SyntheticSystemState


class EconomicSystemsValidator:
    """
    Validator for economic systems domain.
    
    Metrics:
    - Market coherence (volatility, correlation)
    - Supply chain efficiency
    - Systemic risk measures
    - Transaction network topology
    """
    
    def __init__(self, seed: Optional[int] = None):
        """Initialize validator"""
        self.domain_name = "Economic Systems"
        if seed is not None:
            np.random.seed(seed)
    
    def generate_dataset(
        self,
        n_samples: int = 200,
        market_types: Optional[List[str]] = None
    ) -> List[SyntheticSystemState]:
        """
        Generate synthetic economic coherence data.
        
        In a real implementation, this would:
        - Analyze market volatility patterns
        - Measure supply chain resilience
        - Track systemic risk indicators
        
        For now, we use synthetic data simulating these measurements.
        
        Args:
            n_samples: Number of measurement samples
            market_types: Types of markets to measure
            
        Returns:
            List of system states representing economic coherence
        """
        if market_types is None:
            market_types = ['equity', 'commodity', 'forex', 'crypto']
        
        # Synthetic: Economic systems have cycles and hidden dependencies
        # β represents latent systemic risks
        from ..synthetic_data import SyntheticDataGenerator
        
        generator = SyntheticDataGenerator(n_layers=7, seed=hash(self.domain_name) % (2**32))
        
        # Economic systems have moderate coherence with volatility
        states = generator.generate_mixed_coherence_states(
            beta=0.0291,
            n_samples=n_samples,
            coherence_range=(0.3, 0.8)  # Markets vary with conditions
        )
        
        return states
    
    def create_objective_function(self, states: List[SyntheticSystemState]) -> callable:
        """
        Create objective function for economic systems domain.
        
        Measures market coherence and systemic risk.
        """
        def objective(beta: float, data: np.ndarray) -> float:
            alpha = 1 - beta
            total_error = 0.0
            
            for state in states:
                n_layers = len(state.layer_energies)
                
                # Model: economic systems have visible and hidden dynamics
                # α = observable market activity
                # β = latent systemic risks and hidden dependencies
                
                predicted = np.zeros(n_layers)
                manifested_layers = int(alpha * n_layers)
                
                # Observable market layers
                for i in range(manifested_layers):
                    predicted[i] = alpha * np.exp(-i / n_layers)
                
                # Hidden systemic risk layers
                for i in range(manifested_layers, n_layers):
                    predicted[i] = beta * np.exp(-(i - manifested_layers) / 3)
                
                # Normalize
                total_pred = np.sum(predicted)
                if total_pred > 0:
                    predicted /= total_pred
                
                # MSE
                error = np.mean((predicted - state.layer_energies) ** 2)
                total_error += error
            
            return total_error / len(states)
        
        return objective
