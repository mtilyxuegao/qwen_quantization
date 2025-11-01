#!/bin/bash
# Multi-Configuration Performance Benchmark Script
# Each model server is started once and tested with all configurations
# Usage: bash performance/run_multi_config_benchmark.sh

# Activate environment
cd "$(dirname "$0")/.."
source venv/bin/activate

# Create log directories
mkdir -p logs/performance_logs/server_logs
mkdir -p logs/performance_logs/result_logs

echo "======================================"
echo "Multi-Configuration Performance Benchmark"
echo "Time: $(date)"
echo "======================================"
echo ""

# Define test configurations
# Format: CONFIG_NAME|BATCH_SIZE|INPUT_LEN|OUTPUT_LEN|DESCRIPTION
declare -a CONFIGS=(
    "base|32|256|32|Base Configuration (Current)"
    "interactive|1|128|64|Small Batch Interactive"
    "prefill_bound|1|2048|32|Long Input (Prefill-bound)"
    "decode_bound|1|256|512|Long Generation (Decode-bound)"
    "medium_batch|8|256|128|Medium Batch Processing"
    "high_concurrency|64|256|128|High Concurrency Limit"
    "long_context|1|16384|32|Ultra-Long Context"
)

# Define models to test (only successful ones)
# Format: MODEL_NAME|MODEL_PATH|QUANTIZATION|GPU_ID|PORT|DESCRIPTION
declare -a MODELS=(
    "original|Qwen/Qwen3-4B-Instruct-2507||1|30001|Original (BF16)"
    "w8a8_smooth_ptq|/data/jisenli2/huggingface/Qwen3-4B-Instruct-2507-INT8-W8A8-SMOOTH-PTQ|w8a8_int8|2|30002|W8A8-SMOOTH-PTQ"
    "w8a8_smooth_gptq|/data/jisenli2/huggingface/Qwen3-4B-Instruct-2507-INT8-W8A8-SMOOTH-GPTQ|w8a8_int8|3|30003|W8A8-SMOOTH-GPTQ"
    "w8a16_awq|/data/jisenli2/huggingface/Qwen3-4B-Instruct-2507-INT8-W8A16-AWQ||4|30004|W8A16-AWQ"
    "w8a16_smooth_awq|/data/jisenli2/huggingface/Qwen3-4B-Instruct-2507-INT8-W8A16-SMOOTH-AWQ||5|30005|W8A16-SMOOTH-AWQ"
    "w8a16_sparse_awq|/data/jisenli2/huggingface/Qwen3-4B-Instruct-2507-INT8-W8A16-SPARSE-AWQ||6|30006|W8A16-SPARSE-AWQ"
    "w8a8_sparse_smooth_gptq|/data/jisenli2/huggingface/Qwen3-4B-Instruct-2507-INT8-W8A8-SPARSE-SMOOTH-GPTQ|w8a8_int8|7|30007|W8A8-SPARSE-SMOOTH-GPTQ"
)

N_REPEATS=3

echo "Total models: ${#MODELS[@]}"
echo "Total configurations: ${#CONFIGS[@]}"
echo "Repeats per config: $N_REPEATS"
echo "Total benchmarks per model: $((${#CONFIGS[@]} * N_REPEATS))"
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

# Check available GPUs
nvidia-smi -L 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Warning: Cannot detect GPU, please check CUDA environment"
fi
echo ""

# Directory paths
SERVER_LOG_DIR="logs/performance_logs/server_logs"
RESULT_LOG_DIR="logs/performance_logs/result_logs"

# Array to track background process PIDs
pids=()

