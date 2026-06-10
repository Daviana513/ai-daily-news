#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试修复SSL连接问题
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

def test_with_ssl_fix():
    """测试修复SSL后的连接"""

    api_key = os.getenv('LAOZHAI_API_KEY')
    base_url = os.getenv('LAOZHAI_BASE_URL')
    model = os.getenv('PROCESSOR_MODEL', 'qwen-plus')

    print(f"API Key: {api_key[:10] if api_key else 'None'}...")
    print(f"Base URL: {base_url}")
    print(f"Model: {model}")

    if not api_key or not base_url:
        print("缺少API配置!")
        return False

    try:
        api_url = f"{base_url}/chat/completions"
        print(f"测试URL: {api_url}")

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

        # 尝试不同的SSL配置
        ssl_configs = [
            ("默认SSL配置", {}),
            ("禁用SSL验证", {"verify": False}),
            ("使用TLSv1.2", {"verify": False, "ssl_version": "TLSv1_2"}),
        ]

        for config_name, ssl_kwargs in ssl_configs:
            print(f"\n尝试配置: {config_name}")
            try:
                response = requests.post(
                    api_url,
                    headers=headers,
                    json=data,
                    timeout=30,
                    **ssl_kwargs
                )

                if response.status_code == 200:
                    result = response.json()
                    message = result['choices'][0]['message']['content']
                    print(f"[成功] {config_name}!")
                    print(f"模型回复: {message}")
                    return config_name, ssl_kwargs
                else:
                    print(f"[失败] 状态码: {response.status_code}")
                    print(f"响应: {response.text[:200]}")

            except Exception as e:
                print(f"[失败] {config_name}: {str(e)}")

        print("\n所有SSL配置都失败了!")
        return False

    except Exception as e:
        print(f"测试异常: {str(e)}")
        return False

if __name__ == "__main__":
    result = test_with_ssl_fix()
    if result:
        config_name, ssl_kwargs = result
        print(f"\n推荐使用: {config_name}")
        print(f"SSL配置: {ssl_kwargs}")
    else:
        print("\n需要进一步调查网络问题")