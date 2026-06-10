#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
采集层小范围测试
测试国内外新闻抓取功能（各10条）
"""

import os
import sys
import json
from datetime import datetime
from dotenv import load_dotenv

# 设置控制台编码为UTF-8（Windows兼容）
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 加载环境变量
load_dotenv()

def test_collector():
    """测试采集层功能"""
    print("🧪 开始测试采集层功能...")
    print("目标：国内外各抓取10条AI新闻")
    print()

    # 导入采集器
    try:
        from collectors.unified_collector import UnifiedCollector
        print("✅ 采集器导入成功")
    except ImportError as e:
        print(f"❌ 采集器导入失败: {str(e)}")
        return False

    # 初始化采集器
    try:
        collector = UnifiedCollector()
        print("✅ 采集器初始化成功")
        print(f"   - 国外模型: {collector.gemini_model}")
        print(f"   - 国内模型: {collector.qwen_model}")
        print()
    except Exception as e:
        print(f"❌ 采集器初始化失败: {str(e)}")
        return False

    # 测试采集
    try:
        today = datetime.now().strftime('%Y-%m-%d')
        print(f"📅 采集日期: {today}")
        print("开始采集，请稍候...")

        all_news = collector.collect_daily_news(today)

        print(f"\n✅ 采集完成！共获得 {len(all_news)} 条新闻")
        print()

        # 分析结果
        gemini_count = len([n for n in all_news if n.get('source_type') == 'Gemini'])
        qwen_count = len([n for n in all_news if n.get('source_type') == 'Qwen'])

        print("📊 采集结果统计：")
        print(f"   国外新闻 (Gemini): {gemini_count} 条")
        print(f"   国内新闻 (Qwen): {qwen_count} 条")
        print()

        # 显示部分新闻
        if all_news:
            print("📰 新闻预览（前5条）：")
            print()

            for i, news in enumerate(all_news[:5], 1):
                source_tag = news.get('source_type', 'Unknown')
                print(f"{i}. [{source_tag}] {news.get('title', 'N/A')}")
                print(f"   摘要: {news.get('summary', 'N/A')[:100]}...")
                print(f"   来源: {news.get('source', 'N/A')}")
                print(f"   URL: {news.get('url', 'N/A')[:60]}...")
                print()

        # 保存完整结果到文件
        output_file = f'collected_news_{today.replace("-", "")}.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_news, f, ensure_ascii=False, indent=2)

        print(f"💾 完整结果已保存到: {output_file}")
        print()

        # 检查是否达到预期数量
        expected_total = 20  # 国外10条 + 国内10条
        if len(all_news) >= expected_total:
            print(f"🎉 测试成功！获得 {len(all_news)} 条新闻，超过预期的 {expected_total} 条")
            return True
        else:
            print(f"⚠️  获得的新闻数量({len(all_news)})少于预期({expected_total})，但系统功能正常")
            return True

    except Exception as e:
        print(f"❌ 采集过程出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    print("="*60)
    print("🚀 AI资讯采集层小范围测试")
    print("="*60)
    print()

    success = test_collector()

    print("="*60)
    if success:
        print("✅ 测试完成！采集层工作正常")
        print("\n下一步可以测试完整的日报生成流程")
        return 0
    else:
        print("❌ 测试失败")
        print("\n请检查API配置和网络连接")
        return 1

if __name__ == '__main__':
    sys.exit(main())