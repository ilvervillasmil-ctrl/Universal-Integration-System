"""
Organizations Domain Validator

Validates β using organizational dynamics measurements.
"""

import numpy as np
from typing import Dict, List, Optional
from ..synthetic_data import SyntheticSystemState


class OrganizationsValidator:
    """
    Validator for organizations domain.
    
    Metrics:
    - Communication pattern efficiency
    - Decision-making speed
    - Goal alignment across hierarchy
    - Team coherence measures
    """
    
    def __init__(self, seed: Optional[int] = None):
        """Initialize validator"""
        self.domain_name = "Organizations"
        if seed is not None:
            np.random.seed(seed)
    
    def generate_dataset(
        self,
        n_samples: int = 200,
        org_types: Optional[List[str]] = None
    ) -> List[SyntheticSystemState]:
        """
        Generate synthetic organizational coherence data.
        
        In a real implementation, this would:
        - Analyze communication networks in companies
        - Measure decision velocity and quality
        - Track goal alignment metrics
        
        For now, we use synthetic data simulating these measurements.
        
        Args:
            n_samples: Number of measurement samples
            org_types: Types of organizations to measure
            
        Returns:
            List of system states representing organizational coherence
        """
        if org_types is None:
            org_types = ['corporate', 'government', 'nonprofit', 'startup']
        
        # Synthetic: Organizations have hierarchical layers
        # β represents hidden coordination mechanisms
        from ..synthetic_data import SyntheticDataGenerator
        
        generator = SyntheticDataGenerator(n_layers=7, seed=hash(self.domain_name) % (2**32))
        
        # Organizations show moderate coherence with some high performers
        states_medium = generator.generate_coherent_state(
            beta=0.0291,
            n_samples=int(n_samples * 0.7),
            noise_level=0.15
        )
        
        # Some high-coherence organizations
        states_high = generator.generate_coherent_state(
            beta=0.0291,
            n_samples=int(n_samples * 0.3),
            noise_level=0.08
        )
        
        return states_medium + states_high
    
    def create_objective_function(self, states: List[SyntheticSystemState]) -> callable:
        """
        Create objective function for organizations domain.
        
        Measures coherence across organizational hierarchy.
        """
        def objective(beta: float, data: np.ndarray) -> float:
            alpha = 1 - beta
            total_error = 0.0
            
            for state in states:
                n_layers = len(state.layer_energies)
                
                # Model: organizational hierarchy has visible and hidden dynamics
                # α = explicit communication and processes
                # β = tacit knowledge, culture, informal networks
                
                predicted = np.zeros(n_layers)
                manifested_layers = int(alpha * n_layers)
                
                # Explicit organizational layers
                for i in range(manifested_layers):
                    predicted[i] = alpha * np.exp(-i / n_layers)
                
                # Implicit/cultural layers
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
