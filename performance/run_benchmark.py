#!/usr/bin/env python3
"""
Automated Performance Benchmark Script
- Run each model 3 times and calculate average
- Auto-save logs to logs/performance_logs/
"""

import subprocess
import time
import json
import re
import argparse
from pathlib import Path
from datetime import datetime

# Configuration
MODELS = [
    {
        "name": "original",
        "path": "Qwen/Qwen3-4B-Instruct-2507",
        "quantization": None,
    },
    {
        "name": "w8a8_smooth_ptq",
        "path": "/data/jisenli2/huggingface/Qwen3-4B-Instruct-2507-INT8-W8A8-SMOOTH-PTQ",
        "quantization": "w8a8_int8",
    },
    {
        "name": "w8a16_smooth_awq",
        "path": "/data/jisenli2/huggingface/Qwen3-4B-Instruct-2507-INT8-W8A16-SMOOTH-AWQ",
        "quantization": None,
    },
    {
        "name": "w8a16_smooth_ptq",
        "path": "/data/jisenli2/huggingface/Qwen3-4B-Instruct-2507-INT8-W8A16-SMOOTH-PTQ",
        "quantization": None,
    },
]

BENCHMARK_CONFIG = {
    "port": 30000,
    "gpu": 1,  # Use GPU 1-7, avoid GPU 0
    "batch_size": 32,
    "input_len": 256,
    "output_len": 32,
    "n_repeats": 3,  # Run each model 3 times
}

BASE_LOG_DIR = Path(__file__).parent.parent / "logs" / "performance_logs"
SERVER_LOG_DIR = BASE_LOG_DIR / "server_logs"
RESULT_LOG_DIR = BASE_LOG_DIR / "result_logs"


def start_server(model_path, port, gpu, quantization=None, server_log_file=None):
    """Start sglang server"""
    cmd = [
        "python", "-m", "sglang.launch_server",
        "--model-path", model_path,
        "--port", str(port),
        "--host", "0.0.0.0",
        "--tp", "1",
    ]
    
    if quantization:
        cmd.extend(["--quantization", quantization])
    
    env = {"CUDA_VISIBLE_DEVICES": str(gpu)}
    
    print(f"  🚀 Starting server: {model_path}")
    
    # Redirect server output to log file if provided
    if server_log_file:
        log_file = open(server_log_file, "w")
        process = subprocess.Popen(
            cmd,
            env={**subprocess.os.environ, **env},
            stdout=log_file,
            stderr=subprocess.STDOUT,  # Redirect stderr to stdout
        )
        print(f"  📝 Server log: {server_log_file}")
    else:
        process = subprocess.Popen(
            cmd,
            env={**subprocess.os.environ, **env},
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    
    # Wait for server to be ready
    print(f"  ⏳ Waiting for server to be ready...")
    time.sleep(20)
    
    return process


def run_benchmark(model_path, port, batch_size, input_len, output_len, run_name="default", retry=True):
    """Run benchmark once with optional retry on failure"""
    cmd = [
        "python", "-m", "sglang.bench_one_batch_server",
        "--base-url", f"http://127.0.0.1:{port}",
        "--model-path", model_path,
        "--batch-size", str(batch_size),
        "--input-len", str(input_len),
        "--output-len", str(output_len),
        "--run-name", run_name,
    ]
    
    max_attempts = 2 if retry else 1
    
    for attempt in range(max_attempts):
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300,
            )
            
            # Check for common errors
            if "ZeroDivisionError" in result.stderr or "ZeroDivisionError" in result.stdout:
                if attempt < max_attempts - 1:
                    print(f"     ⚠️  ZeroDivisionError detected, retrying...")
                    time.sleep(2)
                    continue
                else:
                    print(f"     ❌ Benchmark failed after {max_attempts} attempts")
                    return ""
            
            return result.stdout
            
        except subprocess.TimeoutExpired:
            if attempt < max_attempts - 1:
                print(f"     ⚠️  Timeout, retrying...")
                time.sleep(2)
            else:
                print(f"     ❌ Benchmark timeout after {max_attempts} attempts")
                return ""
    
    return ""


def parse_benchmark_output(output):
    """Parse benchmark output from sglang.bench_one_batch_server"""
    metrics = {}
    
    # Parse from the summary section (after warmup)
    patterns = {
        "latency_s": r"latency:\s*([\d.]+)\s*s",
        "ttft_s": r"ttft:\s*([\d.]+)\s*s",
        "output_throughput": r"output throughput:\s*([\d.]+)\s*tok/s",
        "overall_throughput": r"overall throughput:\s*([\d.]+)\s*tok/s",
        "last_gen_throughput": r"last generation throughput:\s*([\d.]+)\s*tok/s",
        "input_throughput": r"input throughput:\s*([\d.]+)\s*tok/s",
    }
    
    # Find the section after "Warmup End"
    warmup_end_idx = output.find("======== Warmup End")
    if warmup_end_idx != -1:
        output_section = output[warmup_end_idx:]
    else:
        output_section = output
    
    for key, pattern in patterns.items():
        match = re.search(pattern, output_section, re.IGNORECASE)
        if match:
            metrics[key] = float(match.group(1))
    
    return metrics


