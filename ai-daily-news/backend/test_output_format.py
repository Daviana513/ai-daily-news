#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试输出格式是否与前端期望一致
"""

import sys
import os
from datetime import datetime

# 设置控制台编码
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from collectors.newsapi_collector import NewsAPICollector
from processors.optimized_processor import OptimizedDigester, OptimizedTranslator

def test_output_format():
    """测试输出格式"""
    print("🔍 测试输出格式")
    print("="*60)

    # 采集新闻
    print("1. 采集新闻...")
    collector = NewsAPICollector()
    today = datetime.now().strftime('%Y-%m-%d')
    raw_news = collector.collect_daily_news(today)

    # 消化处理
    print("2. 消化处理...")
    digester = OptimizedDigester()
    news_to_process = raw_news[:15]
    digested_news = digester.digest_news_fast(news_to_process, today)

    # 通俗化处理
    print("3. 通俗化处理...")
    translator = OptimizedTranslator()
    final_news = translator.translate_fast(digested_news)

    # 检查格式
    print("\n" + "="*60)
    print("📋 格式检查")
    print("="*60)

    # 检查必需字段
    required_fields = {
        'date': str,
        'top5': list,
        'digest_table': list,
        'further_reading': list,
        'insight': dict
    }

    all_good = True
    for field, field_type in required_fields.items():
        if field not in final_news:
            print(f"❌ 缺少字段: {field}")
            all_good = False
        elif not isinstance(final_news[field], field_type):
            print(f"❌ 字段类型错误: {field} (期望{field_type.__name__}, 实际{type(final_news[field]).__name__})")
            all_good = False
        else:
            print(f"✅ {field}: {type(final_news[field]).__name__}")

    # 检查top5格式
    if 'top5' in final_news and len(final_news['top5']) > 0:
        print("\n📰 检查Top5格式:")
        top5_required = ['title', 'summary', 'source_url', 'why_important']
        for i, news in enumerate(final_news['top5'][:1], 1):  # 只检查第一条
            print(f"  新闻{i}:")
            for field in top5_required:
                if field in news:
                    value = news[field]
                    if value:
                        print(f"    ✅ {field}: {value[:50]}...")
                    else:
                        print(f"    ⚠️  {field}: 空值")
                        all_good = False
                else:
                    print(f"    ❌ 缺少字段: {field}")
                    all_good = False

    # 检查digest_table格式
    if 'digest_table' in final_news and len(final_news['digest_table']) > 0:
        print("\n📊 检查概览表格格式:")
        table_required = ['category', 'title', 'importance']
        for i, item in enumerate(final_news['digest_table'][:1], 1):
            print(f"  条目{i}:")
            for field in table_required:
                if field in item:
                    print(f"    ✅ {field}: {item[field]}")
                else:
                    print(f"    ❌ 缺少字段: {field}")
                    all_good = False

    # 检查further_reading格式
    if 'further_reading' in final_news and len(final_news['further_reading']) > 0:
        print("\n📖 检查延伸阅读格式:")
        reading_required = ['title', 'url']
        for i, item in enumerate(final_news['further_reading'][:1], 1):
            print(f"  条目{i}:")
            for field in reading_required:
                if field in item:
                    print(f"    ✅ {field}: {item[field][:50]}...")
                else:
                    print(f"    ❌ 缺少字段: {field}")
                    all_good = False

    # 检查insight格式
    if 'insight' in final_news:
        print("\n💡 检查洞察格式:")
        insight_required = ['trend', 'risk']
        for field in insight_required:
            if field in final_news['insight']:
                print(f"  ✅ {field}: {final_news['insight'][field][:50]}...")
            else:
                print(f"  ❌ 缺少字段: insight.{field}")
                all_good = False

    # 最终结果
    print("\n" + "="*60)
    if all_good:
        print("🎉 格式检查通过！所有必需字段都存在。")
    else:
        print("⚠️  格式检查发现问题，请检查上述错误。")
    print("="*60)

    return all_good

def main():
    try:
        success = test_output_format()
        return 0 if success else 1
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())
