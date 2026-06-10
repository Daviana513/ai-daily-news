#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的API测试脚本
"""

import requests
import json
import time

def test_api():
    """测试API连接和功能"""
    api_url = "http://localhost:5000"

    print("=== 测试API连接 ===")

    # 1. 测试健康检查
    try:
        response = requests.get(f"{api_url}/health", timeout=5)
        if response.status_code == 200:
            print("[OK] 健康检查成功")
        else:
            print(f"[FAIL] 健康检查失败: {response.status_code}")
            return
    except Exception as e:
        print(f"[FAIL] 连接失败: {str(e)}")
        return

    # 2. 测试生成新闻（设置较长超时）
    print("\n=== 测试生成新闻 ===")
    print("这可能需要1-2分钟，请耐心等待...")

    start_time = time.time()

    try:
        response = requests.post(
            f"{api_url}/api/generate-daily-news",
            headers={"Content-Type": "application/json"},
            json={"date": "2026-06-01"},
            timeout=120  # 2分钟超时
        )

        elapsed_time = time.time() - start_time
        print(f"请求完成，耗时: {elapsed_time:.2f}秒")

        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                print("[OK] 新闻生成成功!")
                print(f"性能数据: {result.get('performance', {})}")
            else:
                print(f"[FAIL] 生成失败: {result.get('error', '未知错误')}")
        else:
            print(f"[FAIL] API错误: {response.status_code}")
            print(f"响应内容: {response.text[:200]}")

    except requests.exceptions.Timeout:
        print(f"[FAIL] 请求超时 (已等待 {time.time() - start_time:.2f}秒)")
    except Exception as e:
        print(f"[FAIL] 请求失败: {str(e)}")

if __name__ == "__main__":
    test_api()