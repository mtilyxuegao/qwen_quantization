#!/usr/bin/env python3
"""
Parallel Evaluation Tool - Manages single sglang server and evaluation tasks
Called by shell script to process one model evaluation at a time
"""
import os
import sys
import time
import argparse
import subprocess
import requests


def start_server(model_path, gpu_id, port):
    """Start sglang server"""
    env = os.environ.copy()
    env["CUDA_VISIBLE_DEVICES"] = str(gpu_id)
    
    cmd = [
        "python", "-m", "sglang.launch_server",
        "--model-path", model_path,
        "--port", str(port),
        "--host", "0.0.0.0",
        "--tp", "1"
    ]
    
    # W8A8 INT8 models require quantization parameter
    if "W8A8" in model_path.upper():
        cmd.extend(["--quantization", "w8a8_int8"])
        print(f"🚀 Starting server: GPU {gpu_id}, Port {port}, Model: {model_path} (W8A8 INT8)")
    else:
        print(f"🚀 Starting server: GPU {gpu_id}, Port {port}, Model: {model_path}")
    
    process = subprocess.Popen(cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return process


def wait_for_server(port, timeout=300):
    """Wait for server to be ready"""
    start = time.time()
    while time.time() - start < timeout:
        try:
            response = requests.get(f"http://localhost:{port}/health", timeout=2)
            if response.status_code == 200:
                print(f"✅ Server ready on port {port}")
                return True
        except:
            pass
        time.sleep(5)
    return False


def run_evaluation(model_preset, base_url, variant, config_name, sampling_mode, n_repeats):
    """Run evaluation"""
    cmd = [
        "python", "run_gpqa_sglang.py",
        "--model", model_preset,
        "--base-url", base_url,
        "--variant", variant,
        "--n-repeats", str(n_repeats)
    ]
    
    # config_name is optional
    if config_name:
        cmd.extend(["--config-name", config_name])
    
    if sampling_mode == "greedy":
        cmd.append("--greedy")
    
    print(f"📊 Running evaluation: {model_preset} + {sampling_mode} + {variant}")
    if config_name:
        print(f"   Config: {config_name}")
    result = subprocess.run(cmd)
    return result.returncode == 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-path", required=True, help="Model path or HF ID")
    parser.add_argument("--model-preset", required=True, help="Preset model name")
    parser.add_argument("--gpu-id", type=int, required=True, help="GPU ID")
    parser.add_argument("--port", type=int, required=True, help="Port number")
    parser.add_argument("--variant", default="diamond", help="Dataset variant")
    parser.add_argument("--config-name", default=None, help="Optional configuration name")
    parser.add_argument("--sampling-mode", default="dosample", choices=["dosample", "greedy"])
    parser.add_argument("--n-repeats", type=int, default=10, help="Number of repeats")
    args = parser.parse_args()
    
    # Start server
    server_process = start_server(args.model_path, args.gpu_id, args.port)
    
    try:
        # Wait for server to be ready
        if not wait_for_server(args.port):
            print(f"❌ Server startup timeout")
            return 1
        
        # Run evaluation
        base_url = f"http://127.0.0.1:{args.port}/v1"
        success = run_evaluation(
            args.model_preset, base_url, args.variant,
            args.config_name, args.sampling_mode, args.n_repeats
        )
        
        return 0 if success else 1
        
    finally:
        # Cleanup server
        print(f"🛑 Shutting down server (port {args.port})")
        server_process.terminate()
        try:
            server_process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            server_process.kill()


if __name__ == "__main__":
    sys.exit(main())

