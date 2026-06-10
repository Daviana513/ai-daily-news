#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终配置验证测试
"""

import sys
import os
sys.path.append('.')

# 设置控制台编码
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from collectors.newsapi_collector_final import FinalNewsAPICollector

def main():
    print("🚀 最终优化配置验证测试")
    print("="*60)

    api_key = "4032bc55beef4064bacfcfc46b1f1479"
    collector = FinalNewsAPICollector(api_key)

    print("\n🌍 采集国际AI新闻（优化后关键词）:")
    print("-"*60)
    int_news = collector.collect_international_ai_news(5)

    print(f"\n🇨🇳 采集国内AI新闻（优化后关键词）:")
    print("-"*60)
    dom_news = collector.collect_domestic_ai_news(5)

    print(f"\n📊 预览结果:")
    print("="*60)

    print("\n🌍 国际新闻（前3条）:")
    for i, news in enumerate(int_news[:3], 1):
        print(f"{i}. {news['title']}")
        print(f"   来源: {news['source']}")
        print(f"   URL: {news['url'][:60]}...")

    print(f"\n🇨🇳 国内新闻（前3条）:")
    for i, news in enumerate(dom_news[:3], 1):
        print(f"{i}. {news['title']}")
        print(f"   来源: {news['source']}")
        print(f"   URL: {news['url'][:60]}...")

    print(f"\n✅ 最终配置验证完成！")
    print(f"总采集: {len(int_news) + len(dom_news)} 条AI新闻")
    print(f"相关性预期: ~60%（基于测试结果）")

if __name__ == '__main__':
    main()