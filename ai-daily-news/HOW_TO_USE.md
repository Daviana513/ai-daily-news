# 🚀 使用指南 - 老张代理版本

## 📝 配置说明

您的系统已配置为使用以下API服务：

- **Gemini API**: 通过老张代理服务
- **Doubao API**: 通过火山引擎ARK API

## 🔑 API密钥配置

您的 `.env` 文件已包含以下配置：

```env
# Gemini API配置（通过老张代理）
GEMINI_API_KEY=sk-qzrIjuE6d0cDhqTC98C4E6Ae0aDe4aCbA4Ed161027EdDdBb
GEMINI_BASE_URL=www.laozhang.ai

# Doubao API配置（通过火山引擎ARK）
ARK_API_KEY=ark-7ac4d5f3-13ad-4ec0-8ecb-72ca75b0adcf-9fa34
```

## 📦 安装依赖

```bash
# 进入后端目录
cd Desktop/ai-daily-news/backend

# 安装Python依赖
pip install -r requirements.txt
```

## 🧪 测试API连接

在启动服务前，先测试API密钥是否正常工作：

```bash
# 在backend目录下运行
python test_api.py
```

您应该看到类似这样的输出：

```
🚀 开始测试API密钥配置...

🧪 测试 Gemini API（老张代理）...
✅ Gemini API 工作正常
   响应: 你好！我是Gemini，一个由Google开发的大型语言模型...

🧪 测试 Doubao API（ARK）...
✅ Doubao API 工作正常
   响应: 你好！我是豆包，字节跳动的AI助手...

==================================================
🎉 所有API密钥配置正确！系统可以正常使用。
```

## 🚀 启动服务

API测试通过后，启动主服务：

```bash
# 在backend目录下运行
python api.py
```

您应该看到：

```
INFO: Gemini采集层初始化完成（使用老张代理）
INFO: Doubao消化层初始化完成（使用ARK API）
INFO: Doubao说人话层初始化完成（使用ARK API）
INFO: API密钥配置检查通过
 * Running on http://0.0.0.0:5000
```

## 🌐 打开前端

**方法1：直接打开**
```bash
# 直接双击打开 frontend/index.html 文件
```

**方法2：使用本地服务器**
```bash
# 在frontend目录下运行
cd ../frontend
python -m http.server 3000
# 然后访问 http://localhost:3000
```

## 🎯 测试完整流程

1. 打开前端页面
2. 点击"生成今日日报"按钮
3. 观察加载进度（采集→消化→说人话）
4. 查看生成的AI资讯日报

## ⚠️ 故障排除

### API测试失败

**Gemini API 失败：**
- 检查 `GEMINI_API_KEY` 是否正确
- 确认 `GEMINI_BASE_URL` 设置为 `www.laozhang.ai`
- 检查网络连接

**Doubao API 失败：**
- 检查 `ARK_API_KEY` 是否正确
- 确认ARK API额度是否充足
- 检查网络连接

### 生成日报失败

1. **检查API状态**：
   ```bash
   python test_api.py
   ```

2. **查看详细日志**：
   在 `api.py` 的日志输出中查看具体错误信息

3. **检查网络连接**：
   确保能够访问外部API服务

### 速度慢或超时

- Gemini联网搜索可能需要1-2分钟
- Doubao处理需要30-60秒
- 整个流程预计需要2-3分钟

## 📊 监控使用情况

### API调用次数

每次生成日报会调用：
- Gemini API: 1次（采集层）
- Doubao API: 2次（消化层+说人话层）

### 费用估算

- Gemini: 按输入/输出token计费
- Doubao: 按使用量计费

建议监控API使用量，避免超支。

## 🔄 更新API密钥

如果需要更换API密钥：

1. 编辑 `backend/.env` 文件
2. 更新对应的 `API_KEY` 值
3. 重启API服务器
4. 运行 `python test_api.py` 验证

## 🚀 下一步

配置完成后，您可以：

1. **本地测试**：确保一切正常工作
2. **部署到生产环境**：参考 `DEPLOYMENT.md`
3. **定制化**：根据需要调整prompt和输出格式

## 📞 获取帮助

如果遇到问题：

1. 检查 `.env` 文件配置
2. 运行 `python test_api.py` 诊断
3. 查看控制台详细日志
4. 参考 `README.md` 和 `DEPLOYMENT.md`

---

**现在您可以开始使用AI资讯日报系统了！** 🎉