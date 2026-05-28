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
body { background: var(--bg); color: var(--ink); font-family: var(--fb); font-size: 19px; }

/* ── Header ── */
header { background: var(--white); border-bottom: 1px solid var(--bdr); }
.header-band {
  background: var(--teal); padding: 9px 32px;
  display: flex; align-items: center; justify-content: space-between;
}
.header-band-text {
  font-family: var(--fm); font-size: 12px; letter-spacing: .12em;
  text-transform: uppercase; color: rgba(255,255,255,.8);
}
.live-dot {
  width: 7px; height: 7px; border-radius: 50%;
  background: #5effd8; display: inline-block;
  margin-right: 8px; animation: blink 2s ease-in-out infinite;
}
.header-body {
  max-width: 1000px; margin: 0 auto; padding: 36px 32px 30px;
  display: flex; align-items: flex-end; justify-content: space-between; gap: 24px;
}
h1 {
  font-family: var(--fh); font-size: clamp(36px, 5.5vw, 64px);
  font-weight: 700; color: var(--ink); letter-spacing: -.025em; line-height: 1.08;
  font-style: italic;
}
.header-desc { font-size: 15px; color: var(--ink3); margin-top: 10px; line-height: 1.5; }
.header-stats { display: flex; gap: 28px; flex-shrink: 0; padding-bottom: 4px; }
.stat { text-align: center; }
.stat-n { font-family: var(--fh); font-size: 36px; font-weight: 700; color: var(--teal); line-height: 1; }
.stat-l { font-size: 13px; color: var(--ink3); margin-top: 4px; }

/* ── Nav (tab switcher) ── */
nav {
  position: sticky; top: 0; z-index: 100;
  background: rgba(255,255,255,.97); backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--bdr);
}
.nav-wrap {
  max-width: 1000px; margin: 0 auto; padding: 0 32px;
  display: flex; overflow-x: auto; scrollbar-width: none;
}
nav::-webkit-scrollbar { display: none; }
nav a {
  font-family: var(--fb); font-size: 15px; font-weight: 500;
  color: var(--ink2); text-decoration: none;
  padding: 15px 18px; white-space: nowrap;
  border-bottom: 2.5px solid transparent; margin-bottom: -1px;
  transition: color .18s, border-color .18s;
  cursor: pointer;
}
nav a:hover { color: var(--ink); }
nav a.active { color: var(--teal); border-bottom-color: var(--teal); }

/* ── Main: section carousel ── */
.main-outer { max-width: 1000px; margin: 0 auto; padding: 32px 32px 80px; }

.sections-slider {
  display: flex;
  overflow: hidden; /* JS controls scroll */
}

/* ── Section panel ── */
.s {
  flex: 0 0 100%;
  background: var(--card);
  border: 1px solid var(--bdr);
  border-radius: 14px;
  overflow: hidden;
  box-shadow: 0 1px 4px rgba(0,0,0,.05);
  animation: rise .35s both;
  /* panels are shown/hidden via JS, not scroll */
  display: none;
}
.s.active { display: block; }

.sh {
  display: flex; align-items: center; gap: 12px;
  padding: 18px 26px; border-bottom: 1px solid var(--bdr);
}
.s-icon {
  width: 34px; height: 34px; border-radius: 9px;
  display: flex; align-items: center; justify-content: center;
  font-size: 18px; flex-shrink: 0;
}
.sh h2 { font-family: var(--fb); font-size: 17px; font-weight: 600; color: var(--ink); flex: 1; }
.sh .cnt {
  font-family: var(--fm); font-size: 12px; color: var(--ink3);
  background: var(--bg); border: 1px solid var(--bdr);
  padding: 3px 11px; border-radius: 20px;
}

