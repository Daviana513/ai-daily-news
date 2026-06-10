#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unified Processor - 消化层和说人话层
使用老张代理API的qwen-plus模型
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

class UnifiedDigester:
    """消化层：使用qwen-plus进行筛选和结构化"""

    def __init__(self):
        """初始化老张代理API客户端"""
        self.api_key = os.getenv('LAOZHAI_API_KEY')
        self.base_url = os.getenv('LAOZHAI_BASE_URL')
        self.model = os.getenv('PROCESSOR_MODEL', 'qwen-plus')

        if not self.api_key or not self.base_url:
            raise ValueError("缺少老张代理API配置")

        self.api_url = f"{self.base_url}/chat/completions"
        logger.info("统一消化层初始化完成（老张代理API - qwen-plus）")

    def digest_news(self, raw_news: List[Dict[str, Any]], today: str) -> Dict[str, Any]:
        """消化原始资讯，输出结构化数据"""
        try:
            raw_news_text = self._format_raw_news(raw_news)
            prompt = self._build_digester_prompt(raw_news_text, today)
            response_text = self._call_api(prompt)

            logger.info("消化层处理完成")
            return self._parse_response(response_text)

        except Exception as e:
            logger.error(f"消化层发生错误: {str(e)}")
            raise

    def _format_raw_news(self, raw_news: List[Dict[str, Any]]) -> str:
        """格式化原始新闻为prompt输入"""
        formatted_text = ""
        for i, news in enumerate(raw_news, 1):
            source_tag = f"[{news.get('source_type', 'Unknown')}]" if 'source_type' in news else ""
            formatted_text += f"""
新闻{i} {source_tag}：
标题：{news.get('title', '')}
摘要：{news.get('summary', '')}
来源：{news.get('source', '')}
URL：{news.get('url', '')}
"""
        return formatted_text

    def _build_digester_prompt(self, raw_news_text: str, today: str) -> str:
        """构建消化层prompt"""
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
6. further_reading从Top5之外的素材中挑选3-5条
7. insight.trend提炼今日多条新闻背后的共同趋势
8. insight.risk指出今日新闻隐含的潜在风险

**重要字段映射**：
- 原始素材中的"URL"字段必须映射到Top5的"source_url"字段
- 原始素材中的"URL"字段必须映射到延伸阅读的"url"字段
- 确保所有URL都完整保留，不要遗漏或修改

【输出格式】
严格按照以下JSON结构输出：

{{
  "date": "{today}",
  "audience": "非专业人士",
  "top5": [
    {{
      "id": 1,
      "title": "原始标题或编辑后的简洁标题",
      "summary": "原文摘要（编辑语言）",
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

请严格按照JSON格式输出。"""

    def _call_api(self, prompt: str) -> str:
        """调用老张代理API"""
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }

        data = {
            'model': self.model,
            'messages': [{'role': 'user', 'content': prompt}],
            'temperature': 0.3,
            'max_tokens': 3000
        }

        try:
            response = requests.post(self.api_url, headers=headers, json=data, timeout=60)
            response.raise_for_status()

            result = response.json()
            return result['choices'][0]['message']['content']

        except requests.exceptions.RequestException as e:
            logger.error(f"API调用失败: {str(e)}")
            raise

    def _parse_response(self, response_text: str) -> Dict[str, Any]:
        """解析API响应"""
        try:
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1

            if json_start == -1 or json_end == 0:
                raise ValueError("响应中未找到有效的JSON格式")

            json_str = response_text[json_start:json_end]
            return json.loads(json_str)

        except json.JSONDecodeError as e:
            logger.error(f"JSON解析失败: {str(e)}")
            raise ValueError(f"API返回的不是有效的JSON格式: {str(e)}")


class UnifiedTranslator:
    """说人话层：使用qwen-plus进行通俗化改写"""

    def __init__(self):
        """初始化老张代理API客户端"""
        self.api_key = os.getenv('LAOZHAI_API_KEY')
        self.base_url = os.getenv('LAOZHAI_BASE_URL')
        self.model = os.getenv('PROCESSOR_MODEL', 'qwen-plus')

        if not self.api_key or not self.base_url:
            raise ValueError("缺少老张代理API配置")

        self.api_url = f"{self.base_url}/chat/completions"
        logger.info("统一说人话层初始化完成（老张代理API - qwen-plus）")

    def translate_to_plain_language(self, digested_news: Dict[str, Any]) -> Dict[str, Any]:
        """将结构化内容通俗化"""
        try:
            digest_json = json.dumps(digested_news, ensure_ascii=False)
            prompt = self._build_translator_prompt(digest_json)
            response_text = self._call_api(prompt)

            logger.info("说人话层处理完成")
            return self._parse_response(response_text)

        except Exception as e:
            logger.error(f"说人话层发生错误: {str(e)}")
            raise

    def _build_translator_prompt(self, digest_json: str) -> str:
        """构建说人话层prompt"""
        return f"""【角色定义】
你是一位能把复杂事情讲得很简单的科普达人。
你的受众是完全没有技术背景的普通人。
你的风格是：准确但不卖弄、生动但不失真。

【任务说明】
以下是今日AI日报的结构化数据（编辑语言版本）。
请针对无技术背景的普通人，对所有文本字段进行通俗化改写。
不改变任何结构、不增删新闻条目、不改变任何事实。

输入数据：
{digest_json}

【操作规则】
1. title改写规则：
   - 必须是一句话，让没有AI背景的人一眼看懂发生了什么
   - 不能出现任何未经解释的技术术语

2. summary改写规则：
   - 控制在40字以内
   - 语气像"跟朋友发微信"

3. why_important改写规则：
   - 必须回答"这件事会不会影响我的工作、生活或钱包？"
   - 用读者熟悉的生活场景打比方

4. 术语处理规则：
   - 所有技术术语第一次出现时必须用括号加注解释
   - 用日常生活中的事物打比方

5. insight改写规则：
   - trend用"今天AI圈有个值得注意的趋势："开头
   - risk用"不过有一点需要留意："开头

【输出格式】
严格按照JSON格式输出，不输出任何JSON以外的内容。"""

    def _call_api(self, prompt: str) -> str:
        """调用老张代理API"""
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }

        data = {
            'model': self.model,
            'messages': [{'role': 'user', 'content': prompt}],
            'temperature': 0.4,
            'max_tokens': 3000
        }

        try:
            response = requests.post(self.api_url, headers=headers, json=data, timeout=60)
            response.raise_for_status()

            result = response.json()
            return result['choices'][0]['message']['content']

        except requests.exceptions.RequestException as e:
            logger.error(f"API调用失败: {str(e)}")
            raise

    def _parse_response(self, response_text: str) -> Dict[str, Any]:
        """解析API响应"""
        try:
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1

            if json_start == -1 or json_end == 0:
                raise ValueError("响应中未找到有效的JSON格式")

            json_str = response_text[json_start:json_end]
            return json.loads(json_str)

        except json.JSONDecodeError as e:
            logger.error(f"JSON解析失败: {str(e)}")
            raise ValueError(f"API返回的不是有效的JSON格式: {str(e)}")