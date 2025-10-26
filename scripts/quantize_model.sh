#!/bin/bash
#SBATCH --job-name=qwen_quantize
#SBATCH --output=/home/jisenli2/qwen_quantization/logs/quantize_%j.out
#SBATCH --error=/home/jisenli2/qwen_quantization/logs/quantize_%j.err
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=64
#SBATCH --mem=500G
#SBATCH --gres=gpu:1
#SBATCH --time=200:00:00
#SBATCH --partition=batch
# SBATCH --nodelist=research-external-03

# 确保 logs 目录存在
mkdir -p /home/jisenli2/qwen_quantization/logs

# 打印作业信息
echo "========================================"
echo "Qwen3-4B INT8 量化任务"
echo "========================================"
echo "作业ID: $SLURM_JOB_ID"
echo "作业名称: $SLURM_JOB_NAME"
echo "节点: $SLURM_NODELIST"
echo "开始时间: $(date)"
echo "========================================"

# 激活 venv 虚拟环境
echo "激活虚拟环境..."
source /home/jisenli2/qwen_quantization/venv/bin/activate

# 打印 Python 和 GPU 信息
echo ""
echo "Python 版本:"
python --version
echo ""
echo "Python 路径:"
which python
echo ""
echo "GPU 信息:"
nvidia-smi
echo "========================================"

# 进入工作目录
cd /home/jisenli2/qwen_quantization/scripts

# 运行量化脚本
echo "开始运行量化脚本..."
python quantize_model.py

# 检查退出状态
if [ $? -eq 0 ]; then
    echo "========================================"
    echo "✅ 量化任务成功完成!"
    echo "结束时间: $(date)"
    echo "========================================"
else
    echo "========================================"
    echo "❌ 量化任务失败!"
    echo "结束时间: $(date)"
    echo "========================================"
    exit 1
fi

