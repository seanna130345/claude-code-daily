import httpx
import time
import random
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/124.0.0.0 Safari/537.36",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}

TODAY = datetime.now().strftime("%Y-%m-%d")


def _parse_rss(url: str, count: int = 5) -> list[dict]:
    try:
        resp = httpx.get(url, headers=HEADERS, timeout=15, follow_redirects=True)
        resp.raise_for_status()
        root = ET.fromstring(resp.content)
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        results = []
        for item in root.findall(".//item")[:count]:
            title = item.findtext("title", "")
            link = item.findtext("link", "")
            desc = item.findtext("description", "")
            pub = (item.findtext("pubDate", "") or TODAY)[:10]
            if title and link:
                results.append({"title": title, "url": link, "raw": title + " " + BeautifulSoup(desc, "html.parser").get_text()[:300], "published": pub})
        if not results:
            for entry in root.findall(".//atom:entry", ns)[:count]:
                title = entry.findtext("atom:title", "", ns)
                link_el = entry.find("atom:link", ns)
                link = link_el.get("href", "") if link_el is not None else ""
                summary = entry.findtext("atom:summary", "", ns)
                pub = (entry.findtext("atom:updated", TODAY, ns) or TODAY)[:10]
                if title and link:
                    results.append({"title": title, "url": link, "raw": title + " " + summary[:300], "published": pub})
        return results
    except Exception as e:
        print(f"[RSS] {url[:50]} 错误: {e}")
        return []


