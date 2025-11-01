#!/usr/bin/env python3
"""
Analyze benchmark results from result.jsonl and generate markdown report
"""

import json
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Any
import statistics


def parse_result_file(result_file: Path) -> List[Dict[str, Any]]:
    """Parse result.jsonl file"""
    results = []
    with open(result_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                results.append(json.loads(line))
    return results


def extract_model_name(run_name: str) -> str:
    """Extract model name from run_name (e.g., 'w8a8_smooth_ptq_run1' -> 'w8a8_smooth_ptq')"""
    parts = run_name.rsplit('_run', 1)
    return parts[0] if len(parts) > 1 else run_name


def group_by_config_and_model(results: List[Dict[str, Any]]) -> Dict[tuple, Dict[str, List[Dict]]]:
    """
    Group results by configuration and model
    Returns: {(batch_size, input_len, output_len): {model_name: [result1, result2, ...]}}
    """
    grouped = defaultdict(lambda: defaultdict(list))
    
    for result in results:
        config = (result['batch_size'], result['input_len'], result['output_len'])
        model_name = extract_model_name(result['run_name'])
        grouped[config][model_name].append(result)
    
    return grouped


def calculate_stats(values: List[float]) -> Dict[str, float]:
    """Calculate mean and std for a list of values"""
    if not values:
        return {'mean': 0.0, 'std': 0.0, 'count': 0}
    
    return {
        'mean': statistics.mean(values),
        'std': statistics.stdev(values) if len(values) > 1 else 0.0,
        'count': len(values)
    }


def analyze_model_results(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze results for a single model"""
    metrics = ['latency', 'output_throughput', 'overall_throughput', 'input_throughput']
    
    analysis = {
        'run_count': len(results),
        'runs': []
    }
    
    # Collect all runs
    for result in results:
        run_data = {'run_name': result['run_name']}
        for metric in metrics:
            if metric in result:
                run_data[metric] = result[metric]
        analysis['runs'].append(run_data)
    
    # Calculate statistics for each metric
    for metric in metrics:
        values = [r[metric] for r in results if metric in r]
        if values:
            analysis[metric] = calculate_stats(values)
    
    return analysis


def format_value(value: float, std: float = None) -> str:
    """Format value with optional std"""
    if std is not None and std > 0:
        return f"{value:.2f} ± {std:.2f}"
    else:
        return f"{value:.2f}"


def generate_markdown_report(grouped_results: Dict[tuple, Dict[str, List[Dict]]]) -> str:
    """Generate markdown report from grouped results"""
    
    md_lines = ["# Performance Benchmark Results\n"]
    md_lines.append(f"**Generated from:** `result.jsonl`\n")
    md_lines.append("---\n")
    
    for config, models in sorted(grouped_results.items()):
        batch_size, input_len, output_len = config
        
        md_lines.append(f"\n## Configuration: batch_size={batch_size}, input_len={input_len}, output_len={output_len}\n")
        md_lines.append(f"**Total models tested:** {len(models)}\n")
        
        # Analyze each model
        model_stats = {}
        for model_name, results in models.items():
            model_stats[model_name] = analyze_model_results(results)
        
        # Summary table
        md_lines.append("\n### Summary Table\n")
        md_lines.append("| Model | Runs | Latency (s) | Output Throughput (tok/s) | Overall Throughput (tok/s) | Input Throughput (tok/s) |")
        md_lines.append("|-------|------|-------------|---------------------------|----------------------------|--------------------------|")
        
        # Sort models by output_throughput (descending)
        sorted_models = sorted(
            model_stats.items(),
            key=lambda x: x[1].get('output_throughput', {}).get('mean', 0),
            reverse=True
        )
        
        for model_name, stats in sorted_models:
            runs = stats['run_count']
            
            # Format metrics with mean ± std
            latency = format_value(
                stats.get('latency', {}).get('mean', 0),
                stats.get('latency', {}).get('std', 0)
            )
            
            output_throughput = format_value(
                stats.get('output_throughput', {}).get('mean', 0),
                stats.get('output_throughput', {}).get('std', 0)
            )
            
            overall_throughput = format_value(
                stats.get('overall_throughput', {}).get('mean', 0),
                stats.get('overall_throughput', {}).get('std', 0)
            )
            
            input_throughput = format_value(
                stats.get('input_throughput', {}).get('mean', 0),
                stats.get('input_throughput', {}).get('std', 0)
            )
            
            md_lines.append(
                f"| `{model_name}` | {runs} | {latency} | {output_throughput} | {overall_throughput} | {input_throughput} |"
            )
        
        # Detailed breakdown for each model
        md_lines.append("\n### Detailed Results\n")
        
        for model_name, stats in sorted(model_stats.items()):
            md_lines.append(f"\n#### {model_name}\n")
            md_lines.append(f"- **Total runs:** {stats['run_count']}\n")
            
            # Individual runs
            md_lines.append("- **Individual runs:**\n")
            for run in stats['runs']:
                run_name = run['run_name']
                md_lines.append(f"  - `{run_name}`:")
                
                latency_val = run.get('latency')
                md_lines.append(f"    - Latency: {latency_val:.2f}s" if latency_val is not None else "    - Latency: N/A")
                
                output_tp = run.get('output_throughput')
                md_lines.append(f"    - Output Throughput: {output_tp:.2f} tok/s" if output_tp is not None else "    - Output Throughput: N/A")
                
                overall_tp = run.get('overall_throughput')
                md_lines.append(f"    - Overall Throughput: {overall_tp:.2f} tok/s" if overall_tp is not None else "    - Overall Throughput: N/A")
                
                input_tp = run.get('input_throughput')
                md_lines.append(f"    - Input Throughput: {input_tp:.2f} tok/s" if input_tp is not None else "    - Input Throughput: N/A")
            
            # Statistics
            md_lines.append("- **Statistics:**\n")
            for metric in ['latency', 'output_throughput', 'overall_throughput', 'input_throughput']:
                if metric in stats:
                    metric_stats = stats[metric]
                    metric_display = metric.replace('_', ' ').title()
                    md_lines.append(
                        f"  - {metric_display}: {metric_stats['mean']:.2f} ± {metric_stats['std']:.2f}"
                    )
    
    # Performance ranking
    md_lines.append("\n---\n")
    md_lines.append("\n## Performance Ranking (by Output Throughput)\n")
    
    for config, models in sorted(grouped_results.items()):
        batch_size, input_len, output_len = config
        
        # Calculate average output_throughput for each model
        model_perf = []
        for model_name, results in models.items():
            stats = analyze_model_results(results)
            avg_throughput = stats.get('output_throughput', {}).get('mean', 0)
            model_perf.append((model_name, avg_throughput))
        
        # Sort by throughput (descending)
        model_perf.sort(key=lambda x: x[1], reverse=True)
        
        md_lines.append(f"\n### Configuration: batch_size={batch_size}, input_len={input_len}, output_len={output_len}\n")
        
        for rank, (model_name, throughput) in enumerate(model_perf, 1):
            emoji = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else f"{rank}."
            md_lines.append(f"{emoji} **{model_name}**: {throughput:.2f} tok/s")
    
    return "\n".join(md_lines)


def main():
    # Paths
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    result_file = project_root / "result.jsonl"
    output_file = script_dir / "benchmark_analysis.md"
    
    # Check if result file exists
    if not result_file.exists():
        print(f"❌ Error: {result_file} not found!")
        return
    
    print(f"📊 Analyzing results from: {result_file}")
    
    # Parse results
    results = parse_result_file(result_file)
    print(f"✅ Parsed {len(results)} benchmark results")
    
    # Group by configuration and model
    grouped = group_by_config_and_model(results)
    print(f"📋 Found {len(grouped)} configuration(s)")
    
    for config, models in grouped.items():
        batch_size, input_len, output_len = config
        print(f"  - Config (batch={batch_size}, input={input_len}, output={output_len}): {len(models)} models")
    
    # Generate markdown report
    markdown = generate_markdown_report(grouped)
    
    # Save report
    with open(output_file, 'w') as f:
        f.write(markdown)
    
    print(f"\n✅ Report generated: {output_file}")
    print(f"📄 View the report:")
    print(f"   cat {output_file}")


if __name__ == "__main__":
    main()

