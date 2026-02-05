"""
Human Psychology Domain Validator

Validates β using psychological state measurements.
"""

import numpy as np
from typing import Dict, List, Optional
from ..synthetic_data import SyntheticSystemState


class HumanPsychologyValidator:
    """
    Validator for human psychology domain.
    
    Metrics:
    - EEG patterns during meditation
    - Flow state measurements
    - Therapeutic progress indicators
    - Self-reported coherence
    """
    
    def __init__(self, seed: Optional[int] = None):
        """Initialize validator"""
        self.domain_name = "Human Psychology"
        if seed is not None:
            np.random.seed(seed)
    
    def generate_dataset(
        self,
        n_samples: int = 200,
        states: Optional[List[str]] = None
    ) -> List[SyntheticSystemState]:
        """
        Generate synthetic psychological coherence data.
        
        In a real implementation, this would:
        - Analyze EEG data from meditation sessions
        - Measure flow state characteristics
        - Track therapy session outcomes
        
        For now, we use synthetic data simulating these measurements.
        
        Args:
            n_samples: Number of measurement samples
            states: Types of psychological states to measure
            
        Returns:
            List of system states representing psychological coherence
        """
        if states is None:
            states = ['meditation', 'flow', 'therapy', 'baseline']
        
        # Synthetic: Human psychology shows high variability
        # but coherent states cluster around characteristic β
        from ..synthetic_data import SyntheticDataGenerator
        
        generator = SyntheticDataGenerator(n_layers=7, seed=hash(self.domain_name) % (2**32))
        
        # Generate mixed coherence (humans vary widely)
        dataset = generator.generate_mixed_coherence_states(
            beta=0.0291,  # Hypothesis: same β as other domains
            n_samples=n_samples,
            coherence_range=(0.2, 0.85)  # Wide range for human variability
        )
        
        return dataset
    
    def create_objective_function(self, states: List[SyntheticSystemState]) -> callable:
        """
        Create objective function for psychology domain.
        
        Measures coherence across psychological layers.
        """
        def objective(beta: float, data: np.ndarray) -> float:
            alpha = 1 - beta
            total_error = 0.0
            
            for state in states:
                n_layers = len(state.layer_energies)
                
                # Model: consciousness has manifest and unmanifest aspects
                # α = conscious processing
                # β = unconscious/latent processing
                
                predicted = np.zeros(n_layers)
                manifested_layers = int(alpha * n_layers)
                
                # Conscious layers
                for i in range(manifested_layers):
                    predicted[i] = alpha * np.exp(-i / n_layers)
                
                # Unconscious/latent layers
                for i in range(manifested_layers, n_layers):
                    predicted[i] = beta * np.exp(-(i - manifested_layers) / 3)
                
                # Normalize
                total_pred = np.sum(predicted)
                if total_pred > 0:
                    predicted /= total_pred
                
                # MSE weighted by coherence (more coherent states = more reliable)
                weight = state.coherence
                error = weight * np.mean((predicted - state.layer_energies) ** 2)
                total_error += error
            
            # Normalize by sum of weights
            total_weight = sum(s.coherence for s in states)
            return total_error / total_weight if total_weight > 0 else total_error / len(states)
        
        return objective
