#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
豆包API endpoint探测脚本
尝试多种可能的endpoint格式
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

def test_endpoints():
    """测试各种可能的endpoint格式"""
    api_key = os.getenv('DOUBAO_API_KEY')

    if not api_key:
        print("❌ 缺少 DOUBAO_API_KEY")
        return False

    print("🔍 开始探测豆包API endpoint...")
    print(f"API密钥: {api_key[:20]}...")

    # 定义各种可能的endpoint格式
    endpoints = [
        # 火山引擎ARK可能的格式
        "https://ark.cn-beijing.volces.com/api/v3/chat/completions",
        "https://ark.cn-beijing.volces.com/api/v4/chat/completions",
        "https://ark.cn-beijing.volces.com/v3/chat/completions",
        "https://ark.cn-beijing.volces.com/v4/chat/completions",

        # 其他可能的域名
        "https://api.volcengine.com/api/v3/chat/completions",
        "https://api.volcengine.com/v3/chat/completions",

        # 豆包可能的endpoint
        "https://doubao-api.volces.com/v3/chat/completions",
        "https://doubao.volces.com/api/v3/chat/completions",
        "https://ark.cn-beijing.volccr.com/api/v3/chat/completions",

        # OpenAI兼容格式
        "https://api.volces.com/v1/chat/completions",
        "https://openai.volces.com/v1/chat/completions"
    ]

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    data = {
        'model': 'doubao-pro-1.6',
        'messages': [{'role': 'user', 'content': '你好'}],
        'max_tokens': 50
    }

    for endpoint in endpoints:
        try:
            print(f"测试: {endpoint}")
            response = requests.post(endpoint, headers=headers, json=data, timeout=10)

            if response.status_code == 200:
                print(f"✅ 成功！正确的endpoint: {endpoint}")
                result = response.json()
                print(f"响应: {result.get('choices', [{}])[0].get('message', {}).get('content', 'N/A')[:50]}...")

                # 保存到环境变量
                with open('.env', 'a') as f:
                    f.write(f"\n# 正确的豆包endpoint\nDOUBAO_API_ENDPOINT={endpoint}\n")

                return endpoint

            elif response.status_code == 401:
                print(f"   ❌ 401 未授权 - API密钥可能无效")
                return None

            elif response.status_code == 404:
                print(f"   ❌ 404 Not Found")

            else:
                print(f"   ❌ 状态码: {response.status_code}")

        except requests.exceptions.ConnectionError:
            print(f"   ❌ 连接失败")
        except Exception as e:
            print(f"   ❌ 错误: {str(e)}")

    print("\n❌ 所有endpoint都失败")
    print("\n可能的原因:")
    print("1. API密钥格式不正确")
    print("2. API服务域名已更改")
    print("3. 需要特殊的请求头或认证方式")
    print("4. 网络连接问题")

    return None

def main():
    endpoint = test_endpoints()

    print("\n" + "="*60)
    if endpoint:
        print("🎉 找到正确的endpoint！")
        print(f"请在.env文件中设置: DOUBAO_API_ENDPOINT={endpoint}")
        return 0
    else:
        print("⚠️  未能找到正确的endpoint")
        print("建议:")
        print("1. 检查API密钥是否正确且有效")
        print("2. 联系豆包/火山引擎技术支持确认正确的API地址")
        print("3. 查看官方文档获取最新的endpoint信息")
        return 1

if __name__ == '__main__':
    sys.exit(main())