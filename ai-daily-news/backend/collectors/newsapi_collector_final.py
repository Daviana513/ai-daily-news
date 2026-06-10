#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终优化的NewsAPI采集器
基于测试结果的最佳关键词配置
"""

import requests
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any

class FinalNewsAPICollector:
    """最终优化的NewsAPI采集器"""

    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://newsapi.org/v2/everything"

    def collect_international_ai_news(self, limit=10, days_back=1):
        """
        采集国际AI新闻

        Args:
            limit: 新闻条数
            days_back: 回溯天数
        """
        params = {
            # 基于测试结果优化的关键词
            'q': '(ChatGPT OR "GPT-4" OR "GPT-5" OR Claude OR Gemini OR Llama OR "generative AI" OR "large language model" OR "multimodal AI") AND (launch OR release OR update OR breakthrough OR announce OR unveil)',
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

                return news_list
            else:
                print(f"❌ 国际新闻采集失败: {response.status_code}")
                return []

        except Exception as e:
            print(f"❌ 国际新闻采集异常: {str(e)}")
            return []

    def collect_domestic_ai_news(self, limit=10, days_back=1):
        """
        采集国内AI新闻

        Args:
            limit: 新闻条数
            days_back: 回溯天数
        """
        params = {
            # 基于测试结果优化的关键词
            'q': '("ChatGPT" OR "OpenAI" OR "GPT-4" OR "大模型" OR "通义千问" OR "文心一言" OR "豆包" OR "Kimi" OR "生成式AI" OR "多模态AI") AND (发布 OR 升级 OR 更新 OR 突破 OR 推出 OR 发布会)',
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

                return news_list
            else:
                print(f"❌ 国内新闻采集失败: {response.status_code}")
                return []

        except Exception as e:
            print(f"❌ 国内新闻采集异常: {str(e)}")
            return []

    def collect_all_ai_news(self, international_limit=10, domestic_limit=10):
        """采集所有AI新闻"""
        print("📡 使用优化后的NewsAPI采集AI新闻")

        international_news = self.collect_international_ai_news(international_limit)
        domestic_news = self.collect_domestic_ai_news(domestic_limit)

        all_news = international_news + domestic_news

        print(f"✅ 采集完成: 国际{len(international_news)}条 + 国内{len(domestic_news)}条 = 总计{len(all_news)}条")

        return all_news

# 使用示例
"""
api_key = "4032bc55beef4064bacfcfc46b1f1479"
collector = FinalNewsAPICollector(api_key)

# 采集今日AI新闻
news = collector.collect_all_ai_news(international_limit=10, domestic_limit=10)

# 查看结果
for item in news:
    print(f"{item['title']}")
    print(f"来源: {item['source']}")
    print(f"URL: {item['url']}")
    print()
"""