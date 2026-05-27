from datetime import datetime


def render_html(data: dict, output_path: str):
    date_str = data.get("date", datetime.now().strftime("%Y-%m-%d"))
    sections = data.get("sections", {})

    def render_section(title: str, items: list, section_id: str) -> str:
        if not items:
            return f'<div class="section" id="{section_id}"><h2>{title}</h2><p class="empty">暂无数据</p></div>'
        rows = ""
        for i, item in enumerate(items, 1):
            source_badge = f'<span class="badge">{item.get("source", "")}</span>'
            summary = item.get("summary", item.get("title", ""))
            url = item.get("url", "#")
            title_text = item.get("title", "")
            pub = item.get("published", "")
            rows += f"""
            <div class="item">
              <div class="item-header">
                <span class="num">{i}</span>
                {source_badge}
                <span class="pub-date">{pub}</span>
              </div>
              <div class="item-title"><a href="{url}" target="_blank" rel="noopener">{title_text}</a></div>
              <div class="item-summary">{summary}</div>
            </div>"""
        return f'<div class="section" id="{section_id}"><h2>{title}</h2>{rows}</div>'

    trending_items = sections.get("github_trending", [])
    claude_items = sections.get("claude_code", [])
    ai_items = sections.get("ai_news", [])
    tech_items = sections.get("tech_news", [])
    world_items = sections.get("world_news", [])
    china_items = sections.get("china_news", [])

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>每日科技日报 · {date_str}</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: #f5f5f5; color: #333; }}
  header {{ background: #1a1a2e; color: #fff; padding: 20px 24px; }}
  header h1 {{ font-size: 20px; font-weight: 600; }}
  header .date {{ font-size: 13px; color: #aaa; margin-top: 4px; }}
  nav {{ background: #fff; border-bottom: 1px solid #e0e0e0; padding: 0 24px; display: flex; gap: 0; overflow-x: auto; }}
  nav a {{ display: block; padding: 12px 16px; font-size: 14px; color: #555; text-decoration: none; white-space: nowrap; border-bottom: 2px solid transparent; }}
  nav a:hover, nav a.active {{ color: #1a1a2e; border-bottom-color: #1a1a2e; }}
  main {{ max-width: 860px; margin: 24px auto; padding: 0 16px; }}
  .section {{ background: #fff; border-radius: 8px; padding: 20px; margin-bottom: 24px; }}
  .section h2 {{ font-size: 16px; font-weight: 600; margin-bottom: 16px; padding-bottom: 10px; border-bottom: 1px solid #eee; }}
  .item {{ padding: 12px 0; border-bottom: 1px solid #f0f0f0; }}
  .item:last-child {{ border-bottom: none; padding-bottom: 0; }}
  .item-header {{ display: flex; align-items: center; gap: 8px; margin-bottom: 6px; }}
  .num {{ font-size: 12px; color: #999; min-width: 18px; }}
  .badge {{ font-size: 11px; background: #f0f0f0; color: #666; padding: 2px 7px; border-radius: 10px; }}
  .pub-date {{ font-size: 11px; color: #bbb; margin-left: auto; }}
  .item-title a {{ font-size: 14px; color: #1a1a2e; text-decoration: none; line-height: 1.5; }}
  .item-title a:hover {{ text-decoration: underline; }}
  .item-summary {{ font-size: 13px; color: #666; margin-top: 4px; line-height: 1.6; }}
  .empty {{ color: #999; font-size: 14px; }}
  footer {{ text-align: center; padding: 24px; font-size: 12px; color: #bbb; }}
</style>
</head>
<body>
<header>
  <h1>每日科技日报</h1>
  <div class="date">{date_str} · 自动生成</div>
</header>
<nav>
  <a href="#world-news" class="active">国际新闻 ({len(world_items)})</a>
  <a href="#china-news">国内新闻 ({len(china_items)})</a>
  <a href="#tech-news">科技 ({len(tech_items)})</a>
  <a href="#ai-news">全球AI ({len(ai_items)})</a>
  <a href="#github-trending">GitHub Top5 ({len(trending_items)})</a>
  <a href="#claude-code">Claude Code ({len(claude_items)})</a>
</nav>
<main>
  {render_section(f"国际新闻事件 · Top {len(world_items)}", world_items, "world-news")}
  {render_section(f"国内新闻 · Top {len(china_items)}", china_items, "china-news")}
  {render_section(f"全球科技动态 · Top {len(tech_items)}", tech_items, "tech-news")}
  {render_section(f"全球AI动态 · Top {len(ai_items)}", ai_items, "ai-news")}
  {render_section(f"GitHub 每日 Top 5（按标星排名）", trending_items, "github-trending")}
  {render_section(f"Claude Code 项目/资讯 · Top {len(claude_items)}", claude_items, "claude-code")}
</main>
<footer>数据每日自动更新 · 由 Claude Haiku 生成摘要</footer>
<script>
  document.querySelectorAll('nav a').forEach(a => {{
    a.addEventListener('click', function() {{
      document.querySelectorAll('nav a').forEach(x => x.classList.remove('active'));
      this.classList.add('active');
    }});
  }});
</script>
</body>
</html>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[HTML] 已生成: {output_path}")
