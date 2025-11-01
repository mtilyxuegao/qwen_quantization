#!/usr/bin/env python3
"""
Quantize Qwen3-4B-Instruct-2507 model to INT8
Supports various W8A16 and W8A8 quantization methods
"""
import logging
import os
import argparse
from datetime import datetime
from pathlib import Path

from transformers import AutoTokenizer, AutoModelForCausalLM
from datasets import load_dataset
from llmcompressor import oneshot
from llmcompressor.modifiers.quantization import GPTQModifier
from llmcompressor.modifiers.awq import AWQModifier
from llmcompressor.modifiers.smoothquant import SmoothQuantModifier
from llmcompressor.modifiers.pruning import SparseGPTModifier

# Basic configuration
MODEL_ID = "Qwen/Qwen3-4B-Instruct-2507"
MODEL_BASE_DIR = "/data/jisenli2/huggingface"
LOG_DIR = "/home/jisenli2/qwen_quantization/logs/quantization_logs"

NUM_CALIBRATION_SAMPLES = 512
MAX_SEQUENCE_LENGTH = 2048

# Setup logger
def setup_logger(method_name=None):
    """Configure logging system with both file and console output"""
    # Create logs directory
    os.makedirs(LOG_DIR, exist_ok=True)
    
    # Generate log filename with method name (light prefix to distinguish from shell-redirected quant_*.log)
    if method_name:
        log_file = os.path.join(LOG_DIR, f"light_quantize_{method_name}.log")
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = os.path.join(LOG_DIR, f"light_quantize_{timestamp}.log")
    
    # Configure log format
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    
    # Create logger
    logger = logging.getLogger('quantization')
    logger.setLevel(logging.INFO)
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # File handler
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(log_format, date_format))
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter(log_format, date_format))
    
    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    logger.info(f"Log file: {log_file}")
    
    return logger

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Quantize Qwen3-4B-Instruct-2507 model")
    parser.add_argument(
        "--method",
        type=str,
        required=True,
        choices=[
            # W8A16 methods
            "w8a16_ptq",
            "w8a16_gptq", 
            "w8a16_awq",
            "w8a16_sparse_gptq",
            "w8a16_sparse_awq",
            "w8a16_smooth_gptq",
            "w8a16_smooth_ptq",
            "w8a16_smooth_awq",
            # W8A8 methods (priority, note: AWQ doesn't support A8)
            "w8a8_smooth_gptq",
            "w8a8_sparse_smooth_gptq",
            "w8a8_smooth_ptq",
        ],
        help="Quantization method"
    )
    args = parser.parse_args()
    
    # Initialize logger (pass method name for clear log filename)
    logger = setup_logger(method_name=args.method)
    
    logger.info("=" * 60)
    logger.info(f"Quantization Method: {args.method.upper()}")
    logger.info("=" * 60)
    logger.info("")
    logger.info("=" * 60)
    logger.info("Step 1/5: Load Model and Tokenizer")
    logger.info("=" * 60)
    
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        device_map="auto",
        torch_dtype="auto",
    )
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    
    logger.info(f"✅ Model loaded: {MODEL_ID}")
    logger.info(f"✅ Tokenizer loaded")
    
    logger.info("")
    logger.info("=" * 60)
    logger.info("Step 2/5: Prepare Calibration Data")
    logger.info("=" * 60)
    
    # Load and preprocess dataset
    logger.info("Loading dataset...")
    ds = load_dataset("HuggingFaceH4/ultrachat_200k", split="train_sft")
    ds = ds.shuffle(seed=42).select(range(NUM_CALIBRATION_SAMPLES))
    logger.info(f"Loaded {len(ds)} samples")
    
    def preprocess(example):
        return {"text": tokenizer.apply_chat_template(example["messages"], tokenize=False)}
    
    logger.info("Preprocessing data...")
    ds = ds.map(preprocess, desc="Preprocessing", num_proc=4)  # Add progress bar and multiprocessing
    
    def tokenize(sample):
        return tokenizer(
            sample["text"], 
            padding=False, 
            max_length=MAX_SEQUENCE_LENGTH, 
            truncation=True, 
            add_special_tokens=False
        )
    
    logger.info("Tokenizing...")
    ds = ds.map(tokenize, remove_columns=ds.column_names, desc="Tokenizing", num_proc=4)  # Add progress bar and multiprocessing
    
    logger.info(f"✅ Calibration data prepared: {NUM_CALIBRATION_SAMPLES} samples")
    
    logger.info("")
    logger.info("=" * 60)
    logger.info("Step 3/5: Configure Quantization Algorithm")
    logger.info("=" * 60)
    
    # Select recipe based on method
    # ==================== W8A16 Methods ====================
    if args.method == "w8a16_ptq":
        recipe = [
            GPTQModifier(
                targets="Linear",
                scheme="W8A16",
                ignore=["lm_head"],
                dampening_frac=0.0
            )
        ]
        output_suffix = "W8A16-PTQ"
        logger.info("Method: Simple PTQ (W8A16) - Fast Baseline")
        logger.info("  - Weights: INT8, Activations: FP16")
        logger.info("  - Dampening: 0.0")
        
    elif args.method == "w8a16_gptq":
        recipe = [
            GPTQModifier(
                targets="Linear",
                scheme="W8A16",
                ignore=["lm_head"],
                dampening_frac=0.01
            )
        ]
        output_suffix = "W8A16-GPTQ"
        logger.info("Method: GPTQ (W8A16)")
        logger.info("  - Weights: INT8, Activations: FP16")
        logger.info("  - Dampening: 0.01")
        
    elif args.method == "w8a16_awq":
        # AWQ uses config_groups, group_size=128 (standard configuration)
        recipe = [
            AWQModifier(
                ignore=["lm_head"],
                config_groups={
                    "group_0": {
                        "targets": ["Linear"],
                        "weights": {
                            "num_bits": 8,
                            "type": "int",
                            "symmetric": True,
                            "strategy": "group",  # Group quantization
                            "group_size": 128,  # AWQ standard group_size
                        }
                    }
                }
            )
        ]
        output_suffix = "W8A16-AWQ"
        logger.info("Method: AWQ (W8A16)")
        logger.info("  - Weights: INT8, Activations: FP16")
        logger.info("  - Activation-aware Weight Quantization")
        logger.info("  - group_size=128 (standard grouping)")
        
    elif args.method == "w8a16_sparse_gptq":
        recipe = [
            SparseGPTModifier(
                targets="Linear",
                sparsity=0.5
            ),
            GPTQModifier(
                targets="Linear",
                scheme="W8A16",
                ignore=["lm_head"],
                dampening_frac=0.01
            )
        ]
        output_suffix = "W8A16-SPARSE-GPTQ"
        logger.info("Method: SparseGPT → GPTQ (W8A16)")
        logger.info("  - Sparsity: 50%")
        logger.info("  - Weights: INT8, Activations: FP16")
        logger.info("  - Prune first, then quantize")
        
    elif args.method == "w8a16_sparse_awq":
        recipe = [
            SparseGPTModifier(
                targets="Linear",
                sparsity=0.5
            ),
            AWQModifier(
                ignore=["lm_head"],
                config_groups={
                    "group_0": {
                        "targets": ["Linear"],
                        "weights": {
                            "num_bits": 8,
                            "type": "int",
                            "symmetric": True,
                            "strategy": "group",
                            "group_size": 128,
                        }
                    }
                }
            )
        ]
        output_suffix = "W8A16-SPARSE-AWQ"
        logger.info("Method: SparseGPT → AWQ (W8A16)")
        logger.info("  - Sparsity: 50%")
        logger.info("  - Weights: INT8, Activations: FP16")
        logger.info("  - Prune first, then quantize")
        logger.info("  - group_size=128 (standard grouping)")
        
    elif args.method == "w8a16_smooth_gptq":
        recipe = [
            SmoothQuantModifier(smoothing_strength=0.5),
            GPTQModifier(
                targets="Linear",
                scheme="W8A16",
                ignore=["lm_head"],
                dampening_frac=0.01
            )
        ]
        output_suffix = "W8A16-SMOOTH-GPTQ"
        logger.info("Method: SmoothQuant + GPTQ (W8A16)")
        logger.info("  - Weights: INT8, Activations: FP16")
        logger.info("  - Smoothing: 0.5 (for comparison, less benefit with W8A16)")
        
    elif args.method == "w8a16_smooth_ptq":
        recipe = [
            SmoothQuantModifier(smoothing_strength=0.5),
            GPTQModifier(
                targets="Linear",
                scheme="W8A16",
                ignore=["lm_head"],
                dampening_frac=0.0  # PTQ: no dampening
            )
        ]
        output_suffix = "W8A16-SMOOTH-PTQ"
        logger.info("Method: SmoothQuant + PTQ (W8A16)")
        logger.info("  - Weights: INT8, Activations: FP16")
        logger.info("  - Smoothing: 0.5, Dampening: 0.0 (fast PTQ)")
        
    elif args.method == "w8a16_smooth_awq":
        recipe = [
            SmoothQuantModifier(smoothing_strength=0.5),
            AWQModifier(
                ignore=["lm_head"],
                config_groups={
                    "group_0": {
                        "targets": ["Linear"],
                        "weights": {
                            "num_bits": 8,
                            "type": "int",
                            "symmetric": True,
                            "strategy": "group",
                            "group_size": 128,
                        }
                    }
                }
            )
        ]
        output_suffix = "W8A16-SMOOTH-AWQ"
        logger.info("Method: SmoothQuant + AWQ (W8A16)")
        logger.info("  - Weights: INT8, Activations: FP16")
        logger.info("  - Smoothing: 0.5 (for comparison)")
        logger.info("  - group_size=128 (standard grouping)")
        
    # ==================== W8A8 Methods ====================
    elif args.method == "w8a8_smooth_gptq":
        recipe = [
            SmoothQuantModifier(smoothing_strength=0.8),
            GPTQModifier(
                targets="Linear",
                scheme="W8A8",
                ignore=["lm_head"],
                dampening_frac=0.01
            )
        ]
        output_suffix = "W8A8-SMOOTH-GPTQ"
        logger.info("Method: SmoothQuant + GPTQ (W8A8)")
        logger.info("  - Weights: INT8, Activations: INT8")
        logger.info("  - Smoothing: 0.8")
        
    elif args.method == "w8a8_sparse_smooth_gptq":
        recipe = [
            SparseGPTModifier(
                targets="Linear",
                sparsity=0.5
            ),
            SmoothQuantModifier(smoothing_strength=0.8),
            GPTQModifier(
                targets="Linear",
                scheme="W8A8",
                ignore=["lm_head"],
                dampening_frac=0.01
            )
        ]
        output_suffix = "W8A8-SPARSE-SMOOTH-GPTQ"
        logger.info("Method: SparseGPT → SmoothQuant + GPTQ (W8A8)")
        logger.info("  - Sparsity: 50%")
        logger.info("  - Weights: INT8, Activations: INT8")
        logger.info("  - Smoothing: 0.8")
        logger.info("  - More memory/throughput efficient, but more accuracy loss")
        
    elif args.method == "w8a8_smooth_ptq":
        recipe = [
            SmoothQuantModifier(smoothing_strength=0.8),
            GPTQModifier(
                targets="Linear",
                scheme="W8A8",
                ignore=["lm_head"],
                dampening_frac=0.0
            )
        ]
        output_suffix = "W8A8-SMOOTH-PTQ"
        logger.info("Method: SmoothQuant + Simple PTQ (W8A8)")
        logger.info("  - Weights: INT8, Activations: INT8")
        logger.info("  - Smoothing: 0.8")
        logger.info("  - Dampening: 0.0 (fast baseline, medium accuracy)")
        
    # Set output directory
    OUTPUT_DIR = f"{MODEL_BASE_DIR}/Qwen3-4B-Instruct-2507-INT8-{output_suffix}"
    
    logger.info(f"  - Ignored layers: lm_head")
    logger.info(f"  - Calibration samples: {NUM_CALIBRATION_SAMPLES}")
    logger.info(f"  - Output directory: {OUTPUT_DIR}")
    logger.info("")
    logger.info("⏳ This may take 30-60 minutes, please be patient...")
    
    logger.info("")
    logger.info("=" * 60)
    logger.info("Step 4/5: Apply Quantization")
    logger.info("=" * 60)
    
    import time
    start_time = time.time()
    
    # Apply quantization (llmcompressor will automatically show progress bar)
    logger.info("Starting quantization...")
    oneshot(
        model=model,
        dataset=ds,
        recipe=recipe,
        max_seq_length=MAX_SEQUENCE_LENGTH,
        num_calibration_samples=NUM_CALIBRATION_SAMPLES,
    )
    
    elapsed_time = time.time() - start_time
    logger.info(f"✅ Quantization completed (elapsed time: {elapsed_time/60:.1f} minutes)")
    
    logger.info("")
    logger.info("=" * 60)
    logger.info("Step 5/5: Save Quantized Model")
    logger.info("=" * 60)
    
    model.save_pretrained(OUTPUT_DIR, save_compressed=True)
    tokenizer.save_pretrained(OUTPUT_DIR)
    
    logger.info(f"✅ Quantized model saved to: {OUTPUT_DIR}")
    logger.info("")
    logger.info("=" * 60)
    logger.info("🎉 Quantization process completed!")
    logger.info("=" * 60)
    logger.info(f"📂 Original model: {MODEL_ID}")
    logger.info(f"📂 Quantized model: {OUTPUT_DIR}")
    logger.info(f"📊 Quantization scheme: {output_suffix}")

if __name__ == "__main__":
    main()

