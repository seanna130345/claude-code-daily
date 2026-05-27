from datetime import datetime

_CSS = """\
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,700;1,9..144,300&family=Plus+Jakarta+Sans:wght@400;500;600&family=Fira+Code:wght@400;500&display=swap');

:root {
  --white:   #ffffff;
  --bg:      #f5f4f0;
  --card:    #ffffff;
  --bdr:     #e8e5de;
  --bdr2:    #d0ccc3;
  --ink:     #1c1b18;
  --ink2:    #5a5750;
  --ink3:    #a09c95;
  --teal:    #1b7a6e;
  --teal-bg: #edf6f4;
  --amber:   #b85c00;
  --amber-bg:#fdf3e8;
  --rose:    #a83240;
  --rose-bg: #fdf0f2;
  --sky:     #1a5276;
  --sky-bg:  #eaf1f8;
  --sage:    #3d6b4f;
  --sage-bg: #edf4ef;
  --slate:   #374151;
  --slate-bg:#f0f2f5;
  --fh: 'Fraunces', Georgia, serif;
  --fb: 'Plus Jakarta Sans', sans-serif;
  --fm: 'Fira Code', monospace;
}

* { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; }
body { background: var(--bg); color: var(--ink); font-family: var(--fb); font-size: 15px; }

/* ── Header ── */
header {
  background: var(--white);
  border-bottom: 1px solid var(--bdr);
}
.header-band {
  background: var(--teal);
  padding: 7px 32px;
  display: flex; align-items: center; justify-content: space-between;
}
.header-band-text {
  font-family: var(--fm); font-size: 10px; letter-spacing: .15em;
  text-transform: uppercase; color: rgba(255,255,255,.75);
}
.live-dot {
  width: 6px; height: 6px; border-radius: 50%;
  background: #5effd8; display: inline-block;
  margin-right: 7px; animation: blink 2s ease-in-out infinite;
}
.header-body {
  max-width: 920px; margin: 0 auto;
  padding: 32px 28px 28px;
  display: flex; align-items: flex-end; justify-content: space-between; gap: 24px;
}
.header-title {}
h1 {
  font-family: var(--fh); font-size: clamp(30px, 5.5vw, 56px);
  font-weight: 700; color: var(--ink); letter-spacing: -.025em; line-height: 1.08;
  font-style: italic;
}
.header-desc {
  font-size: 13px; color: var(--ink3); margin-top: 10px; line-height: 1.5;
}
.header-stats {
  display: flex; gap: 20px; flex-shrink: 0; padding-bottom: 4px;
}
.stat { text-align: center; }
.stat-n {
  font-family: var(--fh); font-size: 28px; font-weight: 700;
  color: var(--teal); line-height: 1;
}
.stat-l { font-size: 11px; color: var(--ink3); margin-top: 3px; }

/* ── Nav ── */
nav {
  position: sticky; top: 0; z-index: 100;
  background: rgba(255,255,255,.95); backdrop-filter: blur(10px);
  border-bottom: 1px solid var(--bdr);
}
.nav-wrap {
  max-width: 920px; margin: 0 auto; padding: 0 28px;
  display: flex; overflow-x: auto; scrollbar-width: none;
}
nav::-webkit-scrollbar { display: none; }
nav a {
  font-family: var(--fb); font-size: 12.5px; font-weight: 500;
  color: var(--ink2); text-decoration: none;
  padding: 12px 15px; white-space: nowrap;
  border-bottom: 2px solid transparent; margin-bottom: -1px;
  transition: color .18s, border-color .18s;
}
nav a:hover { color: var(--ink); }
nav a.active { color: var(--teal); border-bottom-color: var(--teal); }

/* ── Main ── */
main { max-width: 920px; margin: 0 auto; padding: 28px 28px 80px; }

/* ── Section card ── */
.s {
  background: var(--card);
  border: 1px solid var(--bdr);
  border-radius: 12px;
  margin-bottom: 20px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0,0,0,.04);
  animation: rise .4s both;
}
.s:nth-child(1){animation-delay:.00s} .s:nth-child(2){animation-delay:.05s}
.s:nth-child(3){animation-delay:.10s} .s:nth-child(4){animation-delay:.15s}
.s:nth-child(5){animation-delay:.20s} .s:nth-child(6){animation-delay:.25s}
.s:nth-child(7){animation-delay:.30s}

.sh {
  display: flex; align-items: center; gap: 10px;
  padding: 14px 20px;
  border-bottom: 1px solid var(--bdr);
}
.s-icon {
  width: 28px; height: 28px; border-radius: 7px;
  display: flex; align-items: center; justify-content: center;
  font-size: 14px; flex-shrink: 0;
}
.sh h2 { font-family: var(--fb); font-size: 14px; font-weight: 600; color: var(--ink); flex: 1; }
.sh .cnt {
  font-family: var(--fm); font-size: 10.5px; color: var(--ink3);
  background: var(--bg); border: 1px solid var(--bdr);
  padding: 2px 8px; border-radius: 20px;
}

/* section color themes */
.s-world  .s-icon { background: var(--rose-bg);  color: var(--rose); }
.s-china  .s-icon { background: var(--amber-bg); color: var(--amber); }
.s-tech   .s-icon { background: var(--sky-bg);   color: var(--sky); }
.s-ai     .s-icon { background: var(--teal-bg);  color: var(--teal); }
.s-robot  .s-icon { background: var(--sage-bg);  color: var(--sage); }
.s-github .s-icon { background: var(--slate-bg); color: var(--slate); }
.s-claude .s-icon { background: var(--amber-bg); color: var(--amber); }

/* ── Item ── */
.item {
  display: flex; gap: 14px; padding: 14px 20px;
  border-bottom: 1px solid var(--bdr);
  transition: background .15s;
  cursor: pointer;
}
.item:last-child { border-bottom: none; }
.item:hover { background: #fbfaf8; }

.rk {
  font-family: var(--fm); font-size: 11px; color: var(--bdr2);
  min-width: 18px; padding-top: 3px; flex-shrink: 0;
  font-weight: 500;
}

.bd { flex: 1; min-width: 0; }

.tt {
  display: block; font-family: var(--fb); font-size: 14.5px; font-weight: 500;
  color: var(--ink); text-decoration: none; line-height: 1.55;
  margin-bottom: 6px; transition: color .15s;
}
.tt:hover { color: var(--teal); }

.mt { display: flex; gap: 7px; align-items: center; margin-bottom: 8px; flex-wrap: wrap; }
.sc {
  font-family: var(--fm); font-size: 10px; font-weight: 500;
  color: var(--teal); background: var(--teal-bg);
  padding: 2px 8px; border-radius: 5px;
}
.dt { font-family: var(--fm); font-size: 10px; color: var(--ink3); }

.sm { font-size: 13px; color: var(--ink2); line-height: 1.75; }

.empty { font-size: 13px; color: var(--ink3); padding: 20px; font-style: italic; }

/* ── Footer ── */
footer {
  text-align: center; padding: 28px 20px;
  font-family: var(--fm); font-size: 10px; letter-spacing: .1em;
  text-transform: uppercase; color: var(--ink3);
  border-top: 1px solid var(--bdr);
}

@keyframes rise {
  from { opacity: 0; transform: translateY(10px); }
  to   { opacity: 1; transform: translateY(0); }
}
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:.3} }

@media (max-width: 640px) {
  .header-body { flex-direction: column; align-items: flex-start; gap: 16px; }
  .header-stats { gap: 16px; }
  h1 { font-size: 30px; }
  main { padding: 20px 16px 60px; }
  .sh { padding: 12px 16px; }
  .item { padding: 12px 16px; }
  .header-band { padding: 7px 16px; }
}"""

