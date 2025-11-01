#!/bin/bash
#SBATCH --job-name=quant_smooth_ptq
#SBATCH --output=logs/quantization_logs/quant_%A.out
#SBATCH --error=logs/quantization_logs/quant_%A.err
#SBATCH --time=2:00:00
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=16
#SBATCH --mem=100G

# Activate environment
source venv/bin/activate

# Create log subdirectory
mkdir -p logs/quantization_logs

echo "======================================"
echo "Starting Parallel Quantization Tasks"
echo "Time: $(date)"
echo "======================================"

# Define quantization tasks
# Format: METHOD|GPU_ID|DESCRIPTION
# Note: AWQ doesn't support A8, so only W8A16 AWQ methods
declare -a QUANT_TASKS=(
    # ============ W8A8 Completed (3 methods) ============
    # "w8a8_smooth_gptq|0|⭐ SmoothQuant+GPTQ W8A8"  # ✅ Completed
    # "w8a8_smooth_ptq|1|SmoothQuant+PTQ W8A8"  # ✅ Completed
    # "w8a8_sparse_smooth_gptq|2|SparseGPT→SmoothQuant+GPTQ W8A8"  # ⚠️ Disabled (slow inference)
    
    # ============ W8A16 Completed (7 methods) ============
    # "w8a16_ptq|0|Simple PTQ W8A16"  # ✅ Completed
    # "w8a16_gptq|1|GPTQ W8A16"  # ✅ Completed
    # "w8a16_sparse_gptq|2|SparseGPT+GPTQ W8A16"  # ⚠️ Disabled (slow inference)
    # "w8a16_smooth_gptq|3|SmoothQuant+GPTQ W8A16"  # ✅ Completed
    # "w8a16_awq|0|AWQ W8A16"  # ✅ Completed
    # "w8a16_sparse_awq|1|SparseGPT+AWQ W8A16"  # ✅ Completed
    # "w8a16_smooth_awq|2|SmoothQuant+AWQ W8A16"  # ✅ Completed
    
    # ============ W8A16 To Run (1 method) ============
    "w8a16_smooth_ptq|0|⭐ SmoothQuant+PTQ W8A16 (Complete experiment matrix)"
)

echo "Total tasks: ${#QUANT_TASKS[@]}"
echo ""

# Create base temporary directory (avoid multi-process conflicts)
BASE_TEMP_DIR="/data/jisenli2/quant_temp"
mkdir -p $BASE_TEMP_DIR
echo "Base temporary directory: $BASE_TEMP_DIR"
echo "SLURM Job ID: $SLURM_JOB_ID"
echo ""

# Start all quantization tasks (background parallel)
pids=()
for task in "${QUANT_TASKS[@]}"; do
    IFS='|' read -r method gpu_id description <<< "$task"
    
    # Create independent temporary directory for each task (use SLURM Job ID)
    TASK_TEMP_DIR="${BASE_TEMP_DIR}/${method}_${SLURM_JOB_ID}"
    mkdir -p "$TASK_TEMP_DIR"
    
    echo "Starting quantization task: $description"
    echo "  Method: $method"
    echo "  GPU: $gpu_id"
    echo "  Temp directory: $TASK_TEMP_DIR"
    echo ""
    
    # Set GPU, temp directory and HuggingFace cache directory environment variables and run quantization
    CUDA_VISIBLE_DEVICES=$gpu_id \
    TMPDIR="$TASK_TEMP_DIR" \
    HF_HOME=/data/jisenli2/huggingface \
    python quantization/quantize_model.py \
        --method "$method" \
        > "logs/quantization_logs/quant_${method}.log" 2>&1 &
    
    pids+=($!)
    
    # Avoid starting too many tasks simultaneously
    sleep 10
done

echo "======================================"
echo "All quantization tasks started, waiting for completion..."
echo "======================================"
echo ""

# Wait for all tasks to complete
success_count=0
fail_count=0

for i in "${!pids[@]}"; do
    pid=${pids[$i]}
    task=${QUANT_TASKS[$i]}
    IFS='|' read -r method gpu_id description <<< "$task"
    
    wait $pid
    exit_code=$?
    
    if [ $exit_code -eq 0 ]; then
        echo "✅ Task completed: $description (PID $pid)"
        ((success_count++))
    else
        echo "❌ Task failed: $description (PID $pid, Exit Code: $exit_code)"
        ((fail_count++))
    fi
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
rm -rf "${BASE_TEMP_DIR}"/*_${SLURM_JOB_ID} 2>/dev/null
echo "✅ Temporary files cleaned"
echo ""

echo "Quantized models saved in: /data/jisenli2/huggingface/"
echo "Log files in: logs/quant_*.log"

