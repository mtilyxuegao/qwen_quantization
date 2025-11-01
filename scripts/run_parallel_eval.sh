#!/bin/bash
#SBATCH --job-name=gpqa_eval
#SBATCH --output=logs/eval_logs/eval_%A.out
#SBATCH --error=logs/eval_logs/eval_%A.err
#SBATCH --time=08:00:00
#SBATCH --gres=gpu:3
#SBATCH --cpus-per-task=64
#SBATCH --mem=400G

# Activate environment
source venv/bin/activate

# Create log subdirectory
mkdir -p logs/eval_logs

# Basic configuration
BASE_PORT=30000
MODEL_BASE="/data/jisenli2/huggingface"
HF_MODEL="Qwen/Qwen3-4B-Instruct-2507"

# Define test matrix - 3 Sparse models
# Format: MODEL_PRESET|MODEL_PATH|GPU_ID|SAMPLING_MODE|VARIANT|CONFIG_NAME|N_REPEATS
# Config: diamond + greedy + 50 repeats
declare -a TEST_CONFIGS=(
    # 3 Sparse quantized models - 50 repeats each
    "w8a16_sparse_gptq|${MODEL_BASE}/Qwen3-4B-Instruct-2507-INT8-W8A16-SPARSE-GPTQ|1|greedy|diamond||50"
    "w8a16_sparse_awq|${MODEL_BASE}/Qwen3-4B-Instruct-2507-INT8-W8A16-SPARSE-AWQ|2|greedy|diamond||50"
    "w8a8_sparse_smooth_gptq|${MODEL_BASE}/Qwen3-4B-Instruct-2507-INT8-W8A8-SPARSE-SMOOTH-GPTQ|3|greedy|diamond||50"
)

# Create logs directory
mkdir -p logs

echo "======================================"
echo "Starting Parallel Evaluation Tasks"
echo "Total tasks: ${#TEST_CONFIGS[@]}"
echo "======================================"

# Start all evaluation tasks (background parallel)
pids=()
for config in "${TEST_CONFIGS[@]}"; do
    IFS='|' read -r preset path gpu_id sampling variant config_name n_repeats <<< "$config"
    port=$((BASE_PORT + gpu_id))
    
    echo "Starting: $preset (GPU $gpu_id, Port $port)"
    
    python scripts/parallel_eval.py \
        --model-path "$path" \
        --model-preset "$preset" \
        --gpu-id "$gpu_id" \
        --port "$port" \
        --variant "$variant" \
        --config-name "$config_name" \
        --sampling-mode "$sampling" \
        --n-repeats "$n_repeats" \
        > "logs/eval_logs/${preset}_${sampling}_${variant}.log" 2>&1 &
    
    pids+=($!)
    sleep 5  # Avoid starting too many servers simultaneously
done

# Wait for all tasks to complete
echo ""
echo "Waiting for all evaluation tasks to complete..."
for pid in "${pids[@]}"; do
    wait $pid
    echo "Task PID $pid completed"
done

echo ""
echo "======================================"
echo "All evaluation tasks completed!"
echo "======================================"

