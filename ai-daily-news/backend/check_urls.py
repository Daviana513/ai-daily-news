#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查URL字段是否正确
"""

import sys
import os
from datetime import datetime
import json

# 设置控制台编码
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from collectors.newsapi_collector import NewsAPICollector
from processors.optimized_processor import OptimizedDigester

def check_urls():
    """检查URL字段"""
    print("🔍 检查URL传递")
    print("="*60)

    # 采集新闻
    print("1. 采集原始新闻...")
    collector = NewsAPICollector()
    today = datetime.now().strftime('%Y-%m-%d')
    raw_news = collector.collect_daily_news(today)

    # 显示原始新闻的URL
    print("\n📰 原始新闻URL示例:")
    for i, news in enumerate(raw_news[:3], 1):
        print(f"{i}. 标题: {news['title'][:60]}...")
        print(f"   URL: {news.get('url', 'N/A')}")
        print()

    # 消化处理
    print("2. 消化处理...")
    digester = OptimizedDigester()
    news_to_process = raw_news[:15]
    digested_news = digester.digest_news_fast(news_to_process, today)

    # 显示消化后的URL
    print("\n📋 消化后Top5的URL:")
    if 'top5' in digested_news:
        for i, news in enumerate(digested_news['top5'], 1):
            print(f"{i}. 标题: {news['title'][:60]}...")
            print(f"   source_url: {news.get('source_url', 'N/A')}")
            print()

    # 检查延伸阅读的URL
    print("📖 延伸阅读的URL:")
    if 'further_reading' in digested_news:
        for i, item in enumerate(digested_news['further_reading'][:3], 1):
            print(f"{i}. 标题: {item['title'][:60]}...")
            print(f"   url: {item.get('url', 'N/A')}")
            print()

    # 保存完整输出到文件
    print("💾 保存完整输出到 check_output.json...")
    with open('check_output.json', 'w', encoding='utf-8') as f:
        json.dump(digested_news, f, ensure_ascii=False, indent=2)
    print("✅ 已保存")

if __name__ == '__main__':
    try:
        check_urls()
    except Exception as e:
        print(f"❌ 错误: {str(e)}")
        import traceback
        traceback.print_exc()
