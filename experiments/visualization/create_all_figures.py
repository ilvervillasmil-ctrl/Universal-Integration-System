"""
Complete visualization suite for Phase 1 results
Generates publication-ready figures
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats
import pandas as pd
import json

# Set publication style
plt.style.use('seaborn-v0_8-paper')
sns.set_palette("husl")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 14

class PublicationFigures:
    """
    Generates all figures for Phase 1 paper
    """
    
    def __init__(self, results_dir='experiments/results'):
        self.results_dir = results_dir
        self.pi_4 = np.pi / 4
        
    def figure_1_kappa_distribution(self, domain_results):
        """
        Figure 1: κ distribution across domains with π/4 reference
        Box plot + individual points + confidence intervals
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        
        domains = list(domain_results.keys())
        kappa_values = [domain_results[d]['kappa_empirical'] for d in domains]
        
        # Box plot
        bp = ax.boxplot(kappa_values, labels=domains, patch_artist=True,
                       widths=0.6, showfliers=False)
        
        # Color boxes
        colors = sns.color_palette("Set2", len(domains))
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        
        # Add individual points with jitter
        for i, (domain, kappas) in enumerate(zip(domains, kappa_values), 1):
            y = kappas if isinstance(kappas, list) else [kappas]
            x = np.random.normal(i, 0.04, size=len(y))
            ax.scatter(x, y, alpha=0.4, s=20, color='black')
        
        # π/4 reference line
        ax.axhline(self.pi_4, color='red', linestyle='--', linewidth=2,
                  label=f'π/4 = {self.pi_4:.4f}', zorder=10)
        
        # Confidence interval for π/4 (±5%)
        ax.axhspan(self.pi_4 * 0.95, self.pi_4 * 1.05, 
                  alpha=0.1, color='red', label='±5% tolerance')
        
        # Formatting
        ax.set_ylabel('κ (renormalization factor)', fontsize=12)
        ax.set_xlabel('Domain', fontsize=12)
        ax.set_title('Distribution of κ Across Five Independent Domains', 
                    fontsize=14, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        ax.legend(loc='upper right')
        
        # Rotate x-labels if needed
        plt.xticks(rotation=45, ha='right')
        
        plt.tight_layout()
        plt.savefig(f'{self.results_dir}/meta_analysis/figure_1_kappa_distribution.png')
        plt.savefig(f'{self.results_dir}/meta_analysis/figure_1_kappa_distribution.pdf')
        plt.close()
        
        print("✅ Figure 1 saved: κ distribution across domains")
        
    def figure_2_convergence_plot(self, domain_results):
        """
        Figure 2: Scatter plot showing convergence to π/4
        With regression line and confidence band
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        
        domains = list(domain_results.keys())
        kappa_values = [domain_results[d]['kappa_empirical'] for d in domains]
        sample_sizes = [domain_results[d]['n'] for d in domains]
        
        # Scatter plot with size proportional to sample size
        sizes = [n * 2 for n in sample_sizes]
        scatter = ax.scatter(range(len(domains)), kappa_values, s=sizes, 
                           alpha=0.6, c=range(len(domains)), cmap='viridis',
                           edgecolors='black', linewidth=1)
        
        # π/4 reference line
        ax.axhline(self.pi_4, color='red', linestyle='--', linewidth=2,
                  label=f'π/4 = {self.pi_4:.4f}')
        
        # Mean across domains
        mean_kappa = np.mean(kappa_values)
        ax.axhline(mean_kappa, color='blue', linestyle='-', linewidth=2,
                  label=f'Mean κ = {mean_kappa:.4f}')
        
        # Confidence band for mean
        std_kappa = np.std(kappa_values)
        ax.axhspan(mean_kappa - 2*std_kappa, mean_kappa + 2*std_kappa,
                  alpha=0.2, color='blue', label='95% CI (mean)')
        
        # Formatting
        ax.set_xticks(range(len(domains)))
        ax.set_xticklabels(domains, rotation=45, ha='right')
        ax.set_ylabel('κ (renormalization factor)', fontsize=12)
        ax.set_xlabel('Domain', fontsize=12)
        ax.set_title('Convergence of κ to π/4 Across Domains',
                    fontsize=14, fontweight='bold')
        ax.grid(alpha=0.3)
        ax.legend(loc='upper right')
        
        # Add colorbar for clarity
        cbar = plt.colorbar(scatter, ax=ax)
        cbar.set_label('Domain Index', fontsize=10)
        
        plt.tight_layout()
        plt.savefig(f'{self.results_dir}/meta_analysis/figure_2_convergence_plot.png')
        plt.savefig(f'{self.results_dir}/meta_analysis/figure_2_convergence_plot.pdf')
        plt.close()
        
        print("✅ Figure 2 saved: Convergence plot")
    
    def figure_3_confidence_intervals(self, domain_results):
        """
        Figure 3: Forest plot with 95% CIs for each domain
        """
        fig, ax = plt.subplots(figsize=(8, 10))
        
        domains = list(domain_results.keys())
        kappa_values = [domain_results[d]['kappa_empirical'] for d in domains]
        cis = [domain_results[d]['95_ci'] for d in domains]
        
        # Forest plot
        y_positions = range(len(domains))
        
        for i, (domain, kappa, ci) in enumerate(zip(domains, kappa_values, cis)):
            # Point estimate
            ax.plot(kappa, i, 'o', markersize=10, color='black')
            
            # Confidence interval
            ax.plot([ci[0], ci[1]], [i, i], '-', linewidth=2, color='gray')
            
            # Caps
            ax.plot([ci[0], ci[0]], [i-0.1, i+0.1], '-', linewidth=1, color='gray')
            ax.plot([ci[1], ci[1]], [i-0.1, i+0.1], '-', linewidth=1, color='gray')
        
        # π/4 reference line
        ax.axvline(self.pi_4, color='red', linestyle='--', linewidth=2,
                  label=f'π/4 = {self.pi_4:.4f}')
        
        # Formatting
        ax.set_yticks(y_positions)
        ax.set_yticklabels(domains)
        ax.set_xlabel('κ (95% Confidence Interval)', fontsize=12)
        ax.set_title('Confidence Intervals for κ by Domain',
                    fontsize=14, fontweight='bold')
        ax.grid(axis='x', alpha=0.3)
        ax.legend(loc='lower right')
        
        plt.tight_layout()
        plt.savefig(f'{self.results_dir}/meta_analysis/figure_3_confidence_intervals.png')
        plt.savefig(f'{self.results_dir}/meta_analysis/figure_3_confidence_intervals.pdf')
        plt.close()
        
        print("✅ Figure 3 saved: Confidence intervals")
    
    def figure_4_optimization_landscape(self, beta_range, error_curve):
        """
        Figure 4: Error surface as function of β
        Shows minimum at β ≈ 0.0291
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Plot error curve
        ax.plot(beta_range, error_curve, linewidth=2, color='blue')
        
        # Mark minimum
        min_idx = np.argmin(error_curve)
        beta_optimal = beta_range[min_idx]
        error_min = error_curve[min_idx]
        
        ax.plot(beta_optimal, error_min, 'ro', markersize=12,
               label=f'Optimal β = {beta_optimal:.4f}')
        
        # Mark theoretical β
        beta_theoretical = 1/27
        ax.axvline(beta_theoretical, color='green', linestyle='--', linewidth=2,
                  label=f'β_theoretical = {beta_theoretical:.4f}')
        
        # Mark predicted β (theoretical × π/4)
        beta_predicted = beta_theoretical * self.pi_4
        ax.axvline(beta_predicted, color='orange', linestyle=':', linewidth=2,
                  label=f'β_predicted = {beta_predicted:.4f}')
        
        # Formatting
        ax.set_xlabel('β (mystery parameter)', fontsize=12)
        ax.set_ylabel('Root Mean Squared Error', fontsize=12)
        ax.set_title('Optimization Landscape: Finding Optimal β',
                    fontsize=14, fontweight='bold')
        ax.grid(alpha=0.3)
        ax.legend(loc='upper right')
        
        plt.tight_layout()
        plt.savefig(f'{self.results_dir}/meta_analysis/figure_4_optimization_landscape.png')
        plt.savefig(f'{self.results_dir}/meta_analysis/figure_4_optimization_landscape.pdf')
        plt.close()
        
        print("✅ Figure 4 saved: Optimization landscape")
    
    def figure_5_method_comparison(self, method_results):
        """
        Figure 5: Comparison of optimization methods
        Shows all methods converge to same κ
        """
        fig, ax = plt.subplots(figsize=(8, 6))
        
        methods = list(method_results.keys())
        kappa_values = [method_results[m]['kappa'] for m in methods]
        stds = [method_results[m]['std'] for m in methods]
        
        # Bar plot with error bars
        x_pos = np.arange(len(methods))
        bars = ax.bar(x_pos, kappa_values, yerr=stds, capsize=10,
                     alpha=0.7, edgecolor='black', linewidth=1.5)
        
        # Color bars
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
        for bar, color in zip(bars, colors):
            bar.set_color(color)
        
        # π/4 reference line
        ax.axhline(self.pi_4, color='red', linestyle='--', linewidth=2,
                  label=f'π/4 = {self.pi_4:.4f}', zorder=10)
        
        # Formatting
        ax.set_xticks(x_pos)
        ax.set_xticklabels(methods)
        ax.set_ylabel('κ (mean ± std)', fontsize=12)
        ax.set_xlabel('Optimization Method', fontsize=12)
        ax.set_title('Convergence Across Optimization Methods',
                    fontsize=14, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        ax.legend(loc='upper right')
        
        plt.tight_layout()
        plt.savefig(f'{self.results_dir}/meta_analysis/figure_5_method_comparison.png')
        plt.savefig(f'{self.results_dir}/meta_analysis/figure_5_method_comparison.pdf')
        plt.close()
        
        print("✅ Figure 5 saved: Method comparison")
    
    def figure_6_sensitivity_analysis(self, sensitivity_data):
        """
        Figure 6: Sensitivity to sample size, noise, outliers
        Multi-panel figure
        """
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        
        # Panel A: Sample size
        ax = axes[0]
        sample_sizes = sensitivity_data['sample_size']['n']
        kappas = sensitivity_data['sample_size']['kappa']
        ax.plot(sample_sizes, kappas, 'o-', linewidth=2, markersize=8)
        ax.axhline(self.pi_4, color='red', linestyle='--', linewidth=2)
        ax.set_xlabel('Sample Size (n)', fontsize=12)
        ax.set_ylabel('κ', fontsize=12)
        ax.set_title('(A) Sensitivity to Sample Size', fontsize=12, fontweight='bold')
        ax.grid(alpha=0.3)
        
        # Panel B: Noise level
        ax = axes[1]
        noise_levels = sensitivity_data['noise']['sigma']
        kappas = sensitivity_data['noise']['kappa']
        ax.plot(noise_levels, kappas, 's-', linewidth=2, markersize=8, color='orange')
        ax.axhline(self.pi_4, color='red', linestyle='--', linewidth=2)
        ax.set_xlabel('Noise Level (σ)', fontsize=12)
        ax.set_ylabel('κ', fontsize=12)
        ax.set_title('(B) Sensitivity to Noise', fontsize=12, fontweight='bold')
        ax.grid(alpha=0.3)
        
        # Panel C: Outlier removal
        ax = axes[2]
        categories = ['With Outliers', 'Without Outliers']
        kappas = [sensitivity_data['outliers']['with'], 
                 sensitivity_data['outliers']['without']]
        bars = ax.bar(categories, kappas, alpha=0.7, edgecolor='black', linewidth=1.5)
        bars[0].set_color('#E74C3C')
        bars[1].set_color('#2ECC71')
        ax.axhline(self.pi_4, color='red', linestyle='--', linewidth=2)
        ax.set_ylabel('κ', fontsize=12)
        ax.set_title('(C) Impact of Outliers', fontsize=12, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f'{self.results_dir}/meta_analysis/figure_6_sensitivity_analysis.png')
        plt.savefig(f'{self.results_dir}/meta_analysis/figure_6_sensitivity_analysis.pdf')
        plt.close()
        
        print("✅ Figure 6 saved: Sensitivity analysis")
    
    def generate_all_figures(self, results):
        """
        Master function to generate all figures
        
        Args:
            results: Dictionary with structure:
                {
                    'domains': {
                        'ai_systems': {'kappa_empirical': float, 'n': int, '95_ci': [float, float]},
                        'human_psychology': {...},
                        ...
                    },
                    'optimization': {
                        'beta_range': array,
                        'error_curve': array
                    },
                    'methods': {
                        'grid_search': {'kappa': float, 'std': float},
                        'gradient_descent': {...},
                        ...
                    },
                    'sensitivity': {
                        'sample_size': {'n': array, 'kappa': array},
                        'noise': {'sigma': array, 'kappa': array},
                        'outliers': {'with': float, 'without': float}
                    }
                }
        """
        print("\n🎨 Generating publication figures...")
        print("=" * 50)
        
        self.figure_1_kappa_distribution(results['domains'])
        self.figure_2_convergence_plot(results['domains'])
        self.figure_3_confidence_intervals(results['domains'])
        self.figure_4_optimization_landscape(
            results['optimization']['beta_range'],
            results['optimization']['error_curve']
        )
        self.figure_5_method_comparison(results['methods'])
        self.figure_6_sensitivity_analysis(results['sensitivity'])
        
        print("=" * 50)
        print("✅ All 6 figures generated successfully!")
        print(f"📁 Saved to: {self.results_dir}/meta_analysis/\n")


# Example usage when results are available:
if __name__ == "__main__":
    # This is example code - replace with actual results when available
    
    # Example results structure
    example_results = {
        'domains': {
            'ai_systems': {
                'kappa_empirical': 0.783,
                'n': 127,
                '95_ci': [0.751, 0.815]
            },
            'human_psychology': {
                'kappa_empirical': 0.791,
                'n': 89,
                '95_ci': [0.750, 0.832]
            },
            'organizations': {
                'kappa_empirical': 0.781,
                'n': 203,
                '95_ci': [0.757, 0.805]
            },
            'physical_systems': {
                'kappa_empirical': 0.786,
                'n': 56,
                '95_ci': [0.737, 0.835]
            },
            'economic_systems': {
                'kappa_empirical': 0.788,
                'n': 142,
                '95_ci': [0.758, 0.818]
            }
        },
        'optimization': {
            'beta_range': np.linspace(0.01, 0.05, 100),
            'error_curve': np.random.random(100) * 0.1 + 0.05
        },
        'methods': {
            'grid_search': {'kappa': 0.785, 'std': 0.032},
            'gradient_descent': {'kappa': 0.787, 'std': 0.038},
            'bayesian_optimization': {'kappa': 0.786, 'std': 0.034}
        },
        'sensitivity': {
            'sample_size': {
                'n': np.array([25, 50, 100, 200]),
                'kappa': np.array([0.780, 0.785, 0.786, 0.786])
            },
            'noise': {
                'sigma': np.array([0.01, 0.05, 0.10]),
                'kappa': np.array([0.786, 0.784, 0.782])
            },
            'outliers': {
                'with': 0.786,
                'without': 0.787
            }
        }
    }
    
    # Generate figures
    fig_gen = PublicationFigures()
    fig_gen.generate_all_figures(example_results)
    
    print("\n💡 To use with real results:")
    print("   1. Load results from experiments/results/meta_analysis/combined_results.json")
    print("   2. Pass to fig_gen.generate_all_figures(results)")
