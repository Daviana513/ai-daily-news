#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
豆包API测试脚本
专门测试豆包1.6 API连接
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

def test_doubao_api():
    """测试豆包API（ARK）"""
    print("🧪 测试 豆包1.6 API（ARK）...")

    api_key = os.getenv('DOUBAO_API_KEY')

    if not api_key:
        print("❌ 缺少 DOUBAO_API_KEY")
        return False

    # 尝试不同的endpoint格式
    endpoints = [
        "https://ark.cn-beijing.volces.com/api/v3/chat/completions",
        "https://ark.cn-beijing.volces.com/api/v4/chat/completions",
        "https://ark.cn-beijing.volces.com/v3/chat/completions"
    ]

    for endpoint in endpoints:
        try:
            print(f"尝试endpoint: {endpoint}")
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {api_key}'
            }

            data = {
                'model': 'doubao-pro-1.6',  # 使用1.6版本
                'messages': [{'role': 'user', 'content': '你好，请简单介绍一下你自己。'}],
                'max_tokens': 100
            }

            response = requests.post(endpoint, headers=headers, json=data, timeout=30)

            if response.status_code == 200:
                result = response.json()
                message = result['choices'][0]['message']['content']
                print(f"✅ 豆包API 工作正常！")
                print(f"   使用的endpoint: {endpoint}")
                print(f"   响应: {message[:50]}...")

                # 保存正确的endpoint到环境变量
                with open('.env', 'a') as f:
                    f.write(f"\n# 正确的endpoint\nDOUBAO_API_ENDPOINT={endpoint}\n")

                return True
            else:
                print(f"   状态码: {response.status_code}")

        except Exception as e:
            print(f"   错误: {str(e)}")
            continue

    print("❌ 所有endpoint都失败")
    print("请检查API密钥是否正确，或联系API提供商确认正确的endpoint格式")
    return False

def main():
    """运行测试"""
    print("🚀 开始测试豆包API配置...\n")

    doubao_ok = test_doubao_api()

    print("\n" + "="*50)
    if doubao_ok:
        print("🎉 豆包API配置正确！系统可以正常使用。")
        return 0
    else:
        print("⚠️  豆包API配置有问题，请检查:")
        print("   - DOUBAO_API_KEY 是否正确")
        print("   - API密钥是否有效")
        print("   - 网络连接是否正常")
        return 1

if __name__ == '__main__':
    sys.exit(main())