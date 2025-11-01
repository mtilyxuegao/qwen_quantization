#!/usr/bin/env python3
"""
Performance Visualization Script
Generates comprehensive performance comparison charts from benchmark results
"""

import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Configuration
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
RESULT_FILE = PROJECT_ROOT / "result.jsonl"
OUTPUT_DIR = SCRIPT_DIR / "figures"
OUTPUT_DIR.mkdir(exist_ok=True)

# Scenario mapping
SCENARIO_CONFIGS = {
    (32, 256, 32): "Balanced Baseline",
    (1, 128, 64): "Small Batch Interactive",
    (1, 2048, 32): "Long Input (Prefill)",
    (1, 256, 512): "Long Output (Decode)",
    (8, 256, 128): "Medium Batch",
    (64, 256, 128): "High Concurrency",
    (1, 16384, 32): "16K Long Context"
}

# Selected models for visualization
SELECTED_MODELS = ["original", "w8a8_smooth_ptq", "w8a8_smooth_gptq", "w8a16_smooth_awq"]

# Model display names (prettier) - with line breaks for horizontal display
MODEL_DISPLAY_NAMES = {
    "original": "BF16\nBaseline",
    "w8a8_smooth_ptq": "W8A8\nSQ→PTQ",
    "w8a8_smooth_gptq": "W8A8\nSQ→GPTQ",
    "w8a16_smooth_awq": "W8A16\nSQ→AWQ"
}

# Color palette for models
MODEL_COLORS = {
    "original": "#2E4057",
    "w8a8_smooth_ptq": "#048A81",
    "w8a8_smooth_gptq": "#06D6A0",
    "w8a16_smooth_awq": "#C73E1D"
}


