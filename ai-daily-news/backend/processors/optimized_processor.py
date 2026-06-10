#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
优化版处理器
减少处理时间，提升用户体验
"""

import os
import json
import logging
import requests
from typing import List, Dict, Any
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# 禁用SSL警告
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()

logger = logging.getLogger(__name__)

class OptimizedDigester:
    """优化版消化层：更快速的处理"""

    def __init__(self):
        self.api_key = os.getenv('LAOZHAI_API_KEY')
        self.api_base_url = os.getenv('LAOZHAI_BASE_URL')
        self.model = os.getenv('PROCESSOR_MODEL', 'qwen-plus')
        self.api_url = f"{self.api_base_url}/chat/completions"
        logger.info("优化消化层初始化完成")

    def digest_news_fast(self, raw_news: List[Dict[str, Any]], today: str) -> Dict[str, Any]:
        """快速消化处理"""
        try:
            # 保存原始URL映射
            url_mapping = {i: news.get('url', '') for i, news in enumerate(raw_news, 1)}

            # 优化prompt，保持清晰但更简洁
            raw_news_text = self._format_news_compact(raw_news)

            prompt = f"""你是一个AI新闻编辑，请从以下{len(raw_news)}条AI新闻中选择最重要的5条。

选择标准：
1. 覆盖不同类别（至少3个类别）
2. 优先级：技术突破>产品发布>行业动态>融资消息
3. 对普通人有实际影响

新闻列表：
{raw_news_text}

**关键指令**：
1. 用序号标识你选择的新闻（1-{len(raw_news)}）
2. 输出时，在source_url字段填写新闻序号
3. 后续会自动将序号替换为真实URL

