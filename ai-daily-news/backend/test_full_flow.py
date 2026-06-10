#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整测试：模拟实际API调用流程
"""
import sys
import os
import time
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("🧪 完整流程测试")
print("="*60)

try:
    from dotenv import load_dotenv
    load_dotenv()

    import requests
    from collectors.newsapi_collector import NewsAPICollector
    from processors.optimized_processor import OptimizedDigester

    api_key = os.getenv('LAOZHAI_API_KEY')
    base_url = os.getenv('LAOZHAI_BASE_URL')

    print(f"✅ 环境变量加载成功")

    # 测试1: NewsAPI采集
    print("\n📡 测试1: NewsAPI采集...")
    collector = NewsAPICollector()

    start = time.time()
    today = "2026-05-31"
    raw_news = collector.collect_daily_news(today)

    collect_time = time.time() - start
    print(f"✅ 采集成功：{len(raw_news)}条新闻，耗时{collect_time:.2f}秒")

    if len(raw_news) < 5:
        print("❌ 采集的新闻数量不足，无法继续测试")
        sys.exit(1)

    # 测试2: 消化层处理（只处理前5条，快速测试）
    print("\n🧠 测试2: 消化层处理（5条新闻）...")
    digester = OptimizedDigester()

    news_to_process = raw_news[:5]
    print(f"处理 {len(news_to_process)} 条新闻")

    start = time.time()

    try:
        # 设置更长的超时时间来测试
        print("调用老张API（超时120秒）...")
        digested_news = digester.digest_news_fast(news_to_process, today)

        digest_time = time.time() - start
        print(f"✅ 消化成功，耗时{digest_time:.2f}秒")

    except Exception as e:
        digest_time = time.time() - start
        print(f"❌ 消化失败，耗时{digest_time:.2f}秒")
        print(f"错误: {str(e)}")

        if "timeout" in str(e).lower():
            print("\n💡 建议：")
            print("   老张API服务器响应太慢（超过120秒）")
            print("   可能需要：")
            print("   1. 检查老张API服务器状态")
            print("   2. 考虑使用更快的AI模型")
            print("   3. 优化prompt减少token数量")

except Exception as e:
    print(f"❌ 测试失败: {str(e)}")
    import traceback
    traceback.print_exc()

finally:
    print("\n" + "="*60)
    print("测试完成")
