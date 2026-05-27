from datetime import datetime

_CSS = """\
:root {
  --bg: #06080b; --s1: #0c1016; --bdr: #1c2535;
  --acc: #3effa0; --acc2: #ff6e40;
  --t1: #cdd6e0; --t2: #7a8a9a; --t3: #37455a;
  --fh: 'Syne', sans-serif; --fb: 'Lora', serif; --fm: 'JetBrains Mono', monospace;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; }
body { background: var(--bg); color: var(--t1); font-family: var(--fb); }
body::before {
  content: ''; position: fixed; inset: 0; pointer-events: none; z-index: 0;
  background: repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(255,255,255,.008) 2px, rgba(255,255,255,.008) 4px);
}
header {
  position: relative; padding: 48px 32px 40px;
  background: linear-gradient(140deg, #0b1520 0%, #060810 65%);
  border-bottom: 1px solid var(--bdr); overflow: hidden;
}
header::after {
  content: ''; position: absolute; bottom: 0; left: 0; right: 0;
  height: 2px; background: linear-gradient(90deg, transparent, var(--acc) 50%, transparent);
}
.badge {
  font-family: var(--fm); font-size: 10px; letter-spacing: .2em; text-transform: uppercase;
  color: var(--acc); display: flex; align-items: center; gap: 8px; margin-bottom: 16px;
}
.badge::before {
  content: ''; width: 6px; height: 6px; background: var(--acc);
  border-radius: 50%; animation: blink 2s infinite; flex-shrink: 0;
}
h1 {
  font-family: var(--fh); font-size: clamp(26px, 5vw, 50px); font-weight: 800;
  letter-spacing: -.02em; color: #fff; line-height: 1;
}
.hdate { font-family: var(--fm); font-size: 11px; color: var(--t2); margin-top: 12px; }
.bgword {
  position: absolute; right: -8px; top: -4px; font-family: var(--fh); font-size: 160px;
  font-weight: 800; color: rgba(255,255,255,.018); line-height: 1;
  pointer-events: none; user-select: none;
}
nav {
  position: sticky; top: 0; z-index: 100;
  background: rgba(6,8,11,.9); backdrop-filter: blur(16px);
  border-bottom: 1px solid var(--bdr); padding: 0 20px;
  display: flex; gap: 0; overflow-x: auto; scrollbar-width: none;
}
nav::-webkit-scrollbar { display: none; }
nav a {
  font-family: var(--fm); font-size: 10.5px; letter-spacing: .06em;
  color: var(--t2); text-decoration: none; padding: 11px 14px;
  white-space: nowrap; border-bottom: 2px solid transparent;
  transition: color .2s, border-color .2s;
}
nav a:hover { color: var(--t1); }
nav a.active { color: var(--acc); border-bottom-color: var(--acc); }
main { max-width: 800px; margin: 0 auto; padding: 36px 20px 72px; }
.s { margin-bottom: 52px; animation: up .5s both; }
.s:nth-child(1) { animation-delay: .0s; }
.s:nth-child(2) { animation-delay: .06s; }
.s:nth-child(3) { animation-delay: .12s; }
.s:nth-child(4) { animation-delay: .18s; }
.s:nth-child(5) { animation-delay: .24s; }
.s:nth-child(6) { animation-delay: .30s; }
.s:nth-child(7) { animation-delay: .36s; }
.sh {
  display: flex; align-items: center; gap: 12px;
  margin-bottom: 20px; padding-bottom: 12px; border-bottom: 1px solid var(--bdr);
}
.sn {
  font-family: var(--fm); font-size: 10px; letter-spacing: .1em; color: var(--acc);
  background: rgba(62,255,160,.07); border: 1px solid rgba(62,255,160,.18);
  padding: 3px 8px; border-radius: 3px; flex-shrink: 0;
}
.sh h2 { font-family: var(--fh); font-size: 15px; font-weight: 700; color: #fff; }
.item {
  display: flex; gap: 16px; padding: 15px 14px;
  margin: 0 -14px; border-bottom: 1px solid var(--bdr);
  border-left: 2px solid transparent; border-radius: 0;
  transition: background .2s, border-color .2s, border-radius .2s;
}
.item:last-child { border-bottom: none; }
.item:hover {
  background: var(--s1); border-left-color: var(--acc); border-radius: 0 6px 6px 0;
  border-bottom-color: transparent;
}
.rk {
  font-family: var(--fm); font-size: 12px; color: var(--t3);
  min-width: 22px; padding-top: 3px; flex-shrink: 0; transition: color .2s;
}
.item:hover .rk { color: var(--acc); }
.bd { flex: 1; min-width: 0; }
.tt {
  display: block; font-family: var(--fb); font-size: 15px; font-weight: 500;
  color: var(--t1); text-decoration: none; line-height: 1.5; margin-bottom: 7px;
  transition: color .2s;
}
.tt:hover { color: var(--acc); }
.mt { display: flex; gap: 10px; align-items: center; margin-bottom: 9px; flex-wrap: wrap; }
.sc {
  font-family: var(--fm); font-size: 9.5px; letter-spacing: .08em; color: var(--acc2);
  background: rgba(255,110,64,.07); border: 1px solid rgba(255,110,64,.18);
  padding: 2px 7px; border-radius: 3px;
}
.dt { font-family: var(--fm); font-size: 10px; color: var(--t3); }
.sm { font-size: 13px; color: var(--t2); line-height: 1.72; font-style: italic; }
.empty { font-family: var(--fm); font-size: 12px; color: var(--t3); padding: 16px 0; }
footer {
  text-align: center; padding: 32px 20px; font-family: var(--fm); font-size: 10px;
  letter-spacing: .15em; color: var(--t3); border-top: 1px solid var(--bdr); text-transform: uppercase;
}
@keyframes up { from { opacity: 0; transform: translateY(14px); } to { opacity: 1; transform: translateY(0); } }
@keyframes blink { 0%,100% { opacity: 1; } 50% { opacity: .2; } }
@media (max-width: 600px) {
  header { padding: 32px 20px 28px; }
  .bgword { font-size: 100px; }
  h1 { font-size: 26px; }
  main { padding: 24px 16px 48px; }
}"""

