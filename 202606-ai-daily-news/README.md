# AI每日资讯日报推送系统

一个为非技术背景人群打造的AI资讯日报系统，通过三层架构处理复杂AI资讯，输出普通人能理解的每日简报。

## 项目特色

- **三层处理架构**：采集层 → 消化层 → 说人话层
- **受众精准**：面向完全没有技术背景的普通人
- **通俗化表达**：将专业术语转化为生活化的比喻
- **一键生成**：简单点击按钮即可获得当日AI资讯日报

## 系统架构

```
用户点击按钮 → 前端发送请求 → Python API → 执行三层处理 → 返回结果 → 前端展示
```

### 三层处理流程

1. **采集层（Gemini）**：联网搜索当日AI原始资讯，返回15-20条原始素材
2. **消化层（Doubao 1.8）**：筛选Top5、分类、评重要性、提炼洞察
3. **说人话层（Doubao 1.8）**：针对非技术背景人群进行通俗化改写

## 项目结构

```
ai-daily-news/
├── backend/                # Python后端
│   ├── api.py             # 主API服务器
│   ├── collectors/        # 采集层
│   │   ├── __init__.py
│   │   └── gemini_collector.py
│   ├── processors/        # 消化层和说人话层
│   │   ├── __init__.py
│   │   ├── doubao_digester.py
│   │   └── doubao_translator.py
│   ├── requirements.txt   # Python依赖
│   └── .env.example      # 环境变量示例
├── frontend/              # 前端界面
│   ├── index.html        # 主页面
│   ├── style.css         # 样式文件
│   └── script.js         # 交互逻辑
└── README.md             # 项目说明
```

## 快速开始

### 1. 环境准备

确保你已安装：
- Python 3.8+
- pip

### 2. 后端设置

```bash
# 进入后端目录
cd backend

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入你的API密钥：
# GEMINI_API_KEY=your_gemini_api_key
# DOUBAO_API_KEY=your_doubao_api_key

# 启动API服务器
python api.py
```

API服务器将在 `http://localhost:5000` 启动。

### 3. 前端部署

```bash
# 部署到Vercel
# 1. 在Vercel中创建新项目
# 2. 连接frontend目录
# 3. 部署设置会自动识别静态文件
# 4. 点击部署
```

### 4. API后端部署

推荐使用 Railway 或 Render：

**Railway部署步骤：**
1. 在 Railway 中创建新项目
2. 连接GitHub仓库
3. Railway会自动识别Python项目
4. 设置环境变量（GEMINI_API_KEY, DOUBAO_API_KEY）
5. 部署完成，获得API URL

**Render部署步骤：**
1. 在 Render 中创建新的Web Service
2. 连接GitHub仓库
3. 设置Python版本和环境变量
4. 部署完成

## API接口

### POST /api/generate-daily-news
生成每日AI资讯日报

**响应示例：**
```json
{
  "success": true,
  "data": {
    "date": "2026-05-30",
    "audience": "非专业人士",
    "top5": [...],
    "digest_table": [...],
    "further_reading": [...],
    "insight": {...}
  },
  "generated_at": "2026-05-30T12:00:00"
}
```

### GET /api/latest-daily-news
获取最新生成的日报

### GET /health
健康检查

## 配置说明

### API密钥获取

**Gemini API Key：**
1. 访问 [Google AI Studio](https://aistudio.google.com/)
2. 创建API密钥
3. 复制密钥到 `.env` 文件

**Doubao API Key：**
1. 访问 [火山引擎](https://console.volcengine.com/)
2. 开通机器学习平台服务
3. 创建API密钥
4. 复制密钥到 `.env` 文件

### 前端配置

在 `frontend/script.js` 中修改API地址：

```javascript
// 部署时改为实际的API地址
const API_BASE_URL = 'https://your-backend-api.com';
```

## 使用说明

1. 打开前端页面
2. 点击"生成今日日报"按钮
3. 等待处理完成（约1-2分钟）
4. 查看生成的AI资讯日报

## 输出示例

日报包含以下内容：

- **📈 今日趋势**：多条新闻背后的共同趋势
- **⚠️ 需要留意**：潜在风险和警示
- **今日重点**：Top5重要新闻的通俗化解读
- **延伸阅读**：深入了解特定方向的推荐
- **今日概览**：所有新闻的分类概览

## 技术栈

- **后端**：Python + Flask
- **前端**：HTML + CSS + JavaScript
- **AI模型**：Gemini（采集）、Doubao 1.8（消化+说人话）
- **部署**：Vercel（前端）、Railway/Render（后端）

## 注意事项

1. **API费用**：使用Gemini和Doubao API会产生费用，请注意控制使用量
2. **响应时间**：完整的三层处理需要1-2分钟，请耐心等待
3. **内容质量**：输出质量依赖AI模型性能，可能需要调优prompt
4. **部署安全**：不要在前端代码中暴露API密钥

## 故障排除

**API连接失败：**
- 检查后端服务是否正常运行
- 确认API地址配置正确
- 查看浏览器控制台错误信息

**生成失败：**
- 检查API密钥是否正确配置
- 确认API额度是否充足
- 查看后端日志了解详细错误

**内容质量问题：**
- 调整三层处理器的prompt
- 修改模型参数（temperature、max_tokens等）
- 添加后处理规则

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！