# GPQA 评估指南

使用 `run_gpqa_sglang.py` 进行 GPQA 评估

**配置：** Zero-shot + Greedy (temperature=0.0) + 16k tokens

---

## 🚀 使用方法

### 1. 启动 sglang 服务器

```bash
# 原始模型（使用 HuggingFace ID）
python -m sglang.launch_server \
  --model-path Qwen/Qwen3-4B-Instruct-2507 \
  --host 127.0.0.1 \
  --port 30000 \
  --trust-remote-code

# 量化模型（本地路径）
python -m sglang.launch_server \
  --model-path /data/jisenli2/huggingface/Qwen3-4B-Instruct-2507-INT8-W8A16 \
  --host 127.0.0.1 \
  --port 30000 \
  --trust-remote-code
```

### 2. 运行评估

```bash
# 原始模型 - diamond (198题)
python run_gpqa_sglang.py --model original

# 原始模型 - extended (546题)
python run_gpqa_sglang.py --model original --variant extended

# 量化模型 - diamond (198题)
python run_gpqa_sglang.py --model w8a16

# 快速测试 (10题)
python run_gpqa_sglang.py --model original --num-examples 10
```

---

## 📋 参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--model` | - | `original` 或 `w8a16` |
| `--variant` | `diamond` | `diamond` (198题) / `extended` (546题) |
| `--num-examples` | `None` | 测试样本数 (None=全部) |

---

## 📊 结果位置

```
results/
├── Qwen3-4B-Instruct-2507/              # 原始模型
│   ├── gpqa_diamond/                    # Diamond 变体 (默认)
│   │   ├── results.html
│   │   └── results.json
│   └── gpqa_extended/                   # Extended 变体
│       ├── results.html
│       └── results.json
│
└── Qwen3-4B-Instruct-2507-INT8-W8A16/   # 量化模型
    └── gpqa_diamond/
        ├── results.html
        └── results.json
```

**默认变体：** `diamond` (198题，最难)

**JSON 内容：** 准确率 (`score`) + 详细指标 (`metrics`) + 配置 (`config`)

## 🛠️ 常用命令

```bash
# 杀死 sglang 进程
pkill -9 -f sglang

# 或通过端口
lsof -ti:30000 | xargs kill -9
```

---

## 📝 代码修改说明

- `simple_evals/gpqa_eval.py`: 从 HuggingFace 加载数据集 (支持 diamond/extended/main)
- `simple_evals/common.py`: 简化 prompt (移除 "Think step by step")
- `run_gpqa_sglang.py`: Sglang 适配器 + CLI (在项目根目录)
