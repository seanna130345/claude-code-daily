# 每日科技日报

每天早上 9 点（北京时间）自动抓取全球科技、AI、GitHub、Claude Code 最新资讯，生成中文摘要，推送到微信，并发布到 GitHub Pages 网页。

**网页版**：https://seanna130345.github.io/claude-code-daily

---

## 内容板块

| 板块 | 来源 | 每日条数 |
|------|------|---------|
| 国际新闻 Top 5 | BBC、AP News、Al Jazeera、Bing | 5 条 |
| 国内新闻 Top 5 | 36kr、澎湃新闻、Bing | 5 条 |
| 全球科技动态 Top 5 | TechCrunch、The Verge、Wired、Bing | 5 条 |
| 全球 AI 动态 Top 5 | TechCrunch AI、MIT Technology Review、HackerNews、Bing | 5 条 |
| GitHub 每日 Top 5 | GitHub Search API（按新增 Star 排名） | 5 条 |
| Claude Code 资讯 Top 5 | GitHub、哔哩哔哩、微信公众号（搜狗）、Reddit r/ClaudeAI | 5 条 |

---

## 实现原理

### 整体流程

```
GitHub Actions（每天 UTC 01:00 = 北京 09:00）
        │
        ▼
  1. 爬取数据（crawlers/）
        │
        ▼
  2. 生成中文摘要（summarizer.py）
        │
        ├──▶ 3a. 生成 HTML（generate_html.py）→ docs/index.html → GitHub Pages
        │
        ├──▶ 3b. 保存 JSON 存档（data/YYYY-MM-DD.json）
        │
        └──▶ 3c. 推送微信（wxpusher_sender.py）→ Server酱 → 方糖公众号
```

### 各模块说明

#### 1. 数据爬取（`crawlers/`）

**`crawlers/news_crawler.py`** — 通用新闻爬虫

- `fetch_world_news()`：依次请求 BBC RSS、AP News RSS（via RSSHub）、Al Jazeera RSS，再用 Bing 搜索补充，合并去重后取前 5 条
- `fetch_china_news()`：依次请求 36kr RSS、澎湃新闻 RSS，再用 Bing 搜索补充，合并去重后取前 5 条
- `fetch_tech_news()`：依次请求 TechCrunch RSS、The Verge RSS、Wired RSS，再用 Bing 搜索补充，合并去重后取前 5 条
- `fetch_ai_news()`：依次请求 TechCrunch AI RSS、MIT Technology Review RSS、HackerNews API，再用 Bing 搜索补充，合并去重后取前 5 条
- `fetch_github_trending()`：调用 GitHub Search API，按 `created` 时间过滤近 1 天、按 Star 数降序，取前 5 条
- `_parse_rss()`：通用 RSS/Atom 解析器，支持标准 RSS 和 Atom 两种格式
- `_bing_search()`：直接请求 Bing 搜索页面，用 BeautifulSoup 解析结果，无需 API Key

**`crawlers/claude_code_crawler.py`** — Claude Code 专项爬虫

- `fetch_github()`：用 GitHub Search API 搜索包含 "claude code" 或 "anthropic claude" 的仓库和 Issue，按相关度（60%）+ Star 数（40%）综合评分排序
- `fetch_bilibili()`：通过 Bing 搜索 `site:bilibili.com/video "Claude Code"` 获取 B 站视频（B 站 API 在境外服务器被封，降级为 Bing 搜索）
- `fetch_wechat_via_sogou()`：通过搜狗微信搜索（weixin.sogou.com）获取公众号文章
- `fetch_reddit_claudeai()`：请求 Reddit r/ClaudeAI 的 JSON API，获取热门帖子

#### 2. 摘要生成（`summarizer.py`）

调用柏拉图（bltcy.ai）提供的 OpenAI 兼容 API，使用 `claude-haiku-4-5-20251001` 模型，对每条资讯生成 100-200 字的中文摘要。

- API 地址：`https://api.bltcy.ai/v1/chat/completions`
- 失败自动重试，最多 3 次，指数退避
- 未配置 API Key 时跳过摘要，直接用标题代替

#### 3a. 生成 HTML（`generate_html.py`）

将数据渲染成静态 HTML 文件，写入 `docs/index.html`。GitHub Pages 自动将 `docs/` 目录发布为网站，无需服务器。

#### 3b. JSON 存档（`data/`）

每次运行将完整数据保存为 `data/YYYY-MM-DD.json`，长期积累历史记录。

#### 3c. 微信推送（`wxpusher_sender.py`）

通过 Server酱（sct.ftqq.com）将日报推送到微信。格式为 Markdown：每条资讯标题+链接单独一行，摘要另起一段。

---

## 目录结构

```
claude-code-daily/
├── .github/
│   └── workflows/
│       └── daily.yml          # GitHub Actions 定时任务配置
├── crawlers/
│   ├── __init__.py
│   ├── news_crawler.py        # 通用新闻爬虫（国际/国内/科技/AI/GitHub）
│   └── claude_code_crawler.py # Claude Code 专项爬虫
├── data/                      # 每日 JSON 存档（自动生成）
│   └── YYYY-MM-DD.json
├── docs/                      # GitHub Pages 网站目录
│   └── index.html             # 每日自动覆盖更新
├── main.py                    # 主入口，串联所有模块
├── summarizer.py              # Claude API 摘要生成
├── generate_html.py           # HTML 渲染
├── wxpusher_sender.py         # Server酱微信推送
└── requirements.txt           # Python 依赖
```

---

## 部署方法

### 1. Fork 或克隆仓库

```bash
git clone https://github.com/seanna130345/claude-code-daily.git
cd claude-code-daily
```

### 2. 配置 GitHub Secrets

在仓库 **Settings → Secrets and variables → Actions → New repository secret** 中添加：

| Secret 名称 | 说明 | 获取方式 |
|------------|------|---------|
| `BLTCY_API_KEY` | 柏拉图 API Key，用于生成中文摘要 | 注册 https://bltcy.ai 获取 |
| `SERVER_CHAN_KEY` | Server酱 SendKey，用于微信推送 | 注册 https://sct.ftqq.com 获取 |

> `GITHUB_TOKEN` 由 GitHub Actions 自动提供，无需手动配置。

### 3. 开启 GitHub Pages

在仓库 **Settings → Pages** 中：
- Source 选择 **Deploy from a branch**
- Branch 选择 **master**，目录选择 **/docs**
- 保存后等待几分钟，网页即可访问

### 4. 手动触发测试

在仓库 **Actions → 每日科技日报 → Run workflow** 中点击运行，验证配置是否正确。

---

## 自动运行时间

GitHub Actions 配置为每天 **UTC 01:00**（北京时间 09:00）自动运行。

运行完成后：
- `docs/index.html` 更新为当天日报
- `data/YYYY-MM-DD.json` 新增当天存档
- 微信收到推送通知

---

## 依赖

```
httpx==0.27.0
beautifulsoup4==4.12.3
```

Python 版本要求：3.11+
