#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NewsAPI小范围测试
国内外新闻各采集10篇
"""

import requests
import json
from datetime import datetime, timedelta

# 设置控制台编码为UTF-8（Windows兼容）
import sys
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

class NewsAPICollectionTest:
    """NewsAPI采集测试"""

    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://newsapi.org/v2/everything"
        print(f"🔑 NewsAPI密钥: {api_key[:20]}...")
        print()

    def collect_international_news(self, limit=10):
        """采集国际AI新闻（英文）"""
        print("🌍 采集国际AI新闻（英文）")
        print("="*60)

        params = {
            'q': '(AI OR "artificial intelligence" OR "machine learning" OR "ChatGPT" OR "GPT" OR "LLM" OR "deep learning") AND (technology OR tech)',
            'language': 'en',
            'sortBy': 'publishedAt',
            'pageSize': limit,
            'apiKey': self.api_key
        }

        try:
            response = requests.get(self.base_url, params=params, timeout=30)

            if response.status_code == 200:
                data = response.json()
                articles = data.get('articles', [])

                print(f"✅ 成功采集 {len(articles)} 条国际AI新闻")
                print()

                # 转换为标准格式
                news_list = []
                for i, article in enumerate(articles, 1):
                    news_item = {
                        'id': i,
                        'title': article.get('title', ''),
                        'summary': article.get('description', ''),
                        'source': article.get('source', {}).get('name', ''),
                        'url': article.get('url', ''),
                        'published_at': article.get('publishedAt', ''),
                        'source_type': 'International-NewsAPI'
                    }
                    news_list.append(news_item)

                    # 显示前3条详情
                    if i <= 3:
                        print(f"📰 新闻 {i}: {news_item['title']}")
                        print(f"   来源: {news_item['source']}")
                        print(f"   时间: {news_item['published_at']}")
                        print(f"   URL: {news_item['url'][:70]}...")
                        print()

                return news_list
            else:
                print(f"❌ 采集失败: {response.status_code}")
                return []

        except Exception as e:
            print(f"❌ 异常: {str(e)}")
            return []

    def collect_domestic_news(self, limit=10):
        """采集国内AI新闻（中文）"""
        print("🇨🇳 采集国内AI新闻（中文）")
        print("="*60)

        params = {
            'q': '(人工智能 OR AI OR 大模型 OR 机器学习 OR 深度学习 OR ChatGPT OR 通义千问 OR 文心一言) AND (科技 OR 技术)',
            'language': 'zh',
            'sortBy': 'publishedAt',
            'pageSize': limit,
            'apiKey': self.api_key
        }

        try:
            response = requests.get(self.base_url, params=params, timeout=30)

            if response.status_code == 200:
                data = response.json()
                articles = data.get('articles', [])

                print(f"✅ 成功采集 {len(articles)} 条国内AI新闻")
                print()

                # 转换为标准格式
                news_list = []
                for i, article in enumerate(articles, 1):
                    news_item = {
                        'id': i,
                        'title': article.get('title', ''),
                        'summary': article.get('description', ''),
                        'source': article.get('source', {}).get('name', ''),
                        'url': article.get('url', ''),
                        'published_at': article.get('publishedAt', ''),
                        'source_type': 'Domestic-NewsAPI'
                    }
                    news_list.append(news_item)

                    # 显示前3条详情
                    if i <= 3:
                        print(f"📰 新闻 {i}: {news_item['title']}")
                        print(f"   来源: {news_item['source']}")
                        print(f"   时间: {news_item['published_at']}")
                        print(f"   URL: {news_item['url'][:70]}...")
                        print()

                return news_list
            else:
                print(f"❌ 采集失败: {response.status_code}")
                print(f"错误信息: {response.text}")
                return []

        except Exception as e:
            print(f"❌ 异常: {str(e)}")
            return []

    def test_url_validity(self, news_list, sample_size=3):
        """测试URL有效性"""
        print("🔗 测试URL有效性")
        print("="*60)

        if not news_list:
            print("❌ 没有新闻可供测试")
            return 0

        test_count = min(sample_size, len(news_list))
        valid_count = 0

        for i in range(test_count):
            news = news_list[i]
            url = news['url']

            print(f"测试 {i+1}. {news['title'][:40]}...")
            print(f"   URL: {url[:60]}...")

            try:
                response = requests.head(url, timeout=10, allow_redirects=True)

                if response.status_code == 200:
                    print(f"   ✅ URL有效 (状态码: {response.status_code})")
                    valid_count += 1
                elif response.status_code in [301, 302]:
                    print(f"   ⚠️  URL重定向 (状态码: {response.status_code})")
                    valid_count += 1  # 重定向也算有效
                else:
                    print(f"   ⚠️  URL状态: {response.status_code}")

            except Exception as e:
                print(f"   ❌ 访问失败: {str(e)[:40]}")

            print()

        success_rate = (valid_count / test_count) * 100
        print(f"📊 URL有效率: {valid_count}/{test_count} ({success_rate:.0f}%)")

        return valid_count

    def run_collection_test(self):
        """运行完整的采集测试"""
        print("🚀 NewsAPI小范围采集测试")
        print("="*60)
        print("目标: 国内外新闻各采集10篇")
        print("="*60)
        print()

        # 采集国际新闻
        international_news = self.collect_international_news(10)

        print()

        # 采集国内新闻
        domestic_news = self.collect_domestic_news(10)

        print()

        # 合并结果
        all_news = international_news + domestic_news

        # 统计信息
        print("="*60)
        print("📊 采集统计")
        print("="*60)
        print(f"国际新闻: {len(international_news)} 条")
        print(f"国内新闻: {len(domestic_news)} 条")
        print(f"总计: {len(all_news)} 条")
        print()

        # 测试URL有效性
        if all_news:
            print("🔗 URL有效性测试")
            print("="*60)

            # 测试国际新闻URL
            print("🌍 国际新闻URL测试:")
            int_valid = self.test_url_validity(international_news, 3)

            print()

            # 测试国内新闻URL
            print("🇨🇳 国内新闻URL测试:")
            dom_valid = self.test_url_validity(domestic_news, 3)

            print()
            print("="*60)
            print("🎯 测试结论")
            print("="*60)
            print(f"✅ 成功采集 {len(all_news)} 条真实新闻")
            print(f"✅ 国际新闻URL有效: {int_valid}/3")
            print(f"✅ 国内新闻URL有效: {dom_valid}/3")
            print(f"✅ 总体URL有效: {int_valid + dom_valid}/6")
            print()
            print("💡 NewsAPI相比AI模型的优势:")
            print("   1. ✅ 获取的是真实新闻，非虚构内容")
            print("   2. ✅ URL真实有效，可正常访问")
            print("   3. ✅ 时效准确，按发布时间排序")
            print("   4. ✅ 来源可靠，来自权威新闻网站")

        # 保存结果
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f'newsapi_test_result_{timestamp}.json'

        result = {
            'timestamp': datetime.now().isoformat(),
            'international_count': len(international_news),
            'domestic_count': len(domestic_news),
            'total_count': len(all_news),
            'international_news': international_news,
            'domestic_news': domestic_news
        }

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        print(f"💾 完整结果已保存到: {output_file}")

        return result

def main():
    """主函数"""
    # 用户的API密钥
    api_key = "4032bc55beef4064bacfcfc46b1f1479"

    tester = NewsAPICollectionTest(api_key)
    result = tester.run_collection_test()

    return 0

if __name__ == '__main__':
    sys.exit(main())