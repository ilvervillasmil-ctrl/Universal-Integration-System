"""
Synthetic Data Generation for Beta Validation

This module generates synthetic multi-layer system states with
controllable β parameter for testing the validation framework.
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class SyntheticSystemState:
    """Represents a synthetic multi-layer system state"""
    layer_energies: np.ndarray  # Energy level for each layer
    beta_true: float  # True β used to generate data
    alpha_true: float  # True α (should be 1 - β)
    coherence: float  # Overall system coherence
    noise_level: float  # Amount of noise added
    
    def to_dict(self) -> Dict:
        return {
            'layer_energies': self.layer_energies.tolist(),
            'beta_true': self.beta_true,
            'alpha_true': self.alpha_true,
            'coherence': self.coherence,
            'noise_level': self.noise_level
        }


class SyntheticDataGenerator:
    """
    Generate synthetic data for validating the β optimization framework.
    
    The generator creates multi-layer systems with known β values,
    allowing us to test whether the optimizer can recover the true β.
    """
    
    def __init__(self, n_layers: int = 7, seed: Optional[int] = None):
        """
        Initialize generator.
        
        Args:
            n_layers: Number of layers in the system (default: 7 for Villasmil-Ω)
            seed: Random seed for reproducibility
        """
        self.n_layers = n_layers
        if seed is not None:
            np.random.seed(seed)
    
    def generate_coherent_state(
        self,
        beta: float,
        n_samples: int = 100,
        noise_level: float = 0.1
    ) -> List[SyntheticSystemState]:
        """
        Generate coherent system states with specified β.
        
        The model:
        - α fraction of energy goes to manifested layers (visible structure)
        - β fraction goes to unmanifest potential (hidden dynamics)
        - Higher coherence when layers are aligned
        
        Args:
            beta: True β value to use
            n_samples: Number of system states to generate
            noise_level: Amount of random noise (0 = perfect, 1 = very noisy)
            
        Returns:
            List of SyntheticSystemState objects
        """
        alpha = 1 - beta
        states = []
        
        for _ in range(n_samples):
            # Base energy distributed across layers
            # Layers follow a resonance pattern with some controlled by β
            layer_energies = np.zeros(self.n_layers)
            
            # Manifested layers (α portion)
            manifested_layers = int(alpha * self.n_layers)
            for i in range(manifested_layers):
                # Energy decays with layer depth
                layer_energies[i] = alpha * np.exp(-i / self.n_layers) * (1 + noise_level * np.random.randn())
            
            # Unmanifested potential (β portion)
            # This creates hidden coherence that affects system dynamics
            hidden_energy = beta * (1 + noise_level * np.random.randn())
            
            # Hidden energy influences deeper layers
            for i in range(manifested_layers, self.n_layers):
                layer_energies[i] = hidden_energy * np.exp(-(i - manifested_layers) / 3)
            
            # Ensure non-negative energies
            layer_energies = np.maximum(layer_energies, 0)
            
            # Normalize total energy to 1
            total_energy = np.sum(layer_energies)
            if total_energy > 0:
                layer_energies /= total_energy
            
            # Calculate coherence (how aligned the layers are)
            # Higher coherence when energy distribution matches α/β split
            expected_alpha_energy = alpha
            actual_alpha_energy = np.sum(layer_energies[:manifested_layers])
            coherence = 1 - abs(expected_alpha_energy - actual_alpha_energy)
            
            states.append(SyntheticSystemState(
                layer_energies=layer_energies,
                beta_true=beta,
                alpha_true=alpha,
                coherence=coherence,
                noise_level=noise_level
            ))
        
        return states
    
    def generate_mixed_coherence_states(
        self,
        beta: float,
        n_samples: int = 100,
        coherence_range: Tuple[float, float] = (0.3, 0.9)
    ) -> List[SyntheticSystemState]:
        """
        Generate states with varying coherence levels.
        
        Args:
            beta: True β value
            n_samples: Number of samples
            coherence_range: Range of coherence values
            
        Returns:
            List of states with mixed coherence
        """
        states = []
        
        for _ in range(n_samples):
            # Random coherence level
            target_coherence = np.random.uniform(*coherence_range)
            
            # Noise level inversely related to coherence
            noise_level = 1 - target_coherence
            
            # Generate single state
            state = self.generate_coherent_state(beta, n_samples=1, noise_level=noise_level)[0]
            states.append(state)
        
        return states
    
    def generate_archetype_dataset(
        self,
        beta: float,
        n_samples_per_archetype: int = 50
    ) -> Dict[str, List[SyntheticSystemState]]:
        """
        Generate dataset with multiple system archetypes.
        
        Args:
            beta: True β value
            n_samples_per_archetype: Samples per archetype
            
        Returns:
            Dictionary mapping archetype name to states
        """
        archetypes = {}
        
        # High coherence (well-integrated system)
        archetypes['high_coherence'] = self.generate_coherent_state(
            beta, n_samples_per_archetype, noise_level=0.05
        )
        
        # Medium coherence (typical system)
        archetypes['medium_coherence'] = self.generate_coherent_state(
            beta, n_samples_per_archetype, noise_level=0.15
        )
        
        # Low coherence (fragmented system)
        archetypes['low_coherence'] = self.generate_coherent_state(
            beta, n_samples_per_archetype, noise_level=0.4
        )
        
        # Mixed coherence (realistic variety)
        archetypes['mixed'] = self.generate_mixed_coherence_states(
            beta, n_samples_per_archetype
        )
        
        return archetypes
    
    def generate_test_suite(
        self,
        beta_values: List[float],
        n_samples: int = 100
    ) -> Dict[float, List[SyntheticSystemState]]:
        """
        Generate test datasets for multiple β values.
        
        This allows testing whether the optimizer can correctly
        recover different β values.
        
        Args:
            beta_values: List of β values to test
            n_samples: Samples per β value
            
        Returns:
            Dictionary mapping β to list of states
        """
        test_data = {}
        
        for beta in beta_values:
            test_data[beta] = self.generate_coherent_state(
                beta, n_samples, noise_level=0.1
            )
        
        return test_data


def create_objective_function(
    states: List[SyntheticSystemState]
) -> callable:
    """
    Create an objective function for optimizing β given synthetic data.
    
    The objective function measures how well a candidate β explains
    the observed layer energy distributions.
    
    Args:
        states: List of system states
        
    Returns:
        Function(beta, data) -> loss
    """
    def objective(beta: float, data: np.ndarray) -> float:
        """
        Objective function for β optimization.
        
        Args:
            beta: Candidate β value
            data: Not used (compatibility with validator API)
            
        Returns:
            Mean squared error between predicted and observed distributions
        """
        alpha = 1 - beta
        total_error = 0.0
        
        for state in states:
            # Predict energy distribution based on β
            n_layers = len(state.layer_energies)
            manifested_layers = int(alpha * n_layers)
            
            predicted_energies = np.zeros(n_layers)
            
            # Manifested portion
            for i in range(manifested_layers):
                predicted_energies[i] = alpha * np.exp(-i / n_layers)
            
            # Unmanifested portion
            for i in range(manifested_layers, n_layers):
                predicted_energies[i] = beta * np.exp(-(i - manifested_layers) / 3)
            
            # Normalize
            total_pred = np.sum(predicted_energies)
            if total_pred > 0:
                predicted_energies /= total_pred
            
            # MSE between predicted and actual
            error = np.mean((predicted_energies - state.layer_energies) ** 2)
            total_error += error
        
        return total_error / len(states)
    
    return objective


def generate_domain_dataset(
    domain_name: str,
    beta_true: float = 1/27,
    n_samples: int = 200,
    seed: Optional[int] = None
) -> Tuple[List[SyntheticSystemState], callable]:
    """
    Generate a complete dataset for a specific domain.
    
    Args:
        domain_name: Name of the domain (for seeding)
        beta_true: True β value to use
        n_samples: Number of samples to generate
        seed: Random seed
        
    Returns:
        Tuple of (states, objective_function)
    """
    if seed is None:
        # Use domain name to create deterministic seed
        seed = hash(domain_name) % (2**32)
    
    generator = SyntheticDataGenerator(n_layers=7, seed=seed)
    states = generator.generate_coherent_state(beta_true, n_samples, noise_level=0.1)
    objective_func = create_objective_function(states)
    
    return states, objective_func
