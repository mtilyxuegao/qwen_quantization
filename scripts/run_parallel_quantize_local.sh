#!/bin/bash
# Local parallel quantization script (no sbatch needed)
# Usage: bash scripts/run_parallel_quantize_local.sh

# Activate environment
source venv/bin/activate

# Create logs directory
mkdir -p logs

echo "======================================"
echo "Starting Parallel Quantization Tasks (Local Mode)"
echo "Time: $(date)"
echo "======================================"

# Define quantization tasks
# Format: METHOD|GPU_ID|DESCRIPTION
# Note: AWQ doesn't support A8, so only 3 W8A8 methods
declare -a QUANT_TASKS=(
    # ============ W8A8 Valid Configs (3 methods) ============
    "w8a8_smooth_gptq|0|⭐ SmoothQuant+GPTQ W8A8"
    "w8a8_smooth_ptq|1|SmoothQuant+PTQ W8A8 (fast baseline)"
    "w8a8_sparse_smooth_gptq|2|SparseGPT→SmoothQuant+GPTQ W8A8 (memory efficient)"
    
    # ============ W8A16 Standard Methods (5 methods) ============
    "w8a16_ptq|3|Simple PTQ W8A16 (baseline)"
    "w8a16_gptq|4|GPTQ W8A16"
    "w8a16_awq|5|AWQ W8A16"
    "w8a16_sparse_gptq|6|SparseGPT+GPTQ W8A16"
    "w8a16_smooth_gptq|7|SmoothQuant+GPTQ W8A16"
    
    # ============ W8A16 Additional Methods (2 methods) ============
    # "w8a16_sparse_awq|0|SparseGPT+AWQ W8A16"
    # "w8a16_smooth_awq|1|SmoothQuant+AWQ W8A16"
)

echo "Total tasks: ${#QUANT_TASKS[@]}"
echo ""

# Create base temporary directory (avoid multi-process conflicts)
BASE_TEMP_DIR="/data/jisenli2/quant_temp"
mkdir -p $BASE_TEMP_DIR
echo "Base temporary directory: $BASE_TEMP_DIR"
echo ""

# Check available GPUs
nvidia-smi -L 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Warning: Cannot detect GPUs, please check CUDA environment"
fi
echo ""

# Start all quantization tasks (background parallel)
pids=()
for task in "${QUANT_TASKS[@]}"; do
    IFS='|' read -r method gpu_id description <<< "$task"
    
    # Create independent temporary directory for each task
    TASK_TEMP_DIR="${BASE_TEMP_DIR}/${method}_$$"
    mkdir -p "$TASK_TEMP_DIR"
    
    echo "Starting quantization task: $description"
    echo "  Method: $method"
    echo "  GPU: $gpu_id"
    echo "  Temp directory: $TASK_TEMP_DIR"
    echo "  Log: logs/quant_${method}.log"
    echo ""
    
    # Set GPU, temp directory and HuggingFace cache directory environment variables and run quantization
    CUDA_VISIBLE_DEVICES=$gpu_id \
    TMPDIR="$TASK_TEMP_DIR" \
    HF_HOME=/data/jisenli2/huggingface \
    python quantization/quantize_model.py \
        --method "$method" \
        > "logs/quant_${method}.log" 2>&1 &
    
    pids+=($!)
    
    # Avoid starting too many tasks simultaneously
    sleep 10
done

echo "======================================"
echo "All quantization tasks started, waiting for completion..."
echo "======================================"
echo ""
echo "Real-time log monitoring:"
echo "  tail -f logs/quant_w8a8_smooth_gptq.log"
echo "  tail -f logs/quant_*.log"
echo ""

# Wait for all tasks to complete
success_count=0
fail_count=0

for i in "${!pids[@]}"; do
    pid=${pids[$i]}
    task=${QUANT_TASKS[$i]}
    IFS='|' read -r method gpu_id description <<< "$task"
    
    echo "Waiting for task: $description (PID $pid)..."
    wait $pid
    exit_code=$?
    
    if [ $exit_code -eq 0 ]; then
        echo "✅ Task completed: $description"
        ((success_count++))
    else
        echo "❌ Task failed: $description (Exit Code: $exit_code)"
        echo "   Check log: logs/quant_${method}.log"
        ((fail_count++))
    fi
    echo ""
done

echo ""
echo "======================================"
echo "All quantization tasks completed!"
echo "Time: $(date)"
echo "======================================"
echo "Success: $success_count"
echo "Failed: $fail_count"
echo ""

# Cleanup temporary directory
echo "Cleaning up temporary directory..."
rm -rf "${BASE_TEMP_DIR}"/*_$$ 2>/dev/null
echo "✅ Temporary files cleaned"
echo ""

echo "Quantized models saved in: /data/jisenli2/huggingface/"
echo ""
echo "Model list:"
ls -lh /data/jisenli2/huggingface/Qwen3-4B-Instruct-2507-INT8-* 2>/dev/null | awk '{print "  " $9}' || echo "  (No quantized models yet)"

