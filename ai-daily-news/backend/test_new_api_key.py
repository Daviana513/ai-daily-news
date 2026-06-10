#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试新的NewsAPI密钥
"""

import requests
import json

def test_new_api_key():
    """测试新的API密钥"""
    api_key = '5da59a3e57504c608618a86c77fc70de'
    base_url = "https://newsapi.org/v2/everything"

    print("测试新的NewsAPI密钥...")
    print(f"API Key: {api_key[:10]}...")

    try:
        params = {
            'q': 'ChatGPT OR OpenAI',
            'language': 'en',
            'pageSize': 5,
            'apiKey': api_key
        }

        print("正在请求NewsAPI...")
        response = requests.get(base_url, params=params, timeout=30)

        print(f"状态码: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            articles = data.get('articles', [])
            print(f"成功! 获取到 {len(articles)} 条新闻")

            if articles:
                print("\n前3条新闻标题:")
                for i, article in enumerate(articles[:3], 1):
                    print(f"{i}. {article.get('title', 'N/A')}")

            return True
        else:
            print(f"失败! 状态码: {response.status_code}")
            print(f"响应内容: {response.text[:300]}")
            return False

    except requests.exceptions.Timeout:
        print("请求超时!")
        return False
    except requests.exceptions.ConnectionError as e:
        print(f"连接错误: {str(e)}")
        return False
    except Exception as e:
        print(f"异常: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_new_api_key()
    if success:
        print("\n[OK] NewsAPI密钥验证成功!")
    else:
        print("\n[FAIL] NewsAPI密钥验证失败!")