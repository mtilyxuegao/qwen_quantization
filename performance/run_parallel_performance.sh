#!/bin/bash
# Parallel Performance Benchmark Script (Background Execution)
# Usage: bash performance/run_parallel_performance.sh

# Activate environment
cd "$(dirname "$0")/.."
source venv/bin/activate

# Create log directories
mkdir -p logs/performance_logs/server_logs
mkdir -p logs/performance_logs/result_logs

echo "======================================"
echo "Starting Parallel Performance Benchmark"
echo "Time: $(date)"
echo "======================================"

# Benchmark configuration (can be modified)
BATCH_SIZE=32
INPUT_LEN=256
OUTPUT_LEN=32
N_REPEATS=3

echo "Config: batch_size=$BATCH_SIZE, input_len=$INPUT_LEN, output_len=$OUTPUT_LEN"
echo "Repeats per model: $N_REPEATS"
echo ""

# Clean up any existing sglang processes and ports
echo "Cleaning up existing sglang processes..."
pkill -f sglang 2>/dev/null || true
for port in {30001..30007}; do
    lsof -ti:$port | xargs kill -9 2>/dev/null || true
done
sleep 3
echo "✅ Cleanup completed"
echo ""

# Define benchmark tasks
# Format: MODEL_NAME|MODEL_PATH|QUANTIZATION|GPU_ID|PORT|DESCRIPTION
declare -a PERF_TASKS=(
    # ============================================
    # ✅ COMPLETED MODELS (7 models, 3 runs each)
    # ============================================
    # "original|Qwen/Qwen3-4B-Instruct-2507||1|30001|Original (BF16)"  # ✅ Completed
    # "w8a8_smooth_ptq|/data/jisenli2/huggingface/Qwen3-4B-Instruct-2507-INT8-W8A8-SMOOTH-PTQ|w8a8_int8|2|30002|W8A8-SMOOTH-PTQ"  # ✅ Completed
    # "w8a8_smooth_gptq|/data/jisenli2/huggingface/Qwen3-4B-Instruct-2507-INT8-W8A8-SMOOTH-GPTQ|w8a8_int8|3|30003|W8A8-SMOOTH-GPTQ"  # ✅ Completed
    # "w8a16_awq|/data/jisenli2/huggingface/Qwen3-4B-Instruct-2507-INT8-W8A16-AWQ||4|30004|W8A16-AWQ"  # ✅ Completed
    # "w8a16_smooth_awq|/data/jisenli2/huggingface/Qwen3-4B-Instruct-2507-INT8-W8A16-SMOOTH-AWQ||2|30002|W8A16-SMOOTH-AWQ"  # ✅ Completed
    # "w8a16_sparse_awq|/data/jisenli2/huggingface/Qwen3-4B-Instruct-2507-INT8-W8A16-SPARSE-AWQ||4|30004|W8A16-SPARSE-AWQ"  # ✅ Completed
    # "w8a8_sparse_smooth_gptq|/data/jisenli2/huggingface/Qwen3-4B-Instruct-2507-INT8-W8A8-SPARSE-SMOOTH-GPTQ|w8a8_int8|5|30005|W8A8-SPARSE-SMOOTH-GPTQ"  # ✅ Completed
    
    # ============================================
    # ❌ FAILED MODELS (4 models with issues)
    # ============================================
    # These models consistently fail with CUDA errors or other issues:
    # "w8a16_smooth_gptq|/data/jisenli2/huggingface/Qwen3-4B-Instruct-2507-INT8-W8A16-SMOOTH-GPTQ||1|30001|W8A16-SMOOTH-GPTQ"  # ❌ Failed (0/3)
    # "w8a16_sparse_gptq|/data/jisenli2/huggingface/Qwen3-4B-Instruct-2507-INT8-W8A16-SPARSE-GPTQ||3|30003|W8A16-SPARSE-GPTQ"  # ❌ Failed (0/3)
    # "w8a16_ptq|/data/jisenli2/huggingface/Qwen3-4B-Instruct-2507-INT8-W8A16-PTQ||6|30006|W8A16-PTQ"  # ❌ Failed (0/3)
    # "w8a16_gptq|/data/jisenli2/huggingface/Qwen3-4B-Instruct-2507-INT8-W8A16-GPTQ||7|30007|W8A16-GPTQ"  # ❌ Failed (0/3) - CUDA error
    
    # ============================================
    # 🔄 REMAINING MODELS TO TEST
    # ============================================
    # "w8a16_smooth_ptq|/data/jisenli2/huggingface/Qwen3-4B-Instruct-2507-INT8-W8A16-SMOOTH-PTQ||1|30001|W8A16-SMOOTH-PTQ"  # Not tested yet
)

echo "Total active tasks: ${#PERF_TASKS[@]}"
echo ""

# Check available GPUs
nvidia-smi -L 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Warning: Cannot detect GPU, please check CUDA environment"
fi
echo ""

# Start all benchmark tasks (parallel in background)
pids=()
timestamp=$(date +%Y%m%d_%H%M%S)