请输出JSON格式（只输出JSON，不要其他内容）：
{{
  "date": "{today}",
  "top5": [
    {{"title": "新闻标题", "summary": "简要摘要", "source_url": "序号(1-{len(raw_news)})", "why_important": "为什么重要"}}
  ],
  "digest_table": [
    {{"category": "类别", "title": "标题", "importance": "高/中/低"}}
  ],
  "further_reading": [
    {{"title": "标题", "url": "序号(1-{len(raw_news)})"}}
  ],
  "insight": {{
    "trend": "今日趋势观察",
    "risk": "潜在风险提示"
  }}
}}"""

            result = self._call_api_fast(prompt)

            # 将序号替换为真实URL
            result = self._replace_url_numbers(result, url_mapping, raw_news)

            return result

        except Exception as e:
            logger.error(f"快速消化失败: {str(e)}")
            raise

    def _replace_url_numbers(self, result: Dict[str, Any], url_mapping: Dict[int, str], raw_news: List[Dict[str, Any]]) -> Dict[str, Any]:
        """将URL序号替换为真实URL"""
        try:
            # 替换top5中的source_url
            if 'top5' in result:
                for item in result['top5']:
                    source_url = item.get('source_url', '')
                    if source_url.isdigit():
                        news_index = int(source_url)
                        if news_index in url_mapping:
                            item['source_url'] = url_mapping[news_index]

            # 替换further_reading中的url
            if 'further_reading' in result:
                for item in result['further_reading']:
                    url = item.get('url', '')
                    if url.isdigit():
                        news_index = int(url)
                        if news_index in url_mapping:
                            item['url'] = url_mapping[news_index]

            return result

        except Exception as e:
            logger.error(f"URL替换失败: {str(e)}")
            return result

    def _format_news_compact(self, news_list: List[Dict[str, Any]]) -> str:
        """紧凑格式化新闻，减少token数量"""
        formatted = ""
        for i, news in enumerate(news_list, 1):
            formatted += f"{i}.{news.get('title', '')}摘要:{news.get('summary', '')}\n"
        return formatted

    def _call_api_fast(self, prompt: str) -> Dict[str, Any]:
        """快速API调用"""
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }

        data = {
            'model': self.model,
            'messages': [{'role': 'user', 'content': prompt}],
            'temperature': 0.3,
            'max_tokens': 2000  # 增加token数量以完整返回JSON
        }

        try:
            # 创建session并配置重试机制
            session = requests.Session()
            retry_strategy = Retry(
                total=3,
                backoff_factor=1,
                status_forcelist=[429, 500, 502, 503, 504],
                allowed_methods=["POST"]
            )
            adapter = HTTPAdapter(max_retries=retry_strategy)
            session.mount("https://", adapter)
            session.mount("http://", adapter)

            # 禁用SSL验证（解决SSL连接问题）
            response = session.post(
                self.api_url,
                headers=headers,
                json=data,
                timeout=180,
                verify=False  # 禁用SSL验证
            )
            response.raise_for_status()

            result = response.json()
            response_text = result['choices'][0]['message']['content']
            return self._parse_response(response_text)

        except requests.exceptions.SSLError as e:
            logger.error(f"SSL连接错误: {str(e)}")
            logger.error("尝试使用无SSL验证的方式...")
            # 如果SSL验证失败，尝试禁用验证
            try:
                response = requests.post(
                    self.api_url,
                    headers=headers,
                    json=data,
                    timeout=180,
                    verify=False
                )
                response.raise_for_status()
                result = response.json()
                response_text = result['choices'][0]['message']['content']
                return self._parse_response(response_text)
            except Exception as retry_error:
                logger.error(f"重试失败: {str(retry_error)}")
                raise
        except Exception as e:
            logger.error(f"API调用失败: {str(e)}")
            raise

    def _parse_response(self, response_text: str) -> Dict[str, Any]:
        """解析API响应"""
        try:
            logger.info(f"原始响应长度: {len(response_text)}")

            # 方法1: 直接尝试解析整个响应
            try:
                return json.loads(response_text.strip())
            except json.JSONDecodeError:
                pass

            # 方法2: 提取JSON部分（找到第一个完整的JSON对象）
            json_start = response_text.find('{')
            if json_start == -1:
                # 尝试清除可能的markdown代码块标记
                if "```json" in response_text:
                    response_text = response_text.split("```json")[1].split("```")[0]
                    json_start = response_text.find('{')
                if json_start == -1:
                    raise ValueError("响应中没有找到JSON开始标记")

            # 寻找匹配的结束括号
            brace_count = 0
            json_end = -1

            for i in range(json_start, len(response_text)):
                char = response_text[i]
                if char == '{':
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        json_end = i + 1
                        break

            if json_end == -1:
                # 如果找不到完整JSON，尝试到最后一个}
                last_brace = response_text.rfind('}')
                if last_brace > json_start:
                    json_end = last_brace + 1
                    logger.warning("JSON可能不完整，尝试修复")
                else:
                    raise ValueError("响应中没有找到完整的JSON对象")

            json_str = response_text[json_start:json_end]
            logger.info(f"提取的JSON长度: {len(json_str)}")

            # 尝试解析提取的JSON
            result = json.loads(json_str)
            logger.info("JSON解析成功")
            return result

        except json.JSONDecodeError as e:
            logger.error(f"JSON解析失败: {str(e)}")
            logger.error(f"响应内容前500字符: {response_text[:500]}")
            logger.error(f"响应内容后500字符: {response_text[-500:]}")
            raise
        except Exception as e:
            logger.error(f"解析异常: {str(e)}")
            raise

class OptimizedTranslator:
    """优化版说人话层：更快速的改写"""

    def __init__(self):
        self.api_key = os.getenv('LAOZHAI_API_KEY')
        self.api_base_url = os.getenv('LAOZHAI_BASE_URL')
        self.model = os.getenv('PROCESSOR_MODEL', 'qwen-plus')
        self.api_url = f"{self.api_base_url}/chat/completions"
        logger.info("优化说人话层初始化完成")

    def translate_fast(self, digested_news: Dict[str, Any]) -> Dict[str, Any]:
        """快速通俗化改写"""
        try:
            digest_json = json.dumps(digested_news, ensure_ascii=False)

            prompt = f"""你是AI科普专家，把技术新闻变成普通人能懂的内容。

输入数据：
{digest_json}

改写要求：
1. 标题：一句话让普通人看懂（用比喻、生活化语言）
2. 摘要：40字内，微信聊天语气
3. 为什么重要：直接回答"会不会影响我的工作/生活/钱包"
4. 术语解释：用生活比喻（例如："API就像餐厅服务员"）
5. 趋势：用"今天AI圈有个值得注意的趋势："开头
6. 风险：用"不过有一点需要留意："开头

**重要：保持原JSON结构不变，只改写文本内容。特别是source_url字段必须保留原始链接。**

