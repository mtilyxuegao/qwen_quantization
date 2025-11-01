#!/usr/bin/env python3
"""
Generate a summary report for selected models with mean ± max deviation.
"""

import json
from pathlib import Path
from collections import defaultdict

# Configuration
RESULT_FILE = Path(__file__).parent.parent / "result.jsonl"
OUTPUT_FILE = Path(__file__).parent / "summary_report.md"

# Selected models (match the naming in result.jsonl)
SELECTED_MODELS = {
    "original": "BF16 Baseline",
    "w8a8_smooth_ptq": "W8A8 SQ→PTQ",
    "w8a8_smooth_gptq": "W8A8 SQ→GPTQ",
    "w8a16_smooth_awq": "W8A16 SQ→AWQ"
}

# Configuration naming
CONFIG_NAMES = {
    (32, 256, 32): "Base Configuration (32,256,32)",
    (1, 128, 64): "Small Batch Interactive (1,128,64)",
    (1, 2048, 32): "Long Input (1,2048,32)",
    (1, 256, 512): "Long Generation (1,256,512)",
    (8, 256, 128): "Medium Batch Processing (8,256,128)",
    (64, 256, 128): "High Concurrency (64,256,128)",
    (1, 16384, 32): "Ultra-Long Context (1,16384,32)"
}

def load_results():
    """Load and parse result.jsonl"""
    results = []
    with open(RESULT_FILE, 'r') as f:
        for line in f:
            if line.strip():
                results.append(json.loads(line))
    return results

def extract_model_name(run_name):
    """Extract model name from run_name (remove _runX suffix and config suffix)"""
    # Remove _runX suffix
    for suffix in ["_run1", "_run2", "_run3"]:
        if run_name.endswith(suffix):
            run_name = run_name[:-len(suffix)]
            break
    
    # Remove config suffixes (must match actual run_name format)
    config_suffixes = [
        "_base",
        "_interactive", 
        "_prefill_bound",
        "_decode_bound",
        "_medium_batch",
        "_high_concurrency",
        "_long_context"
    ]
    for suffix in config_suffixes:
        if run_name.endswith(suffix):
            run_name = run_name[:-len(suffix)]
            break
    
    return run_name

def compute_max_deviation(values):
    """Compute max deviation: Max(max - avg, avg - min)"""
    if not values:
        return 0.0
    avg = sum(values) / len(values)
    max_val = max(values)
    min_val = min(values)
    return max(max_val - avg, avg - min_val)

def organize_data(results):
    """Organize results by model and configuration"""
    # Structure: model -> config -> metric -> [values]
    data = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    
    skipped_configs = set()
    processed_count = 0
    skipped_model_count = 0
    skipped_config_count = 0
    
    for result in results:
        run_name = result.get("run_name", "")
        model_name = extract_model_name(run_name)
        
        # Skip if not in selected models
        if model_name not in SELECTED_MODELS:
            skipped_model_count += 1
            continue
        
        # Get configuration
        batch_size = result.get("batch_size")
        input_len = result.get("input_len")
        output_len = result.get("output_len")
        config_key = (batch_size, input_len, output_len)
        
        # Skip if config not recognized
        if config_key not in CONFIG_NAMES:
            skipped_configs.add((config_key, run_name))
            skipped_config_count += 1
            continue
        
        # Extract metrics
        metrics = {
            "latency": result.get("latency"),
            "output_throughput": result.get("output_throughput"),
            "overall_throughput": result.get("overall_throughput")
        }
        
        # Add to data structure
        for metric, value in metrics.items():
            if value is not None:
                data[model_name][config_key][metric].append(value)
        
        processed_count += 1
    
    print(f"  Processed: {processed_count} results")
    print(f"  Skipped: {skipped_model_count} (other models) + {skipped_config_count} (unrecognized configs)")
    
    return data

def generate_markdown(data):
    """Generate markdown report"""
    lines = []
    
    # Header
    lines.append("# Performance Summary Report")
    lines.append("")
    lines.append("**Selected Models:**")
    for model_key, model_name in SELECTED_MODELS.items():
        lines.append(f"- {model_name}")
    lines.append("")
    lines.append("**Metrics:** Mean ± Max Deviation")
    lines.append("")
    lines.append("*Max Deviation = Max(max - avg, avg - min)*")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # For each model
    for model_key in SELECTED_MODELS.keys():
        model_display_name = SELECTED_MODELS[model_key]
        
        if model_key not in data:
            continue
        
        lines.append(f"## {model_display_name}")
        lines.append("")
        
        # Table header
        lines.append("| Configuration | Latency (s) | Output Throughput (tok/s) | Overall Throughput (tok/s) |")
        lines.append("|--------------|-------------|---------------------------|----------------------------|")
        
        # For each configuration (in order)
        for config_key in CONFIG_NAMES.keys():
            config_name = CONFIG_NAMES[config_key]
            
            if config_key not in data[model_key]:
                continue
            
            metrics = data[model_key][config_key]
            
            # Calculate mean and max deviation for each metric
            stats = {}
            for metric in ["latency", "output_throughput", "overall_throughput"]:
                if metric in metrics and metrics[metric]:
                    values = metrics[metric]
                    mean = sum(values) / len(values)
                    max_dev = compute_max_deviation(values)
                    stats[metric] = (mean, max_dev)
                else:
                    stats[metric] = (None, None)
            
            # Format row
            latency_mean, latency_dev = stats["latency"]
            output_mean, output_dev = stats["output_throughput"]
            overall_mean, overall_dev = stats["overall_throughput"]
            
            latency_str = f"{latency_mean:.2f} ± {latency_dev:.2f}" if latency_mean is not None else "N/A"
            output_str = f"{output_mean:.2f} ± {output_dev:.2f}" if output_mean is not None else "N/A"
            overall_str = f"{overall_mean:.2f} ± {overall_dev:.2f}" if overall_mean is not None else "N/A"
            
            lines.append(f"| {config_name} | {latency_str} | {output_str} | {overall_str} |")
        
        lines.append("")
        lines.append("---")
        lines.append("")
    
    return "\n".join(lines)

def main():
    print("=" * 80)
    print("Generating Summary Report")
    print("=" * 80)
    print()
    
    # Load results
    print(f"Loading results from: {RESULT_FILE}")
    results = load_results()
    print(f"Loaded {len(results)} benchmark results")
    print()
    
    # Organize data
    print("Organizing data...")
    data = organize_data(results)
    print(f"Processed data for {len(data)} models")
    for model_name in data:
        print(f"  - {model_name}: {len(data[model_name])} configurations")
    print()
    
    # Generate markdown
    print("Generating markdown report...")
    markdown = generate_markdown(data)
    
    # Save to file
    with open(OUTPUT_FILE, 'w') as f:
        f.write(markdown)
    
    print(f"✅ Report generated: {OUTPUT_FILE}")
    print()
    print("=" * 80)
    print()

if __name__ == "__main__":
    main()

