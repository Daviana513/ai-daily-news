#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
豆包API测试脚本 - 使用正确的模型名
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
    """测试豆包API（使用Doubao-Smart-Router模型）"""
    print("🧪 测试 豆包API（Doubao-Smart-Router）...")

    api_key = "ark-7ac4d5f3-13ad-4ec0-8ecb-72ca75b0adcf-9fa34"

    print(f"API密钥: {api_key[:20]}...")
    print("模型名: Doubao-Smart-Router")
    print()

    # 基于之前的测试，这个endpoint返回401（说明endpoint正确，但认证需要调整）
    endpoints = [
        "https://api.volcengine.com/api/v3/chat/completions",
        "https://ark.cn-beijing.volces.com/api/v3/chat/completions",
        "https://ark.cn-beijing.volces.com/v3/chat/completions"
    ]

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    data = {
        'model': 'Doubao-Smart-Router',  # 使用正确的模型名
        'messages': [{'role': 'user', 'content': '你好，请简单介绍一下你自己。'}],
        'max_tokens': 100
    }

    for endpoint in endpoints:
        try:
            print(f"测试endpoint: {endpoint}")
            response = requests.post(endpoint, headers=headers, json=data, timeout=30)
            print(f"状态码: {response.status_code}")

            if response.status_code == 200:
                result = response.json()
                message = result['choices'][0]['message']['content']
                print(f"✅ 豆包API 工作正常！")
                print(f"使用的endpoint: {endpoint}")
                print(f"响应: {message[:100]}...")

                # 更新.env文件
                with open('.env', 'w') as f:
                    f.write(f"# 豆包API配置\n")
                    f.write(f"DOUBAO_API_KEY={api_key}\n")
                    f.write(f"DOUBAO_API_ENDPOINT={endpoint}\n")
                    f.write(f"DOUBAO_MODEL=Doubao-Smart-Router\n")
                    f.write(f"\n# 服务器配置\n")
                    f.write(f"PORT=5000\n")
                    f.write(f"DEBUG=True\n")

                print(f"\n✅ 已更新.env文件配置")
                return True, endpoint

            elif response.status_code == 401:
                print(f"   401 认证失败 - 可能API密钥格式或权限有问题")
                # 尝试不同的认证格式
                print(f"   尝试不同的认证格式...")

                alt_headers = {
                    'Content-Type': 'application/json',
                    'Authorization': api_key  # 不加Bearer前缀
                }

                alt_response = requests.post(endpoint, headers=alt_headers, json=data, timeout=30)
                if alt_response.status_code == 200:
                    print(f"✅ 使用不带Bearer的认证成功！")
                    result = alt_response.json()
                    message = result['choices'][0]['message']['content']
                    print(f"响应: {message[:100]}...")

                    # 更新.env文件，注明不需要Bearer
                    with open('.env', 'w') as f:
                        f.write(f"# 豆包API配置\n")
                        f.write(f"DOUBAO_API_KEY={api_key}\n")
                        f.write(f"DOUBAO_API_ENDPOINT={endpoint}\n")
                        f.write(f"DOUBAO_MODEL=Doubao-Smart-Router\n")
                        f.write(f"DOUBAO_AUTH_TYPE=basic\n")
                        f.write(f"\n# 服务器配置\n")
                        f.write(f"PORT=5000\n")
                        f.write(f"DEBUG=True\n")

                    return True, endpoint

            elif response.status_code == 404:
                print(f"   404 Not Found")

            elif response.status_code == 400:
                print(f"   400 Bad Request - 可能是模型名或参数格式问题")
                error_detail = response.text
                print(f"   错误详情: {error_detail[:200]}")

        except Exception as e:
            print(f"   错误: {str(e)}")

        print()

    return False, None

def main():
    """运行测试"""
    print("🚀 开始测试豆包API配置...\n")

    success, endpoint = test_doubao_api()

    print("\n" + "="*60)
    if success:
        print("🎉 豆包API配置成功！")
        print(f"正确配置: endpoint={endpoint}")
        print("模型名: Doubao-Smart-Router")
        print("\n现在可以启动API服务器了！")
        return 0
    else:
        print("⚠️  豆包API连接失败")
        print("\n请检查:")
        print("1. API密钥是否正确且有效")
        print("2. 是否已开通豆包API服务权限")
        print("3. 账户余额是否充足")
        print("4. 网络连接是否正常")
        print("\n建议登录火山引擎控制台检查API密钥状态和服务权限")
        return 1

if __name__ == '__main__':
    sys.exit(main())