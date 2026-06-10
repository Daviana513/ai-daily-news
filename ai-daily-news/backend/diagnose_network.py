#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网络诊断脚本 - 检查可能导致"网络请求失败"的原因
"""

import os
import requests
import json
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_newsapi_connection():
    """测试NewsAPI连接"""
    print("\n=== 测试 NewsAPI 连接 ===")

    api_key = '4032bc55beef4064bacfcfc46b1f1479'
    base_url = "https://newsapi.org/v2/everything"

    try:
        params = {
            'q': 'ChatGPT',
            'language': 'en',
            'pageSize': 1,
            'apiKey': api_key
        }

        print(f"请求URL: {base_url}")
        print(f"API Key: {api_key[:10]}...")

        response = requests.get(base_url, params=params, timeout=30)

        print(f"状态码: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"✅ NewsAPI连接成功!")
            print(f"返回文章数量: {len(data.get('articles', []))}")
            return True
        else:
            print(f"❌ NewsAPI请求失败!")
            print(f"响应内容: {response.text[:200]}")
            return False

    except requests.exceptions.Timeout:
        print("❌ NewsAPI连接超时!")
        return False
    except requests.exceptions.ConnectionError as e:
        print(f"❌ NewsAPI连接错误: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ NewsAPI测试异常: {str(e)}")
        return False

def test_laozhang_api_connection():
    """测试老张代理API连接"""
    print("\n=== 测试老张代理API连接 ===")

    api_key = os.getenv('LAOZHAI_API_KEY')
    base_url = os.getenv('LAOZHAI_BASE_URL')
    model = os.getenv('PROCESSOR_MODEL', 'qwen-plus')

    print(f"API Key: {api_key[:10]}... 如果存在的话")
    print(f"Base URL: {base_url}")
    print(f"模型: {model}")

    if not api_key or not base_url:
        print("❌ 缺少API配置!")
        return False

    try:
        api_url = f"{base_url}/chat/completions"
        print(f"请求URL: {api_url}")

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        }

        data = {
            'model': model,
            'messages': [{'role': 'user', 'content': '你好，请回复"连接成功"'}],
            'temperature': 0.3,
            'max_tokens': 50
        }

        print("发送测试请求...")
        response = requests.post(api_url, headers=headers, json=data, timeout=30)

        print(f"状态码: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            message = result['choices'][0]['message']['content']
            print(f"✅ 老张代理API连接成功!")
            print(f"模型回复: {message}")
            return True
        else:
            print(f"❌ 老张代理API请求失败!")
            print(f"响应内容: {response.text[:200]}")
            return False

    except requests.exceptions.Timeout:
        print("❌ 老张代理API连接超时!")
        return False
    except requests.exceptions.ConnectionError as e:
        print(f"❌ 老张代理API连接错误: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ 老张代理API测试异常: {str(e)}")
        return False

def test_general_network():
    """测试通用网络连接"""
    print("\n=== 测试通用网络连接 ===")

    test_urls = [
        ("Google", "https://www.google.com"),
        ("百度", "https://www.baidu.com"),
        ("GitHub", "https://api.github.com")
    ]

    for name, url in test_urls:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print(f"✅ {name} 连接正常")
            else:
                print(f"⚠️ {name} 连接异常 (状态码: {response.status_code})")
        except Exception as e:
            print(f"❌ {name} 连接失败: {str(e)}")

def check_env_config():
    """检查环境配置"""
    print("\n=== 检查环境配置 ===")

    required_vars = [
        'LAOZHAI_API_KEY',
        'LAOZHAI_BASE_URL',
        'PROCESSOR_MODEL'
    ]

    for var in required_vars:
        value = os.getenv(var)
        if value:
            if 'API_KEY' in var or 'KEY' in var:
                print(f"✅ {var}: {value[:10]}... (已配置)")
            else:
                print(f"✅ {var}: {value}")
        else:
            print(f"❌ {var}: 未配置")

if __name__ == "__main__":
    print("=" * 50)
    print("AI Daily News 网络诊断工具")
    print("=" * 50)

    # 检查配置
    check_env_config()

    # 测试网络
    test_general_network()

    # 测试NewsAPI
    newsapi_ok = test_newsapi_connection()

    # 测试老张代理API
    laozhang_ok = test_laozhang_api_connection()

    # 总结
    print("\n" + "=" * 50)
    print("诊断结果总结")
    print("=" * 50)

    if newsapi_ok and laozhang_ok:
        print("✅ 所有连接正常，问题可能在代码逻辑")
    elif newsapi_ok and not laozhang_ok:
        print("❌ 老张代理API连接失败，请检查API密钥和网络")
    elif not newsapi_ok and laozhang_ok:
        print("❌ NewsAPI连接失败，可能是API密钥问题")
    else:
        print("❌ 所有API连接失败，请检查网络连接")

    print("\n建议修复措施：")
    if not newsapi_ok:
        print("- 检查NewsAPI密钥是否有效")
        print("- 确认网络可以访问 newsapi.org")

    if not laozhang_ok:
        print("- 检查老张代理API密钥是否正确")
        print("- 确认网络可以访问 api.laozhang.ai")
        print("- 检查API账户是否有余额")