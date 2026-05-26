import httpx
import time
import random
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}

RELEVANCE_KEYWORDS = [
    "claude code", "claude-code", "anthropic", "claude cli",
    "claude agent", "claude mcp", "claude tool",
]


def _relevance_score(item: dict) -> float:
    text = (item.get("title", "") + " " + item.get("raw", "")).lower()
    score = sum(1.0 for kw in RELEVANCE_KEYWORDS if kw in text)
    return min(score / 3.0, 1.0)


def _combined_score(item: dict) -> float:
    import math
    relevance = _relevance_score(item)
    stars = item.get("stars", 0)
    star_score = min(math.log1p(stars) / math.log1p(500), 1.0)
    return relevance * 0.6 + star_score * 0.4


def fetch_github(token: str) -> list[dict]:
    results = []
    headers = {**HEADERS, "Authorization": f"token {token}", "Accept": "application/vnd.github+json"}
    since = (datetime.utcnow() - timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%SZ")

    url = "https://api.github.com/search/repositories"
    params = {
        "q": f'"claude code" OR "claude-code" OR "anthropic claude" created:>{since[:10]}',
        "sort": "stars",
        "order": "desc",
        "per_page": 20,
    }
    try:
        resp = httpx.get(url, headers=headers, params=params, timeout=15)
        resp.raise_for_status()
        for item in resp.json().get("items", []):
            stars = item.get("stargazers_count", 0)
            results.append({
                "source": "GitHub",
                "title": item["full_name"],
                "url": item["html_url"],
                "raw": f"{item['full_name']}: {item.get('description', '')}",
                "stars": stars,
                "published": item.get("created_at", "")[:10],
            })
    except Exception as e:
        print(f"[GitHub repo] 错误: {e}")

    time.sleep(random.uniform(1, 2))

    url2 = "https://api.github.com/search/issues"
    params2 = {
        "q": f"claude code in:title created:>{since[:10]} type:issue",
        "sort": "created",
        "order": "desc",
        "per_page": 10,
    }
    try:
        resp2 = httpx.get(url2, headers=headers, params=params2, timeout=15)
        resp2.raise_for_status()
        for item in resp2.json().get("items", [])[:10]:
            results.append({
                "source": "GitHub Issue",
                "title": item["title"],
                "url": item["html_url"],
                "raw": item["title"] + " " + item.get("body", "")[:300],
                "stars": 0,
                "published": item.get("created_at", "")[:10],
            })
    except Exception as e:
        print(f"[GitHub issue] 错误: {e}")

    results.sort(key=_combined_score, reverse=True)
    return results[:10]


def fetch_bilibili() -> list[dict]:
    """通过 RSSHub 获取哔哩哔哩 Claude Code 相关视频"""
    results = []
    # 尝试多个 RSSHub 公共实例
    rsshub_instances = [
        "https://rsshub.app",
        "https://rss.shab.fun",
        "https://rsshub.rssforever.com",
    ]
    keyword = "Claude Code"
    for base in rsshub_instances:
        url = f"{base}/bilibili/search/{keyword}/pubdate"
        try:
            resp = httpx.get(url, headers=HEADERS, timeout=15)
            resp.raise_for_status()
            root = ET.fromstring(resp.content)
            for item in root.findall(".//item")[:10]:
                title = item.findtext("title", "")
                link = item.findtext("link", "")
                desc = BeautifulSoup(item.findtext("description", ""), "html.parser").get_text()[:300]
                pub = item.findtext("pubDate", "")[:10] if item.findtext("pubDate") else datetime.now().strftime("%Y-%m-%d")
                if title and link:
                    results.append({
                        "source": "哔哩哔哩",
                        "title": title,
                        "url": link,
                        "raw": title + " " + desc,
                        "stars": 0,
                        "published": pub,
                    })
            if results:
                print(f"  [哔哩哔哩] 使用实例: {base}")
                break
        except Exception as e:
            print(f"  [哔哩哔哩] {base} 失败: {e}")
            continue
    return results


def fetch_wechat_via_sogou() -> list[dict]:
    """通过搜狗微信搜索获取公众号文章"""
    results = []
    url = "https://weixin.sogou.com/weixin"
    params = {
        "type": 2,  # 2=文章
        "query": "Claude Code",
        "ie": "utf8",
        "s_from": "input",
        "_sug_": "n",
        "_sug_type_": "",
    }
    headers = {
        **HEADERS,
        "Referer": "https://weixin.sogou.com/",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }
    try:
        resp = httpx.get(url, headers=headers, params=params, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        for item in soup.select("ul.news-list li")[:10]:
            title_el = item.select_one("h3 a") or item.select_one(".txt-box h3 a")
            snippet_el = item.select_one("p.txt-info") or item.select_one(".txt-box p")
            if not title_el:
                continue
            href = title_el.get("href", "")
            # 搜狗返回的是跳转链接，保留原样
            if not href.startswith("http"):
                href = "https://weixin.sogou.com" + href
            results.append({
                "source": "微信公众号",
                "title": title_el.get_text(strip=True),
                "url": href,
                "raw": title_el.get_text(strip=True) + " " + (snippet_el.get_text(strip=True) if snippet_el else ""),
                "stars": 0,
                "published": datetime.now().strftime("%Y-%m-%d"),
            })
    except Exception as e:
        print(f"[微信/搜狗] 错误: {e}")
    return results


def fetch_all(github_token: str) -> list[dict]:
    print("[Claude Code] 抓取 GitHub...")
    github = fetch_github(github_token)
    print(f"  → {len(github)} 条")

    time.sleep(random.uniform(1, 2))
    print("[Claude Code] 抓取哔哩哔哩(RSSHub)...")
    bili = fetch_bilibili()
    print(f"  → {len(bili)} 条")

    time.sleep(random.uniform(1, 2))
    print("[Claude Code] 抓取微信公众号(搜狗)...")
    wechat = fetch_wechat_via_sogou()
    print(f"  → {len(wechat)} 条")

    # 三个来源各自独立，合并去重，总数控制在10条
    seen = set()
    result = []
    for item in github + bili + wechat:
        if item["url"] not in seen:
            seen.add(item["url"])
            result.append(item)
        if len(result) >= 10:
            break

    return result
