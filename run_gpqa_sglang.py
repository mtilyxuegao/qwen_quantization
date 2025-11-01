#!/usr/bin/env python3
"""
Run GPQA evaluation using sglang backend (Zero-shot)
Designed for Qwen3-4B-Instruct and W8A16 quantized models

Usage:
    # Original model
    python run_gpqa_sglang.py --model original
    
    # Quantized model
    python run_gpqa_sglang.py --model w8a16
    
    # Custom configuration
    python run_gpqa_sglang.py \
        --model-name Qwen3-4B-Instruct-2507 \
        --base-url http://127.0.0.1:30000/v1 \
        --variant extended \
        --max-tokens 32768
"""
import sys
import json
import argparse
from pathlib import Path
from openai import OpenAI

# Add parent directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

# Import simple_evals packages
from simple_evals.gpqa_eval import GPQAEval
from simple_evals.types import SamplerBase, SamplerResponse
from simple_evals import common


class SglangSampler(SamplerBase):
    """
    Sglang Backend Sampler
    Supports OpenAI-compatible API
    """
    
    def __init__(
        self, 
        base_url: str, 
        temperature: float | None = None,
        top_p: float | None = None,
        presence_penalty: float | None = None,
        max_tokens: int = 16384,
        seed: int = 1234,
        system_message: str = "You are a helpful assistant."
    ):
        """
        Args:
            base_url: sglang server address, e.g. http://127.0.0.1:30000/v1
            temperature: sampling temperature (None = use model default, 0.0 = greedy)
            top_p: nucleus sampling parameter (None = use model default)
            presence_penalty: presence penalty parameter (None = use model default)
            max_tokens: maximum number of tokens to generate
            seed: random seed (for reproducibility)
            system_message: system prompt message
        """
        # Increase timeout for complex questions (default 600s too short)
        # GPQA questions + max_tokens=16k may take a long time
        self.client = OpenAI(
            base_url=base_url, 
            api_key="dummy",
            timeout=3600.0  # 60 minute timeout
        )
        self.temperature = temperature
        self.top_p = top_p
        self.presence_penalty = presence_penalty
        self.max_tokens = max_tokens
        self.seed = seed
        self.system_message = system_message
    
    def _pack_message(self, content: str, role: str):
        """Pack message into OpenAI format"""
        return {"role": role, "content": content}
    
    def __call__(self, message_list):
        """
        Call sglang backend to generate response
        
        Args:
            message_list: List of messages (not including system message)
            
        Returns:
            SamplerResponse
        """
        # Add system message
        messages = [self._pack_message(self.system_message, "system")] + message_list
        
        # Build request parameters (only pass non-None parameters)
        request_kwargs = {
            "model": "default",  # sglang ignores this parameter
            "messages": messages,
            "max_tokens": self.max_tokens,
            "seed": self.seed
        }
        
        # Only explicitly set parameters will override model defaults
        if self.temperature is not None:
            request_kwargs["temperature"] = self.temperature
        if self.top_p is not None:
            request_kwargs["top_p"] = self.top_p
        if self.presence_penalty is not None:
            request_kwargs["presence_penalty"] = self.presence_penalty
        
        # Call sglang (only use OpenAI-compatible parameters)
        response = self.client.chat.completions.create(**request_kwargs)
        
        return SamplerResponse(
            response_text=response.choices[0].message.content,
            response_metadata={"usage": response.usage},
            actual_queried_message_list=messages,
        )


