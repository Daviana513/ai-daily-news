#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
豆包API测试脚本 - 使用正确的模型名 Doubao-Seed-1.8
"""

import os
import sys
import requests
import json

# 设置控制台编码为UTF-8（Windows兼容）
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def test_doubao_api_final():
    """测试豆包API（使用Doubao-Seed-1.8模型）"""
    print("🧪 测试 豆包API（Doubao-Seed-1.8）...")

    api_key = "ark-7ac4d5f3-13ad-4ec0-8ecb-72ca75b0adcf-9fa34"
    model = "Doubao-Seed-1.8"

    print(f"API密钥: {api_key[:20]}...")
    print(f"模型: {model}")
    print()

    # 最可能的endpoint
    endpoints = [
        "https://api.volcengine.com/api/v3/chat/completions",
        "https://ark.cn-beijing.volces.com/api/v3/chat/completions",
        "https://ark.cn-beijing.volces.com/v3/chat/completions"
    ]

    # 测试不同的认证方式
    auth_methods = [
        {
            "name": "Bearer Token",
            "get_headers": lambda key: {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {key}'
            }
        },
        {
            "name": "Direct API Key",
            "get_headers": lambda key: {
                'Content-Type': 'application/json',
                'Authorization': key
            }
        }
    ]

    # 测试数据
    data = {
        'model': model,
        'messages': [{'role': 'user', 'content': '你好，请简单介绍一下你自己。'}],
        'max_tokens': 100
    }

    for endpoint in endpoints:
        for auth_method in auth_methods:
            try:
                print(f"测试: {endpoint} + {auth_method['name']}")

                headers = auth_method['get_headers'](api_key)
                response = requests.post(endpoint, headers=headers, json=data, timeout=30)

                print(f"   状态码: {response.status_code}")

                if response.status_code == 200:
                    result = response.json()
                    message = result['choices'][0]['message']['content']
                    print(f"✅ 豆包API 工作正常！")
                    print(f"   Endpoint: {endpoint}")
                    print(f"   认证方式: {auth_method['name']}")
                    print(f"   响应: {message[:100]}...")

                    # 更新.env文件
                    with open('.env', 'w') as f:
                        f.write(f"# 豆包API配置\n")
                        f.write(f"DOUBAO_API_KEY={api_key}\n")
                        f.write(f"DOUBAO_API_ENDPOINT={endpoint}\n")
                        f.write(f"DOUBAO_MODEL={model}\n")
                        f.write(f"DOUBAO_AUTH_TYPE={'bearer' if 'Bearer' in auth_method['name'] else 'direct'}\n")
                        f.write(f"\n# 服务器配置\n")
                        f.write(f"PORT=5000\n")
                        f.write(f"DEBUG=True\n")

                    print(f"\n✅ 已更新.env文件配置")
                    return True, endpoint, auth_method['name']

                elif response.status_code == 401:
                    print(f"   ❌ 认证失败")

                elif response.status_code == 404:
                    print(f"   ❌ Endpoint不存在")

                else:
                    print(f"   ❌ 状态码: {response.status_code}")
                    try:
                        error_detail = response.json()
                        print(f"   错误详情: {json.dumps(error_detail, ensure_ascii=False)[:200]}")
                    except:
                        print(f"   响应内容: {response.text[:200]}")

            except Exception as e:
                print(f"   ❌ 异常: {str(e)}")

            print()

    return False, None, None

def main():
    """运行最终测试"""
    print("🚀 豆包API最终测试\n")

    success, endpoint, auth_method = test_doubao_api_final()

    print("="*60)
    if success:
        print("🎉 豆包API配置成功！")
        print(f"✓ Endpoint: {endpoint}")
        print(f"✓ 认证方式: {auth_method}")
        print(f"✓ 模型: Doubao-Seed-1.8")
        print("\n现在可以启动API服务器了！")
        print("运行: python api.py")
        return 0
    else:
        print("⚠️  豆包API连接失败")
        print("\n所有可能的endpoint和认证方式都已测试完毕。")
        print("\n建议:")
        print("1. 登录火山引擎控制台检查API密钥和权限")
        print("2. 确认已开通豆包API服务")
        print("3. 检查账户余额和使用限制")
        print("4. 查看豆包API官方文档获取最新的endpoint信息")
        return 1

if __name__ == '__main__':
    sys.exit(main())