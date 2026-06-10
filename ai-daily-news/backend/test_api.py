#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API密钥测试脚本
测试Gemini和Doubao API密钥是否正确配置
"""

import os
import sys
import requests
from dotenv import load_dotenv

# 设置控制台编码为UTF-8（Windows兼容）
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 加载环境变量
load_dotenv()

def test_gemini_api():
    """测试Gemini API（老张代理）"""
    print("🧪 测试 Gemini API（老张代理）...")

    api_key = os.getenv('GEMINI_API_KEY')
    api_base = os.getenv('GEMINI_API_BASE', 'https://www.laozhang.ai/v1')

    if not api_key:
        print("❌ 缺少 GEMINI_API_KEY")
        return False

    try:
        api_url = f"{api_base}/chat/completions"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        }

        data = {
            'model': 'gemini-pro',
            'messages': [{'role': 'user', 'content': '你好，请简单介绍一下你自己。'}],
            'max_tokens': 100
        }

        response = requests.post(api_url, headers=headers, json=data, timeout=30)
        response.raise_for_status()

        result = response.json()
        message = result['choices'][0]['message']['content']
        print(f"✅ Gemini API 工作正常")
        print(f"   响应: {message[:50]}...")
        return True

    except Exception as e:
        print(f"❌ Gemini API 测试失败: {str(e)}")
        return False

def test_doubao_api():
    """测试Doubao API（ARK）"""
    print("\n🧪 测试 Doubao API（ARK）...")

    api_key = os.getenv('ARK_API_KEY')
    api_base = os.getenv('ARK_API_BASE', 'https://ark.cn-beijing.volces.com/api/v3')

    if not api_key:
        print("❌ 缺少 ARK_API_KEY")
        return False

    try:
        api_url = f"{api_base}/chat/completions"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        }

        data = {
            'model': 'doubao-pro-1.8',
            'messages': [{'role': 'user', 'content': '你好，请简单介绍一下你自己。'}],
            'max_tokens': 100
        }

        response = requests.post(api_url, headers=headers, json=data, timeout=30)
        response.raise_for_status()

        result = response.json()
        message = result['choices'][0]['message']['content']
        print(f"✅ Doubao API 工作正常")
        print(f"   响应: {message[:50]}...")
        return True

    except Exception as e:
        print(f"❌ Doubao API 测试失败: {str(e)}")
        return False

def main():
    """运行所有测试"""
    print("🚀 开始测试API密钥配置...\n")

    gemini_ok = test_gemini_api()
    doubao_ok = test_doubao_api()

    print("\n" + "="*50)
    if gemini_ok and doubao_ok:
        print("🎉 所有API密钥配置正确！系统可以正常使用。")
        return 0
    else:
        print("⚠️  部分API密钥配置有问题，请检查:")
        if not gemini_ok:
            print("   - Gemini API（GEMINI_API_KEY）")
        if not doubao_ok:
            print("   - Doubao API（ARK_API_KEY）")
        print("\n请检查 .env 文件中的API密钥配置。")
        return 1

if __name__ == '__main__':
    sys.exit(main())