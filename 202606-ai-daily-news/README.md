# AI每日资讯日报推送系统

一个为非技术背景人群打造的AI资讯日报系统，通过三层架构处理复杂AI资讯，输出普通人能理解的每日简报。

## 项目特色

- **三层处理架构**：采集层 → 消化层 → 说人话层
- **受众精准**：面向完全没有技术背景的普通人
- **通俗化表达**：将专业术语转化为生活化的比喻
- **一键生成**：简单点击按钮即可获得当日AI资讯日报
- **混合架构**：NewsAPI采集 + Qwen-Plus处理

## 🚀 一键部署到Railway

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new)

### 部署步骤：

1. **Fork这个仓库到你的GitHub**

2. **在Railway中创建新项目**
   - 访问 [railway.app](https://railway.app)
   - 点击 "New Project" → "Deploy from GitHub repo"
   - 选择你fork的仓库

3. **配置环境变量**
   在Railway的项目设置中添加以下环境变量：
   ```
   LAOZHAI_API_KEY=你的老张代理API密钥
   LAOZHAI_BASE_URL=https://api.laozhang.ai/v1
   NEWSAPI_KEY=你的NewsAPI密钥
   PROCESSOR_MODEL=qwen-plus
   PORT=5000
   ```

4. **获取部署URL**
   - Railway会自动部署并给你一个URL，例如：`https://your-project.railway.app`

5. **完成！** 你的AI日报系统已经在线上运行了

## 本地开发

### 环境准备

确保你已安装：
- Python 3.8+
- pip

### 快速启动

```bash
# 1. 克隆项目
git clone https://github.com/你的用户名/202606-ai-daily-news.git
cd 202606-ai-daily-news

# 2. 配置环境变量
cd backend
cp .env.example .env
# 编辑 .env 文件，填入你的API密钥

# 3. 安装依赖
pip install -r requirements.txt

# 4. 启动服务器
python api.py

# 5. 打开浏览器访问
# 前端: http://localhost:5000/frontend/index.html
# 或直接打开 frontend/index.html 文件
```

## 系统架构

```
用户点击按钮 → 前端发送请求 → Python API → 执行三层处理 → 返回结果 → 前端展示
```

### 三层处理流程

1. **采集层（NewsAPI）**：从NewsAPI获取当日AI相关新闻
2. **消化层（Qwen-Plus）**：筛选Top5、分类、评重要性、提炼洞察
3. **说人话层（Qwen-Plus）**：针对非技术背景人群进行通俗化改写

## API接口

### POST /api/generate-daily-news
生成每日AI资讯日报

**请求示例：**
```json
{
  "date": "2026-06-10"
}
```

**响应示例：**
```json
{
  "success": true,
  "data": {
    "date": "2026-06-10",
    "top5": [
      {
        "title": "通俗化标题",
        "summary": "聊天式摘要",
        "source_url": "新闻链接",
        "why_important": "为什么重要"
      }
    ],
    "insight": {
      "trend": "今天AI圈有个值得注意的趋势：...",
      "risk": "不过有一点需要留意：..."
    }
  },
  "generated_at": "2026-06-10T12:00:00"
}
```

### GET /api/latest-daily-news
获取最新生成的日报

### GET /health
健康检查

## 配置说明

### API密钥获取

**老张代理API Key：**
- 获取地址：[老张代理](https://laozhang.ai)
- 用于AI处理层（消化层+说人话层）

**NewsAPI Key：**
- 获取地址：[NewsAPI.org](https://newsapi.org)
- 用于新闻采集层

### 部署配置

**修改前端API地址：**

如果部署到Railway，需要修改 `frontend/index.html` 中的API地址：

```javascript
// 找到这一行
const CONFIG = {
    API_BASE_URL: 'http://localhost:5000',
    // 改为你的Railway URL
    API_BASE_URL: 'https://your-project.railway.app',
};
```

## 项目结构

```
ai-daily-news/
├── backend/                # Python后端
│   ├── api.py             # 主API服务器
│   ├── collectors/        # 采集层
│   │   ├── __init__.py
│   │   └── newsapi_collector.py
│   ├── processors/        # 消化层和说人话层
│   │   ├── __init__.py
│   │   └── optimized_processor.py
│   ├── requirements.txt   # Python依赖
│   └── .env.example      # 环境变量示例
├── frontend/              # 前端界面
│   ├── index.html        # 主页面
│   └── logo.png         # 前端logo
├── Procfile             # Railway部署配置
├── railway.yaml          # Railway配置文件
└── README.md            # 项目说明
```

## 使用说明

1. 打开前端页面
2. 点击"生成今日日报"按钮
3. 等待处理完成（约1分钟）
4. 查看生成的AI资讯日报

## 输出示例

日报包含以下内容：

- **📈 今日趋势**：多条新闻背后的共同趋势
- **⚠️ 需要留意**：潜在风险和警示
- **今日重点**：Top5重要新闻的通俗化解读
- **为什么重要**：对普通人的实际影响
- **来源链接**：查看完整新闻

## 技术栈

- **后端**：Python + Flask
- **前端**：HTML + CSS + JavaScript
- **数据源**：NewsAPI
- **AI处理**：老张代理 + Qwen-Plus
- **部署**：Railway（推荐）

## 故障排除

**API连接失败：**
- 检查后端服务是否正常运行
- 确认API地址配置正确
- 查看浏览器控制台错误信息

**生成失败：**
- 检查API密钥是否正确配置
- 确认API额度是否充足
- 查看Railway日志了解详细错误

**SSL连接错误：**
- 项目已内置SSL修复，应该不会出现此问题
- 如果仍有问题，检查Railway的环境变量配置

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！