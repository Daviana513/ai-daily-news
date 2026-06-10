#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最小化测试：使用最简单的请求测试老张API
"""
import sys
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import os
import requests
from dotenv import load_dotenv

load_dotenv()

print("🔍 最小化API测试")
print("="*60)

api_key = os.getenv('LAOZHAI_API_KEY')
base_url = os.getenv('LAOZHAI_BASE_URL')
api_url = f"{base_url}/chat/completions"

print(f"API Key: {api_key[:20]}...")
print(f"API URL: {api_url}")

# 测试1: 极简请求
print("\n测试1: 极简请求（10个token）...")
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {api_key}'
}

data = {
    'model': 'qwen-plus',
    'messages': [{'role': 'user', 'content': 'Hi'}],
    'max_tokens': 10
}

try:
    response = requests.post(api_url, headers=headers, json=data, timeout=120)
    print(f"✅ 成功: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"响应: {result['choices'][0]['message']['content']}")
except Exception as e:
    print(f"❌ 失败: {str(e)}")

# 测试2: 稍长请求
print("\n测试2: 稍长请求（JSON输出）...")
data = {
    'model': 'qwen-plus',
    'messages': [{'role': 'user', 'content': '输出JSON: {"test": "ok"}'}],
    'max_tokens': 50
}

try:
    response = requests.post(api_url, headers=headers, json=data, timeout=120)
    print(f"✅ 成功: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"响应: {result['choices'][0]['message']['content']}")
except Exception as e:
    print(f"❌ 失败: {str(e)}")

print("\n" + "="*60)
print("测试完成")