_JS = """\
const links = document.querySelectorAll('nav a');
const secs = document.querySelectorAll('.s');
links.forEach(a => a.addEventListener('click', function() {
  links.forEach(x => x.classList.remove('active'));
  this.classList.add('active');
}));
const obs = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      const id = e.target.id;
      links.forEach(a => a.classList.toggle('active', a.getAttribute('href') === '#' + id));
    }
  });
}, { threshold: 0.25 });
secs.forEach(s => obs.observe(s));"""


def render_html(data: dict, output_path: str):
    date_str = data.get("date", datetime.now().strftime("%Y-%m-%d %H:%M"))
    sections = data.get("sections", {})

    def render_section(title: str, items: list, section_id: str, num: str) -> str:
        head = f'<div class="sh"><span class="sn">{num}</span><h2>{title}</h2></div>'
        if not items:
            return f'<section class="s" id="{section_id}">{head}<p class="empty">暂无数据</p></section>'
        rows = "".join(
            f'<article class="item">'
            f'<span class="rk">{i:02d}</span>'
            f'<div class="bd">'
            f'<a href="{item.get("url","#")}" class="tt" target="_blank" rel="noopener">{item.get("title","")}</a>'
            f'<div class="mt"><span class="sc">{item.get("source","")}</span>'
            f'<span class="dt">{item.get("published","")}</span></div>'
            f'<p class="sm">{item.get("summary", item.get("title",""))}</p>'
            f'</div></article>'
            for i, item in enumerate(items, 1)
        )
        return f'<section class="s" id="{section_id}">{head}<div class="items">{rows}</div></section>'

    w  = sections.get("world_news", [])
    c  = sections.get("china_news", [])
    t  = sections.get("tech_news", [])
    a  = sections.get("ai_news", [])
    r  = sections.get("robot_news", [])
    g  = sections.get("github_trending", [])
    cl = sections.get("claude_code", [])

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>你关注的热点 · {date_str}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=Lora:ital,wght@0,400;0,500;1,400&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>{_CSS}</style>
</head>
<body>
<header>
  <div class="bgword">热点</div>
  <div class="badge">Daily Signal · Auto-Generated</div>
  <h1>你关注的热点</h1>
  <div class="hdate">{date_str}</div>
</header>
<nav>
  <a href="#world-news" class="active">国际新闻</a>
  <a href="#china-news">国内新闻</a>
  <a href="#tech-news">全球科技</a>
  <a href="#ai-news">全球 AI</a>
  <a href="#robot-news">机器人</a>
  <a href="#github-trending">GitHub</a>
  <a href="#claude-code">Claude Code</a>
</nav>
<main>
  {render_section("国际新闻事件 Top 5", w,  "world-news",      "01")}
  {render_section("国内新闻 Top 5",     c,  "china-news",      "02")}
  {render_section("全球科技动态 Top 5", t,  "tech-news",       "03")}
  {render_section("全球 AI 动态 Top 5", a,  "ai-news",         "04")}
  {render_section("全球机器人动态 Top 5",r, "robot-news",      "05")}
  {render_section("GitHub 每日 Top 5",  g,  "github-trending", "06")}
  {render_section("Claude Code 资讯 Top 5", cl, "claude-code", "07")}
</main>
<footer>Signal · 数据每日自动更新 · Claude Haiku 生成摘要</footer>
<script>{_JS}</script>
</body>
</html>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[HTML] 已生成: {output_path}")
