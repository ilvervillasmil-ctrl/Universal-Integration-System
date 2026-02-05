"""
Beta Validation Framework

This module implements a blind optimization framework for validating
the renormalization factor κ = β_empirical / β_theoretical.

Key principle: The optimizer does NOT know that π/4 is the target.
"""

import numpy as np
from typing import Dict, List, Tuple, Optional, Callable
from dataclasses import dataclass
import json
from datetime import datetime
from scipy.optimize import minimize, differential_evolution
from scipy import stats


@dataclass
class OptimizationResult:
    """Results from a single optimization run"""
    beta_optimal: float
    beta_theoretical: float
    kappa: float
    objective_value: float
    method: str
    success: bool
    message: str
    n_iterations: int
    
    def to_dict(self) -> Dict:
        return {
            'beta_optimal': self.beta_optimal,
            'beta_theoretical': self.beta_theoretical,
            'kappa': self.kappa,
            'objective_value': self.objective_value,
            'method': self.method,
            'success': self.success,
            'message': self.message,
            'n_iterations': self.n_iterations
        }


@dataclass
class ValidationReport:
    """Comprehensive validation report across multiple runs"""
    domain_name: str
    beta_theoretical: float
    optimization_results: List[OptimizationResult]
    kappa_mean: float
    kappa_std: float
    kappa_median: float
    kappa_ci_lower: float
    kappa_ci_upper: float
    pi_over_4: float
    timestamp: str
    
    def to_dict(self) -> Dict:
        return {
            'domain_name': self.domain_name,
            'beta_theoretical': self.beta_theoretical,
            'optimization_results': [r.to_dict() for r in self.optimization_results],
            'kappa_mean': self.kappa_mean,
            'kappa_std': self.kappa_std,
            'kappa_median': self.kappa_median,
            'kappa_ci_lower': self.kappa_ci_lower,
            'kappa_ci_upper': self.kappa_ci_upper,
            'pi_over_4': self.pi_over_4,
            'timestamp': self.timestamp
        }
    
    def to_markdown(self) -> str:
        """Generate markdown report"""
        md = f"# Validation Report: {self.domain_name}\n\n"
        md += f"**Timestamp:** {self.timestamp}\n\n"
        md += f"## Summary Statistics\n\n"
        md += f"- **β_theoretical:** {self.beta_theoretical:.6f}\n"
        md += f"- **κ_mean:** {self.kappa_mean:.6f}\n"
        md += f"- **κ_std:** {self.kappa_std:.6f}\n"
        md += f"- **κ_median:** {self.kappa_median:.6f}\n"
        md += f"- **95% CI:** [{self.kappa_ci_lower:.6f}, {self.kappa_ci_upper:.6f}]\n"
        md += f"- **π/4:** {self.pi_over_4:.6f}\n"
        md += f"- **Deviation from π/4:** {abs(self.kappa_mean - self.pi_over_4):.6f} "
        md += f"({abs(self.kappa_mean - self.pi_over_4) / self.pi_over_4 * 100:.2f}%)\n\n"
        
        md += "## Optimization Results\n\n"
        md += "| Method | β_optimal | κ | Objective | Success |\n"
        md += "|--------|-----------|---|-----------|----------|\n"
        for result in self.optimization_results:
            md += f"| {result.method} | {result.beta_optimal:.6f} | {result.kappa:.6f} | "
            md += f"{result.objective_value:.6e} | {'✓' if result.success else '✗'} |\n"
        
        return md


