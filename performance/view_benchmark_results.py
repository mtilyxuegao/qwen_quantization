#!/usr/bin/env python3
"""
View Performance Benchmark Results Summary
"""

import json
from pathlib import Path
from datetime import datetime

BASE_LOG_DIR = Path(__file__).parent.parent / "logs" / "performance_logs"
RESULT_LOG_DIR = BASE_LOG_DIR / "result_logs"


def load_latest_results():
    """Load latest test results for each model"""
    results = {}
    
    if not RESULT_LOG_DIR.exists():
        return results
    
    for model_dir in RESULT_LOG_DIR.iterdir():
        if not model_dir.is_dir():
            continue
        
        model_name = model_dir.name
        
        # Find latest JSON file
        json_files = sorted(model_dir.glob("benchmark_*.json"), reverse=True)
        if json_files:
            with open(json_files[0]) as f:
                data = json.load(f)
                results[model_name] = data
    
    return results


def print_comparison_table(results):
    """Print comparison table"""
    if not results:
        print("❌ No test results found")
        return
    
    print("\n" + "=" * 100)
    print("📊 Performance Benchmark Results Comparison")
    print("=" * 100)
    
    # Table header
    models = sorted(results.keys())
    print(f"\n{'Metric':<25}", end="")
    for model in models:
        print(f"{model:<25}", end="")
    print()
    print("-" * 100)
    
    # Key metrics
    metrics_to_show = [
        ("output_throughput", "Output Throughput (tok/s)"),
        ("overall_throughput", "Overall Throughput (tok/s)"),
        ("latency_s", "Latency (s)"),
        ("ttft_s", "Time to First Token (s)"),
        ("input_throughput", "Input Throughput (tok/s)"),
        ("last_gen_throughput", "Last Gen Throughput (tok/s)"),
    ]
    
    for metric_key, metric_label in metrics_to_show:
        print(f"{metric_label:<25}", end="")
        for model in models:
            avg = results[model]["average"]
            if metric_key in avg:
                value = avg[metric_key]
                std = avg.get(f"{metric_key}_std", 0)
                print(f"{value:.2f} ± {std:.2f}     ", end="")
            else:
                print(f"{'N/A':<25}", end="")
        print()
    
    print("\n" + "=" * 100)
    
    # Detailed information
    print("\n📋 Test Details:")
    for model in models:
        data = results[model]
        timestamp = data.get("timestamp", "Unknown")
        n_runs = len(data.get("individual_runs", []))
        config = data.get("config", {})
        
        print(f"\n  {model}:")
        print(f"    Timestamp: {timestamp}")
        print(f"    Number of runs: {n_runs}")
        print(f"    Config: batch_size={config.get('batch_size')}, "
              f"input_len={config.get('input_len')}, "
              f"output_len={config.get('output_len')}")


def main():
    results = load_latest_results()
    
    if not results:
        print(f"❌ No test results found in {LOG_DIR}/")
        print(f"\nPlease run first: python run_benchmark.py")
        return
    
    print_comparison_table(results)
    
    print(f"\n📁 Detailed logs location: {LOG_DIR}/")
    print()


if __name__ == "__main__":
    main()

