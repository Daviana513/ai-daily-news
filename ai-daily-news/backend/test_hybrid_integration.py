#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速测试：验证混合架构是否正常工作
"""

import sys
import os
sys.path.append('.')

# 设置控制台编码
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def test_hybrid_architecture():
    """测试混合架构"""
    print("🔍 测试混合架构集成")
    print("="*60)

    try:
        # 测试1: 导入NewsAPICollector
        print("📦 测试1: 导入NewsAPICollector...")
        from collectors.newsapi_collector import NewsAPICollector
        print("✅ NewsAPICollector导入成功")

        # 测试2: 初始化采集器
        print("\n📦 测试2: 初始化NewsAPICollector...")
        collector = NewsAPICollector()
        print("✅ NewsAPICollector初始化成功")

        # 测试3: 采集新闻（小规模）
        print("\n📦 测试3: 采集新闻（各2条）...")
        int_news = collector._collect_international_news(2)
        dom_news = collector._collect_domestic_news(2)

        print(f"✅ 国际新闻: {len(int_news)} 条")
        print(f"✅ 国内新闻: {len(dom_news)} 条")

        # 显示新闻预览
        print("\n📰 新闻预览:")
        for i, news in enumerate(int_news + dom_news, 1):
            print(f"{i}. {news['title'][:50]}...")
            print(f"   来源: {news['source']}")

        print(f"\n📊 总计: {len(int_news) + len(dom_news)} 条真实新闻")

        # 测试4: 导入处理器
        print("\n📦 测试4: 导入处理器...")
        from processors.unified_processor import UnifiedDigester, UnifiedTranslator
        print("✅ 处理器导入成功")

        # 测试5: 初始化处理器
        print("\n📦 测试5: 初始化处理器...")
        digester = UnifiedDigester()
        translator = UnifiedTranslator()
        print("✅ 处理器初始化成功")

        print("\n" + "="*60)
        print("🎉 集成测试成功！")
        print("="*60)
        print("✅ 所有组件都能正常导入和初始化")
        print("✅ NewsAPI可以正常采集真实新闻")
        print("✅ 混合架构可以正常工作")

        return True

    except ImportError as e:
        print(f"❌ 导入错误: {str(e)}")
        print("请检查文件路径和依赖是否正确")
        return False

    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    success = test_hybrid_architecture()

    if success:
        print("\n💡 系统已准备好，可以启动API服务器")
        print("运行: python api.py")
    else:
        print("\n⚠️  请检查问题后再启动服务器")

    return 0 if success else 1

if __name__ == '__main__':
    sys.exit(main())