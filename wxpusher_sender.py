import httpx
import os
import json
from datetime import datetime


APP_TOKEN = os.environ.get("WXPUSHER_APP_TOKEN", "")
UID = os.environ.get("WXPUSHER_UID", "")
PAGES_URL = os.environ.get("PAGES_URL", "")


def _format_message(data: dict) -> str:
    date_str = data.get("date", datetime.now().strftime("%Y-%m-%d"))
    sections = data.get("sections", {})

    lines = [f"# 每日科技日报 {date_str}\n"]

    def add_section(title: str, items: list, count: int):
        if not items:
            return
        lines.append(f"\n## {title}\n")
        for i, item in enumerate(items[:count], 1):
            summary = item.get("summary", item.get("title", ""))
            url = item.get("url", "#")
            item_title = item.get("title", "")
            lines.append(f"{i}. **[{item_title}]({url})**")
            lines.append(f"   {summary}\n")

    add_section("Claude Code 项目/资讯", sections.get("claude_code", []), 10)
    add_section("全球AI动态 Top 10", sections.get("ai_news", []), 10)
    add_section("科技发展 Top 5", sections.get("tech_news", []), 5)
    add_section("国际新闻事件 Top 5", sections.get("world_news", []), 5)

    if PAGES_URL:
        lines.append(f"\n---\n[查看完整日报]({PAGES_URL})")

    return "\n".join(lines)


def send_to_wechat(data: dict) -> bool:
    if not APP_TOKEN or not UID:
        print("[WxPusher] 未配置 APP_TOKEN 或 UID，跳过推送")
        return False

    content = _format_message(data)
    date_str = data.get("date", datetime.now().strftime("%Y-%m-%d"))

    payload = {
        "appToken": APP_TOKEN,
        "content": content,
        "summary": f"每日科技日报 {date_str}",
        "contentType": 3,  # 3 = Markdown
        "uids": [UID],
        "url": PAGES_URL or "",
    }

    try:
        resp = httpx.post(
            "https://wxpusher.zjiecode.com/api/send/message",
            json=payload,
            timeout=15,
        )
        resp.raise_for_status()
        result = resp.json()
        if result.get("success"):
            print(f"[WxPusher] 推送成功")
            return True
        else:
            print(f"[WxPusher] 推送失败: {result.get('msg', '')}")
            return False
    except Exception as e:
        print(f"[WxPusher] 推送异常: {e}")
        return False
