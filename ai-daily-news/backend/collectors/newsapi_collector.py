#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NewsAPI Collector - 采集层（混合架构）
使用NewsAPI获取真实AI新闻，解决URL和时效性问题
"""

import os
import requests
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class NewsAPICollector:
    """NewsAPI采集器：获取真实AI新闻"""

    def __init__(self, api_key=None):
        """
        初始化NewsAPI采集器

        Args:
            api_key: NewsAPI密钥，如果不提供则从环境变量读取
        """
        self.api_key = api_key or os.getenv('NEWSAPI_KEY', '5da59a3e57504c608618a86c77fc70de')
        self.base_url = "https://newsapi.org/v2/everything"
        logger.info("NewsAPI采集层初始化完成")

    def collect_daily_news(self, today: str = None) -> List[Dict[str, Any]]:
        """
        采集当日AI资讯

        Args:
            today: 当前日期，格式为 'YYYY-MM-DD'，默认为今天

        Returns:
            包含原始新闻条目的列表
        """
        try:
            if not today:
                today = datetime.now().strftime('%Y-%m-%d')

            logger.info(f"开始使用NewsAPI采集 {today} 的AI资讯...")

            # 并行采集国内外新闻
            int_news = self._collect_international_news(10)
            dom_news = self._collect_domestic_news(10)

            # 合并结果
            all_news = int_news + dom_news

            logger.info(f"NewsAPI采集完成：国际{len(int_news)}条 + 国内{len(dom_news)}条 = 总计{len(all_news)}条")

            return all_news

        except Exception as e:
            logger.error(f"NewsAPI采集层发生错误: {str(e)}")
            raise

    def _collect_international_news(self, limit: int = 10) -> List[Dict[str, Any]]:
        """采集国际AI新闻"""
        try:
            params = {
                'q': '(ChatGPT OR "OpenAI" OR "GPT-4" OR "GPT-5" OR Claude OR Gemini OR Llama OR "generative AI" OR "large language model") AND (launch OR release OR update OR breakthrough OR announce)',
                'language': 'en',
                'sortBy': 'publishedAt',
                'pageSize': limit,
                'apiKey': self.api_key
            }

            response = requests.get(self.base_url, params=params, timeout=30)

            if response.status_code == 200:
                data = response.json()
                articles = data.get('articles', [])

                news_list = []
                for i, article in enumerate(articles, 1):
                    news_list.append({
                        'id': i,
                        'title': article.get('title', ''),
                        'summary': article.get('description', ''),
                        'source': article.get('source', {}).get('name', ''),
                        'url': article.get('url', ''),
                        'published_at': article.get('publishedAt', ''),
                        'source_type': 'International-NewsAPI'
                    })

                return news_list
            else:
                logger.error(f"国际新闻采集失败: {response.status_code}")
                return []

        except Exception as e:
            logger.error(f"国际新闻采集异常: {str(e)}")
            return []

    def _collect_domestic_news(self, limit: int = 10) -> List[Dict[str, Any]]:
        """采集国内AI新闻"""
        try:
            params = {
                'q': '("ChatGPT" OR "OpenAI" OR "GPT-4" OR "大模型" OR "通义千问" OR "文心一言" OR "豆包" OR "Kimi" OR "生成式AI" OR "多模态AI") AND (发布 OR 升级 OR 更新 OR 突破 OR 推出 OR 发布会)',
                'language': 'zh',
                'sortBy': 'publishedAt',
                'pageSize': limit,
                'apiKey': self.api_key
            }

            response = requests.get(self.base_url, params=params, timeout=30)

            if response.status_code == 200:
                data = response.json()
                articles = data.get('articles', [])

                news_list = []
                for i, article in enumerate(articles, 1):
                    news_list.append({
                        'id': i,
                        'title': article.get('title', ''),
                        'summary': article.get('description', ''),
                        'source': article.get('source', {}).get('name', ''),
                        'url': article.get('url', ''),
                        'published_at': article.get('publishedAt', ''),
                        'source_type': 'Domestic-NewsAPI'
                    })

                return news_list
            else:
                logger.error(f"国内新闻采集失败: {response.status_code}")
                return []

        except Exception as e:
            logger.error(f"国内新闻采集异常: {str(e)}")
            return []