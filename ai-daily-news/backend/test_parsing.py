#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
直接测试解析逻辑
"""

import sys
import json

# 设置控制台编码
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 模拟Gemini响应
gemini_response = """好的，AI领域国际资讯采集员已就位。
以下是根据您的要求，搜索并整理的2026年05月31日海外AI领域重要资讯，共7条：

[1] 标题：OpenAI Unveils 'Prism-X', a New Multimodal Foundation Model Setting Industry Benchmarks
摘要：OpenAI于今日正式发布了其最新一代多模态AI模型"Prism-X"。该模型在理解和生成文本、图像及视频方面实现了突破性进展，并在多项跨模态基准测试中超越了现有模型，预示着更自然人机交互的未来。
来源：TechCrunch
URL：https://techcrunch.com/2026/05/31/openai-prism-x-multimodal-model-release/
---

[2] 标题：EU Parliament Approves Landmark 'AI Act 2.0' with Focus on Data Governance and Transparency
摘要：欧盟议会今日投票通过了修订后的《人工智能法案2.0》最终版本。新法案进一步细化了高风险AI系统的监管框架，尤其强调了数据治理、模型可解释性及用户知情权，旨在确保AI技术在欧洲的负责任发展。
来源：The Verge
URL：https://www.theverge.com/2026/05/31/eu-parliament-ai-act-2-0-passed/
---

[3] 标题：Google DeepMind's 'AlphaMed' Achieves Breakthrough in Personalized Cancer Treatment Planning
摘要：Google DeepMind宣布，其AI系统"AlphaMed"在个性化癌症治疗方案规划上取得了重大突破。通过分析海量患者基因数据和临床记录，AlphaMed能为特定癌症类型推荐更精准、副作用更小的治疗路径。
来源：MIT Technology Review
URL：https://www.technologyreview.com/2026/05/31/google-deepmind-alphamed-cancer-ai-breakthrough/"""

# 模拟Qwen响应
qwen_response = """[1] 标题：百度文心一言4.0正式发布，多模态性能达国际领先水平
摘要：百度于2026年5月31日宣布文心一言4.0全球首发，支持100+语言实时交互，代码生成效率提升60%，已接入百度智能云全生态，助力企业降本增效。
来源：机器之心
URL：https://www.jiqizhixin.com/articles/20260531-baidu-wenxin

[2] 标题：国家发改委发布《人工智能产业创新发展指导意见》
摘要：2026年5月31日，国家发改委正式印发《人工智能产业创新发展指导意见》，明确2030年AI产业规模破10万亿元，重点扶持大模型开源生态及医疗、制造等场景应用落地。
来源：澎湃科技
URL：https://www.thepaper.cn/newsDetail_forward_20260531-123456

[3] 标题：阿里巴巴通义千问3.5医疗AI助手获三甲医院批量部署
摘要：2026年5月31日，阿里云推出通义千问3.5医疗版，影像诊断准确率达98.7%，在150家三甲医院试点，可缩短诊断时间40%，加速分级诊疗推进。
来源：36氪
URL：https://36kr.com/p/1234567890"""

def parse_response_debug(response_text: str, source: str):
    """调试版解析函数"""
    news_list = []
    current_item = {}
    current_field = None

    lines = response_text.strip().split('\n')

    for i, line in enumerate(lines):
        line_stripped = line.strip()

        if not line_stripped or line_stripped == '---':
            if current_item and all(key in current_item for key in ['title', 'summary', 'source', 'url']):
                current_item['source_type'] = source
                news_list.append(current_item)
                current_item = {}
                current_field = None
            continue

        # 检查新条目开始
        if line_stripped.startswith('[') and ']' in line_stripped:
            parts = line_stripped.split(']', 1)
            before_bracket = parts[0].replace('[', '').strip()

            # 如果是数字格式（如 [1], [2]）
            if before_bracket.isdigit():
                if current_item and all(key in current_item for key in ['title', 'summary', 'source', 'url']):
                    current_item['source_type'] = source
                    news_list.append(current_item)
                    current_item = {}
                    current_field = None
                continue

        if line_stripped.startswith('标题：'):
            current_field = 'title'
            current_item['title'] = line_stripped.replace('标题：', '').strip()
        elif line_stripped.startswith('摘要：'):
            current_field = 'summary'
            current_item['summary'] = line_stripped.replace('摘要：', '').strip()
        elif line_stripped.startswith('来源：'):
            current_field = 'source'
            current_item['source'] = line_stripped.replace('来源：', '').strip()
        elif line_stripped.startswith('URL：') or line_stripped.startswith('url：'):
            current_field = 'url'
            current_item['url'] = line_stripped.replace('URL：', '').replace('url：', '').strip()
        elif current_field and current_item.get(current_field):
            current_item[current_field] += ' ' + line_stripped

    # 保存最后一条
    if current_item and all(key in current_item for key in ['title', 'summary', 'source', 'url']):
        current_item['source_type'] = source
        news_list.append(current_item)

    return news_list

def main():
    print("🧪 测试解析逻辑")
    print("="*60)

    print("\n📋 测试Gemini响应解析...")
    gemini_news = parse_response_debug(gemini_response, "Gemini")
    print(f"解析到 {len(gemini_news)} 条新闻")
    for i, news in enumerate(gemini_news, 1):
        print(f"{i}. {news.get('title', 'N/A')[:50]}...")

    print(f"\n📋 测试Qwen响应解析...")
    qwen_news = parse_response_debug(qwen_response, "Qwen")
    print(f"解析到 {len(qwen_news)} 条新闻")
    for i, news in enumerate(qwen_news, 1):
        print(f"{i}. {news.get('title', 'N/A')[:50]}...")

    print(f"\n🎯 总结:")
    print(f"Gemini: {len(gemini_news)} 条")
    print(f"Qwen: {len(qwen_news)} 条")
    print(f"总计: {len(gemini_news) + len(qwen_news)} 条")

    # 保存结果
    all_news = gemini_news + qwen_news
    with open('test_parsed_news.json', 'w', encoding='utf-8') as f:
        json.dump(all_news, f, ensure_ascii=False, indent=2)

    print(f"\n💾 解析结果已保存到 test_parsed_news.json")

    return 0

if __name__ == '__main__':
    sys.exit(main())