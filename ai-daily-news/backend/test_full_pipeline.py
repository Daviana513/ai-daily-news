#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整三层流程测试
测试采集→消化→说人话的完整日报生成流程
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

def test_full_pipeline():
    """测试完整的三层处理流程"""
    print("🔄 开始完整三层流程测试...")
    print("目标：采集→消化→说人话，生成最终日报")
    print()

    try:
        # 导入处理器
        from collectors.unified_collector import UnifiedCollector
        from processors.unified_processor import UnifiedDigester, UnifiedTranslator

        print("✅ 处理器导入成功")

        # 初始化处理器
        collector = UnifiedCollector()
        digester = UnifiedDigester()
        translator = UnifiedTranslator()

        print("✅ 处理器初始化成功")
        print()

        # 第一步：采集
        today = datetime.now().strftime('%Y-%m-%d')
        print(f"📅 第一步：采集层（{today}）")
        raw_news = collector.collect_daily_news(today)
        print(f"✅ 采集完成：{len(raw_news)} 条原始新闻")
        print()

        # 第二步：消化
        print("📊 第二步：消化层（筛选Top5+结构化）")
        digested_news = digester.digest_news(raw_news, today)
        print(f"✅ 消化完成")
        print(f"   - Top5新闻: {len(digested_news.get('top5', []))} 条")
        print(f"   - 延伸阅读: {len(digested_news.get('further_reading', []))} 条")
        print(f"   - 洞察: {len(digested_news.get('insight', {}))} 项")
        print()

        # 第三步：说人话
        print("💬 第三步：说人话层（通俗化改写）")
        final_news = translator.translate_to_plain_language(digested_news)
        print(f"✅ 说人话完成")
        print()

        # 显示结果
        print("📋 最终日报预览：")
        print("="*60)

        # 显示Top5
        top5 = final_news.get('top5', [])
        print(f"🔥 今日Top5：")
        for i, news in enumerate(top5, 1):
            print(f"{i}. {news.get('title', 'N/A')}")
            print(f"   摘要: {news.get('summary', 'N/A')}")
            print(f"   为什么重要: {news.get('why_important', 'N/A')}")
            print()

        # 显示洞察
        insight = final_news.get('insight', {})
        if insight:
            print(f"📈 趋势: {insight.get('trend', 'N/A')}")
            print(f"⚠️  风险: {insight.get('risk', 'N/A')}")
            print()

        # 保存结果
        output_file = f'final_daily_news_{today.replace("-", "")}.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(final_news, f, ensure_ascii=False, indent=2)

        print(f"💾 完整日报已保存到: {output_file}")
        print()

        print("="*60)
        print("🎉 完整三层流程测试成功！")
        print(f"✓ 采集: {len(raw_news)} 条原始新闻")
        print(f"✓ 消化: Top{len(top5)} + {len(digested_news.get('further_reading', []))} 条延伸阅读")
        print(f"✓ 说人话: 通俗化完成")

        return True

    except Exception as e:
        print(f"❌ 流程测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    print("="*60)
    print("🚀 AI资讯日报完整流程测试")
    print("="*60)
    print()

    success = test_full_pipeline()

    print()
    if success:
        print("✅ 系统就绪！可以开始生成真实的AI资讯日报")
        print("\n下一步：启动API服务器，通过前端界面使用")
        print("运行: python api.py")
        return 0
    else:
        print("❌ 测试失败，需要进一步调试")
        return 1

if __name__ == '__main__':
    sys.exit(main())