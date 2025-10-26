#!/usr/bin/env python3
"""
量化 Qwen3-4B-Instruct-2507 模型到 INT8
"""
import logging
import os
from datetime import datetime
from pathlib import Path

from transformers import AutoTokenizer, AutoModelForCausalLM
from datasets import load_dataset
from llmcompressor import oneshot  # 修改：oneshot 在顶层，不在 transformers 子模块
from llmcompressor.modifiers.quantization import GPTQModifier

# 配置
MODEL_ID = "Qwen/Qwen3-4B-Instruct-2507"
OUTPUT_DIR = "/data/jisenli2/huggingface/Qwen3-4B-Instruct-2507-INT8-W8A16"
LOG_DIR = "/home/jisenli2/qwen_quantization/logs"

NUM_CALIBRATION_SAMPLES = 512
MAX_SEQUENCE_LENGTH = 2048

# 设置日志
def setup_logger():
    """配置日志系统，同时输出到文件和控制台"""
    # 创建 logs 目录
    os.makedirs(LOG_DIR, exist_ok=True)
    
    # 生成带时间戳的日志文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(LOG_DIR, f"quantize_{timestamp}.log")
    
    # 配置日志格式
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    
    # 创建 logger
    logger = logging.getLogger('quantization')
    logger.setLevel(logging.INFO)
    
    # 清除已有的处理器
    logger.handlers.clear()
    
    # 文件处理器
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(log_format, date_format))
    
    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter(log_format, date_format))
    
    # 添加处理器
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    logger.info(f"日志文件: {log_file}")
    
    return logger

def main():
    # 初始化日志系统
    logger = setup_logger()
    
    logger.info("=" * 60)
    logger.info("步骤 1/4: 加载模型和分词器")
    logger.info("=" * 60)
    
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        device_map="auto",
        torch_dtype="auto",
    )
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    
    logger.info(f"✅ 模型已加载: {MODEL_ID}")
    logger.info(f"✅ 分词器已加载")
    
    logger.info("")
    logger.info("=" * 60)
    logger.info("步骤 2/4: 准备校准数据")
    logger.info("=" * 60)
    
    # 加载和预处理数据集
    logger.info("正在加载数据集...")
    ds = load_dataset("HuggingFaceH4/ultrachat_200k", split="train_sft")
    ds = ds.shuffle(seed=42).select(range(NUM_CALIBRATION_SAMPLES))
    logger.info(f"已加载 {len(ds)} 条样本")
    
    def preprocess(example):
        return {"text": tokenizer.apply_chat_template(example["messages"], tokenize=False)}
    
    logger.info("正在预处理数据...")
    ds = ds.map(preprocess, desc="预处理", num_proc=4)  # 添加进度条和多进程
    
    def tokenize(sample):
        return tokenizer(
            sample["text"], 
            padding=False, 
            max_length=MAX_SEQUENCE_LENGTH, 
            truncation=True, 
            add_special_tokens=False
        )
    
    logger.info("正在分词...")
    ds = ds.map(tokenize, remove_columns=ds.column_names, desc="分词", num_proc=4)  # 添加进度条和多进程
    
    logger.info(f"✅ 校准数据已准备: {NUM_CALIBRATION_SAMPLES} 样本")
    
    logger.info("")
    logger.info("=" * 60)
    logger.info("步骤 3/4: 应用 INT8 量化 (W8A16)")
    logger.info("=" * 60)
    logger.info("⏳ 这可能需要 30-60 分钟，请耐心等待...")
    logger.info("")
    logger.info("量化配置:")
    logger.info("  - GPTQ: W8A16 (权重INT8, 激活FP16)")
    logger.info("  - 忽略层: lm_head")
    logger.info("  - 校准样本: %d", NUM_CALIBRATION_SAMPLES)
    logger.info("")
    
    # 配置量化算法
    recipe = [
        GPTQModifier(targets="Linear", scheme="W8A16", ignore=["lm_head"]),
    ]
    
    import time
    start_time = time.time()
    
    # 应用量化（llmcompressor 会自动显示进度条）
    logger.info("开始量化...")
    oneshot(
        model=model,
        dataset=ds,
        recipe=recipe,
        max_seq_length=MAX_SEQUENCE_LENGTH,
        num_calibration_samples=NUM_CALIBRATION_SAMPLES,
    )
    
    elapsed_time = time.time() - start_time
    logger.info(f"✅ 量化完成 (耗时: {elapsed_time/60:.1f} 分钟)")
    
    logger.info("")
    logger.info("=" * 60)
    logger.info("步骤 4/4: 保存量化模型")
    logger.info("=" * 60)
    
    model.save_pretrained(OUTPUT_DIR, save_compressed=True)
    tokenizer.save_pretrained(OUTPUT_DIR)
    
    logger.info(f"✅ 量化模型已保存到: {OUTPUT_DIR}")
    logger.info("")
    logger.info("=" * 60)
    logger.info("🎉 量化流程完成!")
    logger.info("=" * 60)
    logger.info(f"📂 原始模型: {MODEL_ID}")
    logger.info(f"📂 量化模型: {OUTPUT_DIR}")
    logger.info(f"📊 量化方案: W8A16 (权重INT8, 激活FP16, A100兼容)")

if __name__ == "__main__":
    main()