def fetch_github_trending(token: str = "", count: int = 5) -> list[dict]:
    """GitHub 每日新增 Star 最多的 Top5"""
    results = []
    since = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    headers = {**HEADERS, "Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"token {token}"
    try:
        resp = httpx.get(
            "https://api.github.com/search/repositories",
            headers=headers,
            params={"q": f"created:>{since}", "sort": "stars", "order": "desc", "per_page": count},
            timeout=15,
        )
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


def fetch_hackernews(count: int = 5) -> list[dict]:
    results = []
    try:
        ids = httpx.get("https://hacker-news.firebaseio.com/v0/topstories.json", timeout=10).json()[:20]
        for story_id in ids:
            if len(results) >= count:
                break
            try:
                item = httpx.get(f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json", timeout=10).json()
                if item and item.get("type") == "story":
                    results.append({"title": item.get("title", ""), "url": item.get("url", f"https://news.ycombinator.com/item?id={story_id}"), "raw": item.get("title", ""), "published": TODAY})
            except Exception:
                continue
    except Exception as e:
        print(f"[HackerNews] 错误: {e}")
    return results


def fetch_world_news() -> list[dict]:
    """国际新闻 Top5 — BBC + Reuters Top + Al Jazeera + NPR"""
    print("[国际] 抓取 BBC RSS...")
    bbc = _parse_rss("https://feeds.bbci.co.uk/news/world/rss.xml", 5)
    time.sleep(random.uniform(1, 2))

    print("[国际] 抓取 Al Jazeera RSS...")
    alj = _parse_rss("https://www.aljazeera.com/xml/rss/all.xml", 5)
    time.sleep(random.uniform(1, 2))

    print("[国际] 抓取 NPR RSS...")
    npr = _parse_rss("https://feeds.npr.org/1001/rss.xml", 5)
    time.sleep(random.uniform(1, 2))

    print("[国际] 抓取 Guardian World RSS...")
    guardian = _parse_rss("https://www.theguardian.com/world/rss", 5)

    combined = bbc + alj + npr + guardian
    seen, unique = set(), []
    for item in combined:
        if item["url"] not in seen and item["url"]:
            seen.add(item["url"])
            item["source"] = "国际新闻"
            unique.append(item)
    return unique[:5]


def fetch_china_news() -> list[dict]:
    """国内新闻 Top5 — 36kr + 新浪科技 + InfoQ中文 + 少数派"""
    print("[国内] 抓取 36kr RSS...")
    kr36 = _parse_rss("https://36kr.com/feed", 5)
    time.sleep(random.uniform(1, 2))

    print("[国内] 抓取 新浪科技 RSS...")
    sina = _parse_rss("https://rss.sina.com.cn/news/china/focus15.xml", 5)
    time.sleep(random.uniform(1, 2))

    print("[国内] 抓取 InfoQ中文 RSS...")
    infoq = _parse_rss("https://www.infoq.cn/feed", 5)
    time.sleep(random.uniform(1, 2))

    print("[国内] 抓取 少数派 RSS...")
    sspai = _parse_rss("https://sspai.com/feed", 5)

    combined = kr36 + sina + infoq + sspai
    seen, unique = set(), []
    for item in combined:
        if item["url"] not in seen and item["url"]:
            seen.add(item["url"])
            item["source"] = "国内新闻"
            unique.append(item)
    return unique[:5]


def fetch_tech_news() -> list[dict]:
    """全球科技动态 Top5 — TechCrunch + The Verge + Wired + Ars Technica"""
    print("[科技] 抓取 TechCrunch RSS...")
    tc = _parse_rss("https://techcrunch.com/feed/", 5)
    time.sleep(random.uniform(1, 2))

    print("[科技] 抓取 The Verge RSS...")
    verge = _parse_rss("https://www.theverge.com/rss/index.xml", 5)
    time.sleep(random.uniform(1, 2))

    print("[科技] 抓取 Wired RSS...")
    wired = _parse_rss("https://www.wired.com/feed/rss", 5)
    time.sleep(random.uniform(1, 2))

    print("[科技] 抓取 Ars Technica RSS...")
    ars = _parse_rss("https://feeds.arstechnica.com/arstechnica/index", 5)

    combined = tc + verge + wired + ars
    seen, unique = set(), []
    for item in combined:
        if item["url"] not in seen and item["url"]:
            seen.add(item["url"])
            item["source"] = "科技"
            unique.append(item)
    return unique[:5]


def fetch_ai_news() -> list[dict]:
    """全球AI动态 Top5 — TechCrunch AI + MIT TR + HackerNews + VentureBeat AI"""
    print("[全球AI] 抓取 TechCrunch AI RSS...")
    tc = _parse_rss("https://techcrunch.com/category/artificial-intelligence/feed/", 5)
    time.sleep(random.uniform(1, 2))

    print("[全球AI] 抓取 MIT Technology Review RSS...")
    mit = _parse_rss("https://www.technologyreview.com/feed/", 5)
    time.sleep(random.uniform(1, 2))

    print("[全球AI] 抓取 HackerNews...")
    hn = fetch_hackernews(5)
    time.sleep(random.uniform(1, 2))

    print("[全球AI] 抓取 VentureBeat AI RSS...")
    vb = _parse_rss("https://venturebeat.com/category/ai/feed/", 5)

    combined = tc + mit + hn + vb
    seen, unique = set(), []
    for item in combined:
        if item["url"] not in seen and item["url"]:
            seen.add(item["url"])
            item["source"] = "全球AI"
            unique.append(item)
    return unique[:5]


def fetch_robot_news() -> list[dict]:
    """全球机器人动态 Top5 — IEEE Spectrum + TechCrunch Robotics + The Robot Report"""
    print("[机器人] 抓取 IEEE Spectrum RSS...")
    ieee = _parse_rss("https://spectrum.ieee.org/feeds/topic/robotics.rss", 5)
    time.sleep(random.uniform(1, 2))

    print("[机器人] 抓取 TechCrunch Robotics RSS...")
    tc = _parse_rss("https://techcrunch.com/category/robotics/feed/", 5)
    time.sleep(random.uniform(1, 2))

    print("[机器人] 抓取 The Robot Report RSS...")
    rr = _parse_rss("https://www.therobotreport.com/feed/", 5)

    combined = ieee + tc + rr
    seen, unique = set(), []
    for item in combined:
        if item["url"] not in seen and item["url"]:
            seen.add(item["url"])
            item["source"] = "全球机器人"
            unique.append(item)
    return unique[:5]


def fetch_finance_news() -> list[dict]:
    """国际财经 Top5 — Reuters + Bloomberg + WSJ + FT + CNBC"""
    print("[财经] 抓取 Reuters Business RSS...")
    reuters = _parse_rss("https://feeds.reuters.com/reuters/businessNews", 5)
    time.sleep(random.uniform(1, 2))

    print("[财经] 抓取 Bloomberg Markets RSS...")
    bloomberg = _parse_rss("https://feeds.bloomberg.com/markets/news.rss", 5)
    time.sleep(random.uniform(1, 2))

    print("[财经] 抓取 WSJ Markets RSS...")
    wsj = _parse_rss("https://feeds.a.dj.com/rss/RSSMarketsMain.xml", 5)
    time.sleep(random.uniform(1, 2))

    print("[财经] 抓取 Financial Times RSS...")
    ft = _parse_rss("https://www.ft.com/rss/home/uk", 5)
    time.sleep(random.uniform(1, 2))

    print("[财经] 抓取 CNBC Finance RSS...")
    cnbc = _parse_rss("https://www.cnbc.com/id/10000664/device/rss/rss.html", 5)

    combined = reuters + bloomberg + wsj + ft + cnbc
    seen, unique = set(), []
    for item in combined:
        if item["url"] not in seen and item["url"]:
            seen.add(item["url"])
            item["source"] = "国际财经"
            unique.append(item)
    return unique[:5]
