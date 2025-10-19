#!/usr/bin/env python3
"""
使用 simple-evals 原生 API 运行 GPQA 评估
简洁版本：直接调用 simple-evals，最少自定义
"""
import os
import sys
import json
import argparse
from pathlib import Path
from openai import OpenAI

sys.path.insert(0, str(Path(__file__).parent / "simple-evals"))

from simple_evals.gpqa_eval import GPQAEval
from simple_evals.types import SamplerBase, SamplerResponse
from simple_evals import common


class SglangSampler(SamplerBase):
    """简单的 sglang sampler"""
    
    def __init__(self, base_url: str, temperature: float = 0.7, top_p: float = 0.8, 
                 max_tokens: int = 4096):
        self.client = OpenAI(base_url=base_url, api_key="dummy")
        self.temperature = temperature
        self.top_p = top_p
        self.max_tokens = max_tokens
    
    def _pack_message(self, content: str, role: str):
        return {"role": role, "content": content}
    
    def __call__(self, message_list):
        messages = [self._pack_message("You are a helpful assistant.", "system")] + message_list
        
        response = self.client.chat.completions.create(
            model="default",
            messages=messages,
            temperature=self.temperature,
            top_p=self.top_p,
            max_tokens=self.max_tokens,
            extra_body={"top_k": 20, "min_p": 0.0}  # sglang 额外参数
        )
        
        return SamplerResponse(
            response_text=response.choices[0].message.content,
            response_metadata={"usage": response.usage},
            actual_queried_message_list=messages,
        )


def main():
    parser = argparse.ArgumentParser(description="Simple-evals GPQA 评估")
    parser.add_argument("--model-name", type=str, required=True)
    parser.add_argument("--base-url", type=str, default="http://127.0.0.1:30000/v1")
    parser.add_argument("--num-examples", type=int, default=None)
    parser.add_argument("--n-repeats", type=int, default=10)
    parser.add_argument("--variant", type=str, default="diamond")
    parser.add_argument("--temperature", type=float, default=0.7)
    parser.add_argument("--top-p", type=float, default=0.8)
    parser.add_argument("--max-tokens", type=int, default=4096)
    parser.add_argument("--output-dir", type=str, default="results")
    args = parser.parse_args()
    
    print(f"\n{'='*60}")
    print(f"模型: {args.model_name}")
    print(f"服务器: {args.base_url}")
    print(f"Variant: {args.variant}")
    print(f"Samples: {args.num_examples or 'ALL'} × {args.n_repeats} repeats")
    print(f"Temp: {args.temperature}, Top-P: {args.top_p}")
    print(f"{'='*60}\n")
    
    # 创建 sampler
    sampler = SglangSampler(
        base_url=args.base_url,
        temperature=args.temperature,
        top_p=args.top_p,
        max_tokens=args.max_tokens
    )
    
    # 测试连接
    print("🔌 测试连接...")
    try:
        sampler([{"role": "user", "content": "Hello"}])
        print("✅ 连接成功\n")
    except Exception as e:
        print(f"❌ 连接失败: {e}")
        sys.exit(1)
    
    # 创建评估对象并运行（使用 simple-evals 原生 API）
    print("📚 加载 GPQA 并开始评估...\n")
    gpqa_eval = GPQAEval(
        n_repeats=args.n_repeats,
        variant=args.variant,
        num_examples=args.num_examples
    )
    
    # 运行评估（完全使用 simple-evals 的内部逻辑）
    result = gpqa_eval(sampler)
    
    # 保存结果
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    html_file = output_dir / f"gpqa_{args.model_name}.html"
    json_file = output_dir / f"gpqa_{args.model_name}.json"
    
    html_file.write_text(common.make_report(result))
    json_file.write_text(json.dumps({
        "score": result.score,
        "metrics": result.metrics,
        "n_repeats": args.n_repeats,
        "variant": args.variant,
    }, indent=2))
    
    print(f"\n{'='*60}")
    print(f"🎉 评估完成！")
    print(f"{'='*60}")
    print(f"准确率: {result.score:.4f} ({result.score*100:.2f}%)")
    print(f"HTML: {html_file}")
    print(f"JSON: {json_file}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()

