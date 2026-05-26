import httpx
import time
import random
from datetime import datetime, timedelta


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}


def fetch_github(token: str) -> list[dict]:
    """从 GitHub 搜索 Claude Code 相关仓库和讨论"""
    results = []
    headers = {**HEADERS, "Authorization": f"token {token}", "Accept": "application/vnd.github+json"}
    since = (datetime.utcnow() - timedelta(days=3)).strftime("%Y-%m-%dT%H:%M:%SZ")

    # 搜索仓库
    url = "https://api.github.com/search/repositories"
    params = {"q": f'"claude code" OR "claude-code" created:>{since[:10]}', "sort": "stars", "order": "desc", "per_page": 10}
    try:
        resp = httpx.get(url, headers=headers, params=params, timeout=15)
        resp.raise_for_status()
        for item in resp.json().get("items", [])[:10]:
            results.append({
                "source": "GitHub",
                "title": item["full_name"],
                "url": item["html_url"],
                "raw": f"{item['full_name']}: {item.get('description', '')} Stars:{item.get('stargazers_count', 0)}",
                "published": item.get("created_at", "")[:10],
            })
    except Exception as e:
        print(f"[GitHub repo] 错误: {e}")

    time.sleep(random.uniform(1, 2))

    # 搜索 Issues/Discussions
    url2 = "https://api.github.com/search/issues"
    params2 = {"q": f"claude code in:title created:>{since[:10]} type:issue", "sort": "created", "order": "desc", "per_page": 5}
    try:
        resp2 = httpx.get(url2, headers=headers, params=params2, timeout=15)
        resp2.raise_for_status()
        for item in resp2.json().get("items", [])[:5]:
            results.append({
                "source": "GitHub Issue",
                "title": item["title"],
                "url": item["html_url"],
                "raw": item["title"] + " " + item.get("body", "")[:200],
                "published": item.get("created_at", "")[:10],
            })
    except Exception as e:
        print(f"[GitHub issue] 错误: {e}")

    return results


def fetch_bilibili() -> list[dict]:
    """从 Bilibili 搜索 Claude Code 相关视频"""
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
            results.append({
                "source": "Bilibili",
                "title": item.get("title", "").replace("<em class=\"keyword\">", "").replace("</em>", ""),
                "url": f"https://www.bilibili.com/video/{bvid}",
                "raw": item.get("title", "") + " " + item.get("description", "")[:200],
                "published": datetime.fromtimestamp(item.get("pubdate", 0)).strftime("%Y-%m-%d") if item.get("pubdate") else "",
            })
    except Exception as e:
        print(f"[Bilibili] 错误: {e}")
    return results


def fetch_wechat_via_bing() -> list[dict]:
    """通过 Bing 搜索微信公众号文章"""
    results = []
    query = 'site:mp.weixin.qq.com "Claude Code"'
    url = "https://www.bing.com/search"
    params = {"q": query, "count": 10, "freshness": "Day"}
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
    print("[Claude Code] 抓取 Bilibili...")
    bili = fetch_bilibili()
    print(f"  → {len(bili)} 条")

    time.sleep(random.uniform(1, 2))
    print("[Claude Code] 抓取微信(Bing)...")
    wechat = fetch_wechat_via_bing()
    print(f"  → {len(wechat)} 条")

    all_items = github + bili + wechat
    # 去重（按 URL）
    seen = set()
    unique = []
    for item in all_items:
        if item["url"] not in seen:
            seen.add(item["url"])
            unique.append(item)

    return unique[:20]
