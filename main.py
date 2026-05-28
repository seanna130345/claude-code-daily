#!/usr/bin/env python3
"""每日科技日报主入口"""
import json
import os
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from crawlers.claude_code_crawler import fetch_all as fetch_claude_code
from crawlers.news_crawler import fetch_github_trending, fetch_ai_news, fetch_tech_news, fetch_world_news, fetch_china_news, fetch_robot_news, fetch_finance_news
from summarizer import summarize_batch
from generate_html import render_html
from wxpusher_sender import send_to_wechat

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
    print("--- 抓取国际新闻 ---")
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