# Preset configurations
PRESETS = {
    "original": {
        "model_name": "Qwen3-4B-Instruct-2507",
        "description": "Original BF16 model"
    },
    # ==================== W8A16 Methods ====================
    "w8a16_ptq": {
        "model_name": "Qwen3-4B-Instruct-2507-INT8-W8A16-PTQ",
        "description": "Simple PTQ W8A16 (baseline)"
    },
    "w8a16_gptq": {
        "model_name": "Qwen3-4B-Instruct-2507-INT8-W8A16-GPTQ",
        "description": "GPTQ W8A16"
    },
    "w8a16_awq": {
        "model_name": "Qwen3-4B-Instruct-2507-INT8-W8A16-AWQ",
        "description": "AWQ W8A16"
    },
    "w8a16_sparse_gptq": {
        "model_name": "Qwen3-4B-Instruct-2507-INT8-W8A16-SPARSE-GPTQ",
        "description": "SparseGPT → GPTQ W8A16"
    },
    "w8a16_sparse_awq": {
        "model_name": "Qwen3-4B-Instruct-2507-INT8-W8A16-SPARSE-AWQ",
        "description": "SparseGPT → AWQ W8A16"
    },
    "w8a16_smooth_gptq": {
        "model_name": "Qwen3-4B-Instruct-2507-INT8-W8A16-SMOOTH-GPTQ",
        "description": "SmoothQuant + GPTQ W8A16 (comparison)"
    },
    "w8a16_smooth_ptq": {
        "model_name": "Qwen3-4B-Instruct-2507-INT8-W8A16-SMOOTH-PTQ",
        "description": "SmoothQuant + PTQ W8A16 (complete experiment matrix)"
    },
    "w8a16_smooth_awq": {
        "model_name": "Qwen3-4B-Instruct-2507-INT8-W8A16-SMOOTH-AWQ",
        "description": "SmoothQuant + AWQ W8A16 (comparison)"
    },
    # ==================== W8A8 Methods (Priority) ====================
    "w8a8_smooth_gptq": {
        "model_name": "Qwen3-4B-Instruct-2507-INT8-W8A8-SMOOTH-GPTQ",
        "description": "⭐ SmoothQuant + GPTQ W8A8 (priority)"
    },
    "w8a8_smooth_awq": {
        "model_name": "Qwen3-4B-Instruct-2507-INT8-W8A8-SMOOTH-AWQ",
        "description": "⭐ SmoothQuant + AWQ W8A8 (priority)"
    },
    "w8a8_sparse_smooth_gptq": {
        "model_name": "Qwen3-4B-Instruct-2507-INT8-W8A8-SPARSE-SMOOTH-GPTQ",
        "description": "SparseGPT → SmoothQuant + GPTQ W8A8 (memory efficient)"
    },
    "w8a8_smooth_ptq": {
        "model_name": "Qwen3-4B-Instruct-2507-INT8-W8A8-SMOOTH-PTQ",
        "description": "SmoothQuant + PTQ W8A8 (fast baseline)"
    },
    "w8a8_awq_smooth": {
        "model_name": "Qwen3-4B-Instruct-2507-INT8-W8A8-AWQ-LIGHTSMOOTH",
        "description": "AWQ + Light SmoothQuant W8A8"
    }
}


