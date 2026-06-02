import httpx
import os
from datetime import datetime


SEND_KEYS = [k.strip() for k in os.environ.get("SERVER_CHAN_KEYS", os.environ.get("SERVER_CHAN_KEY", "")).split(",") if k.strip()]
PAGES_URL = os.environ.get("PAGES_URL", "")


def _format_message(data: dict) -> tuple[str, str]:
    """返回 (title, content)"""
    date_str = data.get("date", datetime.now().strftime("%Y-%m-%d"))
    sections = data.get("sections", {})

    title = f"你关注的热点 {date_str}"

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
            lines.append("")
            lines.append(summary)
            lines.append("")
        lines.append("")

    add_section("国际新闻事件 Top 5", sections.get("world_news", []), 5)
    add_section("国内新闻 Top 5", sections.get("china_news", []), 5)
    add_section("全球科技动态 Top 5", sections.get("tech_news", []), 5)
    add_section("国际财经 Top 5", sections.get("finance_news", []), 5)
    add_section("全球AI动态 Top 5", sections.get("ai_news", []), 5)
    add_section("全球机器人动态 Top 5", sections.get("robot_news", []), 5)
    add_section("GitHub 每日 Top 5", sections.get("github_trending", []), 5)
    add_section("Claude Code 项目/资讯 Top 5", sections.get("claude_code", []), 5)

    if PAGES_URL:
        lines.append(f"---\n[查看完整网页日报]({PAGES_URL})")

    return title, "\n".join(lines)


def send_to_wechat(data: dict) -> bool:
    if not SEND_KEYS:
        print("[Server酱] 未配置 SERVER_CHAN_KEYS，跳过推送")
        return False

    title, content = _format_message(data)
    success = 0
    for key in SEND_KEYS:
        try:
            resp = httpx.post(
                f"https://sctapi.ftqq.com/{key}.send",
                data={"title": title, "desp": content},
                timeout=15,
            )
            resp.raise_for_status()
            result = resp.json()
            if result.get("code") == 0:
                print(f"[Server酱] 推送成功: {key[:8]}...")
                success += 1
            else:
                print(f"[Server酱] 推送失败: {key[:8]}... {result.get('message', '')}")
        except Exception as e:
            print(f"[Server酱] 推送异常: {key[:8]}... {e}")
    return success > 0
