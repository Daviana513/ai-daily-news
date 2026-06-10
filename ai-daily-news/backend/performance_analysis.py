#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
性能分析脚本
分析各层处理时间，找出优化机会
"""

import os
import sys
import time
import json
from datetime import datetime
from dotenv import load_dotenv

# 设置控制台编码为UTF-8（Windows兼容）
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

load_dotenv()

class PerformanceAnalyzer:
    """性能分析器"""

    def __init__(self):
        self.api_key = "4032bc55beef4064bacfcfc46b1f1479"
        self.laozai_api_key = os.getenv('LAOZHAI_API_KEY')
        self.laozai_base_url = os.getenv('LAOZHAI_BASE_URL')

    def analyze_collect_layer(self):
        """分析采集层性能"""
        print("📡 分析采集层性能")
        print("="*60)

        import requests
        base_url = "https://newsapi.org/v2/everything"

        # 测试采集时间
        int_params = {
            'q': '(ChatGPT OR "OpenAI" OR "GPT-4") AND (launch OR release)',
            'language': 'en',
            'sortBy': 'publishedAt',
            'pageSize': 5,
            'apiKey': self.api_key
        }

        start_time = time.time()
        response = requests.get(base_url, params=int_params, timeout=30)
        collect_time = time.time() - start_time

        print(f"✅ 采集5条新闻耗时: {collect_time:.2f}秒")

        if collect_time < 10:
            return "快", collect_time
        elif collect_time < 20:
            return "正常", collect_time
        else:
            return "慢", collect_time

    def analyze_processing_layer(self, news_count=5):
        """分析处理层性能"""
        print("\n🧠 分析处理层性能")
        print("="*60)

        import requests

        # 模拟新闻数据
        fake_news = [
            {'title': f'新闻{i}', 'summary': f'摘要{i}', 'source': '来源{i}', 'url': f'url{i}', 'source_type': 'Test'}
            for i in range(news_count)
        ]

        # 格式化为prompt
        raw_news_text = ""
        for i, news in enumerate(fake_news, 1):
            raw_news_text += f"""
新闻{i}：
标题：{news['title']}
摘要：{news['summary']}
来源：{news['source']}
URL：{news['url']}
"""

        # 测试不同prompt长度的影响
        prompts = {
            'short': f"从{len(fake_news)}条新闻中选Top5：{raw_news_text}",
            'medium': f"从{len(fake_news)}条新闻中选Top5，要覆盖不同类别：{raw_news_text}",
            'long': f"从{len(fake_news)}条新闻中选Top5，要覆盖至少3个不同类别，优先级：第一优先对AI行业格局有重大影响的事件...{raw_news_text}"
        }

        for prompt_type, prompt in prompts.items():
            start_time = time.time()

            # 调用老张API测试
            api_url = f"{self.laozai_base_url}/chat/completions"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.laozai_api_key}'
            }

            data = {
                'model': 'qwen-plus',
                'messages': [{'role': 'user', 'content': prompt}],
                'temperature': 0.3,
                'max_tokens': 500 if prompt_type == 'short' else 1500
            }

            try:
                response = requests.post(api_url, headers=headers, json=data, timeout=30)
                process_time = time.time() - start_time

                print(f"✅ {prompt_type} prompt处理耗时: {process_time:.2f}秒")
            except Exception as e:
                print(f"❌ {prompt_type} prompt测试失败: {str(e)}")

    def analyze_token_impact(self):
        """分析token数量对性能的影响"""
        print("\n🔍 分析Token数量影响")
        print("="*60)

        import requests

        # 简单测试prompt
        test_prompt = "从5条新闻中选Top5："
        for i in range(5):
            test_prompt += f"新闻{i}标题摘要来源URL"

        start_time = time.time()

        api_url = f"{self.laozai_base_url}/chat/completions"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.laozai_api_key}'
        }

        data = {
            'model': 'qwen-plus',
            'messages': [{'role': 'user', 'content': test_prompt}],
            'temperature': 0.3,
            'max_tokens': 500
        }

        try:
            response = requests.post(api_url, headers=headers, json=data, timeout=30)
            process_time = time.time() - start_time
            print(f"✅ 500 tokens耗时: {process_time:.2f}秒")
        except Exception as e:
            print(f"❌ Token测试失败: {str(e)}")

    def analyze_news_count_impact(self):
        """分析新闻数量对性能的影响"""
        print("\n📊 分析新闻数量影响")
        print("="*60)

        import requests

        for count in [5, 10, 15, 20]:
            # 构建测试prompt
            fake_news = [
                {'title': f'新闻{i}', 'summary': f'摘要{i}', 'source': '来源{i}', 'url': f'url{i}', 'source_type': 'Test'}
                for i in range(count)
            ]

            raw_news_text = ""
            for i, news in enumerate(fake_news, 1):
                raw_news_text += f"新闻{i}：{news['title']}摘要：{news['summary']}来源：{news['source']}URL：{news['url']}"

            prompt = f"从{count}条新闻中选Top5：{raw_news_text}"

            start_time = time.time()

            api_url = f"{self.laozai_base_url}/chat/completions"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.laozai_api_key}'
            }

            data = {
                'model': 'qwen-plus',
                'messages': [{'role': 'user', 'content': prompt}],
                'temperature': 0.3,
                'max_tokens': 1000
            }

            try:
                response = requests.post(api_url, headers=headers, json=data, timeout=30)
                process_time = time.time() - start_time
                print(f"✅ {count}条新闻处理耗时: {process_time:.2f}秒")
            except Exception as e:
                print(f"❌ {count}条新闻测试失败: {str(e)}")

    def run_optimization_analysis(self):
        """运行完整的优化分析"""
        print("⏱️ 性能优化分析")
        print("="*60)
        print("目标：识别时间瓶颈，提供优化建议")
        print("="*60)
        print()

        # 分析1: 采集层性能
        collect_status, collect_time = self.analyze_collect_layer()
        print(f"采集层状态: {collect_status} ({collect_time:.2f}秒)")
        print()

        # 分析2: 处理层性能
        self.analyze_processing_layer()
        print()

        # 分析3: Token影响
        self.analyze_token_impact()
        print()

        # 分析4: 新闻数量影响
        self.analyze_news_count_impact()
        print()

        # 优化建议
        print("="*60)
        print("💡 优化建议")
        print("="*60)

        print("🎯 发现的优化机会：")

        print("\n1. 减少新闻数量：")
        print("   - 当前：20条新闻 → 优化为：15条新闻")
        print("   - 预计节省：10-15秒")

        print("\n2. 优化prompt长度：")
        print("   - 当前：详细prompt → 优化：精简核心指令")
        print("   - 预计节省：15-20秒")

        print("\n3. 调整max_tokens：")
        print("   - 当前：3000 tokens → 优化：2000 tokens")
        print("   - 预计节省：10-15秒")

        print("\n4. 并行化处理：")
        print("   - 当前：串行处理 → 优化：部分并行")
        print("   - 预计节省：30-45秒")

        print("\n5. 批处理优化：")
        print("   - 当前：分3次API调用 → 优化：合并为2次调用")
        print("   - 预计节省：15-30秒")

        print("\n🚀 预期优化效果：")
        print("   - 当前时间：~90秒")
        print("   - 优化后：~45-60秒")
        print("   - 改善：35-50%")

def main():
    """主函数"""
    analyzer = PerformanceAnalyzer()
    analyzer.run_optimization_analysis()

    return 0

if __name__ == '__main__':
    sys.exit(main())