def main():
    # 构建预设模型的帮助信息
    preset_help = "使用预设模型: " + ", ".join([
        f"{k} ({v['description']})" for k, v in PRESETS.items()
    ])
    
    parser = argparse.ArgumentParser(
        description="使用 sglang 后端运行 GPQA 评估",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 使用预设配置
  python run_gpqa_sglang.py --model original
  python run_gpqa_sglang.py --model w8a16
  
  # 自定义配置
  python run_gpqa_sglang.py \\
      --model-name MyModel \\
      --variant extended \\
      --max-tokens 32768
        """
    )
    
    # 预设或自定义模型
    parser.add_argument(
        "--model",
        type=str,
        choices=list(PRESETS.keys()),
        help=preset_help
    )
    parser.add_argument(
        "--model-name",
        type=str,
        help="自定义模型名称（覆盖 --model）"
    )
    
    # 服务器配置
    parser.add_argument(
        "--base-url",
        type=str,
        default="http://127.0.0.1:30000/v1",
        help="Sglang 服务器地址 (默认: http://127.0.0.1:30000/v1)"
    )
    
    # 评估配置
    parser.add_argument(
        "--variant",
        type=str,
        default="diamond",
        choices=["diamond", "extended", "main"],
        help="GPQA 变体 (默认: diamond)"
    )
    parser.add_argument(
        "--num-examples",
        type=int,
        default=None,
        help="测试样本数（None = 全部）"
    )
    parser.add_argument(
        "--n-repeats",
        type=int,
        default=1,
        help="每个样本重复次数（仅当 num-examples=None 时支持 >1）"
    )
    parser.add_argument(
        "--n-shot",
        type=int,
        default=0,
        help="Few-shot 示例数量 (0=zero-shot, 默认: 0)"
    )
    
    # 采样参数
    parser.add_argument(
        "--greedy",
        action="store_true",
        help="启用 Greedy 解码模式 (Temperature=0.0, TopP=0.8)。默认使用 Do-sample 模式 (Temperature=0.7, TopP=0.8)"
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=None,
        help="采样温度 (默认: greedy=True 时为 0.0, greedy=False 时为 0.7)"
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=16384,
        help="最大生成 token 数 (默认: 16384 = 16k)"
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=1234,
        help="随机种子，用于确保结果可重复 (默认: 1234)"
    )
    
    # 输出配置
    parser.add_argument(
        "--config-name",
        type=str,
        default=None,
        help="可选的配置名称，用于进一步区分实验，如 'qwen_prompt', 'ablation_study' 等。不提供则自动生成基础配置名"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="results",
        help="结果保存目录 (默认: results/)"
    )
    
    args = parser.parse_args()
    
    # 处理采样参数
    if args.greedy:
        # Greedy 模式：显式覆盖模型默认参数
        temperature = args.temperature if args.temperature is not None else 0.0
        top_p = 0.8
        presence_penalty = 0.0
    else:
        # Do-sample 模式（默认）：使用模型自带的默认参数（不覆盖）
        # 模型默认: temperature=0.7, top_k=20, top_p=0.8
        temperature = None
        top_p = None
        presence_penalty = None
    
    # 确定模型名称
    if args.model:
        model_name = PRESETS[args.model]["model_name"]
        preset_desc = PRESETS[args.model]["description"]
    elif args.model_name:
        model_name = args.model_name
        preset_desc = "自定义模型"
    else:
        parser.error("必须指定 --model 或 --model-name")
    
    # 打印配置
    print(f"\n{'='*70}")
    print(f"🚀 GPQA 评估配置")
    print(f"{'='*70}")
    print(f"模型: {model_name}")
    print(f"      ({preset_desc})")
    print(f"服务器: {args.base_url}")
    print(f"变体: {args.variant}")
    print(f"样本数: {args.num_examples or 'ALL'} × {args.n_repeats} repeats")
    shot_mode = f"{args.n_shot}-shot" if args.n_shot > 0 else "Zero-shot"
    
    if args.greedy:
        sampling_mode = "Greedy" if temperature == 0.0 else f"Greedy (Temp={temperature})"
        sampling_detail = f"Temp={temperature}, TopP={top_p}"
    else:
        sampling_mode = "DoSample (使用模型默认参数)"
        sampling_detail = "Temp=0.7, TopK=20, TopP=0.8 (模型默认)"
    
    print(f"采样: {shot_mode}, {sampling_mode}, Max-Tokens={args.max_tokens}, Seed={args.seed}")
    print(f"      参数: {sampling_detail}")
    
    # 提前计算配置名称用于显示
    sampling_part_preview = "greedy" if args.greedy else "dosample"
    shot_part_preview = f"{args.n_shot}shot" if args.n_shot > 0 else "zeroshot"
    repeat_part_preview = f"{args.n_repeats}repeat"
    config_preview = f"{sampling_part_preview}_{shot_part_preview}_{repeat_part_preview}"
    if args.num_examples:
        config_preview += f"_{args.num_examples}samples"
    if args.config_name:
        config_preview += f"_{args.config_name}"
        print(f"配置名称: {config_preview}")
        print(f"          (自动: {sampling_part_preview}_{shot_part_preview}_{repeat_part_preview} + 自定义: {args.config_name})")
    else:
        print(f"配置名称: {config_preview} (自动生成)")
    
    print(f"输出: {args.output_dir}/")
    print(f"{'='*70}\n")
    
    # 创建 Sampler
    sampler = SglangSampler(
        base_url=args.base_url,
        temperature=temperature,
        top_p=top_p,
        presence_penalty=presence_penalty,
        max_tokens=args.max_tokens,
        seed=args.seed
    )
    
    # 测试连接
    print("🔌 测试连接...")
    try:
        test_response = sampler([{"role": "user", "content": "Hello"}])
        print(f"✅ 连接成功（响应: {test_response.response_text[:50]}...）\n")
    except Exception as e:
        print(f"❌ 连接失败: {e}")
        print(f"   请确保 sglang 服务器正在运行:")
        print(f"   python -m sglang.launch_server \\")
        print(f"       --model-path /path/to/model \\")
        print(f"       --host 127.0.0.1 \\")
        print(f"       --port 30000")
        sys.exit(1)
    
    # 加载 GPQA 并开始评估
    print(f"📚 加载 GPQA ({args.variant}) 并开始评估...\n")
    
    gpqa_eval = GPQAEval(
        n_repeats=args.n_repeats,
        variant=args.variant,
        num_examples=args.num_examples,
        n_shot=args.n_shot
    )
    
    # 运行评估
    result = gpqa_eval(sampler)
    
    # 自动生成基础配置名
    # 格式: <采样模式>_<few-shot>_<n_repeat>[_自定义名称]
    sampling_part = "greedy" if args.greedy else "dosample"
    shot_part = f"{args.n_shot}shot" if args.n_shot > 0 else "zeroshot"
    repeat_part = f"{args.n_repeats}repeat"  # 始终显示 repeat
    
    # 基础配置名
    auto_config_name = f"{sampling_part}_{shot_part}_{repeat_part}"
    
    # 如果 num_examples 被指定，也加入基础配置名
    if args.num_examples:
        auto_config_name += f"_{args.num_examples}samples"
    
    # 如果提供了 config_name，附加到自动生成的名称后面
    if args.config_name:
        final_config_name = f"{auto_config_name}_{args.config_name}"
    else:
        final_config_name = auto_config_name
    
    # 构建结果文件名（包含详细配置信息）
    # 例如: results_5shots_dosample_10repeats_seed1234.json
    filename_parts = []
    
    # n_shot
    if args.n_shot > 0:
        filename_parts.append(f"{args.n_shot}shots")
    else:
        filename_parts.append("0shot")
    
    # greedy / dosample
    filename_parts.append(sampling_part)
    
    # n_repeats (始终显示)
    filename_parts.append(f"{args.n_repeats}repeats")
    
    # seed (如果不是默认值1234)
    if args.seed != 1234:
        filename_parts.append(f"seed{args.seed}")
    
    # max_tokens (如果不是默认值16384)
    if args.max_tokens != 16384:
        filename_parts.append(f"{args.max_tokens}tokens")
    
    # num_examples (如果指定了)
    if args.num_examples:
        filename_parts.append(f"{args.num_examples}samples")
    
    filename_suffix = "_".join(filename_parts)
    
    # 保存结果 - 按模型名称、变体、最终配置名组织到子文件夹
    # 结构: results/模型名/gpqa_变体/最终配置名/results_*.html
    # 最终配置名 = 自动生成_[可选自定义名称]
    variant_dir_name = f"gpqa_{args.variant}"
    result_dir = Path(args.output_dir) / model_name / variant_dir_name / final_config_name
    result_dir.mkdir(parents=True, exist_ok=True)
    
    html_file = result_dir / f"results_{filename_suffix}.html"
    json_file = result_dir / f"results_{filename_suffix}.json"
    
    html_file.write_text(common.make_report(result))
    
    # 构建配置字典
    config_dict = {
        "variant": args.variant,
        "n_repeats": args.n_repeats,
        "num_examples": args.num_examples,
        "n_shot": args.n_shot,
        "greedy": args.greedy,
        "max_tokens": args.max_tokens,
        "seed": args.seed,
    }
    
    # 记录实际使用的采样参数
    if args.greedy:
        # Greedy 模式：显式覆盖的参数
        config_dict.update({
            "temperature": temperature,
            "top_p": top_p,
            "presence_penalty": presence_penalty,
        })
    else:
        # Do-sample 模式：使用模型默认参数
        config_dict.update({
            "temperature": "model_default (0.7)",
            "top_k": "model_default (20)",
            "top_p": "model_default (0.8)",
            "note": "使用模型自带的默认采样参数"
        })
    
    # 构建完整的 JSON 输出
    json_output = {
        "model": model_name,
        "config_name": final_config_name,  # 最终配置名（包含自定义部分）
        "auto_config_name": auto_config_name,  # 自动生成的基础部分
        "score": result.score,
        "metrics": result.metrics,
        "config": config_dict
    }
    
    # 如果提供了自定义 config_name，也单独记录
    if args.config_name:
        json_output["custom_config_suffix"] = args.config_name
    
    json_file.write_text(json.dumps(json_output, indent=2))
    
    # 打印结果
    print(f"\n{'='*70}")
    print(f"🎉 评估完成！")
    print(f"{'='*70}")
    print(f"准确率: {result.score:.4f} ({result.score*100:.2f}%)")
    print(f"统计指标数: {len(result.metrics)} 个")
    print(f"配置名称: {final_config_name}")
    if args.config_name:
        print(f"  (基础: {auto_config_name} + 自定义: {args.config_name})")
    print(f"输出目录: {result_dir}/")
    print(f"  ├─ {html_file.name}")
    print(f"  └─ {json_file.name}")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    main()

