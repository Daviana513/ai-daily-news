#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试老张代理API的网络连接
"""
import sys
import os
import requests

# 设置控制台编码
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def test_laozhang_connection():
    """测试老张API连接"""
    print("🔍 测试老张代理API连接")
    print("="*60)

    # 从.env加载配置
    from dotenv import load_dotenv
    load_dotenv()

    api_key = os.getenv('LAOZHAI_API_KEY')
    base_url = os.getenv('LAOZHAI_BASE_URL')

    print(f"API Key: {api_key[:20]}..." if api_key else "❌ 未找到LAOZHAI_API_KEY")
    print(f"Base URL: {base_url}" if base_url else "❌ 未找到LAOZHAI_BASE_URL")

    if not base_url:
        print("\n❌ 请先配置 .env 文件中的 LAOZHAI_BASE_URL")
        return

    # 测试1: 基础连接测试
    print("\n测试1: 基础连接...")
    try:
        response = requests.get(base_url.replace('/v1', ''), timeout=10)
        print(f"✅ 基础连接成功: {response.status_code}")
    except requests.exceptions.Timeout:
        print("❌ 基础连接超时")
        return
    except requests.exceptions.ConnectionError as e:
        print(f"❌ 连接错误: {str(e)}")
        return
    except Exception as e:
        print(f"❌ 其他错误: {str(e)}")
        return

    # 测试2: API调用测试（简单请求）
    print("\n测试2: API调用测试...")
    api_url = f"{base_url}/chat/completions"

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    data = {
        'model': 'qwen-plus',
        'messages': [{'role': 'user', 'content': '测试'}],
        'temperature': 0.3,
        'max_tokens': 100
    }

    try:
        print(f"正在连接: {api_url}")
        print(f"超时设置: 30秒...")

        response = requests.post(api_url, headers=headers, json=data, timeout=30)

        print(f"✅ API调用成功: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print(f"✅ 返回数据: {list(result.keys())}")

    except requests.exceptions.Timeout:
        print("❌ API调用超时（30秒）")
        print("\n💡 建议：")
        print("   1. 检查网络连接")
        print("   2. 尝试增加超时时间")
        print("   3. 检查是否需要代理")

    except requests.exceptions.ConnectionError as e:
        print(f"❌ 连接失败: {str(e)}")
        print("\n💡 可能原因：")
        print("   1. 无法访问 api.laozhang.ai")
        print("   2. 防火墙阻止连接")
        print("   3. API服务器不可用")

    except Exception as e:
        print(f"❌ 其他错误: {str(e)}")

    print("\n" + "="*60)
    print("测试完成")

if __name__ == '__main__':
    test_laozhang_connection()
