import httpx
import time
import random
from datetime import datetime
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/124.0.0.0 Safari/537.36",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}

TODAY = datetime.now().strftime("%Y-%m-%d")


def _bing_search(query: str, count: int = 5) -> list[dict]:
    url = "https://www.bing.com/search"
    params = {"q": query, "count": count, "freshness": "Day"}
    try:
        resp = httpx.get(url, headers=HEADERS, params=params, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        results = []
        for li in soup.select("li.b_algo")[:count]:
            a = li.select_one("h2 a")
            snippet = li.select_one(".b_caption p")
            if a:
                results.append({
                    "title": a.get_text(strip=True),
                    "url": a.get("href", ""),
                    "raw": a.get_text(strip=True) + " " + (snippet.get_text(strip=True) if snippet else ""),
                    "published": TODAY,
                })
        return results
    except Exception as e:
        print(f"[Bing] {query[:30]} 错误: {e}")
        return []


def _parse_rss(url: str, count: int = 5) -> list[dict]:
    try:
        resp = httpx.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        root = ET.fromstring(resp.content)
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        results = []

        # RSS 2.0
        for item in root.findall(".//item")[:count]:
            title = item.findtext("title", "")
            link = item.findtext("link", "")
            desc = item.findtext("description", "")
            pub = item.findtext("pubDate", TODAY)[:10]
            if title and link:
                results.append({"title": title, "url": link, "raw": title + " " + BeautifulSoup(desc, "html.parser").get_text()[:200], "published": pub})

        # Atom
        if not results:
            for entry in root.findall(".//atom:entry", ns)[:count]:
                title = entry.findtext("atom:title", "", ns)
                link_el = entry.find("atom:link", ns)
                link = link_el.get("href", "") if link_el is not None else ""
                summary = entry.findtext("atom:summary", "", ns)
                pub = entry.findtext("atom:updated", TODAY, ns)[:10]
                if title and link:
                    results.append({"title": title, "url": link, "raw": title + " " + summary[:200], "published": pub})

        return results
    except Exception as e:
        print(f"[RSS] {url[:50]} 错误: {e}")
        return []


def fetch_github_trending(token: str = "", count: int = 10) -> list[dict]:
    """GitHub 每日新增 Star 最多的 Top10 仓库"""
    results = []
    from datetime import timedelta
    since = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    headers = {
        **HEADERS,
        "Accept": "application/vnd.github+json",
    }
    if token:
        headers["Authorization"] = f"token {token}"

    url = "https://api.github.com/search/repositories"
    params = {
        "q": f"created:>{since}",
        "sort": "stars",
        "order": "desc",
        "per_page": count,
    }
    try:
        resp = httpx.get(url, headers=headers, params=params, timeout=15)
        resp.raise_for_status()
        for item in resp.json().get("items", [])[:count]:
            results.append({
                "source": "GitHub Trending",
                "title": item["full_name"],
                "url": item["html_url"],
                "raw": f"{item['full_name']}: {item.get('description', '')} Stars:{item.get('stargazers_count', 0)} Language:{item.get('language', '')}",
                "stars": item.get("stargazers_count", 0),
                "published": item.get("created_at", "")[:10],
            })
    except Exception as e:
        print(f"[GitHub Trending] 错误: {e}")
    return results


def fetch_hackernews(count: int = 10) -> list[dict]:
    """HackerNews Top Stories"""
    results = []
    try:
        ids_resp = httpx.get("https://hacker-news.firebaseio.com/v0/topstories.json", timeout=10)
        ids = ids_resp.json()[:30]
        for story_id in ids:
            if len(results) >= count:
                break
            try:
                item = httpx.get(f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json", timeout=10).json()
                if item and item.get("type") == "story":
                    results.append({
                        "title": item.get("title", ""),
                        "url": item.get("url", f"https://news.ycombinator.com/item?id={story_id}"),
                        "raw": item.get("title", ""),
                        "published": TODAY,
                    })
            except Exception:
                continue
    except Exception as e:
        print(f"[HackerNews] 错误: {e}")
    return results


def fetch_ai_news() -> list[dict]:
    """全球 AI 动态 Top 10"""
    print("[全球AI] 抓取 Bing...")
    bing = _bing_search("AI artificial intelligence latest news today", 8)
    time.sleep(random.uniform(1, 2))

    print("[全球AI] 抓取 HackerNews...")
    hn = fetch_hackernews(5)
    time.sleep(random.uniform(1, 2))

    print("[全球AI] 抓取 TechCrunch AI RSS...")
    tc = _parse_rss("https://techcrunch.com/category/artificial-intelligence/feed/", 5)

    combined = bing + hn + tc
    seen, unique = set(), []
    for item in combined:
        if item["url"] not in seen and item["url"]:
            seen.add(item["url"])
            item["source"] = "全球AI"
            unique.append(item)
    return unique[:10]


def fetch_tech_news() -> list[dict]:
    """科技发展 Top 5"""
    print("[科技] 抓取 Bing...")
    bing = _bing_search("technology innovation news today 2026", 5)
    time.sleep(random.uniform(1, 2))

    print("[科技] 抓取 TechCrunch RSS...")
    tc = _parse_rss("https://techcrunch.com/feed/", 5)

    combined = bing + tc
    seen, unique = set(), []
    for item in combined:
        if item["url"] not in seen and item["url"]:
            seen.add(item["url"])
            item["source"] = "科技"
            unique.append(item)
    return unique[:5]


def fetch_world_news() -> list[dict]:
    """国际新闻事件 Top 5"""
    print("[国际] 抓取 BBC RSS...")
    bbc = _parse_rss("https://feeds.bbci.co.uk/news/world/rss.xml", 5)
    time.sleep(random.uniform(1, 2))

    print("[国际] 抓取 Reuters RSS...")
    reuters = _parse_rss("https://feeds.reuters.com/reuters/worldNews", 5)
    time.sleep(random.uniform(1, 2))

    print("[国际] 抓取 Bing...")
    bing = _bing_search("international news world events today", 5)

    combined = bbc + reuters + bing
    seen, unique = set(), []
    for item in combined:
        if item["url"] not in seen and item["url"]:
            seen.add(item["url"])
            item["source"] = "国际新闻"
            unique.append(item)
    return unique[:5]
