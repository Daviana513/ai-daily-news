# Railway 部署指南

## 🚀 快速部署到Railway

### 第一步：准备GitHub仓库

1. **将项目推送到GitHub**
   ```bash
   cd C:\Users\Lenovo\Desktop\202606-ai-daily-news
   git init
   git add .
   git commit -m "Initial commit"

   # 在GitHub上创建新仓库，然后：
   git remote add origin https://github.com/你的用户名/202606-ai-daily-news.git
   git push -u origin main
   ```

### 第二步：Railway部署

1. **访问Railway**
   - 打开 [railway.app](https://railway.app)
   - 使用GitHub账号登录

2. **创建新项目**
   - 点击 "New Project"
   - 选择 "Deploy from GitHub repo"
   - 选择你的仓库

3. **配置环境变量**

   在Railway项目设置中添加以下环境变量：

   ```
   LAOZHAI_API_KEY=sk-TUPts3pygJ3uYLGt90AdE8B1Bb084c2bBaBdBb911b168597
   LAOZHAI_BASE_URL=https://api.laozhang.ai/v1
   NEWSAPI_KEY=5da59a3e57504c608618a86c77fc70de
   PROCESSOR_MODEL=qwen-plus
   PORT=5000
   ```

4. **等待部署完成**
   - Railway会自动检测Python项目
   - 自动安装依赖
   - 启动Flask服务器
   - 大约2-3分钟完成部署

5. **获取你的Railway URL**
   - 部署完成后，Railway会给你一个URL
   - 格式类似：`https://your-project-name.railway.app`

### 第三步：修改前端API地址

1. **编辑前端文件**
   - 打开 `frontend/index.html`
   - 找到第687行的API配置
   - 将 `http://localhost:5000` 改为你的Railway URL

2. **修改示例**
   ```javascript
   // 修改前
   const CONFIG = {
       API_BASE_URL: 'http://localhost:5000',
   ```

   ```javascript
   // 修改后
   const CONFIG = {
       API_BASE_URL: 'https://your-project-name.railway.app',
   ```

3. **提交修改**
   ```bash
   git add frontend/index.html
   git commit -m "Update API URL for Railway deployment"
   git push
   ```

### 第四步：测试部署

1. **访问你的应用**
   - 打开浏览器访问：`https://your-project-name.railway.app/frontend/index.html`
   - 点击"生成今日日报"按钮
   - 应该能看到AI日报生成成功

2. **检查API状态**
   - 访问：`https://your-project-name.railway.app/health`
   - 应该看到健康检查响应

## 🔧 环境变量说明

| 变量名 | 说明 | 获取方式 |
|--------|------|----------|
| `LAOZHAI_API_KEY` | 老张代理API密钥 | [laozhang.ai](https://laozhang.ai) |
| `LAOZHAI_BASE_URL` | API基础URL | 固定值：`https://api.laozhang.ai/v1` |
| `NEWSAPI_KEY` | NewsAPI密钥 | [NewsAPI.org](https://newsapi.org) |
| `PROCESSOR_MODEL` | 处理模型 | 固定值：`qwen-plus` |
| `PORT` | 服务端口 | 固定值：`5000` |

## 📊 部署监控

1. **查看日志**
   - 在Railway项目中点击 "Logs"
   - 实时查看应用运行日志
   - 排查错误和问题

2. **监控资源使用**
   - 查看CPU、内存使用情况
   - Railway免费额度：$5/月

3. **健康检查**
   - Railway会自动检查 `/health` 端点
   - 如果应用无响应会自动重启

## 🎯 常见问题

**Q: 部署失败怎么办？**
A: 检查Railway日志，通常是依赖安装失败或环境变量配置错误

**Q: API连接超时？**
A: 检查环境变量是否正确，特别是API密钥和BASE_URL

**Q: 前端无法连接后端？**
A: 确认前端的API_BASE_URL已修改为Railway URL

**Q: 如何更新应用？**
A: 只需`git push`到GitHub，Railway会自动重新部署

## 💰 费用说明

- **Railway免费额度**: $5/月
- **超出免费额度**: 按实际使用量计费
- **API费用**: 根据你的AI API使用量单独计算

## 🚀 下一步

1. **自定义域名** (可选)
   - 在Railway项目中添加自定义域名
   - 配置DNS记录

2. **性能优化**
   - 监控API调用次数
   - 优化处理速度
   - 添加缓存机制

3. **功能扩展**
   - 添加用户认证
   - 增加历史记录功能
   - 支持多语言

---

**恭喜！你的AI日报系统已经成功部署到Railway！** 🎉