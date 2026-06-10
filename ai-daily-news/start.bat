@echo off
echo ================================================
echo   AI Daily News - 启动脚本
echo ================================================

echo.
echo 📦 检查依赖...
cd backend
python -c "import flask, requests, dotenv" 2>nul
if errorlevel 1 (
    echo ❌ 缺少依赖包，正在安装...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ 依赖安装失败，请手动运行: pip install -r requirements.txt
        pause
        exit /b 1
    )
)

echo.
echo 🧪 测试API连接...
python test_api.py
if errorlevel 1 (
    echo.
    echo ❌ API测试失败，请检查 .env 文件中的密钥配置
    echo    按任意键继续启动服务，或按 Ctrl+C 取消...
    pause
)

echo.
echo 🚀 启动API服务器...
echo "服务器将在 http://localhost:5000 启动"
echo "前端页面: 请双击打开 frontend/index.html"
echo.
echo "按 Ctrl+C 停止服务器"
echo.

python api.py

pause