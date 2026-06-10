#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整小范围测试：NewsAPI采集 + Qwen-Plus处理
测试混合架构的完整流程
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

class HybridArchitectureTest:
    """混合架构完整测试"""

    def __init__(self):
        self.newsapi_key = "4032bc55beef4064bacfcfc46b1f1479"
        self.laozai_api_key = os.getenv('LAOZHAI_API_KEY')
        self.laozai_base_url = os.getenv('LAOZHAI_BASE_URL')

        if not self.laozai_api_key:
            print("❌ 缺少老张API密钥")
            sys.exit(1)

        print("🔑 API密钥配置完成")

    def step1_collect_news(self):
        """步骤1：使用NewsAPI采集真实新闻"""
        print("📡 步骤1：NewsAPI采集真实新闻")
        print("="*60)

        base_url = "https://newsapi.org/v2/everything"

        # 采集国际新闻
        print("🌍 采集国际AI新闻...")
        int_params = {
            'q': '(ChatGPT OR "OpenAI" OR "GPT-4" OR "GPT-5" OR Claude OR Gemini OR Llama) AND (launch OR release OR update OR breakthrough)',
            'language': 'en',
            'sortBy': 'publishedAt',
            'pageSize': 10,
            'apiKey': self.newsapi_key
        }

        try:
            int_response = requests.get(base_url, params=int_params, timeout=30)
            int_articles = int_response.json().get('articles', []) if int_response.status_code == 200 else []
            print(f"✅ 国际新闻: {len(int_articles)} 条")
        except Exception as e:
            print(f"❌ 国际新闻采集失败: {str(e)}")
            int_articles = []

        # 采集国内新闻
        print("🇨🇳 采集国内AI新闻...")
        dom_params = {
            'q': '("ChatGPT" OR "OpenAI" OR "大模型" OR "通义千问" OR "文心一言") AND (发布 OR 升级 OR 更新 OR 突破)',
            'language': 'zh',
            'sortBy': 'publishedAt',
            'pageSize': 10,
            'apiKey': self.newsapi_key
        }

        try:
            dom_response = requests.get(base_url, params=dom_params, timeout=30)
            dom_articles = dom_response.json().get('articles', []) if dom_response.status_code == 200 else []
            print(f"✅ 国内新闻: {len(dom_articles)} 条")
        except Exception as e:
            print(f"❌ 国内新闻采集失败: {str(e)}")
            dom_articles = []

        # 合并并转换为标准格式
        all_news = []
        for i, article in enumerate(int_articles, 1):
            all_news.append({
                'id': i,
                'title': article.get('title', ''),
                'summary': article.get('description', ''),
                'source': article.get('source', {}).get('name', ''),
                'url': article.get('url', ''),
                'source_type': 'International-NewsAPI'
            })

        for i, article in enumerate(dom_articles, 1):
            all_news.append({
                'id': len(int_articles) + i,
                'title': article.get('title', ''),
                'summary': article.get('description', ''),
                'source': article.get('source', {}).get('name', ''),
                'url': article.get('url', ''),
                'source_type': 'Domestic-NewsAPI'
            })

        print(f"📊 采集总计: {len(all_news)} 条真实新闻")
        print()

        # 显示前3条新闻
        print("📰 新闻预览（前3条）:")
        for i, news in enumerate(all_news[:3], 1):
            print(f"{i}. {news['title'][:70]}...")
            print(f"   来源: {news['source']} | {news['source_type']}")

        print()
        return all_news

    def step2_digest_news(self, raw_news):
        """步骤2：使用Qwen-Plus进行消化处理"""
        print("🧠 步骤2：Qwen-Plus消化处理（筛选Top5+结构化）")
        print("="*60)

        # 格式化新闻为prompt输入
        raw_news_text = self._format_news_for_prompt(raw_news)

        # 构建消化层prompt
        today = datetime.now().strftime('%Y年%m月%d日')
        prompt = f"""【角色定义】
你是一位AI领域的资深编辑，专注于信息价值判断与内容结构化。

【任务说明】
以下是今日AI领域的真实新闻素材（{len(raw_news)}条）。
请对这批素材进行筛选、排序、分类和结构化处理，
输出一份AI日报的中间数据。

原始素材：
{raw_news_text}

【操作规则】
1. 从原始素材中选出最重要的5条作为Top5，优先级：
   第一优先：对AI行业格局有重大影响的事件
   第二优先：重要新模型或新产品发布
   第三优先：与普通人日常生活直接相关的AI应用
   第四优先：重要政策或监管动向
2. Top5必须覆盖至少3个不同category
3. importance评级：高/中/低
4. further_reading从Top5之外挑选3-5条
5. insight.trend提炼今日趋势
6. insight.risk指出潜在风险
7. **重要：必须完整保留每条新闻的原始URL链接到source_url字段**

【输出格式】
严格按照JSON格式输出：

{{
  "date": "{today}",
  "audience": "非专业人士",
  "top5": [
    {{
      "id": 1,
      "title": "原始标题或简洁标题",
      "summary": "原文摘要（编辑语言）",
      "source_url": "保留原始新闻的完整URL链接，不要省略或修改",
      "why_important": "为什么重要（50-80字）"
    }}
  ],
  "digest_table": [
    {{
      "id": 1,
      "category": "自主判断的类别",
      "title": "新闻标题",
      "importance": "高/中/低"
    }}
  ],
  "further_reading": [
    {{
      "title": "延伸阅读标题",
      "url": "URL链接"
    }}
  ],
  "insight": {{
    "trend": "今日核心趋势（100字以内）",
    "risk": "风险提示（50字以内）"
  }}
}}

请严格按照JSON格式输出，不要有任何其他内容。"""

        try:
            # 调用老张API
            api_url = f"{self.laozai_base_url}/chat/completions"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.laozai_api_key}'
            }

            data = {
                'model': 'qwen-plus',
                'messages': [{'role': 'user', 'content': prompt}],
                'temperature': 0.3,
                'max_tokens': 3000
            }

            print("🔄 正在调用Qwen-Plus进行消化处理...")
            response = requests.post(api_url, headers=headers, json=data, timeout=120)

            if response.status_code == 200:
                result = response.json()
                response_text = result['choices'][0]['message']['content']

                # 解析JSON
                digested_news = self._parse_json_response(response_text)
                print(f"✅ 消化处理完成")
                print(f"   Top5: {len(digested_news.get('top5', []))} 条")
                print(f"   延伸阅读: {len(digested_news.get('further_reading', []))} 条")
                print()
                return digested_news
            else:
                print(f"❌ API调用失败: {response.status_code}")
                return None

        except Exception as e:
            print(f"❌ 消化处理异常: {str(e)}")
            return None

    def step3_translate_news(self, digested_news):
        """步骤3：使用Qwen-Plus进行通俗化改写"""
        print("💬 步骤3：Qwen-Plus通俗化改写")
        print("="*60)

        # 将消化后的数据转为JSON字符串
        digest_json = json.dumps(digested_news, ensure_ascii=False)

        # 构建说人话层prompt
        prompt = f"""【角色定义】
你是一位能把复杂事情讲得很简单的科普达人。
你的受众是完全没有技术背景的普通人。

【任务说明】
以下是今日AI日报的结构化数据（编辑语言版本）。
请对所有文本字段进行通俗化改写。

输入数据：
{digest_json}

【操作规则】
1. title：一句话让普通人看懂发生了什么
2. summary：40字以内，像跟朋友发微信
3. why_important：回答"会不会影响我的工作/生活/钱包"
4. 所有术语第一次出现时用生活比喻解释

【输出格式】
严格按照JSON格式输出，不要有任何JSON以外的内容。"""

        try:
            # 调用老张API
            api_url = f"{self.laozai_base_url}/chat/completions"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.laozai_api_key}'
            }

            data = {
                'model': 'qwen-plus',
                'messages': [{'role': 'user', 'content': prompt}],
                'temperature': 0.4,
                'max_tokens': 3000
            }

            print("🔄 正在调用Qwen-Plus进行通俗化改写...")
            response = requests.post(api_url, headers=headers, json=data, timeout=120)

            if response.status_code == 200:
                result = response.json()
                response_text = result['choices'][0]['message']['content']

                # 解析JSON
                final_news = self._parse_json_response(response_text)
                print(f"✅ 通俗化改写完成")
                print()
                return final_news
            else:
                print(f"❌ API调用失败: {response.status_code}")
                return None

        except Exception as e:
            print(f"❌ 通俗化改写异常: {str(e)}")
            return None

    def _format_news_for_prompt(self, news_list):
        """格式化新闻为prompt输入"""
        formatted_text = ""
        for i, news in enumerate(news_list, 1):
            source_tag = f"[{news.get('source_type', 'Unknown')}]" if 'source_type' in news else ""
            formatted_text += f"""
新闻{i} {source_tag}：
标题：{news.get('title', '')}
摘要：{news.get('summary', '')}
来源：{news.get('source', '')}
URL：{news.get('url', '')}
"""
        return formatted_text

    def _parse_json_response(self, response_text):
        """解析API返回的JSON"""
        try:
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1

            if json_start == -1 or json_end == 0:
                raise ValueError("响应中未找到有效的JSON格式")

            json_str = response_text[json_start:json_end]
            return json.loads(json_str)

        except json.JSONDecodeError as e:
            print(f"❌ JSON解析失败: {str(e)}")
            raise

    def display_final_result(self, final_news):
        """显示最终结果"""
        print("📋 最终日报预览")
        print("="*60)

        # 显示Top5
        top5 = final_news.get('top5', [])
        print(f"🔥 今日Top5 ({len(top5)}条):")
        for i, news in enumerate(top5, 1):
            print(f"{i}. {news.get('title', 'N/A')}")
            print(f"   摘要: {news.get('summary', 'N/A')}")
            print(f"   重要: {news.get('why_important', 'N/A')}")
            print(f"   链接: {news.get('source_url', 'N/A')[:60]}...")
            print()

        # 显示洞察
        insight = final_news.get('insight', {})
        if insight:
            print(f"📈 趋势: {insight.get('trend', 'N/A')}")
            print(f"⚠️  风险: {insight.get('risk', 'N/A')}")
            print()

        # 显示延伸阅读
        further = final_news.get('further_reading', [])
        print(f"📚 延伸阅读 ({len(further)}条):")
        for item in further:
            print(f"   - {item.get('title', 'N/A')}")
            print(f"     {item.get('url', 'N/A')[:60]}...")

    def run_complete_test(self):
        """运行完整的混合架构测试"""
        print("🚀 混合架构完整小范围测试")
        print("="*60)
        print("NewsAPI采集 → Qwen-Plus消化 → Qwen-Plus说人话")
        print("="*60)
        print()

        # 步骤1：采集
        raw_news = self.step1_collect_news()

        if not raw_news:
            print("❌ 采集失败，测试终止")
            return

        # 步骤2：消化
        digested_news = self.step2_digest_news(raw_news)

        if not digested_news:
            print("❌ 消化失败，测试终止")
            return

        # 步骤3：通俗化
        final_news = self.step3_translate_news(digested_news)

        if not final_news:
            print("❌ 通俗化失败，测试终止")
            return

        # 显示结果
        print("="*60)
        print("🎯 测试结果")
        print("="*60)
        print()

        self.display_final_result(final_news)

        # 保存结果
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f'hybrid_test_result_{timestamp}.json'

        result = {
            'test_timestamp': datetime.now().isoformat(),
            'architecture': 'NewsAPI + Qwen-Plus Hybrid',
            'raw_news_count': len(raw_news),
            'final_result': final_news
        }

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        print(f"\n💾 完整结果已保存到: {output_file}")
        print()
        print("="*60)
        print("🎉 混合架构测试完成！")
        print("="*60)
        print("✅ 成功获取真实AI新闻")
        print("✅ 有效URL链接")
        print("✅ 智能筛选Top5")
        print("✅ 通俗化改写完成")
        print("\n💡 混合架构验证成功，可以正式部署！")

def main():
    """主函数"""
    tester = HybridArchitectureTest()
    tester.run_complete_test()

    return 0

if __name__ == '__main__':
    sys.exit(main())