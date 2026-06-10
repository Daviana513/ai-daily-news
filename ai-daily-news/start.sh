#!/bin/bash

echo "================================================"
echo "  AI Daily News - 启动脚本"
echo "================================================"

echo ""
echo "📦 检查依赖..."
cd backend
python3 -c "import flask, requests, dotenv" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ 缺少依赖包，正在安装..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ 依赖安装失败，请手动运行: pip3 install -r requirements.txt"
        exit 1
    fi
fi

echo ""
echo "🧪 测试API连接..."
python3 test_api.py
if [ $? -ne 0 ]; then
    echo ""
    echo "❌ API测试失败，请检查 .env 文件中的密钥配置"
    echo "   按Enter继续启动服务，或按Ctrl+C取消..."
    read
fi

echo ""
echo "🚀 启动API服务器..."
echo "服务器将在 http://localhost:5000 启动"
echo "前端页面: 请在浏览器中打开 frontend/index.html"
echo ""
echo "按Ctrl+C停止服务器"
echo ""

python3 api.py