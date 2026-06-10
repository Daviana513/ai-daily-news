# 部署指南

## 推荐部署方案

- **前端**：Vercel（静态站点）
- **后端**：Railway 或 Render（Python API服务）

## 第一步：准备代码仓库

```bash
# 1. 创建GitHub仓库
git init
git add .
git commit -m "Initial commit: AI Daily News System"
git remote add origin https://github.com/yourusername/ai-daily-news.git
git push -u origin main
```

## 第二步：部署后端（Railway）

### 2.1 创建Railway账户

1. 访问 [railway.app](https://railway.app/)
2. 使用GitHub账户登录
3. 点击"New Project"

### 2.2 部署Python服务

1. 选择"Deploy from GitHub repo"
2. 选择你的 `ai-daily-news` 仓库
3. Railway会自动检测Python项目

### 2.3 配置环境变量

在Railway项目中设置以下环境变量：

```
GEMINI_API_KEY=your_actual_gemini_key
DOUBAO_API_KEY=your_actual_doubao_key
PORT=5000
```

### 2.4 获取API地址

部署完成后，Railway会提供一个URL，例如：
`https://your-project-name.up.railway.app`

保存这个地址，稍后配置前端时需要使用。

## 第三步：部署前端（Vercel）

### 3.1 创建Vercel账户

1. 访问 [vercel.com](https://vercel.com/)
2. 使用GitHub账户登录

### 3.2 导入项目

1. 点击"Add New Project"
2. 导入你的GitHub仓库
3. Vercel会自动识别为静态站点

### 3.3 配置构建设置

由于是纯HTML+CSS，无需特殊构建设置：

- **Framework Preset**: Other
- **Root Directory**: `frontend`
- **Build Command**: 留空
- **Output Directory**: `.`

### 3.4 修改API地址

在部署前，修改 `frontend/script.js` 中的API地址：

```javascript
// 将API地址改为你的Railway地址
const API_BASE_URL = 'https://your-project-name.up.railway.app';
```

### 3.5 部署

点击"Deploy"按钮，Vercel会自动部署。

部署完成后，你会获得一个URL，例如：
`https://your-project-name.vercel.app`

## 第四步：配置CORS（重要）

为了允许前端调用后端API，需要在后端添加CORS配置。

我们的代码中已经使用了 `flask-cors`，但需要确保配置正确：

```python
# backend/api.py
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 这会允许所有域名的跨域请求
```

如果需要更严格的CORS策略，可以指定具体的前端域名：

```python
CORS(app, resources={r"/api/*": {"origins": "https://your-frontend.vercel.app"}})
```

## 第五步：测试部署

1. 访问你的Vercel前端URL
2. 点击"生成今日日报"按钮
3. 观察是否正常生成日报

## 替代部署方案

### 使用Render部署后端

1. 访问 [render.com](https://render.com/)
2. 创建新的"Web Service"
3. 连接GitHub仓库
4. 设置环境变量
5. Render会自动部署Python应用

### 使用Supabase或Cloudflare Workers

如果需要更灵活的部署方案，可以考虑：

- **Supabase**: 提供数据库和Edge Functions
- **Cloudflare Workers**: 边缘计算，全球分发

## 环境变量管理

### 本地开发

创建 `backend/.env` 文件：

```env
GEMINI_API_KEY=your_gemini_api_key
DOUBAO_API_KEY=your_doubao_api_key
PORT=5000
DEBUG=True
```

### 生产环境

在部署平台的环境变量设置中添加相同的变量，但设置：

```env
DEBUG=False
```

## 监控和日志

### Railway日志

1. 在Railway项目中点击"View Logs"
2. 可以实时查看API服务器的运行状态
3. 检查错误和警告信息

### Vercel分析

1. 在Vercel项目中查看"Analytics"
2. 监控访问量和性能
3. 检查错误率

## 费用估算

### Railway
- 免费层：$5/月信用额度
- 付费层：$5/月起

### Vercel
- 免费层：个人项目完全免费
- 付费层：$20/月起

### API费用
- Gemini: 按使用量计费
- Doubao: 按使用量计费

## 故障排除

### CORS错误

如果前端控制台出现CORS错误：

1. 检查后端的CORS配置
2. 确认前端URL已加入允许列表
3. 检查浏览器控制台的具体错误信息

### API连接失败

1. 检查后端服务是否正常运行
2. 确认API地址配置正确
3. 查看部署平台的日志

### 生成失败

1. 检查API密钥是否正确
2. 确认API额度是否充足
3. 查看后端错误日志

## 域名配置（可选）

### 为前端添加自定义域名

1. 在Vercel项目中点击"Settings"
2. 选择"Domains"
3. 添加你的自定义域名
4. 配置DNS记录

### 为后端添加自定义域名

1. 在Railway项目中点击"Settings"
2. 选择"Domains"
3. 添加自定义域名
4. 配置DNS记录

## 安全建议

1. **API密钥安全**：永远不要将API密钥提交到代码仓库
2. **环境变量**：使用环境变量管理敏感信息
3. **速率限制**：考虑添加API速率限制
4. **错误处理**：不要在错误信息中泄露敏感数据

## 持续部署

配置GitHub集成的自动部署：

- **Railway**：每次推送到主分支自动部署
- **Vercel**：每次推送到主分支自动部署
- 可以在平台设置中关闭自动部署

## 备份和恢复

定期备份重要数据：

1. 导出环境变量配置
2. 备份数据库（如果有）
3. 保存部署配置

这样即使出现问题，也能快速恢复服务。