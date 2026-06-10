# 快速开始指南

## 🚀 5分钟启动你的AI资讯日报

### 第一步：获取API密钥

#### Gemini API密钥
1. 访问 [Google AI Studio](https://aistudio.google.com/)
2. 点击"Create API Key"
3. 选择或创建一个项目
4. 复制生成的API密钥

#### Doubao API密钥
1. 访问 [火山引擎控制台](https://console.volcengine.com/)
2. 开通"机器学习平台"服务
3. 进入"API密钥管理"
4. 创建新的API密钥并复制

### 第二步：配置后端

```bash
# 进入后端目录
cd Desktop/ai-daily-news/backend

# 安装依赖
pip install -r requirements.txt

# 创建环境变量文件
cp .env.example .env

# 编辑.env文件，填入你的API密钥
# GEMINI_API_KEY=你的Gemini密钥
# DOUBAO_API_KEY=你的Doubao密钥
```

### 第三步：启动服务

```bash
# 启动API服务器
python api.py

# 服务将在 http://localhost:5000 启动
```

### 第四步：打开前端

```bash
# 在浏览器中打开前端文件
# 直接双击打开 frontend/index.html 文件
# 或者使用本地服务器：
cd frontend
python -m http.server 3000
```

访问 `http://localhost:3000`，点击"生成今日日报"按钮。

## 🎯 本地测试清单

- [ ] API服务器正常运行（访问 http://localhost:5000/health）
- [ ] 前端页面能正常打开
- [ ] 点击按钮能看到加载动画
- [ ] 能成功生成日报内容
- [ ] 内容格式正确，无乱码

## 🚀 准备部署到生产环境

当本地测试通过后，按照 [DEPLOYMENT.md](./DEPLOYMENT.md) 的指南进行部署：

1. 推送代码到GitHub
2. 在Railway部署后端
3. 在Vercel部署前端
4. 修改前端API地址
5. 测试线上版本

## ⚠️ 常见问题

### Q: API连接失败
A: 检查api.py中的API地址配置，确保后端服务正常运行。

### Q: 生成失败
A: 检查API密钥是否正确，查看控制台错误信息。

### Q: 内容质量问题
A: 可以调整processors中的prompt参数。

## 📞 获取帮助

- 查看 [README.md](./README.md) 了解详细说明
- 参考 [DEPLOYMENT.md](./DEPLOYMENT.md) 解决部署问题
- 检查控制台日志获取详细错误信息

## 🎉 开始使用

现在你已经准备好了！点击按钮生成你的第一份AI资讯日报吧。

---

**下一步：** 将系统部署到云端，让更多人使用你的AI资讯日报服务！