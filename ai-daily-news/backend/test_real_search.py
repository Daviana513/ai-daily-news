#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试AI模型的联网搜索能力
检查是否能真正获取今日新闻
"""

import os
import sys
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

def test_model_search_capability(model_name, model_id):
    """测试特定模型的联网搜索能力"""
    print(f"🔍 测试 {model_name} 的联网搜索能力...")

    api_key = os.getenv('LAOZHAI_API_KEY')
    base_url = os.getenv('LAOZHAI_BASE_URL')

    today = datetime.now().strftime('%Y年%m月%d日')

    # 测试prompt - 明确要求今天的新闻
    prompt = f"""请联网搜索今天的新闻。

今天是：{today}

请搜索：今日最新科技新闻
要求：
1. 必须是今天（{today}）发布的新闻
2. 提供1条新闻的标题、来源、**真实可点击的URL**
3. 确认URL是真实存在的

请直接回答：你能否联网搜索今天的新闻？如果能，请提供一条今天的真实新闻链接。"""

    endpoint = f"{base_url}/chat/completions"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    data = {
        'model': model_id,
        'messages': [{'role': 'user', 'content': prompt}],
        'temperature': 0.3,
        'max_tokens': 500
    }

    try:
        response = requests.post(endpoint, headers=headers, json=data, timeout=30)

        if response.status_code == 200:
            result = response.json()
            message = result['choices'][0]['message']['content']

            print(f"✅ 响应成功")
            print(f"📄 回答：")
            print("="*60)
            print(message)
            print("="*60)

            # 检查是否提到了今天的新闻
            if today in message or "2026" in message or "5月31" in message:
                print(f"✅ 可能包含今日信息")
            else:
                print(f"⚠️  可能没有获取到今日信息")

            return True
        else:
            print(f"❌ API调用失败: {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ 调用异常: {str(e)}")
        return False

def main():
    """主函数"""
    print("="*60)
    print("🌐 AI模型联网搜索能力测试")
    print("="*60)
    print()

    models = [
        ("Gemini Flash Thinking", "gemini-2.5-flash-thinking"),
        ("Qwen Thinking", "qwen3-30b-a3b-thinking-2507"),
        ("Qwen Plus", "qwen-plus")
    ]

    for model_name, model_id in models:
        print()
        test_model_search_capability(model_name, model_id)
        print()

    print("="*60)
    print("📊 测试结论")
    print("="*60)
    print("如果上述回答显示能联网搜索但仍提供旧闻，")
    print("说明模型可能需要使用特定的联网搜索工具或API。")
    print("如果无法联网搜索，我们需要改用其他策略。")

    return 0

if __name__ == '__main__':
    sys.exit(main())