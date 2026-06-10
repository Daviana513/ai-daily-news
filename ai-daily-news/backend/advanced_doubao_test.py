#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
豆包API高级测试脚本
尝试多种可能的认证方式和请求格式
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

def test_doubao_api_advanced():
    """高级测试豆包API"""
    print("🔍 高级测试豆包API...")

    api_key = "ark-7ac4d5f3-13ad-4ec0-8ecb-72ca75b0adcf-9fa34"
    model = "Doubao-Smart-Router"

    print(f"API密钥: {api_key[:20]}...")
    print(f"模型: {model}")
    print()

    # 基于之前的测试，这个endpoint最有可能
    endpoint = "https://api.volcengine.com/api/v3/chat/completions"

    # 测试多种可能的认证方式
    auth_methods = [
        {
            "name": "Bearer Token (标准OpenAI格式)",
            "headers": {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {api_key}'
            }
        },
        {
            "name": "直接使用API Key",
            "headers": {
                'Content-Type': 'application/json',
                'Authorization': api_key
            }
        },
        {
            "name": "API Key in X-API-Key header",
            "headers": {
                'Content-Type': 'application/json',
                'X-API-Key': api_key
            }
        },
        {
            "name": "火山引擎ARK格式",
            "headers": {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {api_key}',
                'X-Request-ID': 'test-123'
            }
        },
        {
            "name": "火山引擎格式 (无Bearer)",
            "headers": {
                'Content-Type': 'application/json',
                'Authorization': api_key,
                'User-Agent': 'DoubaoAPIClient/1.0'
            }
        }
    ]

    # 测试数据
    data = {
        'model': model,
        'messages': [{'role': 'user', 'content': '你好'}],
        'max_tokens': 50
    }

    for method in auth_methods:
        try:
            print(f"测试: {method['name']}")

            response = requests.post(
                endpoint,
                headers=method['headers'],
                json=data,
                timeout=15
            )

            print(f"   状态码: {response.status_code}")

            if response.status_code == 200:
                print(f"✅ 成功！认证方式: {method['name']}")
                result = response.json()
                message = result['choices'][0]['message']['content']
                print(f"   响应: {message[:100]}...")

                return True, method['name'], endpoint

            elif response.status_code == 401:
                print(f"   ❌ 认证失败")
            elif response.status_code == 403:
                print(f"   ❌ 权限不足")
            elif response.status_code == 404:
                print(f"   ❌ Endpoint不存在")
            else:
                print(f"   ❌ 其他错误: {response.status_code}")
                try:
                    error_detail = response.json()
                    print(f"   错误详情: {json.dumps(error_detail, ensure_ascii=False)[:200]}")
                except:
                    print(f"   响应内容: {response.text[:200]}")

        except Exception as e:
            print(f"   ❌ 异常: {str(e)}")

        print()

    # 如果所有方法都失败，尝试不同的数据格式
    print("尝试不同的请求格式...")

    data_formats = [
        {
            "name": "简化数据格式",
            "data": {
                'model': model,
                'messages': [{'role': 'user', 'content': '你好'}]
            }
        },
        {
            "name": "添加temperature参数",
            "data": {
                'model': model,
                'messages': [{'role': 'user', 'content': '你好'}],
                'temperature': 0.7,
                'max_tokens': 50
            }
        },
        {
            "name": "使用prompt而非messages",
            "data": {
                'model': model,
                'prompt': '你好',
                'max_tokens': 50
            }
        }
    ]

    for fmt in data_formats:
        try:
            print(f"测试: {fmt['name']}")

            response = requests.post(
                endpoint,
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {api_key}'
                },
                json=fmt['data'],
                timeout=15
            )

            print(f"   状态码: {response.status_code}")

            if response.status_code == 200:
                print(f"✅ 成功！数据格式: {fmt['name']}")
                return True, fmt['name'], endpoint

        except Exception as e:
            print(f"   ❌ 异常: {str(e)}")

        print()

    return False, None, None

def main():
    """运行高级测试"""
    print("🚀 豆包API高级测试\n")

    success, method, endpoint = test_doubao_api_advanced()

    print("="*60)
    if success:
        print("🎉 找到正确的配置方式！")
        print(f"成功方式: {method}")
        print(f"Endpoint: {endpoint}")
        print(f"模型: Doubao-Smart-Router")
        print("\n现在可以更新配置文件并启动服务器了！")
        return 0
    else:
        print("⚠️  所有测试都失败")
        print("\n可能的问题:")
        print("1. API密钥格式或权限问题")
        print("2. 需要特殊的服务配置或开通")
        print("3. API密钥可能已过期或余额不足")
        print("4. 网络环境或防火墙限制")
        print("\n建议:")
        print("• 登录火山引擎控制台检查API密钥状态")
        print("• 确认已开通豆包API服务权限")
        print("• 检查账户余额和使用限制")
        print("• 查看豆包API官方文档")
        print("• 联系技术支持获取帮助")
        return 1

if __name__ == '__main__':
    sys.exit(main())