class BetaValidator:
    """
    Framework for validating β through blind optimization.
    
    The optimizer minimizes an objective function without knowledge
    that π/4 is the expected renormalization factor.
    """
    
    def __init__(self, beta_theoretical: float = 1/27):
        """
        Initialize validator.
        
        Args:
            beta_theoretical: Theoretical prediction (default: 1/27)
        """
        self.beta_theoretical = beta_theoretical
        self.pi_over_4 = np.pi / 4
        
    def optimize_beta(
        self,
        objective_func: Callable[[float, np.ndarray], float],
        data: np.ndarray,
        method: str = 'grid_search',
        beta_range: Tuple[float, float] = (0.01, 0.05),
        n_grid_points: int = 401,
        **kwargs
    ) -> OptimizationResult:
        """
        Optimize β to minimize objective function.
        
        This is a BLIND optimization - the algorithm does not know π/4 is expected.
        
        Args:
            objective_func: Function(beta, data) -> scalar loss
            data: Input data for optimization
            method: 'grid_search', 'gradient', or 'bayesian'
            beta_range: Search range for β
            n_grid_points: Number of grid points for grid search
            **kwargs: Additional parameters for specific methods
            
        Returns:
            OptimizationResult with optimal β and statistics
        """
        if method == 'grid_search':
            return self._grid_search(objective_func, data, beta_range, n_grid_points)
        elif method == 'gradient':
            return self._gradient_optimize(objective_func, data, beta_range, **kwargs)
        elif method == 'bayesian':
            return self._bayesian_optimize(objective_func, data, beta_range, **kwargs)
        else:
            raise ValueError(f"Unknown method: {method}")
    
    def _grid_search(
        self,
        objective_func: Callable[[float, np.ndarray], float],
        data: np.ndarray,
        beta_range: Tuple[float, float],
        n_grid_points: int
    ) -> OptimizationResult:
        """Grid search optimization"""
        beta_values = np.linspace(beta_range[0], beta_range[1], n_grid_points)
        objective_values = np.array([objective_func(beta, data) for beta in beta_values])
        
        best_idx = np.argmin(objective_values)
        beta_optimal = beta_values[best_idx]
        obj_value = objective_values[best_idx]
        
        return OptimizationResult(
            beta_optimal=beta_optimal,
            beta_theoretical=self.beta_theoretical,
            kappa=beta_optimal / self.beta_theoretical,
            objective_value=obj_value,
            method='grid_search',
            success=True,
            message='Grid search completed',
            n_iterations=n_grid_points
        )
    
    def _gradient_optimize(
        self,
        objective_func: Callable[[float, np.ndarray], float],
        data: np.ndarray,
        beta_range: Tuple[float, float],
        **kwargs
    ) -> OptimizationResult:
        """Gradient-based optimization using L-BFGS-B"""
        # Start from middle of range
        beta_init = (beta_range[0] + beta_range[1]) / 2
        
        result = minimize(
            lambda beta: objective_func(beta[0], data),
            x0=[beta_init],
            method='L-BFGS-B',
            bounds=[beta_range],
            **kwargs
        )
        
        beta_optimal = result.x[0]
        
        return OptimizationResult(
            beta_optimal=beta_optimal,
            beta_theoretical=self.beta_theoretical,
            kappa=beta_optimal / self.beta_theoretical,
            objective_value=result.fun,
            method='L-BFGS-B',
            success=result.success,
            message=result.message,
            n_iterations=result.nit if hasattr(result, 'nit') else 0
        )
    
    def _bayesian_optimize(
        self,
        objective_func: Callable[[float, np.ndarray], float],
        data: np.ndarray,
        beta_range: Tuple[float, float],
        **kwargs
    ) -> OptimizationResult:
        """
        Bayesian optimization using differential evolution.
        
        Note: This is a simplified version. Full Bayesian optimization
        would use Gaussian processes, but that requires additional dependencies.
        """
        max_iter = kwargs.get('maxiter', 100)
        
        result = differential_evolution(
            lambda beta: objective_func(beta[0], data),
            bounds=[beta_range],
            maxiter=max_iter,
            seed=kwargs.get('seed', None)
        )
        
        beta_optimal = result.x[0]
        
        return OptimizationResult(
            beta_optimal=beta_optimal,
            beta_theoretical=self.beta_theoretical,
            kappa=beta_optimal / self.beta_theoretical,
            objective_value=result.fun,
            method='differential_evolution',
            success=result.success,
            message=result.message,
            n_iterations=result.nit
        )
    
    def validate_across_methods(
        self,
        objective_func: Callable[[float, np.ndarray], float],
        data: np.ndarray,
        methods: Optional[List[str]] = None,
        **kwargs
    ) -> List[OptimizationResult]:
        """
        Run multiple optimization methods and compare results.
        
        Args:
            objective_func: Objective function to minimize
            data: Input data
            methods: List of methods to use (default: all three)
            **kwargs: Additional parameters
            
        Returns:
            List of OptimizationResult from each method
        """
        if methods is None:
            methods = ['grid_search', 'gradient', 'bayesian']
        
        results = []
        for method in methods:
            result = self.optimize_beta(objective_func, data, method=method, **kwargs)
            results.append(result)
        
        return results
    
    def generate_report(
        self,
        domain_name: str,
        optimization_results: List[OptimizationResult]
    ) -> ValidationReport:
        """
        Generate comprehensive validation report.
        
        Args:
            domain_name: Name of the domain being validated
            optimization_results: Results from multiple optimization runs
            
        Returns:
            ValidationReport with statistics and analysis
        """
        kappa_values = np.array([r.kappa for r in optimization_results])
        
        # Calculate statistics
        kappa_mean = np.mean(kappa_values)
        kappa_std = np.std(kappa_values, ddof=1)
        kappa_median = np.median(kappa_values)
        
        # 95% confidence interval
        if len(kappa_values) > 1:
            ci = stats.t.interval(
                0.95,
                len(kappa_values) - 1,
                loc=kappa_mean,
                scale=stats.sem(kappa_values)
            )
            kappa_ci_lower, kappa_ci_upper = ci
        else:
            kappa_ci_lower = kappa_mean
            kappa_ci_upper = kappa_mean
        
        return ValidationReport(
            domain_name=domain_name,
            beta_theoretical=self.beta_theoretical,
            optimization_results=optimization_results,
            kappa_mean=kappa_mean,
            kappa_std=kappa_std,
            kappa_median=kappa_median,
            kappa_ci_lower=kappa_ci_lower,
            kappa_ci_upper=kappa_ci_upper,
            pi_over_4=self.pi_over_4,
            timestamp=datetime.now().isoformat()
        )
    
    def save_report(
        self,
        report: ValidationReport,
        json_path: str,
        markdown_path: Optional[str] = None
    ) -> None:
        """
        Save validation report to files.
        
        Args:
            report: ValidationReport to save
            json_path: Path for JSON output
            markdown_path: Optional path for markdown report
        """
        # Save JSON
        with open(json_path, 'w') as f:
            json.dump(report.to_dict(), f, indent=2)
        
        # Save markdown if path provided
        if markdown_path:
            with open(markdown_path, 'w') as f:
                f.write(report.to_markdown())


