#!/usr/bin/env python3
"""
使用 sglang 本地服务器运行 GPQA 评估
确保 sglang 服务器已启动在 http://127.0.0.1:30000
"""
import os
import sys
import json
import argparse
from pathlib import Path
from openai import OpenAI

sys.path.insert(0, str(Path(__file__).parent / "simple-evals"))

from simple_evals.gpqa_eval import GPQAEval
from simple_evals.types import MessageList, SamplerBase, SamplerResponse
from simple_evals import common

# Qwen 推荐的采样参数
SAMPLING_PARAMS = {
    "temperature": 0.7,
    "top_p": 0.8,
    "top_k": 20,
    "min_p": 0.0,
}

# 默认 seed 起始值
DEFAULT_SEED = 1234


class SglangSampler(SamplerBase):
    """sglang sampler with custom sampling parameters and seed control"""
    
    def __init__(self, max_tokens: int = 4096, base_seed: int = DEFAULT_SEED):
        self.client = OpenAI()
        self.max_tokens = max_tokens
        self.base_seed = base_seed
        self.call_count = 0  # 用于递增 seed
    
    def _pack_message(self, role: str, content: str):
        return {"role": role, "content": content}
    
    def __call__(self, message_list: MessageList) -> SamplerResponse:
        messages = [self._pack_message("system", "You are a helpful assistant.")] + message_list
        
        # 每次调用使用不同的 seed: base_seed + call_count
        current_seed = self.base_seed + self.call_count
        self.call_count += 1
        
        response = self.client.chat.completions.create(
            model="default",
            messages=messages,
            temperature=SAMPLING_PARAMS["temperature"],
            top_p=SAMPLING_PARAMS["top_p"],
            max_tokens=self.max_tokens,
            seed=current_seed,  # 添加 seed 参数
            extra_body={"top_k": SAMPLING_PARAMS["top_k"], "min_p": SAMPLING_PARAMS["min_p"]}
        )
        
        return SamplerResponse(
            response_text=response.choices[0].message.content,
            response_metadata={"usage": response.usage},
            actual_queried_message_list=messages,
        )


def main():
    parser = argparse.ArgumentParser(description="运行 GPQA 评估")
    parser.add_argument("--model-name", type=str, default="qwen3-4b-original", 
                        help="模型名称（用于保存结果）")
    parser.add_argument("--base-url", type=str, default="http://127.0.0.1:30000/v1",
                        help="sglang 服务器地址")
    parser.add_argument("--num-examples", type=int, default=None,
                        help="测试样本数（None=全部）")
    parser.add_argument("--n-repeats", type=int, default=10,
                        help="重复评估次数（默认: 10）")
    parser.add_argument("--variant", type=str, default="diamond",
                        help="GPQA 变体 (默认: diamond)")
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED,
                        help="随机种子起始值（默认: 1234）")
    parser.add_argument("--max-tokens", type=int, default=4096,
                        help="最大输出长度")
    parser.add_argument("--output-dir", type=str, default="results",
                        help="结果输出目录")
    
    args = parser.parse_args()
    
    os.environ['OPENAI_API_KEY'] = 'dummy-key'
    os.environ['OPENAI_BASE_URL'] = args.base_url
    
    print("=" * 60)
    print(f"模型: {args.model_name}")
    print(f"服务器: {args.base_url}")
    print(f"Variant: {args.variant}")
    print(f"样本数: {args.num_examples or 'ALL'}")
    print(f"Repeats: {args.n_repeats}")
    print(f"Seed: {args.seed} + n")
    print(f"采样: temp={SAMPLING_PARAMS['temperature']}, top_p={SAMPLING_PARAMS['top_p']}, "
          f"top_k={SAMPLING_PARAMS['top_k']}, min_p={SAMPLING_PARAMS['min_p']}")
    print(f"Max tokens: {args.max_tokens}")
    print("=" * 60)
    
    # 创建 sampler 并测试连接
    sampler = SglangSampler(max_tokens=args.max_tokens, base_seed=args.seed)
    
    print("\n🔌 测试连接...")
    try:
        sampler([{"role": "user", "content": "Hello"}])
        print("✅ 连接成功\n")
    except Exception as e:
        print(f"❌ 连接失败: {e}")
        sys.exit(1)
    
    # 准备输出目录
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 外层循环 repeats，每遍独立评估
    all_results = []
    for repeat in range(args.n_repeats):
        print(f"\n{'='*60}")
        print(f"Repeat {repeat+1}/{args.n_repeats}")
        print(f"{'='*60}")
        
        # 创建单次评估（n_repeats=1）
        gpqa_eval = GPQAEval(n_repeats=1, variant=args.variant, num_examples=args.num_examples)
        
        # 运行评估
        result = gpqa_eval(sampler)
        all_results.append(result)
        
        # 立即保存单次结果
        repeat_file = output_dir / f"gpqa_{args.model_name}_repeat{repeat}.json"
        repeat_file.write_text(json.dumps({
            "repeat": repeat,
            "score": result.score,
            "metrics": result.metrics,
        }, indent=2))
        
        print(f"\n✅ Repeat {repeat+1} 完成: {result.score:.4f} ({result.score*100:.2f}%)")
        print(f"📁 保存: {repeat_file}")
    
    # 统计所有 repeats
    import numpy as np
    scores = [r.score for r in all_results]
    mean_score = np.mean(scores)
    std_score = np.std(scores, ddof=1) if len(scores) > 1 else 0.0
    
    # 保存最终汇总
    final_file = output_dir / f"gpqa_{args.model_name}_final.json"
    final_file.write_text(json.dumps({
        "model": args.model_name,
        "n_repeats": args.n_repeats,
        "mean_score": mean_score,
        "std_score": std_score,
        "all_scores": scores,
        "sampling_params": SAMPLING_PARAMS,
    }, indent=2))
    
    # 保存完整 HTML 报告（合并所有 repeats）
    html_file = output_dir / f"gpqa_{args.model_name}.html"
    html_file.write_text(common.make_report(all_results[0]))  # 使用第一次的HTML
    
    print("\n" + "=" * 60)
    print("🎉 所有评估完成！")
    print("=" * 60)
    print(f"📊 Mean: {mean_score:.4f} ({mean_score*100:.2f}%)")
    print(f"📊 Std:  {std_score:.4f} ({std_score*100:.2f}%)")
    print(f"📊 Scores: {[f'{s:.4f}' for s in scores]}")
    print(f"📁 最终结果: {final_file}")
    print("=" * 60)


if __name__ == "__main__":
    main()

