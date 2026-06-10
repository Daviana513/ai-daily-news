#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
优化版API服务器
集成所有性能优化措施
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import json
from datetime import datetime
import logging
import time

# 导入优化版处理器
from collectors.newsapi_collector import NewsAPICollector
from processors.optimized_processor import OptimizedDigester, OptimizedTranslator

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# 全局变量
latest_daily_news = None
last_update_time = None

@app.route('/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({
        'status': 'healthy',
        'service': 'AI Daily News API (Optimized)',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/generate-daily-news', methods=['POST'])
def generate_daily_news_optimized():
    """生成每日AI资讯日报（优化版）"""
    global latest_daily_news, last_update_time

    try:
        logger.info("开始生成每日AI资讯日报（优化版）...")
        start_time = time.time()

        # 获取今天的日期
        today = datetime.now().strftime('%Y-%m-%d')

        # 步骤1：快速采集
        logger.info("启动NewsAPI采集...")
        collector = NewsAPICollector()
        raw_news = collector.collect_daily_news(today)

        if not raw_news or len(raw_news) < 5:
            return jsonify({
                'success': False,
                'error': '采集的新闻数量不足'
            }), 500

        collect_time = time.time() - start_time
        logger.info(f"采集完成：{len(raw_news)}条新闻，耗时{collect_time:.2f}秒")

        # 步骤2：快速消化（只处理前15条）
        logger.info("启动快速消化处理...")
        digester = OptimizedDigester()

        # 只取前15条新闻进行快速处理
        news_to_process = raw_news[:15]
        digested_news = digester.digest_news_fast(news_to_process, today)

        if not digested_news:
            return jsonify({
                'success': False,
                'error': '消化层处理失败'
            }), 500

        digest_time = time.time() - start_time - collect_time
        logger.info(f"消化完成，耗时{digest_time:.2f}秒")

        # 步骤3：快速通俗化
        logger.info("启动快速通俗化...")
        translator = OptimizedTranslator()
        final_news = translator.translate_fast(digested_news)

        if not final_news:
            return jsonify({
                'success': False,
                'error': '说人话层处理失败'
            }), 500

        translate_time = time.time() - start_time - collect_time - digest_time
        total_time = time.time() - start_time

        logger.info(f"通俗化完成，耗时{translate_time:.2f}秒")
        logger.info(f"总耗时：{total_time:.2f}秒")

        # 更新全局变量
        latest_daily_news = final_news
        last_update_time = datetime.now().isoformat()

        logger.info("每日AI资讯日报生成完成！")

        return jsonify({
            'success': True,
            'data': final_news,
            'generated_at': last_update_time,
            'performance': {
                'total_time': f"{total_time:.2f}秒",
                'collect_time': f"{collect_time:.2f}秒",
                'digest_time': f"{digest_time:.2f}秒",
                'translate_time': f"{translate_time:.2f}秒",
                'news_count': len(raw_news),
                'processed_count': len(news_to_process)
            }
        })

    except Exception as e:
        logger.error(f"生成日报时发生错误: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'服务器错误: {str(e)}'
        }), 500

@app.route('/api/latest-daily-news', methods=['GET'])
def get_latest_daily_news():
    """获取最新生成的日报"""
    if latest_daily_news is None:
        return jsonify({
            'success': False,
            'error': '暂无日报数据，请先生成'
        }), 404

    return jsonify({
        'success': True,
        'data': latest_daily_news,
        'generated_at': last_update_time
    })

@app.route('/api/status', methods=['GET'])
def get_status():
    """获取系统状态"""
    has_news = latest_daily_news is not None

    return jsonify({
        'success': True,
        'status': {
            'has_generated_news': has_news,
            'last_update_time': last_update_time,
            'current_date': datetime.now().strftime('%Y-%m-%d'),
            'optimization': 'enabled'  # 标识为优化版本
        }
    })

if __name__ == '__main__':
    # 检查API密钥配置
    required_keys = ['LAOZHAI_API_KEY', 'LAOZHAI_BASE_URL']
    missing_keys = [key for key in required_keys if not os.getenv(key)]

    if missing_keys:
        logger.error(f"缺少必需的API配置: {', '.join(missing_keys)}")
        logger.error("请在环境变量中设置这些配置，或创建 .env 文件")
    else:
        logger.info("老张代理API配置检查通过")
        logger.info("混合架构：NewsAPI采集 + Qwen-Plus处理（优化版）")

    # 启动服务器
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)