def meta_analysis(reports: List[ValidationReport]) -> Dict:
    """
    Perform meta-analysis across multiple domain validation reports.
    
    Args:
        reports: List of ValidationReport from different domains
        
    Returns:
        Dictionary with meta-analysis results
    """
    all_kappa = []
    domain_kappas = {}
    
    for report in reports:
        kappas = [r.kappa for r in report.optimization_results]
        all_kappa.extend(kappas)
        domain_kappas[report.domain_name] = {
            'mean': report.kappa_mean,
            'std': report.kappa_std,
            'n': len(kappas)
        }
    
    all_kappa = np.array(all_kappa)
    pi_over_4 = np.pi / 4
    
    # Overall statistics
    overall_mean = np.mean(all_kappa)
    overall_std = np.std(all_kappa, ddof=1)
    overall_median = np.median(all_kappa)
    
    # Confidence interval
    ci = stats.t.interval(
        0.95,
        len(all_kappa) - 1,
        loc=overall_mean,
        scale=stats.sem(all_kappa)
    )
    
    # Hypothesis test: H0: κ = π/4
    t_stat, p_value = stats.ttest_1samp(all_kappa, pi_over_4)
    
    # Effect size (Cohen's d)
    cohens_d = (overall_mean - pi_over_4) / overall_std
    
    # Normality test
    shapiro_stat, shapiro_p = stats.shapiro(all_kappa)
    
    return {
        'n_domains': len(reports),
        'n_total_samples': len(all_kappa),
        'overall_mean': overall_mean,
        'overall_std': overall_std,
        'overall_median': overall_median,
        'ci_95_lower': ci[0],
        'ci_95_upper': ci[1],
        'pi_over_4': pi_over_4,
        'deviation_from_pi4': abs(overall_mean - pi_over_4),
        'deviation_percentage': abs(overall_mean - pi_over_4) / pi_over_4 * 100,
        't_statistic': t_stat,
        'p_value': p_value,
        'cohens_d': cohens_d,
        'shapiro_statistic': shapiro_stat,
        'shapiro_p_value': shapiro_p,
        'is_normal': shapiro_p > 0.05,
        'domain_statistics': domain_kappas,
        'timestamp': datetime.now().isoformat()
    }