for task in "${PERF_TASKS[@]}"; do
    IFS='|' read -r model_name model_path quantization gpu_id port description <<< "$task"
    
    # Create log directories
    mkdir -p "logs/performance_logs/server_logs/${model_name}"
    mkdir -p "logs/performance_logs/result_logs/${model_name}"
    
    server_log="logs/performance_logs/server_logs/${model_name}/server_${timestamp}.log"
    benchmark_log="logs/performance_logs/result_logs/${model_name}/benchmark_${timestamp}.log"
    
    echo "Starting benchmark: $description"
    echo "  Model: $model_name"
    echo "  GPU: $gpu_id, Port: $port"
    echo "  Server log: $server_log"
    echo "  Benchmark log: $benchmark_log"
    echo ""
    
    # Build quantization argument
    quant_arg=""
    if [ -n "$quantization" ]; then
        quant_arg="--quantization $quantization"
    fi
    
    # Run benchmark in background
    (
        # Start server in background
        CUDA_VISIBLE_DEVICES=$gpu_id python -m sglang.launch_server \
            --model-path "$model_path" \
            --port "$port" \
            --host 0.0.0.0 \
            --tp 1 \
            $quant_arg \
            > "$server_log" 2>&1 &
        
        server_pid=$!
        
        # Wait for server to be ready (with health check)
        echo "[$(date)] Waiting for server to be ready on port $port..." >> "$benchmark_log"
        max_wait=300  # 5 minutes
        waited=0
        while [ $waited -lt $max_wait ]; do
            if curl -s "http://127.0.0.1:$port/get_server_info" > /dev/null 2>&1; then
                echo "[$(date)] ✅ Server is ready!" >> "$benchmark_log"
                break
            fi
            sleep 10
            waited=$((waited + 10))
            echo "[$(date)] Still waiting... ($waited/${max_wait}s)" >> "$benchmark_log"
        done
        
        if [ $waited -ge $max_wait ]; then
            echo "[$(date)] ❌ Server failed to start within ${max_wait}s" >> "$benchmark_log"
            kill $server_pid 2>/dev/null
            exit 1
        fi
        
        # Extra buffer time
        sleep 5
        
        # Run benchmark 3 times
        for run_num in 1 2 3; do
            echo "[$(date)] Run $run_num/$N_REPEATS for $model_name..." >> "$benchmark_log"
            
            python -m sglang.bench_one_batch_server \
                --base-url "http://127.0.0.1:$port" \
                --model-path "$model_path" \
                --batch-size "$BATCH_SIZE" \
                --input-len "$INPUT_LEN" \
                --output-len "$OUTPUT_LEN" \
                --run-name "${model_name}_run${run_num}" \
                >> "$benchmark_log" 2>&1
            
            if [ $? -eq 0 ]; then
                echo "[$(date)] ✅ Run $run_num completed" >> "$benchmark_log"
            else
                echo "[$(date)] ❌ Run $run_num failed" >> "$benchmark_log"
            fi
            
            # Short break between runs
            if [ $run_num -lt $N_REPEATS ]; then
                sleep 5
            fi
        done
        
        # Kill server
        kill $server_pid 2>/dev/null
        
        # Clean up port
        lsof -ti:$port | xargs kill -9 2>/dev/null || true
        
        echo "[$(date)] Benchmark completed for $model_name" >> "$benchmark_log"
        
    ) &
    
    pids+=($!)
    
    # Avoid starting too many tasks at once
    sleep 5
done

echo "======================================"
echo "All benchmark tasks started, waiting for completion..."
echo "======================================"
echo ""
echo "Monitor logs in real-time:"
for task in "${PERF_TASKS[@]}"; do
    IFS='|' read -r model_name model_path quantization gpu_id port description <<< "$task"
    echo "  tail -f logs/performance_logs/result_logs/${model_name}/benchmark_${timestamp}.log"
done
echo ""

# Wait for all tasks to complete
success_count=0
fail_count=0

for i in "${!pids[@]}"; do
    pid=${pids[$i]}
    task=${PERF_TASKS[$i]}
    IFS='|' read -r model_name model_path quantization gpu_id port description <<< "$task"
    
    echo "Waiting for task: $description (PID $pid)..."
    wait $pid
    exit_code=$?
    
    if [ $exit_code -eq 0 ]; then
        echo "✅ Task completed: $description"
        ((success_count++))
    else
        echo "❌ Task failed: $description (Exit Code: $exit_code)"
        echo "   Check logs:"
        echo "     Server: logs/performance_logs/server_logs/${model_name}/server_${timestamp}.log"
        echo "     Benchmark: logs/performance_logs/result_logs/${model_name}/benchmark_${timestamp}.log"
        ((fail_count++))
    fi
    echo ""
done

echo ""
echo "======================================"
echo "All benchmark tasks completed!"
echo "Time: $(date)"
echo "======================================"
echo "Success: $success_count"
echo "Fail: $fail_count"
echo ""

# Clean up sglang processes and ports
echo "Cleaning up sglang processes and ports..."
pkill -f sglang 2>/dev/null || true
for port in {30001..30007}; do
    lsof -ti:$port | xargs kill -9 2>/dev/null || true
done
echo "✅ Cleanup completed"
echo ""

echo "Results saved in:"
echo "  Server logs: logs/performance_logs/server_logs/"
echo "  Benchmark results: logs/performance_logs/result_logs/"
echo ""
echo "View summary (after processing logs):"
echo "  python performance/view_benchmark_results.py"
echo ""
