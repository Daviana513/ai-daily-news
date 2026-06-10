#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unified Collector - 采集层
使用老张代理API进行双模型采集
- 国外新闻：gemini-2.5-flash-thinking
- 国内新闻：qwen3-30b-a3b-thinking-2507
"""

import os
import json
import logging
import requests
from typing import List, Dict, Any
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

logger = logging.getLogger(__name__)

class UnifiedCollector:
    """采集层：使用老张代理API进行双模型采集"""

    def __init__(self):
        """初始化老张代理API客户端"""
        self.api_key = os.getenv('LAOZHAI_API_KEY')
        self.base_url = os.getenv('LAOZHAI_BASE_URL')

        if not self.api_key or not self.base_url:
            raise ValueError("缺少老张代理API配置")

        # 模型配置
        self.gemini_model = os.getenv('COLLECTOR_GEMINI_MODEL', 'gemini-2.5-flash-thinking')
        self.qwen_model = os.getenv('COLLECTOR_QWEN_MODEL', 'qwen3-30b-a3b-thinking-2507')

        # API endpoint
        self.api_url = f"{self.base_url}/chat/completions"

        logger.info("统一采集层初始化完成（老张代理API）")

    def collect_daily_news(self, today: str) -> List[Dict[str, Any]]:
        """
        采集当日AI资讯（使用双模型）

        Args:
            today: 当前日期，格式为 'YYYY-MM-DD'

        Returns:
            包含原始新闻条目的列表
        """
        try:
            logger.info(f"开始双模型采集 {today} 的AI资讯...")

            # 并行采集国内外新闻
            gemini_news = self._collect_with_gemini(today)
            qwen_news = self._collect_with_qwen(today)

            # 合并新闻
            all_news = gemini_news + qwen_news

            logger.info(f"采集完成：Gemini {len(gemini_news)} 条，Qwen {len(qwen_news)} 条")

            return all_news

        except Exception as e:
            logger.error(f"采集层发生错误: {str(e)}")
            raise

    def _collect_with_gemini(self, today: str) -> List[Dict[str, Any]]:
        """使用Gemini采集国外AI资讯"""
        try:
            prompt = self._build_gemini_prompt(today)
            response_text = self._call_api(prompt, self.gemini_model)
            return self._parse_response(response_text, "Gemini")

        except Exception as e:
            logger.error(f"Gemini采集失败: {str(e)}")
            return []

    def _collect_with_qwen(self, today: str) -> List[Dict[str, Any]]:
        """使用Qwen采集国内AI资讯"""
        try:
            prompt = self._build_qwen_prompt(today)
            response_text = self._call_api(prompt, self.qwen_model)
            return self._parse_response(response_text, "Qwen")

        except Exception as e:
            logger.error(f"Qwen采集失败: {str(e)}")
            return []

    def _call_api(self, prompt: str, model: str) -> str:
        """调用老张代理API"""
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }

        data = {
            'model': model,
            'messages': [{'role': 'user', 'content': prompt}],
            'temperature': 0.7,
            'max_tokens': 4000
        }

        try:
            response = requests.post(self.api_url, headers=headers, json=data, timeout=120)
            response.raise_for_status()

            result = response.json()
            return result['choices'][0]['message']['content']

        except requests.exceptions.RequestException as e:
            logger.error(f"API调用失败 ({model}): {str(e)}")
            raise

    def _build_gemini_prompt(self, today: str) -> str:
        """构建Gemini的prompt（国外新闻）"""
        return f"""【角色定义】
你是一位专注AI领域的国际资讯采集员，擅长搜索全球AI动态。
请重点搜索欧美、日韩等地区的AI资讯。

【任务说明】
今天的日期是{today}。
请联网搜索今日（{today}）海外AI领域的重要资讯，返回8-12条原始新闻素材。
搜索范围：大模型发布、AI政策监管、AI研究突破、AI应用、行业动态。

