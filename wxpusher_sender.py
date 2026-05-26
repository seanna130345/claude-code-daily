import httpx
import os
from datetime import datetime


SEND_KEY = os.environ.get("SERVER_CHAN_KEY", "")
PAGES_URL = os.environ.get("PAGES_URL", "")


def _format_message(data: dict) -> tuple[str, str]:
    """返回 (title, content)"""
    date_str = data.get("date", datetime.now().strftime("%Y-%m-%d"))
    sections = data.get("sections", {})

    title = f"每日科技日报 {date_str}"

    lines = []

    def add_section(heading: str, items: list, count: int):
        if not items:
            return
        lines.append(f"## {heading}")
        for i, item in enumerate(items[:count], 1):
            summary = item.get("summary", item.get("title", ""))
            url = item.get("url", "#")
            item_title = item.get("title", "")
            lines.append(f"{i}. [{item_title}]({url})")
            lines.append(f"   > {summary}")
        lines.append("")

    add_section("Claude Code 项目/资讯", sections.get("claude_code", []), 10)
    add_section("全球AI动态 Top 10", sections.get("ai_news", []), 10)
    add_section("科技发展 Top 5", sections.get("tech_news", []), 5)
    add_section("国际新闻事件 Top 5", sections.get("world_news", []), 5)

    if PAGES_URL:
        lines.append(f"---\n[查看完整网页日报]({PAGES_URL})")

    return title, "\n".join(lines)


def send_to_wechat(data: dict) -> bool:
    if not SEND_KEY:
        print("[Server酱] 未配置 SERVER_CHAN_KEY，跳过推送")
        return False

    title, content = _format_message(data)

    try:
        resp = httpx.post(
            f"https://sctapi.ftqq.com/{SEND_KEY}.send",
            data={"title": title, "desp": content},
            timeout=15,
        )
        resp.raise_for_status()
        result = resp.json()
        if result.get("code") == 0:
            print("[Server酱] 推送成功")
            return True
        else:
            print(f"[Server酱] 推送失败: {result.get('message', '')}")
            return False
    except Exception as e:
        print(f"[Server酱] 推送异常: {e}")
        return False