def compute_average(results):
    """Compute average of multiple runs"""
    if not results:
        return {}
    
    avg = {}
    keys = results[0].keys()
    
    for key in keys:
        values = [r[key] for r in results if key in r]
        if values:
            avg[key] = sum(values) / len(values)
            avg[f"{key}_std"] = (sum((x - avg[key])**2 for x in values) / len(values))**0.5
    
    return avg


def save_results(model_name, run_results, avg_results, raw_outputs):
    """Save results to log files"""
    log_dir = RESULT_LOG_DIR / model_name
    log_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save JSON results
    json_file = log_dir / f"benchmark_{timestamp}.json"
    data = {
        "timestamp": timestamp,
        "model_name": model_name,
        "config": BENCHMARK_CONFIG,
        "individual_runs": run_results,
        "average": avg_results,
    }
    
    with open(json_file, "w") as f:
        json.dump(data, f, indent=2)
    
    # Save raw outputs
    for i, output in enumerate(raw_outputs, 1):
        raw_file = log_dir / f"benchmark_{timestamp}_run{i}.log"
        with open(raw_file, "w") as f:
            f.write(output)
    
    # Save summary report
    summary_file = log_dir / f"benchmark_{timestamp}_summary.txt"
    with open(summary_file, "w") as f:
        f.write(f"=" * 70 + "\n")
        f.write(f"Performance Benchmark Summary - {model_name}\n")
        f.write(f"Timestamp: {timestamp}\n")
        f.write(f"=" * 70 + "\n\n")
        
        f.write("Configuration:\n")
        f.write(f"  Batch Size: {BENCHMARK_CONFIG['batch_size']}\n")
        f.write(f"  Input Length: {BENCHMARK_CONFIG['input_len']}\n")
        f.write(f"  Output Length: {BENCHMARK_CONFIG['output_len']}\n")
        f.write(f"  Repeats: {BENCHMARK_CONFIG['n_repeats']}\n\n")
        
        f.write("Average Results:\n")
        for key, value in sorted(avg_results.items()):
            if not key.endswith("_std"):
                std_key = f"{key}_std"
                std_val = avg_results.get(std_key, 0)
                f.write(f"  {key}: {value:.2f} ± {std_val:.2f}\n")
        
        f.write("\n" + "=" * 70 + "\n")
    
    print(f"  💾 Results saved to: {log_dir}")
    return json_file, summary_file


def benchmark_model(model_config):
    """Benchmark a single model completely"""
    name = model_config["name"]
    path = model_config["path"]
    quantization = model_config.get("quantization")
    
    print(f"\n{'=' * 70}")
    print(f"📊 Benchmarking Model: {name}")
    print(f"{'=' * 70}")
    
    server_process = None
    
    try:
        # Create server log directory and file
        server_log_dir = SERVER_LOG_DIR / name
        server_log_dir.mkdir(parents=True, exist_ok=True)
        server_log_file = server_log_dir / f"server_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        # Start server
        server_process = start_server(
            path,
            BENCHMARK_CONFIG["port"],
            BENCHMARK_CONFIG["gpu"],
            quantization,
            server_log_file=server_log_file,
        )
        
        # Run benchmark multiple times
        run_results = []
        raw_outputs = []
        
        for i in range(BENCHMARK_CONFIG["n_repeats"]):
            print(f"\n  🔄 Run {i + 1}/{BENCHMARK_CONFIG['n_repeats']}...")
            
            run_name = f"{name}_run{i+1}"
            output = run_benchmark(
                path,
                BENCHMARK_CONFIG["port"],
                BENCHMARK_CONFIG["batch_size"],
                BENCHMARK_CONFIG["input_len"],
                BENCHMARK_CONFIG["output_len"],
                run_name=run_name,
                retry=True,
            )
            
            raw_outputs.append(output)
            
            if not output:
                print(f"     ❌ Benchmark failed, skipping this run")
                continue
            
            metrics = parse_benchmark_output(output)
            
            if metrics:
                run_results.append(metrics)
                print(f"     ✅ Completed")
                # Show key metrics
                if "output_throughput" in metrics:
                    print(f"     📈 Output Throughput: {metrics['output_throughput']:.2f} tok/s")
                if "latency_s" in metrics:
                    print(f"     ⏱️  Latency: {metrics['latency_s']:.3f}s")
            else:
                print(f"     ⚠️  Warning: Failed to parse output")
            
            # Short break between runs
            if i < BENCHMARK_CONFIG["n_repeats"] - 1:
                time.sleep(5)
        
        # Check if we have enough successful runs
        if not run_results:
            print(f"\n  ❌ All runs failed, no results to save")
            return False
        
        if len(run_results) < BENCHMARK_CONFIG["n_repeats"]:
            print(f"\n  ⚠️  Warning: Only {len(run_results)}/{BENCHMARK_CONFIG['n_repeats']} runs succeeded")
        
        # Compute average
        avg_results = compute_average(run_results)
        
        # Save results
        json_file, summary_file = save_results(name, run_results, avg_results, raw_outputs)
        
        # Print summary
        print(f"\n  📊 Average Results ({len(run_results)} runs):")
        for key, value in sorted(avg_results.items()):
            if not key.endswith("_std"):
                std_key = f"{key}_std"
                std_val = avg_results.get(std_key, 0)
                print(f"     {key}: {value:.2f} ± {std_val:.2f}")
        
        # Return True if we have at least 1 successful run
        return len(run_results) > 0
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False
        
    finally:
        # Stop server
        if server_process:
            print(f"\n  🛑 Stopping server...")
            server_process.terminate()
            try:
                server_process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                server_process.kill()
            time.sleep(5)


