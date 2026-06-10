#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Doubao Digester - 消化层
使用Doubao对原始资讯进行筛选、分类、结构化处理
"""

import os
import json
import logging
from datetime import datetime
from typing import List, Dict, Any
import requests

logger = logging.getLogger(__name__)

class DoubaoDigester:
    """消化层：使用Doubao筛选和结构化资讯"""

    def __init__(self):
        """初始化Doubao客户端（使用ARK API）"""
        self.api_key = os.getenv('ARK_API_KEY')
        self.api_base = os.getenv('ARK_API_BASE', 'https://ark.cn-beijing.volces.com/api/v3')

        if not self.api_key:
            raise ValueError("缺少ARK_API_KEY环境变量")

        # 构建ARK API URL
        self.api_url = f"{self.api_base}/chat/completions"
        logger.info("Doubao消化层初始化完成（使用ARK API）")

    def digest_news(self, raw_news: List[Dict[str, Any]], today: str) -> Dict[str, Any]:
        """
        消化原始资讯，输出结构化数据

        Args:
            raw_news: 采集层返回的原始新闻列表
            today: 当前日期

        Returns:
            结构化的日报数据（编辑语言版本）
        """
        try:
            # 构建输入文本
            raw_news_text = self._format_raw_news_for_prompt(raw_news)

            # 构建消化层prompt
            prompt = self._build_digester_prompt(raw_news_text, today)

            logger.info("开始使用Doubao进行资讯消化...")

            # 调用Doubao API
            response = self._call_doubao_api(prompt)

            # 解析返回的JSON
            digested_news = self._parse_doubao_response(response)

            logger.info("Doubao消化层处理完成")

            return digested_news

        except Exception as e:
            logger.error(f"Doubao消化层发生错误: {str(e)}")
            raise

    def _format_raw_news_for_prompt(self, raw_news: List[Dict[str, Any]]) -> str:
        """将原始新闻格式化为prompt输入文本"""
        formatted_text = ""
        for i, news in enumerate(raw_news, 1):
            formatted_text += f"""
新闻{i}：
标题：{news.get('title', '')}
摘要：{news.get('summary', '')}
来源：{news.get('source', '')}
URL：{news.get('url', '')}
"""
        return formatted_text

    def _build_digester_prompt(self, raw_news_text: str, today: str) -> str:
        """构建消化层的prompt"""
        return f"""【角色定义】
你是一位AI领域的资深编辑，专注于信息价值判断与内容结构化。
你的判断标准清晰、分类一致、逻辑严谨，擅长从大量信息中提炼真正重要的内容。

【任务说明】
以下是今日AI领域的原始新闻素材（15-20条）。
请对这批素材进行筛选、排序、分类和结构化处理，
输出一份AI日报的中间数据，供下一层进行通俗化改写。

原始素材：
{raw_news_text}

【操作规则】
1. 从原始素材中选出最重要的5条作为Top5，优先级如下：
   第一优先：对AI行业格局有重大影响的事件
   第二优先：重要新模型或新产品发布
   第三优先：与普通人日常生活直接相关的AI应用
   第四优先：重要政策或监管动向
2. Top5必须覆盖至少3个不同category，禁止5条全属同一类别
3. category由你根据内容自主判断，全篇保持命名一致
4. importance评级标准：
   高：影响整个AI行业走向，或直接影响普通用户的产品/政策
   中：对特定领域或群体有明显影响
   低：行业内部动态，对普通用户影响有限
5. digest_table只包含Top5这5条新闻的整理
6. further_reading从Top5之外的素材中挑选3-5条，
   标准是内容有深度、适合想进一步了解某方向的读者
7. insight.trend提炼今日多条新闻背后的共同趋势，
   必须是跨新闻的规律性观察，不是对单条新闻的重复
8. insight.risk指出今日新闻隐含的潜在风险或值得警惕的方向

【质量红线】
1. 禁止在Top5中选入重复事件，即使来源不同
2. 禁止insight只是新闻内容的拼凑，必须有判断和提炼
3. 禁止category命名前后不一致
4. 禁止further_reading包含Top5已有的新闻
5. 此阶段禁止做任何通俗化改写，保持编辑语言即可

【输出格式】
严格按照以下JSON结构输出，不输出任何JSON以外的内容：

{{
  "date": "{today}",
  "audience": "非专业人士",
  "top5": [
    {{
      "id": 1,
      "title": "原始标题或编辑后的简洁标题",
      "summary": "原文摘要（编辑语言，不需要通俗化）",
      "source_url": "https://...",
      "why_important": "为什么重要（编辑视角，50-80字）"
    }}
  ],
  "digest_table": [
    {{
      "id": 1,
      "category": "自主判断的类别",
      "title": "新闻标题",
      "importance": "高 / 中 / 低"
    }}
  ],
  "further_reading": [
    {{
      "title": "延伸阅读标题",
      "url": "https://..."
    }}
  ],
  "insight": {{
    "trend": "今日核心趋势（编辑语言，100字以内）",
    "risk": "风险提示（编辑语言，50字以内）"
  }}
}}

请严格按照以上格式输出，现在开始处理。"""

    def _call_doubao_api(self, prompt: str) -> str:
        """调用Doubao API"""
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }

        data = {
            'model': 'doubao-pro-1.8',  # 使用Doubao 1.8模型
            'messages': [
                {'role': 'user', 'content': prompt}
            ],
            'temperature': 0.3,  # 降低温度以获得更稳定的输出
            'max_tokens': 3000
        }

        try:
            response = requests.post(self.api_url, headers=headers, json=data, timeout=60)
            response.raise_for_status()

            result = response.json()
            return result['choices'][0]['message']['content']

        except requests.exceptions.RequestException as e:
            logger.error(f"Doubao API调用失败: {str(e)}")
            raise

    def _parse_doubao_response(self, response_text: str) -> Dict[str, Any]:
        """解析Doubao返回的JSON响应"""
        try:
            # 提取JSON部分（如果响应中有其他文字）
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1

            if json_start == -1 or json_end == 0:
                raise ValueError("响应中未找到有效的JSON格式")

            json_str = response_text[json_start:json_end]
            parsed_data = json.loads(json_str)

            return parsed_data

        except json.JSONDecodeError as e:
            logger.error(f"JSON解析失败: {str(e)}")
            logger.error(f"原始响应: {response_text}")
            raise ValueError(f"Doubao返回的不是有效的JSON格式: {str(e)}")