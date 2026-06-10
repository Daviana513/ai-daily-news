#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
采集层详细调试脚本
查看API的实际响应内容
"""

import os
import sys
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

# 设置控制台编码为UTF-8（Windows兼容）
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 加载环境变量
load_dotenv()

def test_gemini_collection():
    """测试Gemini模型采集"""
    print("🔍 测试Gemini模型（国外新闻）...")

    api_key = os.getenv('LAOZHAI_API_KEY')
    base_url = os.getenv('LAOZHAI_BASE_URL')
    model = 'gemini-2.5-flash-thinking'

    print(f"API Key: {api_key[:20]}...")
    print(f"Base URL: {base_url}")
    print(f"Model: {model}")
    print()

    # 构建prompt
    today = datetime.now().strftime('%Y-%m-%d')
    prompt = f"""【角色定义】
你是一位专注AI领域的国际资讯采集员，擅长搜索全球AI动态。

【任务说明】
今天的日期是{today}。
请联网搜索今日（{today}）海外AI领域的重要资讯，返回5-8条原始新闻素材。

【操作规则】
1. 英文关键词："AI model release" "artificial intelligence breakthrough" "AI regulation"
2. 优先选择权威媒体：MIT Technology Review、TechCrunch、The Verge
3. 每条新闻包含：标题、100字摘要、来源、URL
4. 时间严格限定为{today}

【输出格式】
每条格式如下：

[编号] 标题：XXX
摘要：XXX（100字以内）
来源：XXX媒体
URL：https://...
---

请返回5-8条海外AI资讯。"""

    print("📝 发送prompt到Gemini...")
    print(f"Prompt长度: {len(prompt)} 字符")
    print()

    # 调用API
    endpoint = f"{base_url}/chat/completions"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    data = {
        'model': model,
        'messages': [{'role': 'user', 'content': prompt}],
        'temperature': 0.7,
        'max_tokens': 2000
    }

    try:
        print("🔄 调用API中...")
        response = requests.post(endpoint, headers=headers, json=data, timeout=120)

        print(f"📊 响应状态码: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            message = result['choices'][0]['message']['content']

            print(f"✅ API调用成功")
            print(f"📄 响应长度: {len(message)} 字符")
            print()
            print("📋 响应内容预览：")
            print("="*60)
            print(message[:1000])
            if len(message) > 1000:
                print("...")
                print(f"(还有 {len(message) - 1000} 字符)")
            print("="*60)

            return message

        else:
            print(f"❌ API调用失败: {response.status_code}")
            print(f"错误详情: {response.text}")
            return None

    except Exception as e:
        print(f"❌ 调用过程出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def test_qwen_collection():
    """测试Qwen模型采集"""
    print("🔍 测试Qwen模型（国内新闻）...")

    api_key = os.getenv('LAOZHAI_API_KEY')
    base_url = os.getenv('LAOZHAI_BASE_URL')
    model = 'qwen3-30b-a3b-thinking-2507'

    print(f"API Key: {api_key[:20]}...")
    print(f"Base URL: {base_url}")
    print(f"Model: {model}")
    print()

    # 构建prompt
    today = datetime.now().strftime('%Y-%m-%d')
    prompt = f"""【角色定义】
你是一位专注AI领域的国内资讯采集员，擅长搜索中国AI行业动态。

【任务说明】
今天的日期是{today}。
请联网搜索今日（{today}）中国AI领域的重要资讯，返回5-8条原始新闻素材。

【操作规则】
1. 中文关键词："AI大模型" "人工智能发布" "AI政策" "人工智能应用"
2. 优先选择权威媒体：机器之心、量子位、36氪、澎湃科技
3. 每条新闻包含：标题、100字摘要、来源、URL
4. 时间严格限定为{today}

【输出格式】
每条格式如下：

[编号] 标题：XXX
摘要：XXX（100字以内）
来源：XXX媒体
URL：https://...
---

请返回5-8条中国AI资讯。"""

    print("📝 发送prompt到Qwen...")
    print(f"Prompt长度: {len(prompt)} 字符")
    print()

    # 调用API
    endpoint = f"{base_url}/chat/completions"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    data = {
        'model': model,
        'messages': [{'role': 'user', 'content': prompt}],
        'temperature': 0.7,
        'max_tokens': 2000
    }

    try:
        print("🔄 调用API中...")
        response = requests.post(endpoint, headers=headers, json=data, timeout=120)

        print(f"📊 响应状态码: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            message = result['choices'][0]['message']['content']

            print(f"✅ API调用成功")
            print(f"📄 响应长度: {len(message)} 字符")
            print()
            print("📋 响应内容预览：")
            print("="*60)
            print(message[:1000])
            if len(message) > 1000:
                print("...")
                print(f"(还有 {len(message) - 1000} 字符)")
            print("="*60)

            return message

        else:
            print(f"❌ API调用失败: {response.status_code}")
            print(f"错误详情: {response.text}")
            return None

    except Exception as e:
        print(f"❌ 调用过程出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def main():
    """主函数"""
    print("="*60)
    print("🚀 采集层详细调试")
    print("="*60)
    print()

    # 测试Gemini
    gemini_response = test_gemini_collection()

    print("\n" + "="*60 + "\n")

    # 测试Qwen
    qwen_response = test_qwen_collection()

    print("\n" + "="*60)
    print("📊 调试总结")
    print("="*60)

    if gemini_response and qwen_response:
        print("✅ 两个模型都返回了响应")
        print(f"Gemini响应长度: {len(gemini_response)} 字符")
        print(f"Qwen响应长度: {len(qwen_response)} 字符")
        print("\n下一步：分析响应格式，优化解析逻辑")

    elif gemini_response or qwen_response:
        print("⚠️  只有一个模型返回响应")
        if gemini_response:
            print("✅ Gemini响应正常")
        else:
            print("❌ Gemini响应失败")
        if qwen_response:
            print("✅ Qwen响应正常")
        else:
            print("❌ Qwen响应失败")

    else:
        print("❌ 两个模型都没有返回响应")
        print("请检查API配置和网络连接")

    return 0

if __name__ == '__main__':
    sys.exit(main())