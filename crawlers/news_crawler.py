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


def _bing_search(query: str, count: int = 5, freshness: str = "Day") -> list[dict]:
    url = "https://www.bing.com/search"
    params = {"q": query, "count": count, "freshness": freshness}
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
    """国际新闻 Top5 — BBC + AP News + Al Jazeera + Bing"""
    print("[国际] 抓取 BBC RSS...")
    bbc = _parse_rss("https://feeds.bbci.co.uk/news/world/rss.xml", 5)
    time.sleep(random.uniform(1, 2))

    print("[国际] 抓取 AP News RSS...")
    ap = _parse_rss("https://rsshub.app/apnews/topics/apf-topnews", 5)
    time.sleep(random.uniform(1, 2))

    print("[国际] 抓取 Al Jazeera RSS...")
    alj = _parse_rss("https://www.aljazeera.com/xml/rss/all.xml", 5)
    time.sleep(random.uniform(1, 2))

    print("[国际] 抓取 Bing...")
    bing = _bing_search("international world news breaking today", 5)

    combined = bbc + ap + alj + bing
    seen, unique = set(), []
    for item in combined:
        if item["url"] not in seen and item["url"]:
            seen.add(item["url"])
            item["source"] = "国际新闻"
            unique.append(item)
    return unique[:5]


def fetch_china_news() -> list[dict]:
    """国内新闻 Top5 — 36kr + 搜狗新闻 + Bing"""
    print("[国内] 抓取 36kr RSS...")
    kr36 = _parse_rss("https://36kr.com/feed", 5)
    time.sleep(random.uniform(1, 2))

    print("[国内] 抓取 Bing 国内新闻...")
    bing = _bing_search("中国 国内 新闻 今日 热点", 5)
    time.sleep(random.uniform(1, 2))

    print("[国内] 抓取 澎湃新闻 RSS...")
    thepaper = _parse_rss("https://www.thepaper.cn/rss_cn.jsp", 5)

    combined = kr36 + thepaper + bing
    seen, unique = set(), []
    for item in combined:
        if item["url"] not in seen and item["url"]:
            seen.add(item["url"])
            item["source"] = "国内新闻"
            unique.append(item)
    return unique[:5]


def fetch_tech_news() -> list[dict]:
    """全球科技动态 Top5 — TechCrunch + The Verge + Wired + Bing"""
    print("[科技] 抓取 TechCrunch RSS...")
    tc = _parse_rss("https://techcrunch.com/feed/", 5)
    time.sleep(random.uniform(1, 2))

    print("[科技] 抓取 The Verge RSS...")
    verge = _parse_rss("https://www.theverge.com/rss/index.xml", 5)
    time.sleep(random.uniform(1, 2))

    print("[科技] 抓取 Wired RSS...")
    wired = _parse_rss("https://www.wired.com/feed/rss", 5)
    time.sleep(random.uniform(1, 2))

    print("[科技] 抓取 Bing...")
    bing = _bing_search("technology innovation news today 2026", 5)

    combined = tc + verge + wired + bing
    seen, unique = set(), []
    for item in combined:
        if item["url"] not in seen and item["url"]:
            seen.add(item["url"])
            item["source"] = "科技"
            unique.append(item)
    return unique[:5]


def fetch_ai_news() -> list[dict]:
    """全球AI动态 Top5 — TechCrunch AI + MIT TR + HackerNews + Bing"""
    print("[全球AI] 抓取 TechCrunch AI RSS...")
    tc = _parse_rss("https://techcrunch.com/category/artificial-intelligence/feed/", 5)
    time.sleep(random.uniform(1, 2))

    print("[全球AI] 抓取 MIT Technology Review RSS...")
    mit = _parse_rss("https://www.technologyreview.com/feed/", 5)
    time.sleep(random.uniform(1, 2))

    print("[全球AI] 抓取 HackerNews...")
    hn = fetch_hackernews(5)
    time.sleep(random.uniform(1, 2))

    print("[全球AI] 抓取 Bing...")
    bing = _bing_search("AI artificial intelligence latest news today 2026", 5)

    combined = tc + mit + hn + bing
    seen, unique = set(), []
    for item in combined:
        if item["url"] not in seen and item["url"]:
            seen.add(item["url"])
            item["source"] = "全球AI"
            unique.append(item)
    return unique[:5]


def fetch_robot_news() -> list[dict]:
    """全球机器人动态 Top5 — IEEE Spectrum + TechCrunch Robotics + Bing"""
    print("[机器人] 抓取 IEEE Spectrum RSS...")
    ieee = _parse_rss("https://spectrum.ieee.org/feeds/topic/robotics.rss", 5)
    time.sleep(random.uniform(1, 2))

    print("[机器人] 抓取 TechCrunch Robotics RSS...")
    tc = _parse_rss("https://techcrunch.com/category/robotics/feed/", 5)
    time.sleep(random.uniform(1, 2))

    print("[机器人] 抓取 Bing...")
    bing = _bing_search("robotics robot humanoid latest news 2026", 5)

    combined = ieee + tc + bing
    seen, unique = set(), []
    for item in combined:
        if item["url"] not in seen and item["url"]:
            seen.add(item["url"])
            item["source"] = "全球机器人"
            unique.append(item)
    return unique[:5]
