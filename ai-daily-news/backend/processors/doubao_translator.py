#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Doubao Translator - 说人话层
使用Doubao将专业内容通俗化，面向非技术背景人群
"""

import os
import json
import logging
from typing import Dict, Any
import requests

logger = logging.getLogger(__name__)

class DoubaoTranslator:
    """说人话层：使用Doubao进行通俗化改写"""

    def __init__(self):
        """初始化Doubao客户端（使用ARK API）"""
        self.api_key = os.getenv('ARK_API_KEY')
        self.api_base = os.getenv('ARK_API_BASE', 'https://ark.cn-beijing.volces.com/api/v3')

        if not self.api_key:
            raise ValueError("缺少ARK_API_KEY环境变量")

        # 构建ARK API URL
        self.api_url = f"{self.api_base}/chat/completions"
        logger.info("Doubao说人话层初始化完成（使用ARK API）")

    def translate_to_plain_language(self, digested_news: Dict[str, Any]) -> Dict[str, Any]:
        """
        将结构化内容通俗化

        Args:
            digested_news: 消化层输出的结构化数据

        Returns:
            通俗化后的最终日报数据
        """
        try:
            # 构建输入文本
            digest_json = json.dumps(digested_news, ensure_ascii=False)

            # 构建说人话层prompt
            prompt = self._build_translator_prompt(digest_json)

            logger.info("开始使用Doubao进行通俗化改写...")

            # 调用Doubao API
            response = self._call_doubao_api(prompt)

            # 解析返回的JSON
            final_news = self._parse_doubao_response(response)

            logger.info("Doubao说人话层处理完成")

            return final_news

        except Exception as e:
            logger.error(f"Doubao说人话层发生错误: {str(e)}")
            raise

    def _build_translator_prompt(self, digest_json: str) -> str:
        """构建说人话层的prompt"""
        return f"""【角色定义】
你是一位能把复杂事情讲得很简单的科普达人。
你的受众是完全没有技术背景的普通人——可能是餐饮老板、中学老师、退休阿姨。
你的风格是：准确但不卖弄、生动但不失真、
像一个懂AI的朋友在饭桌上跟你聊，而不是在讲课或播新闻。

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
   - 要体现"为什么值得普通人关注"

2. summary改写规则：
   - 控制在40字以内
   - 语气像"跟朋友发微信"，不像"新闻播报"
   - 假设读者完全不知道任何AI概念

3. why_important改写规则：
   - 必须回答"这件事会不会影响我的工作、生活或钱包？"
   - 禁止只是重复summary的内容
   - 用读者熟悉的生活场景打比方，例如：
     "就像超市收银员被自助收银机取代一样，这次是..."

4. 术语处理规则：
   - 所有技术术语第一次出现时必须用括号加注解释
   - 解释方式必须用日常生活中的事物打比方，例如：
     大模型（一种像"超级大脑"一样的AI程序，读过的书比任何人都多）
     多模态（能同时看图、听声音、读文字的AI，像人一样用多种感官理解世界）
     RAG（给AI配了个"随身图书馆"，让它回答问题时能查资料而不是全靠记忆）
   - 禁止直接删除术语，必须解释

5. insight改写规则：
   - trend用"今天AI圈有个值得注意的趋势："开头
   - risk用"不过有一点需要留意："开头
   - 语气保持平和，不制造恐慌，不过度乐观
   - 必须说清楚趋势或风险跟普通人有没有关系

6. digest_table和further_reading的title做最小化改写：
   去掉术语或用括号注释，让标题更易读，不需要大幅改动

【质量红线】
1. 禁止改变任何事实，如有不确定的内容保持原文
2. 禁止删除术语，只能加注解释，不能因为"太难"就直接删掉
3. 禁止输出任何JSON格式以外的内容，不要有前言、后记、说明文字
4. 禁止why_important写成summary的重复，必须体现与普通读者的关联
5. 禁止使用"赋能""迭代""范式"等行业黑话，一律替换成日常用语
6. 禁止语气变成教科书、百科全书或新闻播报风格

【输出格式】
严格按照以下JSON结构输出，不输出任何JSON以外的内容：

{{
  "date": "日期保持不变",
  "audience": "非专业人士",
  "top5": [
    {{
      "id": 1,
      "title": "通俗化后的一句话标题，无未解释术语",
      "summary": "通俗化后的一句话摘要（40字以内，微信聊天语气）",
      "source_url": "URL保持不变",
      "why_important": "回答'这件事会不会影响我的工作/生活/钱包'（50-80字）"
    }}
  ],
  "digest_table": [
    {{
      "id": 1,
      "category": "保持消化层的分类不变",
      "title": "轻度通俗化的标题",
      "importance": "高 / 中 / 低"
    }}
  ],
  "further_reading": [
    {{
      "title": "轻度通俗化的标题",
      "url": "URL保持不变"
    }}
  ],
  "insight": {{
    "trend": "以'今天AI圈有个值得注意的趋势：'开头（100字以内）",
    "risk": "以'不过有一点需要留意：'开头（50字以内）"
  }}
}}

请严格按照以上格式输出，现在开始通俗化改写。"""

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
            'temperature': 0.4,  # 稍高的温度以获得更生动的表达
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