/* section color themes */
.s-world   .s-icon { background: var(--rose-bg);  color: var(--rose); }
.s-china   .s-icon { background: var(--amber-bg); color: var(--amber); }
.s-tech    .s-icon { background: var(--sky-bg);   color: var(--sky); }
.s-finance .s-icon { background: var(--sage-bg);  color: var(--sage); }
.s-ai      .s-icon { background: var(--teal-bg);  color: var(--teal); }
.s-robot   .s-icon { background: var(--slate-bg); color: var(--slate); }
.s-github  .s-icon { background: var(--rose-bg);  color: var(--rose); }
.s-claude  .s-icon { background: var(--amber-bg); color: var(--amber); }

/* ── Item (vertical list inside panel) ── */
.item {
  display: flex; gap: 16px; padding: 20px 26px;
  border-bottom: 1px solid var(--bdr);
  transition: background .15s;
}
.item:last-child { border-bottom: none; }
.item:hover { background: #fbfaf8; }

.rk {
  font-family: var(--fm); font-size: 13px; color: var(--bdr2);
  min-width: 22px; padding-top: 4px; flex-shrink: 0; font-weight: 600;
}
.bd { flex: 1; min-width: 0; }
.tt {
  display: block; font-family: var(--fb); font-size: 17px; font-weight: 600;
  color: var(--ink); text-decoration: none; line-height: 1.6;
  margin-bottom: 8px; transition: color .15s;
}
.tt:hover { color: var(--teal); }
.mt { display: flex; gap: 8px; align-items: center; margin-bottom: 10px; flex-wrap: wrap; }
.sc {
  font-family: var(--fm); font-size: 12px; font-weight: 500;
  color: var(--teal); background: var(--teal-bg);
  padding: 3px 10px; border-radius: 5px;
}
.dt { font-family: var(--fm); font-size: 12px; color: var(--ink3); }
.sm { font-size: 16px; color: var(--ink2); line-height: 1.85; }

.empty { font-size: 16px; color: var(--ink3); padding: 28px; font-style: italic; }

/* ── Section nav bar (prev/next + dots) ── */
.sec-nav {
  display: flex; align-items: center; justify-content: space-between;
  padding: 16px 26px; margin-top: 20px;
  background: var(--white); border: 1px solid var(--bdr);
  border-radius: 14px;
}
.sec-nav-btn {
  display: flex; align-items: center; gap: 8px;
  font-family: var(--fb); font-size: 14px; font-weight: 500;
  color: var(--ink2); background: none; border: 1px solid var(--bdr);
  border-radius: 8px; padding: 8px 16px; cursor: pointer;
  transition: all .18s;
}
.sec-nav-btn:hover:not(:disabled) { background: var(--teal); border-color: var(--teal); color: #fff; }
.sec-nav-btn:disabled { opacity: .3; cursor: default; }
.sec-dots { display: flex; gap: 7px; align-items: center; }
.sec-dot {
  width: 8px; height: 8px; border-radius: 50%;
  background: var(--bdr2); transition: background .2s, transform .2s, width .2s;
  cursor: pointer;
}
.sec-dot.active { background: var(--teal); transform: scale(1.25); width: 20px; border-radius: 4px; }
.sec-counter {
  font-family: var(--fm); font-size: 12px; color: var(--ink3);
  min-width: 40px; text-align: center;
}

/* ── Footer ── */
footer {
  text-align: center; padding: 32px 20px; margin-top: 8px;
  font-family: var(--fm); font-size: 12px; letter-spacing: .1em;
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
  .header-stats { gap: 18px; }
  h1 { font-size: 34px; }
  .main-outer { padding: 20px 16px 60px; }
  .sh { padding: 15px 18px; }
  .item { padding: 16px 18px; }
  .header-band { padding: 9px 16px; }
  .sec-nav { padding: 12px 16px; }
  .sec-nav-btn { padding: 7px 12px; font-size: 13px; }
}"""

_JS = """\
const SECTIONS = ['world-news','china-news','tech-news','finance-news','ai-news','robot-news','github-trending','claude-code'];
const panels   = SECTIONS.map(id => document.getElementById(id));
const navLinks = document.querySelectorAll('nav a');
const dots     = document.querySelectorAll('.sec-dot');
const counter  = document.querySelector('.sec-counter');
const prevBtn  = document.querySelector('.btn-sec-prev');
const nextBtn  = document.querySelector('.btn-sec-next');
let cur = 0;

function showSection(n) {
  cur = Math.max(0, Math.min(n, SECTIONS.length - 1));
  panels.forEach((p, i) => p.classList.toggle('active', i === cur));
  navLinks.forEach((a, i) => a.classList.toggle('active', i === cur));
  dots.forEach((d, i) => d.classList.toggle('active', i === cur));
  if (counter) counter.textContent = (cur + 1) + ' / ' + SECTIONS.length;
  if (prevBtn) prevBtn.disabled = cur === 0;
  if (nextBtn) nextBtn.disabled = cur === SECTIONS.length - 1;
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

navLinks.forEach((a, i) => {
  a.addEventListener('click', e => { e.preventDefault(); showSection(i); });
});
dots.forEach((d, i) => d.addEventListener('click', () => showSection(i)));
if (prevBtn) prevBtn.addEventListener('click', () => showSection(cur - 1));
if (nextBtn) nextBtn.addEventListener('click', () => showSection(cur + 1));

/* swipe support */
let tx = 0;
document.addEventListener('touchstart', e => { tx = e.touches[0].clientX; }, { passive: true });
document.addEventListener('touchend', e => {
  const dx = e.changedTouches[0].clientX - tx;
  if (Math.abs(dx) > 50) showSection(dx < 0 ? cur + 1 : cur - 1);
}, { passive: true });

showSection(0);"""

_ICONS = {
    "world-news":      ("🌍", "s-world"),
    "china-news":      ("🇨🇳", "s-china"),
    "tech-news":       ("💡", "s-tech"),
    "finance-news":    ("💹", "s-finance"),
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
    fi = sections.get("finance_news", [])
    a  = sections.get("ai_news", [])
    r  = sections.get("robot_news", [])
    g  = sections.get("github_trending", [])
    cl = sections.get("claude_code", [])
    total = len(w) + len(c) + len(t) + len(fi) + len(a) + len(r) + len(g) + len(cl)
    sections_count = sum(1 for x in [w, c, t, fi, a, r, g, cl] if x)

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

    n_sec = 8
    dots_html = "".join(
        f'<span class="sec-dot{"  active" if i == 0 else ""}"></span>'
        for i in range(n_sec)
    )

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
    <a href="#world-news">🌍 国际新闻</a>
    <a href="#china-news">🇨🇳 国内新闻</a>
    <a href="#tech-news">💡 全球科技</a>
    <a href="#finance-news">💹 国际财经</a>
    <a href="#ai-news">🤖 全球 AI</a>
    <a href="#robot-news">⚙️ 机器人</a>
    <a href="#github-trending">⭐ GitHub</a>
    <a href="#claude-code">✦ Claude Code</a>
  </div>
</nav>
<div class="main-outer">
  <div class="sections-slider">
    {render_section("国际新闻事件 Top 5",    w,  "world-news")}
    {render_section("国内新闻 Top 5",        c,  "china-news")}
    {render_section("全球科技动态 Top 5",    t,  "tech-news")}
    {render_section("国际财经 Top 5",        fi, "finance-news")}
    {render_section("全球 AI 动态 Top 5",    a,  "ai-news")}
    {render_section("全球机器人动态 Top 5",  r,  "robot-news")}
    {render_section("GitHub 每日 Top 5",     g,  "github-trending")}
    {render_section("Claude Code 资讯 Top 5",cl, "claude-code")}
  </div>
  <div class="sec-nav">
    <button class="sec-nav-btn btn-sec-prev" disabled>&#8592; 上一板块</button>
    <div class="sec-dots">{dots_html}</div>
    <span class="sec-counter">1 / {n_sec}</span>
    <button class="sec-nav-btn btn-sec-next">下一板块 &#8594;</button>
  </div>
</div>
<footer>数据每日自动更新 · Claude Haiku 生成摘要 · hot-topics-daily</footer>
<script>{_JS}</script>
</body>
</html>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[HTML] 已生成: {output_path}")
