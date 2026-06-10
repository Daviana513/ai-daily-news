#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
优化效果测试脚本
对比优化前后的性能表现
"""

import sys
import os
import time
from datetime import datetime

# 设置控制台编码为UTF-8（Windows兼容）
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 导入优化版处理器
from collectors.newsapi_collector import NewsAPICollector
from processors.optimized_processor import OptimizedDigester, OptimizedTranslator

def test_optimized_performance():
    """测试优化后的性能"""
    print("🚀 测试优化后的系统性能")
    print("="*60)

    total_start = time.time()

    # 步骤1：采集
    print("📡 步骤1：采集新闻...")
    collect_start = time.time()

    collector = NewsAPICollector()
    today = datetime.now().strftime('%Y-%m-%d')
    raw_news = collector.collect_daily_news(today)

    if not raw_news or len(raw_news) < 5:
        print("❌ 采集的新闻数量不足")
        return False

    collect_time = time.time() - collect_start
    print(f"✅ 采集完成：{len(raw_news)}条新闻，耗时{collect_time:.2f}秒")

    # 步骤2：快速消化
    print("\n🧠 步骤2：快速消化处理...")
    digest_start = time.time()

    digester = OptimizedDigester()
    news_to_process = raw_news[:15]  # 只处理前15条
    digested_news = digester.digest_news_fast(news_to_process, today)

    if not digested_news:
        print("❌ 消化层处理失败")
        return False

    digest_time = time.time() - digest_start
    print(f"✅ 消化完成，耗时{digest_time:.2f}秒")

    # 步骤3：快速通俗化
    print("\n💬 步骤3：快速通俗化...")
    translate_start = time.time()

    translator = OptimizedTranslator()
    final_news = translator.translate_fast(digested_news)

    if not final_news:
        print("❌ 说人话层处理失败")
        return False

    translate_time = time.time() - translate_start
    print(f"✅ 通俗化完成，耗时{translate_time:.2f}秒")

    # 总耗时
    total_time = time.time() - total_start

    # 显示结果
    print("\n" + "="*60)
    print("📊 性能报告（优化版）")
    print("="*60)
    print(f"总耗时：{total_time:.2f}秒")
    print(f"采集层：{collect_time:.2f}秒 ({collect_time/total_time*100:.1f}%)")
    print(f"消化层：{digest_time:.2f}秒 ({digest_time/total_time*100:.1f}%)")
    print(f"说人话层：{translate_time:.2f}秒 ({translate_time/total_time*100:.1f}%)")
    print()
    print(f"处理新闻数：{len(news_to_process)}条")
    print(f"原始新闻数：{len(raw_news)}条")

    # 对比优化前（约90秒）
    baseline_time = 90
    improvement = ((baseline_time - total_time) / baseline_time) * 100

    print("\n" + "="*60)
    print("🎯 优化效果对比")
    print("="*60)
    print(f"优化前：~{baseline_time}秒")
    print(f"优化后：~{total_time:.2f}秒")
    print(f"提升：{improvement:.1f}%")

    # 判断优化目标
    if total_time < 60:
        print("\n🎉 优化成功！已达到目标（<60秒）")
    elif total_time < 75:
        print("\n✅ 优化有效！接近目标（<75秒）")
    else:
        print(f"\n⚠️  仍需优化（当前{total_time:.2f}秒）")

    # 显示日报预览
    print("\n" + "="*60)
    print("📰 日报预览")
    print("="*60)

    if 'top5' in final_news:
        for i, news in enumerate(final_news['top5'], 1):
            print(f"\n{i}. {news.get('title', 'N/A')}")
            if 'summary' in news:
                print(f"   {news['summary'][:60]}...")

    if 'insight' in final_news:
        print(f"\n🔍 趋势：{final_news['insight'].get('trend', 'N/A')[:80]}...")
        print(f"⚠️  风险：{final_news['insight'].get('risk', 'N/A')[:80]}...")

    return True

def main():
    """主函数"""
    try:
        success = test_optimized_performance()
        return 0 if success else 1
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())