_JS = """\
const links = document.querySelectorAll('nav a');
const secs  = document.querySelectorAll('.s');
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
}, { rootMargin: '-15% 0px -65% 0px' });
secs.forEach(s => obs.observe(s));"""

_ICONS = {
    "world-news":      ("🌍", "s-world"),
    "china-news":      ("🇨🇳", "s-china"),
    "tech-news":       ("💡", "s-tech"),
    "ai-news":         ("🤖", "s-ai"),
    "robot-news":      ("⚙️", "s-robot"),
    "github-trending": ("⭐", "s-github"),
    "claude-code":     ("✦", "s-claude"),
}


def render_html(data: dict, output_path: str):
    date_str = data.get("date", datetime.now().strftime("%Y-%m-%d %H:%M"))
    sections = data.get("sections", {})

    w  = sections.get("world_news", [])
    c  = sections.get("china_news", [])
    t  = sections.get("tech_news", [])
    a  = sections.get("ai_news", [])
    r  = sections.get("robot_news", [])
    g  = sections.get("github_trending", [])
    cl = sections.get("claude_code", [])
    total = len(w) + len(c) + len(t) + len(a) + len(r) + len(g) + len(cl)
    sections_count = sum(1 for x in [w, c, t, a, r, g, cl] if x)

    def render_section(title: str, items: list, section_id: str) -> str:
        icon, cls = _ICONS.get(section_id, ("📌", ""))
        head = (f'<div class="sh">'
                f'<div class="s-icon">{icon}</div>'
                f'<h2>{title}</h2>'
                f'<span class="cnt">{len(items)} 条</span>'
                f'</div>')
        if not items:
            return f'<section class="s {cls}" id="{section_id}">{head}<p class="empty">暂无数据</p></section>'
        rows = "".join(
            f'<article class="item">'
            f'<span class="rk">{i:02d}</span>'
            f'<div class="bd">'
            f'<a href="{item.get("url","#")}" class="tt" target="_blank" rel="noopener">{item.get("title","")}</a>'
            f'<div class="mt">'
            f'<span class="sc">{item.get("source","")}</span>'
            f'<span class="dt">{item.get("published","")}</span>'
            f'</div>'
            f'<p class="sm">{item.get("summary", item.get("title",""))}</p>'
            f'</div></article>'
            for i, item in enumerate(items, 1)
        )
        return f'<section class="s {cls}" id="{section_id}">{head}{rows}</section>'

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>你关注的热点 · {date_str}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,700;1,9..144,300&family=Plus+Jakarta+Sans:wght@400;500;600&family=Fira+Code:wght@400;500&display=swap" rel="stylesheet">
<style>{_CSS}</style>
</head>
<body>
<header>
  <div class="header-band">
    <span class="header-band-text"><span class="live-dot"></span>每日自动更新 · {date_str}</span>
    <span class="header-band-text">{total} 条资讯 · {sections_count} 个板块</span>
  </div>
  <div class="header-body">
    <div class="header-title">
      <h1>你关注的热点</h1>
      <div class="header-desc">全球科技 · 国内外要闻 · AI · 机器人 · GitHub · Claude Code</div>
    </div>
    <div class="header-stats">
      <div class="stat"><div class="stat-n">{total}</div><div class="stat-l">今日资讯</div></div>
      <div class="stat"><div class="stat-n">{sections_count}</div><div class="stat-l">内容板块</div></div>
    </div>
  </div>
</header>
<nav>
  <div class="nav-wrap">
    <a href="#world-news" class="active">🌍 国际新闻</a>
    <a href="#china-news">🇨🇳 国内新闻</a>
    <a href="#tech-news">💡 全球科技</a>
    <a href="#ai-news">🤖 全球 AI</a>
    <a href="#robot-news">⚙️ 机器人</a>
    <a href="#github-trending">⭐ GitHub</a>
    <a href="#claude-code">✦ Claude Code</a>
  </div>
</nav>
<main>
  {render_section("国际新闻事件 Top 5",    w,  "world-news")}
  {render_section("国内新闻 Top 5",        c,  "china-news")}
  {render_section("全球科技动态 Top 5",    t,  "tech-news")}
  {render_section("全球 AI 动态 Top 5",    a,  "ai-news")}
  {render_section("全球机器人动态 Top 5",  r,  "robot-news")}
  {render_section("GitHub 每日 Top 5",     g,  "github-trending")}
  {render_section("Claude Code 资讯 Top 5",cl, "claude-code")}
</main>
<footer>数据每日自动更新 · Claude Haiku 生成摘要 · hot-topics-daily</footer>
<script>{_JS}</script>
</body>
</html>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[HTML] 已生成: {output_path}")