# Function to test one model (runs in background)
test_model() {
    local model_spec="$1"
    IFS='|' read -r model_name model_path quantization gpu_id port description <<< "$model_spec"
    
    echo "======================================"
    echo "🚀 [GPU $gpu_id] Testing Model: $description"
    echo "    Model Path: $model_path"
    echo "    GPU: $gpu_id | Port: $port"
    echo "======================================"
    
    # Create log directories for this model
    mkdir -p "$SERVER_LOG_DIR/$model_name"
    mkdir -p "$RESULT_LOG_DIR/$model_name"
    
    local timestamp=$(date +%Y%m%d_%H%M%S)
    local server_log="$SERVER_LOG_DIR/$model_name/server_${timestamp}.log"
    
    # Build server command
    local server_cmd="python -m sglang.launch_server --model-path \"$model_path\" --port $port --host 0.0.0.0 --tp 1"
    if [ -n "$quantization" ]; then
        server_cmd="$server_cmd --quantization $quantization"
    fi
    
    # Start server
    echo "[$(date)] 🚀 [GPU $gpu_id] Starting server..."
    CUDA_VISIBLE_DEVICES=$gpu_id bash -c "$server_cmd" > "$server_log" 2>&1 &
    local server_pid=$!
    
    echo "[$(date)] 📝 [GPU $gpu_id] Server PID: $server_pid"
    echo "[$(date)] 📄 [GPU $gpu_id] Server log: $server_log"
    
    # Wait for server to be ready (with health check)
    echo "[$(date)] ⏳ [GPU $gpu_id] Waiting for server to be ready on port $port..."
    local max_wait=300  # 5 minutes
    local waited=0
    local server_ready=false
    
    while [ $waited -lt $max_wait ]; do
        if curl -s "http://127.0.0.1:$port/get_server_info" > /dev/null 2>&1; then
            echo "[$(date)] ✅ [GPU $gpu_id] Server is ready!"
            server_ready=true
            break
        fi
        sleep 10
        waited=$((waited + 10))
        echo "[$(date)] ⏳ [GPU $gpu_id] Still waiting... ($waited/${max_wait}s)"
    done
    
    if [ "$server_ready" = false ]; then
        echo "[$(date)] ❌ [GPU $gpu_id] Server failed to start within ${max_wait}s"
        kill $server_pid 2>/dev/null
        return 1
    fi
    
    # Extra buffer time
    sleep 5
    
    # Test all configurations on this server
    local config_success=0
    local config_failed=0
    
    for config_spec in "${CONFIGS[@]}"; do
        IFS='|' read -r config_name batch_size input_len output_len config_desc <<< "$config_spec"
        
        echo ""
        echo "  📊 [GPU $gpu_id] Testing Configuration: $config_desc"
        echo "      batch_size=$batch_size, input_len=$input_len, output_len=$output_len"
        
        # Run N_REPEATS times for this configuration
        for ((i=0; i<N_REPEATS; i++)); do
            run_num=$((i+1))
            run_name="${model_name}_${config_name}_run${run_num}"
            
            echo "    [Run $run_num/$N_REPEATS] $run_name"
            
            local benchmark_log="$RESULT_LOG_DIR/$model_name/benchmark_${config_name}_${timestamp}.log"
            
            # Run benchmark
            python -m sglang.bench_one_batch_server \
                --base-url "http://127.0.0.1:$port" \
                --model-path "$model_path" \
                --batch-size $batch_size \
                --input-len $input_len \
                --output-len $output_len \
                --run-name "$run_name" \
                >> "$benchmark_log" 2>&1
            
            if [ $? -eq 0 ]; then
                echo "      ✅ Success"
                ((config_success++))
            else
                echo "      ❌ Failed"
                ((config_failed++))
            fi
            
            # Small delay between runs
            sleep 2
        done
    done
    
    echo ""
    echo "[$(date)] 📊 [GPU $gpu_id] Model $model_name completed:"
    echo "  ✅ Successful: $config_success"
    echo "  ❌ Failed: $config_failed"
    
    # Stop the server
    echo "[$(date)] 🛑 [GPU $gpu_id] Stopping server (PID: $server_pid)..."
    kill $server_pid 2>/dev/null
    sleep 3
    
    # Make sure server and port are cleaned up
    pkill -f "sglang.*$port" 2>/dev/null || true
    lsof -ti:$port | xargs kill -9 2>/dev/null || true
    
    echo "[$(date)] ✅ [GPU $gpu_id] Server stopped and port $port cleaned"
    echo ""
}

# Start all models in parallel (each in background)
echo "🚀 Starting all ${#MODELS[@]} models in parallel..."
echo ""

for model_spec in "${MODELS[@]}"; do
    test_model "$model_spec" &
    pids+=($!)
    sleep 2  # Small delay to avoid race conditions during startup
done

echo "All models started. PIDs: ${pids[@]}"
echo "⏳ Waiting for all models to complete..."
echo ""

# Wait for all background processes to finish
failed=0
for pid in "${pids[@]}"; do
    wait $pid
    exit_code=$?
    if [ $exit_code -ne 0 ]; then
        echo "⚠️  Process $pid exited with code $exit_code"
        ((failed++))
    fi
done

echo ""
echo "======================================"
if [ $failed -eq 0 ]; then
    echo "🎉 All Models Tested Successfully!"
else
    echo "⚠️  Completed with $failed failed model(s)"
fi
echo "Time: $(date)"
echo "======================================"
echo ""
echo "📊 View results:"
echo "   python performance/analyze_results.py"
echo ""

