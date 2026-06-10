#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速测试后端依赖和配置
"""
import sys
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

try:
    print("检查依赖...")
    from collectors.newsapi_collector import NewsAPICollector
    print("✅ NewsAPICollector 导入成功")

    from processors.optimized_processor import OptimizedDigester, OptimizedTranslator
    print("✅ OptimizedProcessor 导入成功")

    from dotenv import load_dotenv
    load_dotenv()
    print("✅ 环境变量加载成功")

    import os
    api_key = os.getenv('LAOZHAI_API_KEY')
    base_url = os.getenv('LAOZHAI_BASE_URL')
    newsapi_key = os.getenv('NEWSAPI_KEY')

    if api_key:
        print(f"✅ LAOZHAI_API_KEY: {api_key[:20]}...")
    else:
        print("❌ LAOZHAI_API_KEY 未设置")

    if base_url:
        print(f"✅ LAOZHAI_BASE_URL: {base_url}")
    else:
        print("❌ LAOZHAI_BASE_URL 未设置")

    if newsapi_key:
        print(f"✅ NEWSAPI_KEY: {newsapi_key[:20]}...")
    else:
        print("❌ NEWSAPI_KEY 未设置")

    print("\n所有依赖检查通过！")

except ImportError as e:
    print(f"❌ 导入错误: {e}")
except Exception as e:
    print(f"❌ 错误: {e}")
