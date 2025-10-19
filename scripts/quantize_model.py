#!/usr/bin/env python3
"""
量化 Qwen3-4B-Instruct-2507 模型到 INT8
"""
from transformers import AutoTokenizer, AutoModelForCausalLM
from datasets import load_dataset
from llmcompressor.transformers import oneshot
from llmcompressor.modifiers.quantization import GPTQModifier
from llmcompressor.modifiers.smoothquant import SmoothQuantModifier

# 配置
MODEL_PATH = "/data/jisenli2/huggingface/models--Qwen--Qwen3-4B-Instruct-2507/snapshots/cdbee75f17c01a7cc42f958dc650907174af0554"
MODEL_ID = "Qwen/Qwen3-4B-Instruct-2507"
OUTPUT_DIR = "/data/jisenli2/huggingface/Qwen3-4B-Instruct-2507-INT8-W8A8"

NUM_CALIBRATION_SAMPLES = 512
MAX_SEQUENCE_LENGTH = 2048

def main():
    print("=" * 60)
    print("步骤 1/4: 加载模型和分词器")
    print("=" * 60)
    
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_PATH,
        device_map="auto",
        torch_dtype="auto",
    )
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
    
    print(f"✅ 模型已加载: {MODEL_ID}")
    print(f"✅ 分词器已加载")
    
    print("\n" + "=" * 60)
    print("步骤 2/4: 准备校准数据")
    print("=" * 60)
    
    # 加载和预处理数据集
    ds = load_dataset("HuggingFaceH4/ultrachat_200k", split="train_sft")
    ds = ds.shuffle(seed=42).select(range(NUM_CALIBRATION_SAMPLES))
    
    def preprocess(example):
        return {"text": tokenizer.apply_chat_template(example["messages"], tokenize=False)}
    
    ds = ds.map(preprocess)
    
    def tokenize(sample):
        return tokenizer(
            sample["text"], 
            padding=False, 
            max_length=MAX_SEQUENCE_LENGTH, 
            truncation=True, 
            add_special_tokens=False
        )
    
    ds = ds.map(tokenize, remove_columns=ds.column_names)
    
    print(f"✅ 校准数据已准备: {NUM_CALIBRATION_SAMPLES} 样本")
    
    print("\n" + "=" * 60)
    print("步骤 3/4: 应用 INT8 量化 (W8A8)")
    print("=" * 60)
    print("⏳ 这可能需要 30-60 分钟，请耐心等待...")
    
    # 配置量化算法
    recipe = [
        SmoothQuantModifier(smoothing_strength=0.8),
        GPTQModifier(targets="Linear", scheme="W8A8", ignore=["lm_head"]),
    ]
    
    # 应用量化
    oneshot(
        model=model,
        dataset=ds,
        recipe=recipe,
        max_seq_length=MAX_SEQUENCE_LENGTH,
        num_calibration_samples=NUM_CALIBRATION_SAMPLES,
    )
    
    print("✅ 量化完成")
    
    print("\n" + "=" * 60)
    print("步骤 4/4: 保存量化模型")
    print("=" * 60)
    
    model.save_pretrained(OUTPUT_DIR, save_compressed=True)
    tokenizer.save_pretrained(OUTPUT_DIR)
    
    print(f"✅ 量化模型已保存到: {OUTPUT_DIR}")
    print("\n" + "=" * 60)
    print("🎉 量化流程完成!")
    print("=" * 60)
    print(f"📂 原始模型: {MODEL_PATH}")
    print(f"📂 量化模型: {OUTPUT_DIR}")
    print(f"📊 量化方案: W8A8 (权重和激活均为 INT8)")

if __name__ == "__main__":
    main()

