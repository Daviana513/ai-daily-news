// 配置API地址
const API_BASE_URL = 'http://localhost:5000'; // 本地开发时使用
// 部署时需要改为实际的API地址，例如：
// const API_BASE_URL = 'https://your-backend-api.com';

// DOM元素
const generateBtn = document.getElementById('generate-btn');
const loading = document.getElementById('loading');
const error = document.getElementById('error');
const dailyNews = document.getElementById('daily-news');
const statusText = document.querySelector('.status-text');

// 加载步骤元素
const stepCollect = document.getElementById('step-collect');
const stepDigest = document.getElementById('step-digest');
const stepTranslate = document.getElementById('step-translate');

// 更新加载步骤
function updateLoadingStep(step) {
    // 重置所有步骤
    [stepCollect, stepDigest, stepTranslate].forEach(s => {
        s.classList.remove('active', 'completed');
    });

    // 根据步骤更新状态
    switch(step) {
        case 'collect':
            stepCollect.classList.add('active');
            break;
        case 'digest':
            stepCollect.classList.add('completed');
            stepDigest.classList.add('active');
            break;
        case 'translate':
            stepCollect.classList.add('completed');
            stepDigest.classList.add('completed');
            stepTranslate.classList.add('active');
            break;
        case 'completed':
            stepCollect.classList.add('completed');
            stepDigest.classList.add('completed');
            stepTranslate.classList.add('completed');
            break;
    }
}

// 显示错误
function showError(message) {
    error.classList.remove('hidden');
    error.querySelector('.error-message').textContent = message;
    loading.classList.add('hidden');
    dailyNews.classList.add('hidden');
    generateBtn.disabled = false;
    statusText.textContent = '生成失败';
}

// 显示日报内容
function showDailyNews(data) {
    // 填充基本信息
    document.getElementById('news-date').textContent = data.date;

    // 填充洞察部分
    document.getElementById('trend-content').textContent = data.insight.trend;
    document.getElementById('risk-content').textContent = data.insight.risk;

    // 填充Top5新闻
    const top5Container = document.getElementById('top5-news');
    top5Container.innerHTML = '';

    data.top5.forEach(news => {
        const newsItem = document.createElement('div');
        newsItem.className = 'news-item';

        // 创建标题和链接
        const titleHtml = news.source_url && news.source_url !== 'N/A' && news.source_url !== ''
            ? `<h3><a href="${news.source_url}" target="_blank">${news.title}</a></h3>`
            : `<h3>${news.title} <small style="color: #666; font-size: 0.8em;">(暂无链接)</small></h3>`;

        // 添加搜索建议
        const searchHtml = news.source_url && news.source_url !== 'N/A' && news.source_url !== ''
            ? ''
            : `<div style="margin-top: 10px; font-size: 0.9em;">
                <a href="https://www.google.com/search?q=${encodeURIComponent(news.title)}" target="_blank" style="color: #667eea;">
                    🔍 在Google搜索此新闻
                </a>
              </div>`;

        newsItem.innerHTML = `
            ${titleHtml}
            <p class="news-summary">${news.summary}</p>
            <div class="news-why">
                <strong>💡 为什么重要：</strong>
                ${news.why_important}
            </div>
            ${searchHtml}
        `;
        top5Container.appendChild(newsItem);
    });

    // 填充延伸阅读
    const furtherContainer = document.getElementById('further-reading');
    furtherContainer.innerHTML = '';

    if (data.further_reading && data.further_reading.length > 0) {
        data.further_reading.forEach(item => {
            const furtherItem = document.createElement('div');
            furtherItem.className = 'further-item';
            furtherItem.innerHTML = `
                <a href="${item.url}" target="_blank">${item.title}</a>
            `;
            furtherContainer.appendChild(furtherItem);
        });
    } else {
        furtherContainer.innerHTML = '<p style="color: #666; font-style: italic;">暂无延伸阅读内容</p>';
    }

    // 填充概览表格
    const tableBody = document.getElementById('digest-table-body');
    tableBody.innerHTML = '';

    if (data.digest_table && data.digest_table.length > 0) {
        data.digest_table.forEach(item => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${item.category}</td>
                <td>${item.title}</td>
                <td><span class="importance-badge ${item.importance.toLowerCase()}">${item.importance}</span></td>
            `;
            tableBody.appendChild(row);
        });
    }

    // 显示日报内容
    loading.classList.add('hidden');
    dailyNews.classList.remove('hidden');
    generateBtn.disabled = false;
    statusText.textContent = `生成完成 (${new Date().toLocaleTimeString()})`;
}

// 生成日报
async function generateDailyNews() {
    try {
        // 禁用按钮
        generateBtn.disabled = true;
        statusText.textContent = '正在生成日报...';

        // 显示加载动画
        loading.classList.remove('hidden');
        error.classList.add('hidden');
        dailyNews.classList.add('hidden');

        // 模拟进度更新
        updateLoadingStep('collect');
        setTimeout(() => updateLoadingStep('digest'), 2000);
        setTimeout(() => updateLoadingStep('translate'), 4000);

        // 调用API
        const response = await fetch(`${API_BASE_URL}/api/generate-daily-news`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || '生成日报失败');
        }

        const result = await response.json();

        if (result.success) {
            updateLoadingStep('completed');
            setTimeout(() => {
                showDailyNews(result.data);
            }, 500);
        } else {
            throw new Error(result.error || '生成日报失败');
        }

    } catch (error) {
        console.error('生成日报时发生错误:', error);
        showError(error.message || '网络连接失败，请检查API服务器是否运行');
    }
}

// 检查API状态
async function checkApiStatus() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        if (response.ok) {
            statusText.textContent = '智羿连接中';
            return true;
        } else {
            statusText.textContent = '智羿连接异常';
            return false;
        }
    } catch (error) {
        statusText.textContent = '智羿未连接';
        console.warn('无法连接到API服务器:', error);
        return false;
    }
}

// 页面加载时检查API状态
document.addEventListener('DOMContentLoaded', () => {
    checkApiStatus();

    // 每30秒检查一次API状态
    setInterval(checkApiStatus, 30000);
});

// 按钮点击事件
generateBtn.addEventListener('click', generateDailyNews);

// 支持回车键触发
document.addEventListener('keydown', (event) => {
    if (event.key === 'Enter' && !generateBtn.disabled) {
        generateDailyNews();
    }
});