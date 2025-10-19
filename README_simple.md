# GPQA 评估 - 简洁版

使用 `run_eval_simple.py` 进行快速 GPQA 评估（完全基于 simple-evals 原生 API）

## 🚀 快速开始

### 1. 启动 sglang 服务器

```bash
# 原始模型
python -m sglang.launch_server \
  --model-path Qwen/Qwen3-4B-Instruct-2507 \
  --port 30000

# 或 INT8 量化模型
python -m sglang.launch_server \
  --model-path /data/jisenli2/huggingface/Qwen3-4B-Instruct-2507-INT8-W8A8 \
  --port 30000
```

### 2. 运行评估

```bash
# 快速测试（10题，1次）
python run_eval_simple.py \
  --model-name test \
  --num-examples 10 \
  --n-repeats 1

# 完整评估（448题，10次）
python run_eval_simple.py --model-name qwen3-4b-original

# INT8 评估
python run_eval_simple.py --model-name qwen3-4b-int8
```

## 📋 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--model-name` | *必需* | 模型名称（用于保存结果文件） |
| `--base-url` | `http://127.0.0.1:30000/v1` | sglang 服务器地址 |
| `--num-examples` | `None` | 限制测试样本数（None=全部448题） |
| `--n-repeats` | `10` | 重复评估次数 |
| `--variant` | `diamond` | GPQA 变体（diamond/extended/main） |
| `--temperature` | `0.7` | 采样温度 |
| `--top-p` | `0.8` | Top-P 采样 |
| `--max-tokens` | `4096` | 最大输出长度 |
| `--output-dir` | `results` | 结果保存目录 |

## 📊 输出文件

评估完成后生成：

```
results/
├── gpqa_{model_name}.json  # 准确率和指标
└── gpqa_{model_name}.html  # 可视化报告
```

## ⏱️ 评估时间

- **快速测试**（10题×1次）：~1分钟
- **完整评估**（448题×10次）：~10-20小时（取决于GPU）

## 💡 使用建议

1. **先测试小样本**，确保服务器和配置正常
2. **使用 screen/tmux** 运行长时间评估
3. **观察进度**：simple-evals 会显示进度条

## 📖 示例

### 测试流程

```bash
# 1. 启动服务器
python -m sglang.launch_server --model-path Qwen/Qwen3-4B-Instruct-2507 --port 30000

# 2. 新终端，先测试
python run_eval_simple.py --model-name test --num-examples 5 --n-repeats 1

# 3. 确认无误后，完整评估
python run_eval_simple.py --model-name qwen3-4b-original
```

### 查看结果

```bash
# 查看准确率
cat results/gpqa_qwen3-4b-original.json | jq '.score'

# 在浏览器打开 HTML 报告
firefox results/gpqa_qwen3-4b-original.html
```

## 🔄 对比两个模型

```python
import json

# 读取结果
with open('results/gpqa_qwen3-4b-original.json') as f:
    orig = json.load(f)

with open('results/gpqa_qwen3-4b-int8.json') as f:
    int8 = json.load(f)

# 对比
print(f"原始模型: {orig['score']:.4f}")
print(f"INT8模型: {int8['score']:.4f}")
print(f"准确率下降: {(orig['score'] - int8['score']):.4f}")
```

## ⚙️ 技术细节

### GPQA Variants

- **diamond**（推荐）：448题，最高质量
- **extended**：~500题
- **main**：完整数据集

### 采样参数

默认使用 Qwen 推荐的参数：
- Temperature: 0.7
- Top-P: 0.8
- Top-K: 20
- Min-P: 0.0

## 🆚 vs run_gpqa_eval.py

| 特性 | run_eval_simple.py | run_gpqa_eval.py |
|------|-------------------|------------------|
| 代码行数 | 128 行 | 177 行 |
| Simple-evals 集成 | ✅ 完全原生 | ⚠️ 自定义循环 |
| 增量保存 | ❌ | ✅ 每遍保存 |
| 统计信息 | 基础 | 详细（均值±标准差） |
| 推荐场景 | 快速评估 | 长时间评估 |

---

**提示**：如需增量保存和详细统计，请使用 `run_gpqa_eval.py`（见主 README.md）

