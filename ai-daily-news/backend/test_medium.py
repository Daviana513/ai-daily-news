#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中等复杂度测试：模拟实际新闻处理
"""
import sys
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import os
import time
from dotenv import load_dotenv

load_dotenv()

print("🧪 中等复杂度测试")
print("="*60)

from processors.optimized_processor import OptimizedDigester

# 模拟3条简单新闻
test_news = [
    {
        'title': 'OpenAI发布新模型',
        'summary': 'OpenAI今天发布了GPT-5，性能大幅提升',
        'url': 'https://example.com/1'
    },
    {
        'title': 'Google推出AI搜索',
        'summary': 'Google在搜索中集成了新的AI功能',
        'url': 'https://example.com/2'
    },
    {
        'title': '微软投资AI芯片',
        'summary': '微软宣布投资10亿美元建设AI芯片工厂',
        'url': 'https://example.com/3'
    }
]

print(f"测试新闻数量: {len(test_news)}")
print("调用消化层API...")

digester = OptimizedDigester()

start = time.time()
try:
    result = digester.digest_news_fast(test_news, "2026-05-31")
    elapsed = time.time() - start

    print(f"✅ 成功！耗时 {elapsed:.2f} 秒")
    print(f"\n返回数据结构: {list(result.keys())}")
    if 'top5' in result:
        print(f"Top5数量: {len(result['top5'])}")

except Exception as e:
    elapsed = time.time() - start
    print(f"❌ 失败，耗时 {elapsed:.2f} 秒")
    print(f"错误: {str(e)}")

print("\n" + "="*60)
print("测试完成")
