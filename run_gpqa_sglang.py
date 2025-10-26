#!/usr/bin/env python3
"""
使用 sglang 后端运行 GPQA 评估（Zero-shot）
专为 Qwen3-4B-Instruct 和 W8A16 量化模型设计

用法:
    # 原始模型
    python run_gpqa_sglang.py --model original
    
    # 量化模型
    python run_gpqa_sglang.py --model w8a16
    
    # 自定义配置
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

# 添加父目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent))

# 导入 simple_evals 包
from simple_evals.gpqa_eval import GPQAEval
from simple_evals.types import SamplerBase, SamplerResponse
from simple_evals import common


class SglangSampler(SamplerBase):
    """
    Sglang 后端 Sampler
    支持 OpenAI-compatible API
    """
    
    def __init__(
        self, 
        base_url: str, 
        temperature: float = 0.0, 
        max_tokens: int = 16384,
        system_message: str = "You are a helpful assistant."
    ):
        """
        Args:
            base_url: sglang 服务器地址，如 http://127.0.0.1:30000/v1
            temperature: 采样温度 (0.0 = greedy)
            max_tokens: 最大生成 token 数
            system_message: 系统提示
        """
        self.client = OpenAI(base_url=base_url, api_key="dummy")
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.system_message = system_message
    
    def _pack_message(self, content: str, role: str):
        """打包消息为 OpenAI 格式"""
        return {"role": role, "content": content}
    
    def __call__(self, message_list):
        """
        调用 sglang 后端生成响应
        
        Args:
            message_list: 消息列表（不包含 system message）
            
        Returns:
            SamplerResponse
        """
        # 添加 system message
        messages = [self._pack_message(self.system_message, "system")] + message_list
        
        # 调用 sglang
        response = self.client.chat.completions.create(
            model="default",  # sglang 忽略此参数
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )
        
        return SamplerResponse(
            response_text=response.choices[0].message.content,
            response_metadata={"usage": response.usage},
            actual_queried_message_list=messages,
        )


# 预设配置
PRESETS = {
    "original": {
        "model_name": "Qwen3-4B-Instruct-2507",
        "description": "原始 BF16 模型"
    },
    "w8a16": {
        "model_name": "Qwen3-4B-Instruct-2507-INT8-W8A16",
        "description": "INT8 量化模型（权重INT8，激活FP16）"
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
    
    # 采样参数
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.0,
        help="采样温度 (默认: 0.0 = greedy)"
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=16384,
        help="最大生成 token 数 (默认: 16384 = 16k)"
    )
    
    # 输出配置
    parser.add_argument(
        "--output-dir",
        type=str,
        default="results",
        help="结果保存目录 (默认: results/)"
    )
    
    args = parser.parse_args()
    
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
    sampling_mode = "Greedy" if args.temperature == 0.0 else f"Temp={args.temperature}"
    print(f"采样: Zero-shot, {sampling_mode}, Max-Tokens={args.max_tokens}")
    print(f"输出: {args.output_dir}/")
    print(f"{'='*70}\n")
    
    # 创建 Sampler
    sampler = SglangSampler(
        base_url=args.base_url,
        temperature=args.temperature,
        max_tokens=args.max_tokens
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
        num_examples=args.num_examples
    )
    
    # 运行评估
    result = gpqa_eval(sampler)
    
    # 保存结果 - 按模型名称和变体组织到子文件夹
    # 结构: results/模型名/gpqa_变体/results.html
    variant_dir_name = f"gpqa_{args.variant}"
    if args.num_examples:
        variant_dir_name += f"_{args.num_examples}samples"
    
    result_dir = Path(args.output_dir) / model_name / variant_dir_name
    result_dir.mkdir(parents=True, exist_ok=True)
    
    html_file = result_dir / "results.html"
    json_file = result_dir / "results.json"
    
    html_file.write_text(common.make_report(result))
    json_file.write_text(json.dumps({
        "model": model_name,
        "score": result.score,
        "metrics": result.metrics,
        "config": {
            "variant": args.variant,
            "n_repeats": args.n_repeats,
            "num_examples": args.num_examples,
            "temperature": args.temperature,
            "max_tokens": args.max_tokens,
        }
    }, indent=2))
    
    # 打印结果
    print(f"\n{'='*70}")
    print(f"🎉 评估完成！")
    print(f"{'='*70}")
    print(f"准确率: {result.score:.4f} ({result.score*100:.2f}%)")
    print(f"统计指标数: {len(result.metrics)} 个")
    print(f"输出目录: {result_dir}/")
    print(f"  ├─ {html_file.name}")
    print(f"  └─ {json_file.name}")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    main()