def load_results(result_file: Path) -> List[Dict]:
    """Load benchmark results from JSONL file"""
    results = []
    with open(result_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                results.append(json.loads(line))
    return results


def extract_model_name(run_name: str) -> str:
    """Extract model name from run_name"""
    # Remove config and run suffix
    parts = run_name.rsplit('_run', 1)
    if len(parts) == 2:
        name_with_config = parts[0]
        # Remove config suffix (base, interactive, etc.)
        for config in ['base', 'interactive', 'prefill_bound', 'decode_bound', 
                      'medium_batch', 'high_concurrency', 'long_context']:
            if name_with_config.endswith('_' + config):
                return name_with_config[:-len(config)-1]
        return name_with_config
    return run_name


def group_by_model_and_scenario(results: List[Dict]) -> Dict[str, Dict[Tuple, List[Dict]]]:
    """
    Group results by model and scenario
    Returns: {model_name: {(batch, input, output): [result1, result2, ...]}}
    """
    grouped = defaultdict(lambda: defaultdict(list))
    
    for result in results:
        model_name = extract_model_name(result['run_name'])
        scenario_key = (result['batch_size'], result['input_len'], result['output_len'])
        grouped[model_name][scenario_key].append(result)
    
    return grouped


def compute_averages(grouped_data: Dict[str, Dict[Tuple, List[Dict]]]) -> Dict[str, Dict[Tuple, Dict]]:
    """
    Compute average metrics for each model and scenario
    Returns: {model_name: {scenario: {metric: avg_value}}}
    """
    averages = {}
    
    for model_name, scenarios in grouped_data.items():
        averages[model_name] = {}
        
        for scenario_key, results in scenarios.items():
            if not results:
                continue
            
            # Compute averages for each metric
            metrics = {}
            for metric in ['latency', 'output_throughput', 'overall_throughput', 'input_throughput']:
                values = [r.get(metric, 0) for r in results if metric in r]
                if values:
                    metrics[metric] = np.mean(values)
                    metrics[f'{metric}_std'] = np.std(values) if len(values) > 1 else 0
                else:
                    metrics[metric] = 0
                    metrics[f'{metric}_std'] = 0
            
            averages[model_name][scenario_key] = metrics
    
    return averages


def plot_overall_throughput_comparison(averages: Dict, output_path: Path):
    """
    Figure 1: Generate 7 separate bar charts, one for each scenario
    Only includes selected models
    """
    scenarios = list(SCENARIO_CONFIGS.keys())
    models = SELECTED_MODELS
    
    for idx, scenario in enumerate(scenarios, 1):
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Prepare data for this scenario
        values = []
        errors = []
        model_labels = []
        colors = []
        
        for model in models:
            if model in averages and scenario in averages[model]:
                values.append(averages[model][scenario]['output_throughput'])
                errors.append(averages[model][scenario]['output_throughput_std'])
                model_labels.append(MODEL_DISPLAY_NAMES[model])
                colors.append(MODEL_COLORS[model])
            else:
                values.append(0)
                errors.append(0)
                model_labels.append(MODEL_DISPLAY_NAMES[model])
                colors.append(MODEL_COLORS[model])
        
        x = np.arange(len(models))
        bars = ax.bar(x, values, color=colors, yerr=errors, capsize=5, alpha=0.85, edgecolor='black', linewidth=1.5)
        
        # Add value labels on bars (positioned above the bars)
        for bar, val in zip(bars, values):
            if val > 0:
                height = bar.get_height()
                # Position label slightly above the bar
                y_offset = max(values) * 0.03  # 3% of max value as offset
                ax.text(bar.get_x() + bar.get_width()/2., height + y_offset,
                       f'{val:.0f}',
                       ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        ax.set_ylabel('Output Throughput (tok/s)', fontsize=12, fontweight='bold')
        ax.set_title(f'Configuration {idx}: {SCENARIO_CONFIGS[scenario]}', 
                     fontsize=13, fontweight='bold', pad=15)
        ax.set_xticks(x)
        ax.set_xticklabels(model_labels, rotation=0, ha='center', fontsize=10)
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        ax.set_ylim(0, max(values) * 1.15 if max(values) > 0 else 100)
        
        plt.tight_layout()
        output_file = output_path / f'1_{idx}_throughput_{SCENARIO_CONFIGS[scenario].lower().replace(" ", "_").replace("(", "").replace(")", "")}.png'
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Saved: {output_file}")


def plot_latency_throughput_scatter(averages: Dict, output_path: Path):
    """
    Figure 2: Scatter plot showing latency vs throughput tradeoff
    """
    fig, ax = plt.subplots(figsize=(14, 10))
    
    # Markers for different scenarios
    scenario_markers = {
        (32, 256, 32): 'o',     # circle
        (1, 128, 64): 's',      # square
        (1, 2048, 32): '^',     # triangle up
        (1, 256, 512): 'v',     # triangle down
        (8, 256, 128): 'D',     # diamond
        (64, 256, 128): 'P',    # plus
        (1, 16384, 32): '*'     # star
    }
    
    # Plot for each model
    for model in MODEL_DISPLAY_NAMES.keys():
        if model not in averages:
            continue
        
        for scenario, marker in scenario_markers.items():
            if scenario not in averages[model]:
                continue
            
            metrics = averages[model][scenario]
            latency = metrics['latency']
            throughput = metrics['output_throughput']
            
            if latency > 0 and throughput > 0:
                ax.scatter(latency, throughput, 
                          c=[MODEL_COLORS[model]], 
                          marker=marker,
                          s=200, alpha=0.7,
                          edgecolors='black', linewidth=0.5,
                          label=f"{MODEL_DISPLAY_NAMES[model]} - {SCENARIO_CONFIGS[scenario]}" 
                                if model == list(MODEL_DISPLAY_NAMES.keys())[0] else "")
    
    # Add legend for scenarios only (using first model)
    first_model = list(MODEL_DISPLAY_NAMES.keys())[0]
    scenario_handles = []
    for scenario, marker in scenario_markers.items():
        handle = plt.scatter([], [], marker=marker, c='gray', s=100, 
                           label=SCENARIO_CONFIGS[scenario])
        scenario_handles.append(handle)
    
    # Add legend for models
    model_handles = []
    for model in MODEL_DISPLAY_NAMES.keys():
        if model in averages:
            handle = plt.scatter([], [], c=[MODEL_COLORS[model]], marker='o', s=100,
                               label=MODEL_DISPLAY_NAMES[model])
            model_handles.append(handle)
    
    # Create two legends
    legend1 = ax.legend(handles=model_handles, loc='upper right', 
                       title='Models', framealpha=0.9, fontsize=9)
    ax.add_artist(legend1)
    ax.legend(handles=scenario_handles, loc='lower left', 
             title='Scenarios', framealpha=0.9, fontsize=9)
    
    ax.set_xlabel('Latency (s)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Output Throughput (tok/s)', fontsize=12, fontweight='bold')
    ax.set_title('Latency vs Throughput Tradeoff\n(Upper-left corner = Best)', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3)
    
    # Add annotation for "better" direction
    ax.annotate('Better Performance', xy=(0.05, 0.95), xycoords='axes fraction',
               fontsize=10, fontweight='bold', color='green',
               bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.3))
    
    plt.tight_layout()
    plt.savefig(output_path / '2_latency_throughput_scatter.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Saved: {output_path / '2_latency_throughput_scatter.png'}")


def plot_prefill_decode_comparison(averages: Dict, output_path: Path):
    """
    Figure 3: Side-by-side comparison of Prefill-bound vs Decode-bound scenarios
    Only includes selected models
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Prefill-bound scenario: (1, 2048, 32)
    prefill_scenario = (1, 2048, 32)
    # Decode-bound scenario: (1, 256, 512)
    decode_scenario = (1, 256, 512)
    
    models = SELECTED_MODELS
    x = np.arange(len(models))
    width = 0.35
    
    # Prefill-bound (use overall_throughput)
    prefill_values = []
    for model in models:
        if model in averages and prefill_scenario in averages[model]:
            prefill_values.append(averages[model][prefill_scenario]['overall_throughput'])
        else:
            prefill_values.append(0)
    
    bars1 = ax1.bar(x, prefill_values, width, 
                    color=[MODEL_COLORS[m] for m in models], alpha=0.9)
    ax1.set_ylabel('Overall Throughput (tok/s)', fontsize=11, fontweight='bold')
    ax1.set_title('Prefill-bound Performance\n(Long Input: 2048 tokens)', 
                  fontsize=12, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels([MODEL_DISPLAY_NAMES[m] for m in models], 
                        rotation=0, ha='center', fontsize=9)
    ax1.grid(axis='y', alpha=0.3)
    
    # Add value labels on bars
    for bar in bars1:
        height = bar.get_height()
        if height > 0:
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom', fontsize=8)
    
    # Decode-bound (use output_throughput)
    decode_values = []
    for model in models:
        if model in averages and decode_scenario in averages[model]:
            decode_values.append(averages[model][decode_scenario]['output_throughput'])
        else:
            decode_values.append(0)
    
    bars2 = ax2.bar(x, decode_values, width,
                    color=[MODEL_COLORS[m] for m in models], alpha=0.9)
    ax2.set_ylabel('Output Throughput (tok/s)', fontsize=11, fontweight='bold')
    ax2.set_title('Decode-bound Performance\n(Long Output: 512 tokens)', 
                  fontsize=12, fontweight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels([MODEL_DISPLAY_NAMES[m] for m in models], 
                        rotation=0, ha='center', fontsize=9)
    ax2.grid(axis='y', alpha=0.3)
    
    # Add value labels on bars
    for bar in bars2:
        height = bar.get_height()
        if height > 0:
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom', fontsize=8)
    
    plt.tight_layout()
    plt.savefig(output_path / '3_prefill_decode_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Saved: {output_path / '3_prefill_decode_comparison.png'}")


def plot_speedup_summary(averages: Dict, output_path: Path):
    """
    Figure 4: Speedup comparison relative to baseline (BF16)
    Only includes selected models
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    baseline_model = "original"
    if baseline_model not in averages:
        print("Warning: Baseline model not found, skipping speedup chart")
        return
    
    # Compute average speedup across all scenarios
    models = [m for m in SELECTED_MODELS if m != baseline_model]
    speedups = []
    
    for model in models:
        if model not in averages:
            speedups.append(0)
            continue
        
        model_speedup = []
        for scenario in SCENARIO_CONFIGS.keys():
            if scenario in averages[baseline_model] and scenario in averages[model]:
                baseline_throughput = averages[baseline_model][scenario]['output_throughput']
                model_throughput = averages[model][scenario]['output_throughput']
                
                if baseline_throughput > 0:
                    speedup = model_throughput / baseline_throughput
                    model_speedup.append(speedup)
        
        if model_speedup:
            speedups.append(np.mean(model_speedup))
        else:
            speedups.append(0)
    
    x = np.arange(len(models))
    bars = ax.bar(x, speedups, color=[MODEL_COLORS[m] for m in models], 
                  alpha=0.9, edgecolor='black', linewidth=1)
    
    # Add horizontal line at y=1 (baseline)
    ax.axhline(y=1.0, color='red', linestyle='--', linewidth=2, 
               label='BF16 Baseline', alpha=0.7)
    
    # Color bars based on speedup (green if >1, red if <1)
    for i, (bar, speedup) in enumerate(zip(bars, speedups)):
        if speedup > 1:
            bar.set_color('green')
            bar.set_alpha(0.7)
        elif speedup < 1:
            bar.set_color('red')
            bar.set_alpha(0.7)
    
    ax.set_xlabel('Model', fontsize=12, fontweight='bold')
    ax.set_ylabel('Average Speedup (vs BF16 Baseline)', fontsize=12, fontweight='bold')
    ax.set_title('Speedup Summary Across All Scenarios\n(Higher is Better)', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels([MODEL_DISPLAY_NAMES[m] for m in models], 
                       rotation=0, ha='center')
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    
    # Add value labels on bars
    for i, (bar, speedup) in enumerate(zip(bars, speedups)):
        if speedup > 0:
            label = f'{speedup:.2f}x'
            color = 'white' if speedup > 1 else 'black'
            ax.text(bar.get_x() + bar.get_width()/2., speedup/2,
                   label, ha='center', va='center', 
                   fontweight='bold', fontsize=10, color=color)
    
    plt.tight_layout()
    plt.savefig(output_path / '4_speedup_summary.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Saved: {output_path / '4_speedup_summary.png'}")


def generate_summary_table(averages: Dict, output_path: Path):
    """
    Generate a summary table of key metrics
    Only includes selected models
    """
    summary_lines = []
    summary_lines.append("=" * 80)
    summary_lines.append("PERFORMANCE SUMMARY TABLE - SELECTED MODELS")
    summary_lines.append("=" * 80)
    summary_lines.append("")
    
    # For each model, compute average metrics
    baseline_model = "original"
    
    for model in SELECTED_MODELS:
        if model not in averages:
            continue
        
        summary_lines.append(f"Model: {MODEL_DISPLAY_NAMES[model]}")
        summary_lines.append("-" * 80)
        
        all_latencies = []
        all_output_throughputs = []
        all_overall_throughputs = []
        
        for scenario in SCENARIO_CONFIGS.keys():
            if scenario not in averages[model]:
                continue
            
            metrics = averages[model][scenario]
            all_latencies.append(metrics['latency'])
            all_output_throughputs.append(metrics['output_throughput'])
            all_overall_throughputs.append(metrics['overall_throughput'])
        
        if all_latencies:
            avg_latency = np.mean(all_latencies)
            avg_output_tp = np.mean(all_output_throughputs)
            avg_overall_tp = np.mean(all_overall_throughputs)
            
            summary_lines.append(f"  Average Latency:           {avg_latency:.4f} s")
            summary_lines.append(f"  Average Output Throughput:  {avg_output_tp:.2f} tok/s")
            summary_lines.append(f"  Average Overall Throughput: {avg_overall_tp:.2f} tok/s")
            
            # Compute speedup vs baseline
            if model != baseline_model and baseline_model in averages:
                baseline_avg = np.mean([averages[baseline_model][s]['output_throughput'] 
                                       for s in SCENARIO_CONFIGS.keys() 
                                       if s in averages[baseline_model]])
                speedup = avg_output_tp / baseline_avg if baseline_avg > 0 else 0
                summary_lines.append(f"  Speedup vs Baseline:        {speedup:.2f}x")
        
        summary_lines.append("")
    
    summary_lines.append("=" * 80)
    
    # Save to file
    summary_file = output_path / "summary_table.txt"
    with open(summary_file, 'w') as f:
        f.write('\n'.join(summary_lines))
    
    print(f"Saved: {summary_file}")
    print("\nSummary:")
    print('\n'.join(summary_lines[:30]))  # Print first 30 lines


def main():
    """Main function to generate all visualizations"""
    print("=" * 80)
    print("Performance Visualization Tool")
    print("=" * 80)
    print("")
    
    # Check if result file exists
    if not RESULT_FILE.exists():
        print(f"Error: Result file not found at {RESULT_FILE}")
        return
    
    print(f"Loading results from: {RESULT_FILE}")
    results = load_results(RESULT_FILE)
    print(f"Loaded {len(results)} benchmark results")
    print("")
    
    # Group and compute averages
    print("Processing data...")
    grouped_data = group_by_model_and_scenario(results)
    averages = compute_averages(grouped_data)
    
    print(f"Found {len(averages)} models:")
    for model in averages.keys():
        num_scenarios = len(averages[model])
        print(f"  - {MODEL_DISPLAY_NAMES.get(model, model)}: {num_scenarios} scenarios")
    print("")
    
    # Generate plots
    print("Generating visualizations...")
    print("-" * 80)
    
    plot_overall_throughput_comparison(averages, OUTPUT_DIR)
    # plot_latency_throughput_scatter(averages, OUTPUT_DIR)  # Skipped per user request
    plot_prefill_decode_comparison(averages, OUTPUT_DIR)
    plot_speedup_summary(averages, OUTPUT_DIR)
    
    print("-" * 80)
    print("")
    
    # Generate summary table
    print("Generating summary table...")
    generate_summary_table(averages, OUTPUT_DIR)
    print("")
    
    print("=" * 80)
    print("All visualizations completed successfully!")
    print(f"Output directory: {OUTPUT_DIR}")
    print("=" * 80)


if __name__ == "__main__":
    main()

