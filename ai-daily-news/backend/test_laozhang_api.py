#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
老张代理API测试脚本
测试所有模型配置是否正常工作
"""

import os
import sys
import requests
import json
from dotenv import load_dotenv

# 设置控制台编码为UTF-8（Windows兼容）
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 加载环境变量
load_dotenv()

def test_laozhang_api():
    """测试老张代理API的所有模型"""
    print("🧪 测试老张代理API配置...")

    api_key = os.getenv('LAOZHAI_API_KEY')
    base_url = os.getenv('LAOZHAI_BASE_URL')

    if not api_key or not base_url:
        print("❌ 缺少API配置")
        return False

    print(f"API Key: {api_key[:20]}...")
    print(f"Base URL: {base_url}")
    print()

    # 需要测试的模型
    models = [
        {
            "name": "采集层 - 国外新闻 (Gemini)",
            "model": "gemini-2.5-flash-thinking",
            "prompt": "请简单介绍一下你自己。"
        },
        {
            "name": "采集层 - 国内新闻 (Qwen)",
            "model": "qwen3-30b-a3b-thinking-2507",
            "prompt": "请简单介绍一下你自己。"
        },
        {
            "name": "处理层 - 消化和说人话 (Qwen Plus)",
            "model": "qwen-plus",
            "prompt": "请简单介绍一下你自己。"
        }
    ]

    endpoint = f"{base_url}/chat/completions"
    all_success = True

    for model_config in models:
        try:
            print(f"测试: {model_config['name']}")
            print(f"   模型: {model_config['model']}")

            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {api_key}'
            }

            data = {
                'model': model_config['model'],
                'messages': [{'role': 'user', 'content': model_config['prompt']}],
                'max_tokens': 100
            }

            response = requests.post(endpoint, headers=headers, json=data, timeout=30)
            print(f"   状态码: {response.status_code}")

            if response.status_code == 200:
                result = response.json()
                message = result['choices'][0]['message']['content']
                print(f"✅ 成功！")
                print(f"   响应: {message[:80]}...")
                print()

            elif response.status_code == 401:
                print(f"❌ 认证失败 - API密钥可能无效")
                all_success = False
                print()

            else:
                print(f"❌ 状态码: {response.status_code}")
                try:
                    error_detail = response.json()
                    print(f"   错误详情: {json.dumps(error_detail, ensure_ascii=False)[:200]}")
                except:
                    print(f"   响应内容: {response.text[:200]}")
                all_success = False
                print()

        except Exception as e:
            print(f"❌ 异常: {str(e)}")
            all_success = False
            print()

    return all_success

def main():
    """运行API测试"""
    print("🚀 老张代理API测试\n")

    success = test_laozhang_api()

    print("="*60)
    if success:
        print("🎉 所有模型测试成功！")
        print("\n配置正确，现在可以启动API服务器了！")
        print("运行: python api.py")
        return 0
    else:
        print("⚠️  部分模型测试失败")
        print("\n请检查:")
        print("1. API密钥是否正确且有效")
        print("2. 老张代理服务是否正常运行")
        print("3. 网络连接是否正常")
        print("4. 模型名称是否正确")
        return 1

if __name__ == '__main__':
    sys.exit(main())