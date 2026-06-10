#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NewsAPI优化关键词测试
测试更精准的AI新闻关键词
"""

import requests
import json
from datetime import datetime

# 设置控制台编码为UTF-8（Windows兼容）
import sys
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

class OptimizedNewsAPITest:
    """优化后的NewsAPI测试"""

    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://newsapi.org/v2/everything"

    def test_international_optimized(self):
        """测试优化后的国际关键词"""
        print("🌍 测试优化后的国际AI关键词")
        print("="*60)

        # 优化后的关键词
        params = {
            'q': '("artificial intelligence" OR "machine learning" OR "deep learning") AND ("model" OR "breakthrough" OR "launch" OR "release" OR "research") AND NOT ("tablet" OR "smartphone")',
            'language': 'en',
            'sortBy': 'publishedAt',
            'pageSize': 10,
            'apiKey': self.api_key
        }

        return self._execute_request(params, "国际新闻")

    def test_domestic_optimized(self):
        """测试优化后的国内关键词"""
        print("🇨🇳 测试优化后的国内AI关键词")
        print("="*60)

        # 优化后的关键词
        params = {
            'q': '("人工智能" OR "AI" OR "机器学习" OR "深度学习") AND ("模型" OR "突破" OR "发布" OR "技术") AND NOT ("手机" OR "平板" OR "体育")',
            'language': 'zh',
            'sortBy': 'publishedAt',
            'pageSize': 10,
            'apiKey': self.api_key
        }

        return self._execute_request(params, "国内新闻")

    def test_ai_specific_international(self):
        """测试更具体的AI国际关键词"""
        print("🤖 测试AI特定术语（国际）")
        print("="*60)

        # 专注于AI产品和模型
        params = {
            'q': '(ChatGPT OR GPT OR Claude OR Gemini OR Llama OR "large language model" OR "generative AI" OR "multimodal AI") AND (launch OR release OR update OR breakthrough)',
            'language': 'en',
            'sortBy': 'publishedAt',
            'pageSize': 10,
            'apiKey': self.api_key
        }

        return self._execute_request(params, "AI特定新闻")

    def test_ai_specific_domestic(self):
        """测试更具体的AI国内关键词"""
        print("🤖 测试AI特定术语（国内）")
        print("="*60)

        # 专注于AI产品和模型
        params = {
            'q': '("大模型" OR "ChatGPT" OR "文心一言" OR "通义千问" OR "豆包" OR "Kimi" OR "生成式AI" OR "多模态AI") AND (发布 OR 更新 OR 突破 OR 技术)',
            'language': 'zh',
            'sortBy': 'publishedAt',
            'pageSize': 10,
            'apiKey': self.api_key
        }

        return self._execute_request(params, "AI特定新闻")

    def _execute_request(self, params, category):
        """执行API请求"""
        try:
            response = requests.get(self.base_url, params=params, timeout=30)

            if response.status_code == 200:
                data = response.json()
                articles = data.get('articles', [])

                print(f"✅ {category}采集成功: {len(articles)} 条")
                print()

                # 显示每条新闻的标题和相关性分析
                relevant_count = 0
                for i, article in enumerate(articles, 1):
                    title = article.get('title', '')
                    source = article.get('source', {}).get('name', '')

                    # 简单的相关性判断
                    relevant_keywords = ['AI', 'artificial intelligence', 'machine learning', 'deep learning',
                                     'ChatGPT', 'GPT', 'Claude', 'Gemini', 'Llama', '大模型', '人工智能']
                    is_relevant = any(keyword.lower() in title.lower() for keyword in relevant_keywords)

                    if is_relevant:
                        relevant_count += 1
                        relevance_mark = "✅"
                    else:
                        relevance_mark = "⚠️"

                    print(f"{relevance_mark} {i}. {title}")
                    print(f"   来源: {source}")
                    print()

                relevance_rate = (relevant_count / len(articles)) * 100 if articles else 0
                print(f"📊 相关性: {relevant_count}/{len(articles)} ({relevance_rate:.0f}%)")

                return {
                    'count': len(articles),
                    'relevant_count': relevant_count,
                    'articles': articles
                }
            else:
                print(f"❌ 请求失败: {response.status_code}")
                return {'count': 0, 'relevant_count': 0, 'articles': []}

        except Exception as e:
            print(f"❌ 异常: {str(e)}")
            return {'count': 0, 'relevant_count': 0, 'articles': []}

    def run_optimization_tests(self):
        """运行所有优化测试"""
        print("🚀 NewsAPI关键词优化测试")
        print("="*60)
        print("对比原始关键词 vs 优化后关键词")
        print("="*60)
        print()

        results = {}

        # 测试1: 优化后的通用关键词
        print("📝 测试组1: 优化后的通用AI关键词")
        print("-"*60)
        results['int_optimized'] = self.test_international_optimized()
        print()
        results['dom_optimized'] = self.test_domestic_optimized()
        print()

        # 测试2: AI特定术语
        print("📝 测试组2: AI特定术语关键词")
        print("-"*60)
        results['int_ai_specific'] = self.test_ai_specific_international()
        print()
        results['dom_ai_specific'] = self.test_ai_specific_domestic()
        print()

        # 总结
        print("="*60)
        print("📊 关键词优化效果对比")
        print("="*60)

        for test_name, result in results.items():
            if result['count'] > 0:
                relevance_rate = (result['relevant_count'] / result['count']) * 100
                print(f"{test_name}:")
                print(f"   总数: {result['count']}")
                print(f"   相关: {result['relevant_count']}")
                print(f"   相关率: {relevance_rate:.0f}%")
                print()

        print("💡 关键词优化建议：")
        print("1. 使用更具体的AI产品名称（ChatGPT, GPT, Claude等）")
        print("2. 添加动作关键词（发布, 突破, 更新等）")
        print("3. 排除干扰词汇（手机, 平板, 体育等）")
        print("4. 使用引号确保精确匹配")
        print("5. 平衡广度和精准度")

def main():
    """主函数"""
    api_key = "4032bc55beef4064bacfcfc46b1f1479"

    tester = OptimizedNewsAPITest(api_key)
    tester.run_optimization_tests()

    return 0

if __name__ == '__main__':
    sys.exit(main())