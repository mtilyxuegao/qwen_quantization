# 系统信息收集

## 硬件配置

### GPU 信息

**GPU 型号：** NVIDIA A100-SXM4-80GB
**显存容量：** 80GB (81920 MiB)
**功耗：** 65W / 500W
**温度：** 33°C
**状态：** 空闲 (0% 利用率)

**CUDA 版本：** 12.1
- PyTorch CUDA 支持：已启用
- nvcc：未在用户空间安装（HPC环境限制）
- CUDA 运行时库：正常可用

---

### CPU 和内存信息

**CPU 型号：** Intel(R) Xeon(R) Platinum 8480+
**CPU 核心数：** 224 核
**总内存：** 2.0 TB
**可用内存：** 1.9 TB
**Swap：** 0 GB (未配置)

---

## 软件环境

### 操作系统
- **系统：** Linux
- **内核版本：** 5.15.0-140-generic
- **Shell：** /bin/bash

### Python 环境
- **Python 版本：** 3.10.12
- **虚拟环境：** venv (位于 /home/jisenli2/qwen_quantization/venv)

### 关键依赖版本

| 包名 | 版本 | 说明 |
|------|------|------|
| llmcompressor | 0.8.1 | 模型量化工具 |
| vllm | 0.11.0 | LLM 推理引擎 |
| sglang | 0.5.3.post3 | LLM 推理引擎 |
| torch | 2.8.0 | PyTorch 深度学习框架 |
| transformers | 4.57.1 | Hugging Face transformers |
| torchao | 0.9.0 | PyTorch 量化加速库 |
| torchaudio | 2.8.0 | PyTorch 音频处理 |
| torchvision | 0.23.0 | PyTorch 视觉处理 |

**PyTorch CUDA 版本：** 12.1
**CUDA 可用性：** 是
**可用 GPU 数量：** 8 个 (预计使用 1 个)

---

## HPC 环境信息

- **工作目录：** /home/jisenli2/qwen_quantization
- **用户名：** jisenli2
- **节点名称：** research-external-05
- **可用 GPU：** NVIDIA A100 80GB (当前节点已分配)
- **共享存储：** /data/shared/huggingface/ (团队共享模型存储)

---

## 存储空间

**存储空间状况：**
- `/home` 分区：9.7TB 总计，8.1TB 已用，1.2TB 可用 (88% 使用率)
- `/data` 分区：9.8TB 总计，8.4TB 已用，1.4TB 可用 (86% 使用率)

**预估存储需求：**
- 原始模型 (Qwen3-4B-Instruct-2507)：~8 GB
- INT8 量化模型：~4-5 GB
- 评估数据集和日志：~1-2 GB
- **总计：** ~15 GB

**下载目标：** 使用 /data 分区存储模型（空间更充裕）

---

## 网络配置

**Hugging Face 配置：**
- 下载目标路径：`/data/jisenli2/huggingface/`
- 本地缓存：`~/.cache/huggingface/hub/`
- 共享模型库：`/data/shared/huggingface/hub/`

**目标模型：**
- Qwen/Qwen3-4B-Instruct-2507 (需要下载)

---

## 日期和时间

- **收集日期：** 2025-10-18
- **时区：** [待确认]


