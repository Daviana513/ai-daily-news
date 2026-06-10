#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试日期参数API
"""
import requests
import json
import sys

# 设置控制台编码为UTF-8（Windows兼容）
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

API_URL = "http://localhost:5000/api/generate-daily-news"

def test_date_api():
    """测试API是否正确处理日期参数"""
    print("测试日期参数API")
    print("="*60)

    # 测试1: 不传日期参数（应该生成今天的）
    print("\n测试1: 不传日期参数")
    try:
        response = requests.post(API_URL, json={}, timeout=120)
        if response.status_code == 200:
            result = response.json()
            print(f"成功: {result.get('generated_at', 'N/A')}")
        else:
            print(f"失败: {response.status_code}")
    except Exception as e:
        print(f"错误: {str(e)}")

    # 测试2: 传入指定日期（2026-05-27）
    print("\n测试2: 传入指定日期 2026-05-27")
    try:
        response = requests.post(API_URL, json={
            "date": "2026-05-27"
        }, timeout=120)
        if response.status_code == 200:
            result = response.json()
            print(f"成功")
            print(f"   Generated at: {result.get('generated_at', 'N/A')}")
        else:
            print(f"失败: {response.status_code}")
            print(f"   错误信息: {response.text}")
    except Exception as e:
        print(f"错误: {str(e)}")

    # 测试3: 传入昨天日期
    print("\n测试3: 传入昨天日期")
    from datetime import datetime, timedelta
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    try:
        response = requests.post(API_URL, json={
            "date": yesterday
        }, timeout=120)
        if response.status_code == 200:
            result = response.json()
            print(f"成功 - 日期: {yesterday}")
        else:
            print(f"失败: {response.status_code}")
    except Exception as e:
        print(f"错误: {str(e)}")

    print("\n" + "="*60)
    print("测试完成")

if __name__ == '__main__':
    test_date_api()