def benchmark_single_model(model_name, model_path, quantization, gpu, port, batch_size, input_len, output_len, n_repeats):
    """Benchmark a single model with specified parameters (for parallel execution)"""
    model_config = {
        "name": model_name,
        "path": model_path,
        "quantization": quantization,
    }
    
    # Override config
    BENCHMARK_CONFIG["port"] = port
    BENCHMARK_CONFIG["gpu"] = gpu
    BENCHMARK_CONFIG["batch_size"] = batch_size
    BENCHMARK_CONFIG["input_len"] = input_len
    BENCHMARK_CONFIG["output_len"] = output_len
    BENCHMARK_CONFIG["n_repeats"] = n_repeats
    
    return benchmark_model(model_config)


def main():
    parser = argparse.ArgumentParser(description="Performance Benchmark for Qwen models")
    parser.add_argument("--model-name", type=str, help="Model name (e.g., original, w8a8_smooth_ptq)")
    parser.add_argument("--model-path", type=str, help="Path to model")
    parser.add_argument("--quantization", type=str, default=None, help="Quantization method (e.g., w8a8_int8)")
    parser.add_argument("--gpu", type=int, default=0, help="GPU device ID")
    parser.add_argument("--port", type=int, default=30000, help="Server port")
    parser.add_argument("--batch-size", type=int, default=32, help="Batch size")
    parser.add_argument("--input-len", type=int, default=256, help="Input length")
    parser.add_argument("--output-len", type=int, default=32, help="Output length")
    parser.add_argument("--n-repeats", type=int, default=3, help="Number of repeats")
    
    args = parser.parse_args()
    
    # Single model mode
    if args.model_name and args.model_path:
        print("\n" + "=" * 70)
        print("🚀 Single Model Benchmark Mode")
        print("=" * 70)
        print(f"Model: {args.model_name}")
        print(f"GPU: {args.gpu}, Port: {args.port}")
        print(f"Config: batch_size={args.batch_size}, input_len={args.input_len}, output_len={args.output_len}")
        print(f"Repeats: {args.n_repeats}")
        print("=" * 70 + "\n")
        
        success = benchmark_single_model(
            args.model_name,
            args.model_path,
            args.quantization,
            args.gpu,
            args.port,
            args.batch_size,
            args.input_len,
            args.output_len,
            args.n_repeats,
        )
        
        if success:
            print("\n✅ Benchmark completed successfully")
            exit(0)
        else:
            print("\n❌ Benchmark failed")
            exit(1)
    
    # Batch mode (all models)
    else:
        print("\n" + "=" * 70)
        print("🚀 Starting Performance Benchmark (Batch Mode)")
        print("=" * 70)
        print(f"Config: batch_size={BENCHMARK_CONFIG['batch_size']}, "
              f"input_len={BENCHMARK_CONFIG['input_len']}, "
              f"output_len={BENCHMARK_CONFIG['output_len']}")
        print(f"Running each model {BENCHMARK_CONFIG['n_repeats']} times to calculate average")
        print(f"Results will be saved to: {LOG_DIR}/")
        
        success_count = 0
        
        for model_config in MODELS:
            success = benchmark_model(model_config)
            if success:
                success_count += 1
        
        print(f"\n" + "=" * 70)
        print(f"✅ Benchmark Completed: {success_count}/{len(MODELS)} models succeeded")
        print(f"📁 Log directory: {LOG_DIR}/")
        print("=" * 70 + "\n")


if __name__ == "__main__":
    main()

