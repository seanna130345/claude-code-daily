import httpx
import time
import random
from datetime import datetime, timedelta


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}

# 相关度关键词权重
RELEVANCE_KEYWORDS = [
    "claude code", "claude-code", "anthropic", "claude cli",
    "claude agent", "claude mcp", "claude tool",
]


def _relevance_score(item: dict) -> float:
    """计算与 Claude Code 的相关度分数（0-1）"""
    text = (item.get("title", "") + " " + item.get("raw", "")).lower()
    score = 0.0
    for kw in RELEVANCE_KEYWORDS:
        if kw in text:
            score += 1.0
    return min(score / 3.0, 1.0)


def _combined_score(item: dict) -> float:
    """相关度（60%）+ 星标数归一化（40%）"""
    relevance = _relevance_score(item)
    stars = item.get("stars", 0)
    # 星标数用 log 归一化，500星以上视为满分
    import math
    star_score = min(math.log1p(stars) / math.log1p(500), 1.0)
    return relevance * 0.6 + star_score * 0.4


def fetch_github(token: str) -> list[dict]:
    results = []
    headers = {**HEADERS, "Authorization": f"token {token}", "Accept": "application/vnd.github+json"}
    since = (datetime.utcnow() - timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%SZ")

    # 搜索仓库（扩大到7天，取更多候选再排序）
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

    # 搜索 Issues/Discussions
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

    # 综合排序：相关度60% + 星标数40%
    results.sort(key=_combined_score, reverse=True)
    return results[:10]


def fetch_bilibili() -> list[dict]:
    results = []
    url = "https://api.bilibili.com/x/web-interface/search/type"
    params = {
        "search_type": "video",
        "keyword": "Claude Code",
        "order": "pubdate",
        "duration": 0,
        "page": 1,
        "page_size": 10,
    }
    try:
        resp = httpx.get(url, headers=HEADERS, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        for item in data.get("data", {}).get("result", [])[:10]:
            bvid = item.get("bvid", "")
            title = item.get("title", "").replace('<em class="keyword">', "").replace("</em>", "")
            results.append({
                "source": "哔哩哔哩",
                "title": title,
                "url": f"https://www.bilibili.com/video/{bvid}",
                "raw": title + " " + item.get("description", "")[:300],
                "stars": 0,
                "published": datetime.fromtimestamp(item.get("pubdate", 0)).strftime("%Y-%m-%d") if item.get("pubdate") else "",
            })
    except Exception as e:
        print(f"[哔哩哔哩] 错误: {e}")
    return results


def fetch_wechat_via_bing() -> list[dict]:
    results = []
    query = 'site:mp.weixin.qq.com "Claude Code"'
    url = "https://www.bing.com/search"
    params = {"q": query, "count": 10, "freshness": "Week"}
    try:
        resp = httpx.get(url, headers=HEADERS, params=params, timeout=15)
        resp.raise_for_status()
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(resp.text, "html.parser")
        for li in soup.select("li.b_algo")[:10]:
            a = li.select_one("h2 a")
            snippet = li.select_one(".b_caption p")
            if a and "mp.weixin.qq.com" in a.get("href", ""):
                results.append({
                    "source": "微信公众号",
                    "title": a.get_text(strip=True),
                    "url": a["href"],
                    "raw": a.get_text(strip=True) + " " + (snippet.get_text(strip=True) if snippet else ""),
                    "stars": 0,
                    "published": datetime.now().strftime("%Y-%m-%d"),
                })
    except Exception as e:
        print(f"[微信/Bing] 错误: {e}")
    return results


def fetch_all(github_token: str) -> list[dict]:
    print("[Claude Code] 抓取 GitHub...")
    github = fetch_github(github_token)
    print(f"  → {len(github)} 条")

    time.sleep(random.uniform(1, 2))
    print("[Claude Code] 抓取哔哩哔哩...")
    bili = fetch_bilibili()
    print(f"  → {len(bili)} 条")

    time.sleep(random.uniform(1, 2))
    print("[Claude Code] 抓取微信公众号(Bing)...")
    wechat = fetch_wechat_via_bing()
    print(f"  → {len(wechat)} 条")

    # 三个来源各自独立，按顺序合并去重，总数控制在10条
    seen = set()
    result = []
    for item in github + bili + wechat:
        if item["url"] not in seen:
            seen.add(item["url"])
            result.append(item)
        if len(result) >= 10:
            break

    return result