请输出JSON格式（只输出JSON，不要其他内容）：
{{
  "date": "保留原date",
  "top5": [
    {{"title": "通俗化标题", "summary": "聊天式摘要", "source_url": "保留原URL链接", "why_important": "为什么重要"}}
  ],
  "digest_table": [
    {{"category": "保留原类别", "title": "保留原标题", "importance": "保留原重要性"}}
  ],
  "further_reading": [
    {{"title": "保留原标题", "url": "保留原URL链接"}}
  ],
  "insight": {{
    "trend": "今天AI圈有个值得注意的趋势：...",
    "risk": "不过有一点需要留意：..."
  }}
}}"""

            return self._call_api_fast(prompt)

        except Exception as e:
            logger.error(f"快速改写失败: {str(e)}")
            raise

    def _call_api_fast(self, prompt: str) -> Dict[str, Any]:
        """快速API调用"""
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }

        data = {
            'model': self.model,
            'messages': [{'role': 'user', 'content': prompt}],
            'temperature': 0.4,
            'max_tokens': 2500  # 增加token数量以完整返回JSON
        }

        try:
            # 创建session并配置重试机制
            session = requests.Session()
            retry_strategy = Retry(
                total=3,
                backoff_factor=1,
                status_forcelist=[429, 500, 502, 503, 504],
                allowed_methods=["POST"]
            )
            adapter = HTTPAdapter(max_retries=retry_strategy)
            session.mount("https://", adapter)
            session.mount("http://", adapter)

            # 禁用SSL验证（解决SSL连接问题）
            response = session.post(
                self.api_url,
                headers=headers,
                json=data,
                timeout=180,
                verify=False  # 禁用SSL验证
            )
            response.raise_for_status()

            result = response.json()
            response_text = result['choices'][0]['message']['content']
            return self._parse_response(response_text)

        except requests.exceptions.SSLError as e:
            logger.error(f"SSL连接错误: {str(e)}")
            logger.error("尝试使用无SSL验证的方式...")
            # 如果SSL验证失败，尝试禁用验证
            try:
                response = requests.post(
                    self.api_url,
                    headers=headers,
                    json=data,
                    timeout=180,
                    verify=False
                )
                response.raise_for_status()
                result = response.json()
                response_text = result['choices'][0]['message']['content']
                return self._parse_response(response_text)
            except Exception as retry_error:
                logger.error(f"重试失败: {str(retry_error)}")
                raise
        except Exception as e:
            logger.error(f"API调用失败: {str(e)}")
            raise

    def _parse_response(self, response_text: str) -> Dict[str, Any]:
        """解析API响应"""
        try:
            logger.info(f"原始响应长度: {len(response_text)}")

            # 方法1: 直接尝试解析整个响应
            try:
                return json.loads(response_text.strip())
            except json.JSONDecodeError:
                pass

            # 方法2: 提取JSON部分（找到第一个完整的JSON对象）
            json_start = response_text.find('{')
            if json_start == -1:
                # 尝试清除可能的markdown代码块标记
                if "```json" in response_text:
                    response_text = response_text.split("```json")[1].split("```")[0]
                    json_start = response_text.find('{')
                if json_start == -1:
                    raise ValueError("响应中没有找到JSON开始标记")

            # 寻找匹配的结束括号
            brace_count = 0
            json_end = -1

            for i in range(json_start, len(response_text)):
                char = response_text[i]
                if char == '{':
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        json_end = i + 1
                        break

            if json_end == -1:
                # 如果找不到完整JSON，尝试到最后一个}
                last_brace = response_text.rfind('}')
                if last_brace > json_start:
                    json_end = last_brace + 1
                    logger.warning("JSON可能不完整，尝试修复")
                else:
                    raise ValueError("响应中没有找到完整的JSON对象")

            json_str = response_text[json_start:json_end]
            logger.info(f"提取的JSON长度: {len(json_str)}")

            # 尝试解析提取的JSON
            result = json.loads(json_str)
            logger.info("JSON解析成功")
            return result

        except json.JSONDecodeError as e:
            logger.error(f"JSON解析失败: {str(e)}")
            logger.error(f"响应内容前500字符: {response_text[:500]}")
            logger.error(f"响应内容后500字符: {response_text[-500:]}")
            raise
        except Exception as e:
            logger.error(f"解析异常: {str(e)}")
            raise

# 使用示例
"""
# 使用优化版处理器
digester = OptimizedDigester()
translator = OptimizedTranslator()

# 快速处理
digested = digester.digest_news_fast(raw_news, today)
final = translator.translate_fast(digested)
"""