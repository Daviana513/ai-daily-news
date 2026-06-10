#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
URL验证工具
检查新闻URL是否真实可访问
"""

import requests
import json
from datetime import datetime

def validate_url(url):
    """验证单个URL是否可访问"""
    try:
        response = requests.head(url, timeout=5, allow_redirects=True)
        return response.status_code == 200
    except:
        return False

def validate_news_urls(news_file):
    """验证新闻文件中的所有URL"""
    with open(news_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"🔍 验证 {news_file} 中的URL...")
    print()

    # 验证Top5 URL
    top5 = data.get('top5', [])
    valid_count = 0
    invalid_urls = []

    for i, news in enumerate(top5, 1):
        url = news.get('source_url', '')
        print(f"{i}. {news.get('title', 'N/A')[:40]}...")
        print(f"   URL: {url}")

        if validate_url(url):
            print(f"   ✅ URL有效")
            valid_count += 1
        else:
            print(f"   ❌ URL无效或不可访问")
            invalid_urls.append({
                'title': news.get('title', ''),
                'url': url,
                'issue': 'URL不可访问'
            })
        print()

    # 验证延伸阅读URL
    further_reading = data.get('further_reading', [])
    further_valid = 0

    for item in further_reading:
        url = item.get('url', '')
        if validate_url(url):
            further_valid += 1

    # 生成报告
    print("="*60)
    print(f"📊 验证结果:")
    print(f"Top5 URL: {valid_count}/{len(top5)} 有效")
    print(f"延伸阅读URL: {further_valid}/{len(further_reading)} 有效")

    if invalid_urls:
        print(f"\n❌ 无效URL列表:")
        for item in invalid_urls:
            print(f"- {item['title'][:40]}...")
            print(f"  {item['url']}")

    return valid_count, len(top5), invalid_urls

if __name__ == '__main__':
    today = datetime.now().strftime('%Y-%m-%d')
    news_file = f'final_daily_news_{today.replace("-", "")}.json'

    try:
        validate_news_urls(news_file)
    except FileNotFoundError:
        print(f"❌ 找不到文件: {news_file}")
        print("请先生成日报，然后再验证URL")