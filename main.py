#!/usr/bin/env python3
"""每日科技日报主入口"""
import json
import os
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import httpx
from crawlers.claude_code_crawler import fetch_all as fetch_claude_code
from crawlers.news_crawler import fetch_github_trending, fetch_ai_news, fetch_tech_news, fetch_world_news, fetch_china_news, fetch_robot_news, fetch_finance_news
from summarizer import summarize_batch
from generate_html import render_html
from wxpusher_sender import send_to_wechat


def fetch_gold_price() -> dict:
    """抓取今日黄金现货价格（CNY/克），来源 Yahoo Finance"""
    try:
        gold_resp = httpx.get(
            "https://query1.finance.yahoo.com/v8/finance/chart/GC=F",
            params={"interval": "1d", "range": "1d"},
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=10,
        )
        gold_resp.raise_for_status()
        meta = gold_resp.json()["chart"]["result"][0]["meta"]
        price_usd = meta["regularMarketPrice"]
        prev_usd = meta.get("chartPreviousClose", price_usd)

        cny_resp = httpx.get(
            "https://query1.finance.yahoo.com/v8/finance/chart/USDCNY=X",
            params={"interval": "1d", "range": "1d"},
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=10,
        )
        cny_resp.raise_for_status()
        usd_cny = cny_resp.json()["chart"]["result"][0]["meta"]["regularMarketPrice"]

        oz_to_gram = 31.1035
        price_cny = price_usd * usd_cny / oz_to_gram
        prev_cny = prev_usd * usd_cny / oz_to_gram
        change = price_cny - prev_cny
        change_pct = change / prev_cny * 100 if prev_cny else 0
        return {"price": price_cny, "change": change, "change_pct": change_pct}
    except Exception as e:
        print(f"[金价] 抓取失败: {e}")
        return {}

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
CST = timezone(timedelta(hours=8))
TODAY = datetime.now(CST).strftime("%Y-%m-%d")
NOW_STR = datetime.now(CST).strftime("%Y-%m-%d %H:%M")
DATA_DIR = Path(__file__).parent / "data"
DOCS_DIR = Path(__file__).parent / "docs"
DATA_DIR.mkdir(exist_ok=True)
DOCS_DIR.mkdir(exist_ok=True)


def main():
    print(f"=== 你关注的热点 {NOW_STR} ===\n")

    # 1. 抓取数据
    print("--- 抓取今日金价 ---")
    gold = fetch_gold_price()
    if gold:
        sign = "+" if gold["change"] >= 0 else ""
        print(f"  → ¥{gold['price']:.2f}/克 ({sign}{gold['change_pct']:.2f}%)")

    print("\n--- 抓取国际新闻 ---")
    world_items = fetch_world_news()

    print("\n--- 抓取国内新闻 ---")
    china_items = fetch_china_news()

    print("\n--- 抓取全球科技 ---")
    tech_items = fetch_tech_news()

    print("\n--- 抓取国际财经 ---")
    finance_items = fetch_finance_news()

    print("\n--- 抓取全球AI ---")
    ai_items = fetch_ai_news()

    print("\n--- 抓取全球机器人 ---")
    robot_items = fetch_robot_news()

    print("\n--- 抓取 GitHub Trending Top5 ---")
    github_trending = fetch_github_trending(GITHUB_TOKEN, count=5)
    print(f"  → {len(github_trending)} 条")

    print("\n--- 抓取 Claude Code ---")
    claude_items = fetch_claude_code(GITHUB_TOKEN)
    print(f"  → {len(claude_items)} 条")

    # 2. 生成摘要
    print("\n--- 生成摘要 ---")
    all_items = world_items + china_items + tech_items + finance_items + ai_items + robot_items + github_trending + claude_items
    all_items = summarize_batch(all_items)

    # 按来源重新分组（保持原始顺序）
    world_final = [x for x in all_items if x in world_items][:5]
    china_final = [x for x in all_items if x in china_items][:5]
    tech_final = [x for x in all_items if x in tech_items][:5]
    finance_final = [x for x in all_items if x in finance_items][:5]
    ai_final = [x for x in all_items if x in ai_items][:5]
    robot_final = [x for x in all_items if x in robot_items][:5]
    trending_final = [x for x in all_items if x in github_trending][:5]
    claude_final = [x for x in all_items if x in claude_items][:5]

    data = {
        "date": NOW_STR,
        "gold": gold,
        "sections": {
            "world_news": world_final,
            "china_news": china_final,
            "tech_news": tech_final,
            "finance_news": finance_final,
            "ai_news": ai_final,
            "robot_news": robot_final,
            "github_trending": trending_final,
            "claude_code": claude_final,
        },
    }

    # 3. 保存 JSON 存档
    json_path = DATA_DIR / f"{TODAY}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"\n[存档] {json_path}")

    # 4. 生成 HTML
    render_html(data, str(DOCS_DIR / "index.html"))

    # 5. 推送微信
    print("\n--- 推送微信 ---")
    send_to_wechat(data)

    print("\n=== 完成 ===")


if __name__ == "__main__":
    main()
