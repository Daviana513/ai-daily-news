#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gemini Collector - 采集层
使用Gemini进行联网搜索，收集当日AI原始资讯
（支持老张代理服务）
"""

import os
import json
import logging
from datetime import datetime
import requests
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class GeminiCollector:
    """采集层：使用Gemini搜索当日AI资讯"""

    def __init__(self):
        """初始化Gemini客户端（使用老张代理）"""
        self.api_key = os.getenv('GEMINI_API_KEY')
        self.api_base = os.getenv('GEMINI_API_BASE', 'https://www.laozhang.ai/v1')

        if not self.api_key:
            raise ValueError("缺少GEMINI_API_KEY环境变量")

        # 构建完整的API URL
        self.api_url = f"{self.api_base}/chat/completions"
        logger.info("Gemini采集层初始化完成（使用老张代理）")

    def collect_daily_news(self, today: str) -> List[Dict[str, Any]]:
        """
        采集当日AI资讯

        Args:
            today: 当前日期，格式为 'YYYY-MM-DD'

        Returns:
            包含原始新闻条目的列表，每个条目包含标题、摘要、来源、URL
        """
        try:
            # 构建采集层prompt
            prompt = self._build_collector_prompt(today)

            logger.info(f"开始使用Gemini搜索 {today} 的AI资讯...")

            # 调用Gemini API（通过老张代理）
            response_text = self._call_gemini_api(prompt)

            logger.info("Gemini搜索完成，开始解析结果...")

            # 解析Gemini返回的原始文本
            raw_news_list = self._parse_gemini_response(response_text)

            logger.info(f"成功解析 {len(raw_news_list)} 条原始资讯")

            return raw_news_list

        except Exception as e:
            logger.error(f"Gemini采集层发生错误: {str(e)}")
            raise

    def _build_collector_prompt(self, today: str) -> str:
        """构建采集层的prompt"""
        return f"""【角色定义】
你是一位专注AI领域的资深信息采集员，有5年科技媒体从业经验，
熟悉中英文AI资讯生态，能快速识别有价值的信息源并过滤低质内容。

【任务说明】
今天的日期是{today}。
请联网搜索今日（{today}）AI领域的重要资讯，返回15-20条原始新闻素材。
搜索范围涵盖：大模型发布与更新、AI政策与监管、AI应用落地、
AI研究突破、AI行业动态（融资/收购/人事）。

【操作规则】
1. 搜索关键词分两组执行：
   中文组："AI大模型" "人工智能发布" "AI政策" "人工智能应用" "大模型融资"
   英文组："AI model release" "artificial intelligence breakthrough"
           "AI regulation" "LLM update"
2. 中文来源与英文来源各占约50%，确保国内外动态均有覆盖
3. 每条新闻必须包含：标题、100字以内的原文摘要、来源媒体名、完整URL
4. 时间范围严格限定为{today}，不收录昨天及更早的内容
5. 同一事件如有多个来源，只保留最权威的一个，其余丢弃
6. 优先选择以下来源：
   中文：机器之心、量子位、36氪、澎湃科技、新华社
   英文：MIT Technology Review、TechCrunch、The Verge、Reuters、Wired

【质量红线】
1. 禁止收录标题含"广告""赞助""推广"字样的内容
2. 禁止收录没有明确来源URL的新闻
3. 禁止收录同一事件超过1条
4. 禁止收录发布时间早于{today}的内容
5. 禁止做任何筛选、排序或改写，只返回原始素材

【输出格式】
以纯文本列表输出，每条格式如下，共15-20条：

[编号] 标题：XXX
摘要：XXX（100字以内）
来源：XXX媒体
URL：https://...
---

请严格按照以上格式输出，现在开始搜索和分析。"""

    def _parse_gemini_response(self, response_text: str) -> List[Dict[str, Any]]:
        """
        解析Gemini返回的原始文本

        Args:
            response_text: Gemini返回的原始文本

        Returns:
            解析后的新闻条目列表
        """
        raw_news_list = []
        current_item = {}
        current_field = None

        lines = response_text.strip().split('\n')

        for line in lines:
            line = line.strip()

            if not line or line == '---':
                # 遇到分隔符，保存当前条目
                if current_item and all(key in current_item for key in ['title', 'summary', 'source', 'url']):
                    raw_news_list.append(current_item)
                    current_item = {}
                    current_field = None
                continue

            # 解析字段
            if line.startswith('[编号]') or line.startswith('['):
                # 新条目开始
                if current_item and all(key in current_item for key in ['title', 'summary', 'source', 'url']):
                    raw_news_list.append(current_item)
                    current_item = {}
                    current_field = None
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
                # 继续上一个字段的内容
                current_item[current_field] += ' ' + line

        # 保存最后一条
        if current_item and all(key in current_item for key in ['title', 'summary', 'source', 'url']):
            raw_news_list.append(current_item)

        return raw_news_list

    def _call_gemini_api(self, prompt: str) -> str:
        """
        调用Gemini API（通过老张代理）

        Args:
            prompt: 发送给Gemini的提示词

        Returns:
            Gemini的响应文本
        """
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }

        data = {
            'model': 'gemini-pro', # 或者根据代理服务的要求使用其他模型名
            'messages': [
                {'role': 'user', 'content': prompt}
            ],
            'temperature': 0.7,
            'max_tokens': 4000
        }

        try:
            response = requests.post(self.api_url, headers=headers, json=data, timeout=120)
            response.raise_for_status()

            result = response.json()
            # 根据OpenAI兼容格式解析响应
            return result['choices'][0]['message']['content']

        except requests.exceptions.RequestException as e:
            logger.error(f"Gemini API调用失败: {str(e)}")
            raise