【操作规则】
1. 英文关键词："AI model release" "artificial intelligence breakthrough" "AI regulation" "LLM update"
2. 优先选择权威媒体：MIT Technology Review、TechCrunch、The Verge、Reuters、Wired
3. 每条新闻包含：标题、100字摘要、来源、**真实可访问的URL**
4. 时间严格限定为{today}
5. 禁止收录广告、软文、重复内容
6. **必须确保URL是真实存在的、可访问的网页链接**

【输出格式】
每条格式如下：

[编号] 标题：XXX
摘要：XXX（100字以内）
来源：XXX媒体
URL：https://...
---

请返回8-12条海外AI资讯。"""

    def _build_qwen_prompt(self, today: str) -> str:
        """构建Qwen的prompt（国内新闻）"""
        return f"""【角色定义】
你是一位专注AI领域的国内资讯采集员，擅长搜索中国AI行业动态。
请重点搜索中国大陆和港澳台地区的AI资讯。

【任务说明】
今天的日期是{today}。
请联网搜索今日（{today}）中国AI领域的重要资讯，返回7-10条原始新闻素材。
搜索范围：大模型发布、AI政策监管、AI应用落地、AI研究、行业动态。

【操作规则】
1. 中文关键词："AI大模型" "人工智能发布" "AI政策" "人工智能应用" "大模型融资"
2. 优先选择权威媒体：机器之心、量子位、36氪、澎湃科技、新华社
3. 每条新闻包含：标题、100字摘要、来源、**真实可访问的URL**
4. 时间严格限定为{today}
5. 禁止收录广告、软文、重复内容
6. **必须确保URL是真实存在的、可访问的网页链接**

【输出格式】
每条格式如下：

[编号] 标题：XXX
摘要：XXX（100字以内）
来源：XXX媒体
URL：https://...
---

请返回7-10条中国AI资讯。"""

    def _parse_response(self, response_text: str, source: str) -> List[Dict[str, Any]]:
        """解析API响应"""
        news_list = []
        current_item = {}
        current_field = None

        lines = response_text.strip().split('\n')

        for line in lines:
            line = line.strip()

            if not line or line == '---':
                if current_item and all(key in current_item for key in ['title', 'summary', 'source', 'url']):
                    current_item['source_type'] = source  # 标记来源
                    news_list.append(current_item)
                    current_item = {}
                    current_field = None
                continue

            # 检查新条目开始 - 支持 [1] 标题：... 这样的格式
            if line.startswith('[') and ']' in line:
                bracket_content = line.split(']', 1)[0].replace('[', '').strip()
                # 如果是数字，可能是新条目开始
                if bracket_content.isdigit():
                    if current_item and all(key in current_item for key in ['title', 'summary', 'source', 'url']):
                        current_item['source_type'] = source
                        news_list.append(current_item)
                        current_item = {}
                        current_field = None

                    # 检查同一行是否还有标题信息
                    rest_of_line = line.split(']', 1)[1].strip()
                    if rest_of_line.startswith('标题：'):
                        current_field = 'title'
                        current_item['title'] = rest_of_line.replace('标题：', '').strip()
                    continue

            if line.startswith('标题：'):
                current_field = 'title'
                current_item['title'] = line.replace('标题：', '').strip()
            elif line.startswith('摘要：'):
                current_field = 'summary'
                current_item['summary'] = line.replace('摘要：', '').strip()
            elif line.startswith('来源：'):
                current_field = 'source'
                current_item['source'] = line.replace('来源：', '').strip()
            elif line.startswith('URL：') or line.startswith('url：'):
                current_field = 'url'
                current_item['url'] = line.replace('URL：', '').replace('url：', '').strip()
            elif current_field and current_item.get(current_field):
                current_item[current_field] += ' ' + line

        # 保存最后一条
        if current_item and all(key in current_item for key in ['title', 'summary', 'source', 'url']):
            current_item['source_type'] = source
            news_list.append(current_item)

        return news_list